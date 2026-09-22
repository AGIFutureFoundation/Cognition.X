#!/usr/bin/env python3
"""Static linter for the shipped HTML pages under apps/.

Every other check in this repo validates the DATASET. This one looks at the
PAGES, because three real faults shipped without anything noticing:

  * a fragment of an older build's data (``var DATA = {...}``) sat in the body
    OUTSIDE any <script> and rendered as visible text;
  * the body was an older shell (#stats, #blocks) while the script addressed
    #nav, #views, #toast, #stateSel, #stateflag, #crumb -- none existed, and
    buildNav()/buildState()/route() threw on load;
  * the doctype was declared twice, and two other single-file apps declared
    no <meta charset> at all, so they rendered mojibake when opened from
    file:// where no server header can rescue them.

Design notes
------------
* stdlib only, no network, no browser.  Files are read as bytes and decoded
  as strict UTF-8 in Python (never shelled out to grep: some pages contain
  deliberate NUL bytes, which make grep report "binary file matches").
* The page is TOKENIZED the way an HTML parser would, rather than counted
  with regexes.  In particular <script> content is scanned with the HTML
  spec's "script data" / "script data escaped" / "script data double
  escaped" states, so a ``<script`` inside a JavaScript regex literal is not
  a tag, while a ``</script>`` inside a template literal DOES end the script
  (exactly as a browser would, which is why it is a fault).
* NUL bytes are never reported.

Suppression: an HTML comment ``<!-- lint-pages: ignore <check> [reason] -->``
anywhere in the file silences that one check for that file.  Use it for a
documented false positive, not to make CI green.

Usage:  python3 tools/lint_pages.py [--warnings-as-errors] [PATH ...]
        (no PATH -> every apps/**/*.html under the repo root)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOB = "apps/**/*.html"

# Directories the default walk skips, and why. An exclusion is a decision
# about what this tool is allowed not to see, so each one is named here
# rather than expressed as a pattern somebody has to decode.
#
#   versions/ - apps/education-os/versions/README.md says superseded
#   builds are "kept here verbatim for provenance". The v0.1.0 archive
#   genuinely carries the faults this linter was written for: a bare
#   `var DATA = {` in its body and eight ids its script addresses that
#   its markup never provides. That is not a bug to fix - it is the
#   record of what shipped, and editing it would destroy the thing it
#   exists to preserve. Passing the path explicitly still lints it, so
#   the record stays inspectable:
#       python3 tools/lint_pages.py apps/education-os/versions
SKIP_DIRS = ("versions",)
CHARSET_PRESCAN_BYTES = 1024  # browsers commit to an encoding within this window

RAW_TEXT = {"script", "style"}
RCDATA = {"title", "textarea"}
ESCAPABLE = {"noscript"}  # raw text when scripting is enabled, which it is for our apps
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
JS_TYPES = {"", "text/javascript", "application/javascript", "module",
            "text/ecmascript", "application/ecmascript"}

WS = " \t\n\r\f"


# ----------------------------------------------------------------------------
# Tokenizer
# ----------------------------------------------------------------------------

class Tok:
    """One token.  kind in {'text','comment','doctype','start','end','raw','bogus'}.

    'raw' is the content of a script/style/title/textarea/noscript element;
    tok.name is the element name and tok.attrs its start-tag attributes.
    tok.closed is False when a raw element ran to end-of-file without its end tag.
    """
    __slots__ = ("kind", "start", "end", "name", "attrs", "closed", "self_closing")

    def __init__(self, kind, start, end, name=None, attrs=None, closed=True, self_closing=False):
        self.kind, self.start, self.end = kind, start, end
        self.name, self.attrs, self.closed, self.self_closing = name, attrs or {}, closed, self_closing


_ATTR_RE = re.compile(
    r"""([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?""", re.S)


def _parse_attrs(s: str) -> dict:
    out = {}
    for m in _ATTR_RE.finditer(s):
        k = m.group(1).lower()
        v = m.group(2) if m.group(2) is not None else m.group(3) if m.group(3) is not None else m.group(4)
        out.setdefault(k, "" if v is None else v)
    return out


def _find_tag_end(text: str, i: int) -> int:
    """Index of the '>' closing a start/end tag beginning at text[i]=='<'.

    Honors quoted attribute values (a '>' inside quotes does not end the tag).
    Returns -1 when the tag never closes.
    """
    n = len(text)
    j = i + 1
    while j < n:
        c = text[j]
        if c == ">":
            return j
        if c == "=":
            k = j + 1
            while k < n and text[k] in WS:
                k += 1
            if k < n and text[k] in "\"'":
                q = text.find(text[k], k + 1)
                if q < 0:
                    return -1
                j = q + 1
                continue
            j = k
            continue
        j += 1
    return -1


def _is_end_tag_at(text: str, j: int, name: str) -> bool:
    """True when text[j:] starts with '</name' followed by ws, '/', or '>'."""
    m = 2 + len(name)
    if text[j:j + m].lower() != "</" + name:
        return False
    return j + m >= len(text) or text[j + m] in WS + "/>"


def _find_script_end(text: str, pos: int) -> int:
    """HTML-spec scan of script data starting at pos.  Returns index of the
    '</script' that ends the element, or -1 if it runs to EOF."""
    state = "data"  # 'data' | 'escaped' | 'double'
    i, n = pos, len(text)
    while i < n:
        j = text.find("<", i)
        if state == "data":
            if j < 0:
                return -1
            if text.startswith("<!--", j):
                state, i = "escaped", j + 4
                continue
            if _is_end_tag_at(text, j, "script"):
                return j
            i = j + 1
        else:
            k = text.find("-->", i)
            if k >= 0 and (j < 0 or k < j):
                state, i = "data", k + 3
                continue
            if j < 0:
                return -1
            if state == "escaped":
                if text[j:j + 7].lower() == "<script" and (j + 7 >= n or text[j + 7] in WS + "/>"):
                    state, i = "double", j + 7
                    continue
                if _is_end_tag_at(text, j, "script"):
                    return j
            else:  # double escaped: </script> does NOT end the element here
                if _is_end_tag_at(text, j, "script"):
                    state, i = "escaped", j + 8
                    continue
            i = j + 1
    return -1


def _find_raw_end(text: str, pos: int, name: str) -> int:
    i = pos
    while True:
        j = text.find("</", i)
        if j < 0:
            return -1
        if _is_end_tag_at(text, j, name):
            return j
        i = j + 2


def tokenize(text: str) -> list[Tok]:
    toks: list[Tok] = []
    i, n = 0, len(text)
    while i < n:
        lt = text.find("<", i)
        if lt < 0:
            toks.append(Tok("text", i, n))
            break
        if lt > i:
            toks.append(Tok("text", i, lt))
        i = lt
        nxt = text[i + 1:i + 2]
        if text.startswith("<!--", i):
            e = text.find("-->", i + 4)
            if e < 0:
                toks.append(Tok("comment", i, n, closed=False))
                break
            toks.append(Tok("comment", i, e + 3))
            i = e + 3
        elif nxt == "!" or nxt == "?":
            e = text.find(">", i)
            e = n if e < 0 else e + 1
            body = text[i:e]
            if body[:9].lower() == "<!doctype":
                toks.append(Tok("doctype", i, e, name=body[9:-1].strip()))
            else:
                toks.append(Tok("bogus", i, e))
            i = e
        elif nxt == "/":
            m = re.match(r"</([A-Za-z][^\s/>]*)", text[i:i + 64])
            if not m:
                e = text.find(">", i)
                e = n if e < 0 else e + 1
                toks.append(Tok("bogus", i, e))
                i = e
                continue
            e = _find_tag_end(text, i)
            e = n if e < 0 else e + 1
            toks.append(Tok("end", i, e, name=m.group(1).lower()))
            i = e
        elif nxt.isascii() and nxt.isalpha():
            m = re.match(r"<([A-Za-z][^\s/>]*)", text[i:i + 64])
            name = m.group(1).lower()
            e = _find_tag_end(text, i)
            if e < 0:
                toks.append(Tok("start", i, n, name=name, closed=False))
                break
            raw_attrs = text[i + 1 + len(name):e]
            self_closing = raw_attrs.rstrip().endswith("/")
            attrs = _parse_attrs(raw_attrs.rstrip().rstrip("/"))
            toks.append(Tok("start", i, e + 1, name=name, attrs=attrs, self_closing=self_closing))
            i = e + 1
            if name in RAW_TEXT or name in RCDATA or name in ESCAPABLE:
                if name == "script":
                    ce = _find_script_end(text, i)
                else:
                    ce = _find_raw_end(text, i, name)
                if ce < 0:
                    toks.append(Tok("raw", i, n, name=name, attrs=attrs, closed=False))
                    break
                toks.append(Tok("raw", i, ce, name=name, attrs=attrs))
                te = text.find(">", ce)
                te = n if te < 0 else te + 1
                toks.append(Tok("end", ce, te, name=name))
                i = te
        else:
            # a lone '<' (e.g. "a < b") is text
            toks.append(Tok("text", i, i + 1))
            i += 1
    return toks


# ----------------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------------

class Report:
    def __init__(self, path: Path, text: str):
        self.path, self.text = path, text
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ignored: set[str] = set()

    def line(self, off: int) -> int:
        return self.text.count("\n", 0, off) + 1

    def error(self, check: str, off: int | None, msg: str):
        if check in self.ignored:
            return
        loc = f"{self.path}:{self.line(off)}" if off is not None else str(self.path)
        self.errors.append(f"{loc}: [{check}] {msg}")

    def warn(self, check: str, off: int | None, msg: str):
        if check in self.ignored:
            return
        loc = f"{self.path}:{self.line(off)}" if off is not None else str(self.path)
        self.warnings.append(f"{loc}: [{check}] {msg}")


_IGNORE_RE = re.compile(r"lint-pages:\s*ignore\s+([\w-]+)")


def check_preamble(rep: Report, toks: list[Tok]):
    """doctype: exactly one, first, and 'html'."""
    doctypes = [t for t in toks if t.kind == "doctype"]
    if not doctypes:
        rep.error("doctype", 0, "no <!DOCTYPE html> -- the page renders in quirks mode")
    elif len(doctypes) > 1:
        lines = ", ".join(str(rep.line(t.start)) for t in doctypes)
        rep.error("doctype", doctypes[1].start,
                  f"doctype declared {len(doctypes)} times (lines {lines}); it must appear exactly once")
    if doctypes:
        first = doctypes[0]
        for t in toks:
            if t is first:
                break
            if t.kind == "comment" or (t.kind == "text" and not rep.text[t.start:t.end].strip("\ufeff" + WS)):
                continue
            rep.error("doctype", first.start,
                      f"doctype is not the first thing in the file ({t.kind} at line {rep.line(t.start)} "
                      "precedes it) -- the page renders in quirks mode")
            break
        if first.name.lower() != "html":
            rep.warn("doctype", first.start, f"non-HTML5 doctype {rep.text[first.start:first.end]!r}")


def check_charset(rep: Report, toks: list[Tok], raw: bytes, bom: bool):
    decl = None
    for t in toks:
        if t.kind != "start" or t.name != "meta":
            continue
        a = t.attrs
        if "charset" in a:
            decl = (a["charset"], t)
            break
        if a.get("http-equiv", "").lower() == "content-type":
            m = re.search(r"charset\s*=\s*['\"]?([\w-]+)", a.get("content", ""), re.I)
            if m:
                decl = (m.group(1), t)
                break
    if decl is None:
        if bom:
            rep.warn("charset", 0, "no <meta charset>; relying on the UTF-8 byte-order mark")
            return
        rep.error("charset", 0,
                  "no <meta charset=\"utf-8\"> -- opened from file:// there is no server header, "
                  "so non-ASCII text renders as mojibake")
        return
    value, tok = decl
    if value.strip().lower().replace("_", "-") not in ("utf-8", "utf8"):
        rep.error("charset", tok.start, f"charset declared as {value!r}; the source is UTF-8")
    byte_end = len(rep.text[:tok.end].encode("utf-8")) + (3 if bom else 0)
    if byte_end > CHARSET_PRESCAN_BYTES:
        rep.error("charset", tok.start,
                  f"<meta charset> ends at byte {byte_end}; browsers only prescan the first "
                  f"{CHARSET_PRESCAN_BYTES} bytes for it, so it may be ignored")


_MOJIBAKE = ["Â·", "Â\xa0", "â€", "Ã©", "Ã¨", "Ã\xa0", "Ã¡", "Ã³", "ðŸ", "\ufffd"]


def check_mojibake(rep: Report):
    for sig in _MOJIBAKE:
        off = rep.text.find(sig)
        if off >= 0:
            n = rep.text.count(sig)
            what = "U+FFFD replacement character" if sig == "\ufffd" else f"{sig!r}"
            rep.error("mojibake", off,
                      f"double-encoded text signature {what} ({n}x) -- a previous build/edit "
                      "decoded UTF-8 bytes as Latin-1/CP1252")


def check_raw_balance(rep: Report, toks: list[Tok]):
    for t in toks:
        if t.kind == "raw" and not t.closed:
            rep.error("unclosed-" + t.name, t.start,
                      f"<{t.name}> is never closed; everything after line {rep.line(t.start)} "
                      f"is swallowed as {t.name} content")
        elif t.kind == "comment" and not t.closed:
            rep.error("unclosed-comment", t.start, "<!-- comment is never closed; the rest of the file is a comment")
        elif t.kind == "start" and not t.closed:
            rep.error("unclosed-tag", t.start, f"<{t.name} start tag never reaches its '>'")
    # a stray </script> or </style> in ordinary markup means a script got cut
    # short earlier (typically by a '</script>' inside a JS string/template literal)
    prev_raw_name = None
    for t in toks:
        if t.kind == "raw":
            prev_raw_name = t.name
            continue
        if t.kind == "end" and t.name in RAW_TEXT | RCDATA:
            if prev_raw_name != t.name:
                rep.error("stray-end-tag", t.start,
                          f"</{t.name}> with no matching open <{t.name}> -- an earlier <{t.name}> "
                          "was probably terminated early")
        if t.kind in ("start", "text", "comment", "doctype", "bogus"):
            if t.kind == "text" and not rep.text[t.start:t.end].strip():
                continue
            prev_raw_name = None


def check_title(rep: Report, toks: list[Tok]):
    svg_depth = 0
    titles = []
    for t in toks:
        if t.kind == "start" and t.name == "svg" and not t.self_closing:
            svg_depth += 1
        elif t.kind == "end" and t.name == "svg":
            svg_depth = max(0, svg_depth - 1)
        elif t.kind == "raw" and t.name == "title" and svg_depth == 0:
            titles.append(t)
    if not titles:
        rep.error("title", 0, "no <title> element")
    else:
        if not rep.text[titles[0].start:titles[0].end].strip():
            rep.error("title", titles[0].start, "<title> is empty")
        if len(titles) > 1:
            rep.error("title", titles[1].start,
                      f"{len(titles)} <title> elements (lines "
                      f"{', '.join(str(rep.line(t.start)) for t in titles)}); a document has one")


_JS_LINE_RES = [
    re.compile(r"^(?:var|let|const)\s+[A-Za-z_$][\w$]*\s*="),
    re.compile(r"^(?:async\s+)?function\s+[A-Za-z_$][\w$]*\s*\("),
    re.compile(r"^\}\s*\)\s*\(\s*\)\s*;?$"),
    re.compile(r"^(?:document|window)\.[A-Za-z_$][\w$]*\s*[(.=]"),
    re.compile(r"^[A-Za-z_$][\w$]*\.(?:addEventListener|innerHTML|querySelector|querySelectorAll|getElementById)\s*[(=]"),
    re.compile(r"^(?:export|import)\s+[{*\w]"),
]
_CODE_PUNCT = set("{}[];=")


def check_code_in_text(rep: Report, toks: list[Tok]):
    """Text nodes (outside script/style/pre/code/textarea) that look like JS."""
    depth = {"pre": 0, "code": 0}
    for t in toks:
        if t.kind == "start" and t.name in depth and not t.self_closing:
            depth[t.name] += 1
        elif t.kind == "end" and t.name in depth:
            depth[t.name] = max(0, depth[t.name] - 1)
        elif t.kind == "text" and not any(depth.values()):
            seg = rep.text[t.start:t.end]
            if len(seg.strip()) < 4:
                continue
            hit = None
            for ln_off, line in _iter_lines(seg):
                s = line.strip()
                if any(r.search(s) for r in _JS_LINE_RES):
                    hit = (t.start + ln_off, s)
                    break
            if hit is None:
                stripped = seg.strip()
                if len(stripped) >= 300:
                    punct = sum(1 for c in stripped if c in _CODE_PUNCT)
                    if punct / len(stripped) >= 0.10:
                        hit = (t.start, stripped[:80])
            if hit:
                off, s = hit
                rep.error("code-in-text", off,
                          f"JavaScript/data outside any <script> renders as visible text: {s[:90]!r}")
                return  # one per file is enough to fail; the rest is noise


def _iter_lines(seg: str):
    off = 0
    for line in seg.splitlines(keepends=True):
        yield off, line
        off += len(line)


_ID_TOKEN = r"[A-Za-z_][\w:.-]*"
_REF_RES = [
    re.compile(r"getElementById\(\s*(['\"])(" + _ID_TOKEN + r")\1\s*\)"),
    re.compile(r"(?:querySelector(?:All)?|\$\$?)\(\s*(['\"])#(" + _ID_TOKEN + r")(?:[\s>+~,.\[:][^'\"]*)?\1\s*[,)]"),
]
_SCRIPT_DEF_RES = [
    re.compile(r"(?<![\w$.-])id\s*=\s*\\?[\"']?(" + _ID_TOKEN + r")(?=\\?[\"'\s>/]|$)"),   # id="x" inside HTML strings
    re.compile(r"\.id\s*=\s*[\"'](" + _ID_TOKEN + r")[\"']"),                              # el.id = 'x'
    re.compile(r"(?<![\w$])id\s*:\s*[\"'](" + _ID_TOKEN + r")[\"']"),                     # {id: 'x'}
    re.compile(r"setAttribute\(\s*[\"']id[\"']\s*,\s*[\"'](" + _ID_TOKEN + r")[\"']"),
]
# ids built at runtime from a literal prefix: v.id='v-'+k, $('#sp-'+k), id="ph-${n}"
_PREFIX_RES = [
    re.compile(r"\.id\s*=\s*['\"]([\w:.-]+)['\"]\s*\+"),
    re.compile(r"['\"]#([\w:.-]+)['\"]\s*\+"),
    re.compile(r"(?<![\w$.-])id=\\?[\"']([\w:.-]+)\$\{"),
    re.compile(r"#([\w:.-]+)\$\{"),
]
# a lookup the script itself tolerates failing: getElementById('x')||..., if(!$('#x')), $('#x')?.foo
_GUARD_AFTER = re.compile(r"^\s*(?:\|\||&&|\?\.|\?[^.]|[!=]==?)")
_GUARD_BEFORE = re.compile(r"(?:!|if\s*\(|Boolean\(|\bwhile\s*\()\s*$")
_BARE_STR_RE = re.compile(r"(?<![#\w$])['\"](" + _ID_TOKEN + r")['\"]")


def check_ids(rep: Report, toks: list[Tok]):
    text = rep.text
    scripts = [t for t in toks if t.kind == "raw" and t.name == "script"
               and t.attrs.get("type", "").strip().lower() in JS_TYPES]
    external = [t for t in toks if t.kind == "start" and t.name == "script" and "src" in t.attrs]

    # ids defined by static markup (and duplicates among them)
    defined: dict[str, int] = {}
    for t in toks:
        if t.kind != "start":
            continue
        v = t.attrs.get("id")
        if v is None or not v.strip():
            continue
        v = v.strip()
        if v in defined:
            rep.error("duplicate-id", t.start,
                      f"id=\"{v}\" is declared twice in the markup (first at line {rep.line(defined[v])}); "
                      "getElementById only ever sees the first")
        else:
            defined[v] = t.start

    if not scripts:
        return
    if external:
        rep.warn("dangling-id", external[0].start,
                 "page loads an external script; ids it creates cannot be seen, dangling-id check skipped")
        return

    # ids the script creates at runtime, by any literal spelling, plus the
    # literal prefixes it builds ids from, plus every bare string literal
    # (an id handed to a factory such as bandSelect("rp-band") shows up as one)
    created: set[str] = set()
    prefixes: set[str] = set()
    bare: set[str] = set()
    for t in scripts:
        body = text[t.start:t.end]
        for r in _SCRIPT_DEF_RES:
            created.update(m.group(1) for m in r.finditer(body))
        for r in _PREFIX_RES:
            prefixes.update(m.group(1) for m in r.finditer(body))
        bare.update(m.group(1) for m in _BARE_STR_RE.finditer(body))
    known = set(defined) | created | bare

    seen: set[str] = set()
    for t in scripts:
        body = text[t.start:t.end]
        for r in _REF_RES:
            for m in r.finditer(body):
                ident = m.group(2)
                if ident in known or ident in seen:
                    continue
                if any(ident.startswith(p) for p in prefixes):
                    continue
                if _GUARD_AFTER.search(body[m.end():m.end() + 12]) or _GUARD_BEFORE.search(body[max(0, m.start() - 12):m.start()]):
                    continue
                seen.add(ident)
                rep.error("dangling-id", t.start + m.start(),
                          f"script addresses #{ident} but no element with id=\"{ident}\" exists in the "
                          "markup and the script never creates one -- the lookup returns null")

    # <label for="x"> pointing nowhere
    for t in toks:
        if t.kind == "start" and t.name == "label" and t.attrs.get("for"):
            v = t.attrs["for"].strip()
            if v and v not in known and not any(v.startswith(p) for p in prefixes):
                rep.warn("dangling-id", t.start, f"<label for=\"{v}\"> but no element has that id")


_PLACEHOLDER_RE = re.compile(r"__[A-Z][A-Z0-9_]{2,}__")


def check_placeholders(rep: Report):
    if rep.path.name == "template.html":
        return
    m = _PLACEHOLDER_RE.search(rep.text)
    if m:
        rep.error("placeholder", m.start(),
                  f"unresolved build placeholder {m.group(0)} in a built page (the build did not inject it)")


def check_viewport(rep: Report, toks: list[Tok]):
    for t in toks:
        if t.kind == "start" and t.name == "meta" and t.attrs.get("name", "").lower() == "viewport":
            return
    rep.warn("viewport", 0, "no <meta name=\"viewport\">; phones will render the desktop layout scaled down")


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------

def lint_file(path: Path, display: Path | None = None) -> Report:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    rep = Report(display or path, "")
    try:
        text = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    except UnicodeDecodeError as e:
        rep.text = raw.decode("utf-8", errors="replace")
        rep.error("encoding", e.start and rep.text.count("\n", 0, e.start),
                  f"file is not valid UTF-8 at byte {e.start}: {e.reason}")
        return rep
    rep.text = text
    # NUL bytes are deliberate in some pages (used as a key separator); never reported.

    toks = tokenize(text)
    for t in toks:
        if t.kind == "comment":
            for m in _IGNORE_RE.finditer(text[t.start:t.end]):
                rep.ignored.add(m.group(1))

    check_preamble(rep, toks)
    check_charset(rep, toks, raw, bom)
    check_mojibake(rep)
    check_raw_balance(rep, toks)
    check_title(rep, toks)
    check_code_in_text(rep, toks)
    check_ids(rep, toks)
    check_placeholders(rep)
    check_viewport(rep, toks)
    return rep


def collect(args: list[str]) -> list[Path]:
    if not args:
        return sorted(p for p in ROOT.glob(DEFAULT_GLOB)
                      if not any(d in p.parts for d in SKIP_DIRS))
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out.extend(sorted(p.rglob("*.html")))
        else:
            out.append(p)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="*", help="files or directories (default: apps/**/*.html)")
    ap.add_argument("--warnings-as-errors", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print problems")
    ns = ap.parse_args(argv)

    files = collect(ns.paths)
    if not files:
        print("lint_pages: no HTML files found", file=sys.stderr)
        return 2
    n_err = n_warn = 0
    for f in files:
        try:
            disp = f.relative_to(ROOT)
        except ValueError:
            disp = f
        rep = lint_file(f, disp)
        for w in rep.warnings:
            print("WARN  " + w)
        for e in rep.errors:
            print("ERROR " + e)
        n_err += len(rep.errors)
        n_warn += len(rep.warnings)
        if not ns.quiet:
            status = "FAIL" if rep.errors else ("warn" if rep.warnings else "ok")
            print(f"{status:4}  {disp}  ({len(rep.errors)} errors, {len(rep.warnings)} warnings)")
    failed = n_err > 0 or (ns.warnings_as_errors and n_warn > 0)
    print(f"lint_pages: {len(files)} files, {n_err} errors, {n_warn} warnings -> {'FAIL' if failed else 'OK'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
