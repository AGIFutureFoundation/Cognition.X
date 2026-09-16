# Hosting the apps — the hardening guide

> The single file is the primary packaging and the safest: open it from a
> USB stick, a file share or a download and nothing changes. This guide is
> for a district, parish or program office that wants a URL. Not legal
> advice; the host's own security policy governs.

## What hosting changes, and what it must not

Served over `https`, each app gets **its own origin** (one path or one
subdomain each), which closes finding 8 of
[`COMPLIANCE_REVIEW.md`](COMPLIANCE_REVIEW.md): apps can no longer read
each other's local storage, and the PWA install metadata becomes
installable. Nothing else may change. The hosted copy must behave exactly
like the file: no request leaves the page, no analytics, no injected
script, no cookie, the same Content-Security-Policy the page already
carries — sent again as an HTTP header, because a header cannot be
edited out of a saved copy.

The browser suite proves this for the released files
(`testHostedCopy` in `tests/browser/smoke.js` serves the apps over HTTP
and runs the same checks as for `file://`). Run it against your own host
by pointing `CX_HOSTED_BASE` at it.

## Rules

1. **Serve the released file unchanged.** Verify it first:
   `sha256sum -c apps/CHECKSUMS.sha256`. Do not minify, bundle, template
   or inject anything — not a banner, not a tag manager, not a font.
2. **One origin per app, or one path per app** under one origin. Never
   share an origin with another site.
3. **Send the same CSP as a header**, byte for byte the value in
   `tools/runtime_lib.py` (`CSP`). If the header and the meta disagree,
   the browser applies both, and the stricter of the two wins for every
   directive — so a looser header cannot weaken the page, but a typo can
   break it. Copy the value; do not retype it.
4. **TLS with HSTS.** Redirect `http` to `https`; `Strict-Transport-Security: max-age=31536000; includeSubDomains`.
5. **No cookies, no sessions, no logins** on the app origin. If the host
   requires authentication, put it in front (a reverse proxy or the
   district's SSO) and pass nothing to the page.
6. **No analytics, no logging of query strings.** Access logs may keep
   the path and status; strip query strings and referrers. The apps keep
   state in fragments (`#/…`), which never reach the server.
7. **Cache-Control: no-store** for `index.html` so a revoked release does
   not linger; the files are small enough.
8. **Keep the CHECKSUMS file next to the apps** so a reader can verify
   what they were served.

## Headers

```
Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; manifest-src blob:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'
Referrer-Policy: no-referrer
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cache-Control: no-store
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

`frame-ancestors` is not in the CSP because it is ignored in a `<meta>`
policy; `X-Frame-Options: DENY` covers it at the header level. Speech
synthesis (the optional Guide voice) needs no permission; the
Permissions-Policy above disables what the apps never use.

### nginx

```nginx
server {
  listen 443 ssl http2;
  server_name louisiana.example.org;            # one origin per app
  root /srv/cognitionx/apps/louisiana;
  add_header Content-Security-Policy "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; manifest-src blob:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'" always;
  add_header Referrer-Policy "no-referrer" always;
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header X-Frame-Options "DENY" always;
  add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()" always;
  add_header Cache-Control "no-store" always;
  location = / { try_files /index.html =404; }
  location / { try_files $uri =404; }
  access_log /var/log/nginx/cognitionx.log combined;   # strip query strings and referrers in the log format if your policy requires
}
server { listen 80; server_name louisiana.example.org; return 301 https://$host$request_uri; }
```

### Apache

```apache
<VirtualHost *:443>
  ServerName louisiana.example.org
  DocumentRoot /srv/cognitionx/apps/louisiana
  Header always set Content-Security-Policy "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; manifest-src blob:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'"
  Header always set Referrer-Policy "no-referrer"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "DENY"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
  Header always set Cache-Control "no-store"
</VirtualHost>
```

### Caddy

```
louisiana.example.org {
  root * /srv/cognitionx/apps/louisiana
  file_server
  header {
    Content-Security-Policy "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; manifest-src blob:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'"
    Referrer-Policy "no-referrer"
    Strict-Transport-Security "max-age=31536000; includeSubDomains"
    X-Content-Type-Options "nosniff"
    X-Frame-Options "DENY"
    Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
    Cache-Control "no-store"
  }
}
```

## Compression

Serve the files compressed. Every app shrinks by 60–80% on the wire
(`docs/PERFORMANCE.md` has the per-app figures: the Education OS goes
from 6.1 MB to 1.65 MB), and pre-compressing at deploy time costs the
server nothing per request:

```
gzip -9 -k apps/*/index.html        # leaves index.html.gz beside each file
```

nginx: `gzip_static on;` in the location block (Apache: `mod_deflate` or
`AddEncoding gzip .gz` with a rewrite to the `.gz` file; Caddy:
`encode gzip` or `file_server { precompressed gzip }`). None of the
headers above change with compression, and the checksums in
`apps/CHECKSUMS.sha256` still apply to the uncompressed files.

## Checking your host

1. Open the hosted app with the browser's network panel: after the
   document, **no request** should appear (the typefaces are embedded).
2. In the console, run `fetch('https://example.com/')` — the browser
   must refuse it under the CSP.
3. `curl -sI https://louisiana.example.org/ | grep -i content-security-policy`
   must print the exact value above.
4. Open the Data & privacy control: the keys listed are the app's own,
   and nothing else on the origin writes any.
5. Run the browser suite against the host:
   `CX_HOSTED_BASE=https://louisiana.example.org/ node tests/browser/smoke.js`
   (the hosted-copy test reads that variable; everything else still runs
   against the files).

## What hosting does not do

It does not add a server-side record: the ledger still lives in the
browser of the device in use, and the records-custody bundle is still the
export. It does not make the apps a "service" in the sense of a data
agreement — no data reaches the host. It does not change the honesty
stances, the credential threshold or the studio law.
