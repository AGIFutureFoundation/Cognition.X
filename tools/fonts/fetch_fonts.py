# One-time acquisition of the latin subsets of the apps' typefaces from Google Fonts (all SIL OFL 1.1).
import re, urllib.request, json, os
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
FAM=["Fraunces:opsz,wght@9..144,600;9..144,800","Instrument+Sans:wght@400;500;600","IBM+Plex+Mono:wght@400;500","Archivo:wght@600;800"]
import pathlib
out=str(pathlib.Path(__file__).resolve().parent.parent.parent/"data"/"fonts"); idx=[]
for fam in FAM:
    css=urllib.request.urlopen(urllib.request.Request("https://fonts.googleapis.com/css2?family="+fam+"&display=swap",headers=UA)).read().decode()
    for m in re.finditer(r"/\*\s*(\w+)\s*\*/\s*@font-face\s*{([^}]*)}", css):
        sub, body = m.group(1), m.group(2)
        if sub!="latin": continue
        name=re.search(r"font-family:\s*'([^']+)'",body).group(1)
        style=re.search(r"font-style:\s*(\w+)",body).group(1)
        weight=re.search(r"font-weight:\s*([\d ]+)",body).group(1).strip()
        url=re.search(r"url\((https://[^)]+\.woff2)\)",body).group(1)
        rng=re.search(r"unicode-range:\s*([^;]+)",body).group(1).strip()
        fn=(name.replace(" ","")+"-"+weight.replace(" ","-")+".woff2")
        data=urllib.request.urlopen(urllib.request.Request(url,headers=UA)).read()
        open(os.path.join(out,fn),"wb").write(data)
        idx.append({"family":name,"style":style,"weight":weight,"file":fn,"bytes":len(data),"unicode_range":rng,"source":url,"license":"SIL Open Font License 1.1"})
        print(name,weight,len(data),fn)
json.dump({"note":"Latin subsets of the typefaces the apps use, fetched once from Google Fonts and embedded into each build as data: URIs so that no app makes a third-party request. All four families are licensed under the SIL Open Font License 1.1 (see LICENSE-OFL.txt). Regenerate with tools/fonts/fetch_fonts.py only when a family changes.","fonts":idx},open(os.path.join(out,"fonts.json"),"w"),indent=1)
print("total",sum(i["bytes"] for i in idx))
