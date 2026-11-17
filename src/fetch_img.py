import json, re, time, sys, os, io, urllib.parse, urllib.request
sys.path.insert(0, "/home/claude/swiss/content")
from PIL import Image
UA = "SwissTravelTechoBuilder/1.0 (https://github.com/Shiyang0530; personal travel e-book)"
OUT = "/home/claude/swiss/site/img"; os.makedirs(OUT, exist_ok=True)
DB = "/home/claude/swiss/imgdb.json"
db = json.load(open(DB)) if os.path.exists(DB) else {}

import subprocess
def get(url, binary=False, tries=8):
    for i in range(tries):
        r = subprocess.run(["curl", "-sS", "-m", "60", "-A", UA, "-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        code = code.decode().strip()
        if code == "200":
            return body if binary else json.loads(body)
        if code == "429":
            time.sleep(20 + 10 * i); continue
        time.sleep(3)
    raise RuntimeError(f"HTTP {code} {url[:100]}")

BAD = re.compile(r"map|karte|plan|logo|\.svg|stamp|briefmarke|postcard|ansichtskarte|wappen|coat.of.arms|diagram|schild|ticket|poster|fahrplan|panneau|signpost|wegweiser|carte|mappa|drawing|zeichnung|gemälde|painting|aquarell|lithograph|stich|engraving|sketch|book|buch|scan|page|seite", re.I)
OKLIC = re.compile(r"^(cc[- ]by(-sa)?( \d\.\d)?|cc0|public domain|pd.*|cc by(-sa)? \d\.\d.*)$", re.I)

def search(q, n=15):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(action="query", generator="search", gsrsearch=q + " filetype:bitmap",
        gsrnamespace=6, gsrlimit=n, prop="imageinfo", iiprop="url|size|mime|extmetadata", iiurlwidth=1000, format="json"))
    d = get(url); time.sleep(1.5)
    return list((d.get("query") or {}).get("pages", {}).values())

def thumb(u, w):
    if u: u = u.split("?")[0]
    if not u or w <= 960: return u
    a, b = u.split("/wikipedia/commons/", 1)
    return f"{a}/wikipedia/commons/thumb/{b}/960px-{b.rsplit('/',1)[1]}"

def strip(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()

def score(p, tokens, season, area=None):
    ii = (p.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
    lic = strip(md.get("LicenseShortName", {}).get("value", ""))
    if not OKLIC.match(lic) or re.search(r"nc|nd", lic, re.I): return None
    if ii.get("mime") != "image/jpeg": return None
    t = p["title"]; w, h = ii.get("width", 0), ii.get("height", 1)
    if w < 900: return None
    s = 0
    if BAD.search(t): s -= 60
    r = w / h
    if 1.2 <= r <= 2.0: s += 20
    elif r < 1: s -= 25
    if w >= 2000: s += 8
    tl = t.lower()
    s += sum(15 for tok in tokens if tok and tok.lower() in tl)
    ass = md.get("Assessments", {}).get("value", "")
    if "featured" in ass: s += 25
    if "quality" in ass: s += 18
    if area and area.lower() in (tl + strip(md.get("ImageDescription", {}).get("value", "")).lower()): s += 14
    if season and re.search(season, tl + strip(md.get("ImageDescription", {}).get("value", "")).lower()): s += 20
    m = re.search(r"(18|19)\d\d", t)
    if m and int(m.group(0)) < 1960: s -= 40
    if p.get("index"): s -= p["index"] * 1.5
    return s, dict(title=t, url=thumb(ii.get("url"), w), page=ii.get("descriptionurl"), lic=lic,
                   by=strip(md.get("Artist", {}).get("value", ""))[:80] or "Wikimedia Commons", w=w, h=h)

def pick(id, queries, tokens, season=None, force=None, area=None):
    best = None
    if force:
        url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(action="query", titles=force, prop="imageinfo",
            iiprop="url|size|mime|extmetadata", iiurlwidth=1000, format="json"))
        pages = list(get(url)["query"]["pages"].values()); time.sleep(1.2)
        sc = score(pages[0], tokens, season)
        return sc[1] if sc else None
    for q in queries[:2]:
        for p in search(q):
            sc = score(p, tokens, season, area)
            if sc and (not best or sc[0] > best[0]): best = sc
        if best and best[0] >= 28: break
    return best[1] if best else None

def download(id, info):
    data = get(info["url"], binary=True); time.sleep(0.8)
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.thumbnail((960, 720))
    im.save(f"{OUT}/{id}.webp", "WEBP", quality=72, method=6)

if __name__ == "__main__":
    jobs = json.load(open("/home/claude/swiss/imgjobs.json"))
    only = set(sys.argv[1:])
    for j in jobs:
        id = j["id"]
        if only and id not in only: continue
        if not only and id in db: continue
        try:
            info = pick(id, j["q"], j["tok"], j.get("season"), j.get("force"), j.get("area"))
            if info:
                download(id, info); db[id] = info
            else:
                db[id] = None
        except Exception as e:
            print("ERR", id, e, flush=True); continue
        json.dump(db, open(DB, "w"), ensure_ascii=False, indent=0)
        print(id, (db[id] or {}).get("title"), flush=True)
