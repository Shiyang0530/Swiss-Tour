"""一次性迁移：把瑞士、京都两本书的旧数据拆进共享资料库（规范 v2.0）。

输入
  瑞士  /home/claude/swiss/out/data.js（build.py 的输出，未叠加资料库）、site/img、imgdb.json
  京都  /home/claude/kyoto-techo/index.html 的数据常量、img/
输出（/home/claude/techo）
  db/entries.json   条目（7 位编号为键）
  db/images.json    图片记录（文件名为键，文件名 = 编号 + 用途后缀）
  db/sources.json   各书的参考资料表
  db/ids.json       旧键 → 编号对照（编号永不更改、永不复用）
  books/{书}/book.json   书的配置
  books/{书}/tree.json   目录顺序与引擎所需的顺序表
  books/{书}/layout.json 插画地图坐标等版面数据
  assets/img/        按新文件名存放的全部图片
重复运行是安全的：编号从 ids.json 读取，不会变化。
"""
import json, os, re, shutil, subprocess, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT, DB, BOOKS, Ids, jload, jdump, js_consts
from schema import SWISS, KYOTO, MISSING, getp, setp

ASSETS = os.path.join(ROOT, "assets", "img")
SW_DIR = "/home/claude/swiss"
KY_DIR = "/home/claude/kyoto-techo"
TODAY = "2026-11-18"

ids = Ids()
E = {}                 # id -> entry
LAYOUT = {"swiss": {}, "kyoto": {}}
KMAP = {"swiss": {}, "kyoto": {}}   # (ns, key) -> id

def new_entry(i, typ, **kw):
    e = dict(id=i, type=typ, parent=None, books={}, name={}, geo=None, country=None, admin=None, tier=2,
             score=dict(cn=None, intl=None, official=None, special=None), tags=[], season={}, summary=None,
             detail=None, practical={}, icon=None, images=[], dictionary=[], verified=None, sources=[], ext={})
    e.update(kw)
    return e

# ---------------- 转换 ----------------
def to_db(book, conv, v):
    if conv is None: return v
    km = KMAP[book]
    def r(k, first):
        if not isinstance(k, str): return None
        order = [first, "t" if first == "n" else "n"]
        for ns in order:
            if (ns, k) in km: return km[(ns, k)]
        return None
    if conv == "ref1":
        i = r(v, "n"); return [i] if i else MISSING
    if conv in ("refs", "trefs"):
        if not isinstance(v, list): return MISSING
        out = [r(k, "t" if conv == "trefs" else "n") for k in v]
        return MISSING if None in out else out
    raise ValueError(conv)

def absorb(e, book, src, obj, spec, skip_derived=True):
    """把一个旧对象拆进条目：能对应的放进字段，版面数据进 layout，其余原样留在 ext。"""
    MAP, LAY, STR = spec["MAP"], spec["LAYOUT"], spec["STRUCT"]
    DER, PART = spec.get("DERIVED", set()), spec.get("PARTIAL", {})
    rec = {"_o": []}
    for k, v in obj.items():
        if k in DER: continue
        rec["_o"].append(k)
        if k in STR: continue
        if k in PART:
            rec[k] = {kk: v[kk] for kk in PART[k] if kk in v}; continue
        if k in LAY:
            LAYOUT[book].setdefault(e["id"], {}).setdefault(src, {})[k] = v; continue
        if k in MAP:
            slot, conv = MAP[k]
            dv = to_db(book, conv, v)
            if dv is not MISSING:
                cur = getp(e, slot)
                empty = cur is MISSING or cur in (None, [], {})
                if empty or cur == dv:
                    if empty: setp(e, slot, dv)
                    continue
        rec[k] = v
    e["ext"].setdefault(book, {})[src] = rec

# ---------------- 地理：经纬度 → 国家 / 一级行政区 ----------------
from shapely.geometry import shape, Point
from shapely.prepared import prep
_ADM = []
for f in json.load(open("/home/claude/geo/ne_10m_admin_1.geojson"))["features"]:
    p = f["properties"]
    if p["adm0_a3"] in ("CHE", "FRA", "ITA", "DEU", "AUT", "LIE", "JPN"):
        g = shape(f["geometry"])
        _ADM.append((prep(g), g, p["iso_a2"], p["iso_3166_2"], p["name_zh"] or p["name"]))
def admin_of(lat, lon):
    pt = Point(lon, lat)
    for pg, g, c, code, nm in _ADM:
        if pg.contains(pt): return c, {"code": code, "name": nm}
    best = min(_ADM, key=lambda a: a[1].distance(pt))   # 湖面、国境线上的点取最近的行政区
    if best[1].distance(pt) < 0.05: return best[2], {"code": best[3], "name": best[4]}
    return None, None

def fill_geo(tree, book):
    """叶子用自己的经纬度；面和大区取子项中心（标 approx）；再按经纬度判定国家和行政区，没有坐标的继承上级。"""
    def cen(i):
        e = E[i]
        if e["geo"] and "lat" in e["geo"]: return (e["geo"]["lat"], e["geo"]["lon"])
        pts = [p for p in (cen(c) for c in tree["nodes"][i]["c"]) if p]
        if pts and e["type"] in ("region", "area", "chapter"):
            lat = sum(p[0] for p in pts) / len(pts); lon = sum(p[1] for p in pts) / len(pts)
            e["geo"] = dict(e["geo"] or {}, lat=round(lat, 4), lon=round(lon, 4), approx=True)
            return (lat, lon)
        if e["geo"] and e["geo"].get("path"):
            p = e["geo"]["path"]; return tuple(p[len(p) // 2][:2])
        return None
    for i in tree["nodes"]:
        if i in E: cen(i)
    def adm(i, inh):
        e = E[i]
        if e["type"] != "chapter":
            p = (e["geo"]["lat"], e["geo"]["lon"]) if e["geo"] and "lat" in e["geo"] else None
            if p is None and e["geo"] and e["geo"].get("path"): p = tuple(e["geo"]["path"][0][:2])
            c, a = admin_of(*p) if p else (None, None)
            if c is None and inh: c, a = inh
            if e["type"] in ("region",) and e["geo"] and e["geo"].get("approx"): a = None   # 大区跨多个行政区
            e["country"], e["admin"] = c, a
            inh = (c, a) if c else inh
        for ch in tree["nodes"][i]["c"]: adm(ch, inh)
    for r in tree["nodes"][tree["root"]]["c"]: adm(r, None)
    for i in tree["nodes"]:          # 不在目录树里的子景点：继承上级
        e = E.get(i)
        if e and e["country"] is None and e["type"] != "chapter":
            p = e["parent"]
            while p and E[p]["country"] is None: p = E[p]["parent"]
            if p: e["country"], e["admin"] = E[p]["country"], E[p]["admin"]

# ---------------- 图片 ----------------
SEASON = {"sakura": "sakura", "momiji": "autumn", "snow": "snow"}
IMG = {}          # filename -> record
IMG_OF = {}       # (book, legacy_key) -> filename
def lic_ok(l):
    l = (l or "").lower()
    if "nc" in l or "nd" in l: return False
    return True
def img_name(owner, role):
    base = f"{owner}_{role}"
    n, k = base, 2
    while n in IMG: n = f"{base}{k}"; k += 1
    return n
def add_img(book, key, owner, role, rec, srcpath):
    if (book, key) in IMG_OF: return IMG_OF[(book, key)]
    ext = os.path.splitext(srcpath)[1] or ".webp"
    fn = img_name(owner, role) + ext
    rec = dict(rec, owner=owner, role=role)
    IMG[fn] = rec; IMG_OF[(book, key)] = fn
    E[owner]["images"].append(fn)
    os.makedirs(ASSETS, exist_ok=True)
    if os.path.exists(srcpath): shutil.copy2(srcpath, os.path.join(ASSETS, fn))
    else: rec["missing"] = True
    return fn

def commons_rec(c, extra=None, book=None, key=None, season=None):
    ai = c.get("ai") or c.get("lic") == "AI 插画"
    r = dict(kind="illustration" if ai else "photo",
             source="作者提供（Microsoft Copilot 生成）" if ai else "Wikimedia Commons",
             author=c.get("by"), license=c.get("lic"), commercial=True if ai else lic_ok(c.get("lic")),
             attribution=None if ai else f'{c.get("by")} / {c.get("lic")} / Wikimedia Commons',
             season=season, quality="normal", url=c.get("u"), title=c.get("t"))
    if extra: r.update(extra)
    r["legacy"] = {book: {"key": key, "src": c["src"], "fields": list(c.keys()), "card": {k: v for k, v in c.items() if k not in ("src", "by", "lic", "u", "t")}}}
    return r

# =====================================================================
# 瑞士
# =====================================================================
def swiss():
    # 迁移的输入是叠加资料库之前的 build 输出和旧文件名的图片（保存在 legacy/ 与 img_legacy/）
    src = os.path.join(ROOT, "legacy", "swiss_data_pre_db.js")
    C = js_consts(open(src if os.path.exists(src) else f"{SW_DIR}/out/data.js", encoding="utf-8").read())
    IMGDB = jload(f"{SW_DIR}/imgdb.json", {})
    B, TERMS, PLAN, MULTI, CARD = C["BOOK"], C["TERMS"], C["PLANDATA"], C["MULTI"], C["CARDIMG"]
    nodes = []
    def walk(n, d, p):
        nodes.append((n, d, p))
        for c in n.get("c", []): walk(c, d + 1, n)
    walk(B, 0, None)
    par = {n["id"]: p for n, d, p in nodes}
    kd = {n["id"]: n.get("kd") for n, d, p in nodes}
    def typ(n, p):
        k, t, mk = n.get("kd"), set(n.get("t", [])), n.get("mk")
        if k == "大区": return "region", None, {}
        if k == "专题": return "chapter", None, {}
        if k in ("目的地", "子地点"): return "area", None, {}
        if k == "老城区": return "area", "old_town", {}
        if k == "多日路线": return "line", "route", dict(mode="hike", is_transport=False)
        if k == "分段": return "line", "stage", dict(mode="hike", is_transport=False)
        if k == "观光火车": return "line", "scenic_train", dict(mode="train", is_transport=True)
        if k == "条目":
            top = p
            while top and kd.get(top["id"]) != "专题": top = par.get(top["id"])
            return ("food" if top and top["id"] == "food" else "dict"), None, {}
        if mk == "ski": return "area", "ski_area", {}
        if mk == "hike": return "line", "hike", dict(mode="hike", is_transport=False)
        if mk == "mtn" or "boat" in t:
            mode = "cog" if "cog" in t else "funicular" if "funi" in t else "cable" if "cable" in t else "boat" if "boat" in t else "train" if "train" in t else "mountain"
            return "line", "transport", dict(mode=mode, is_transport=True)
        if t & {"matsuri", "xmas"} and re.search(r"节|市集|狂欢|下山|庆典|音乐|游行|集市", n["n"]): return "event", None, {}
        if p is not None and kd.get(p["id"]) == "景点": return "subspot", None, {}
        return "spot", None, {}
    tree = {"root": None, "nodes": {}, "terms": [], "plan": [], "multi": [], "cardimg": []}
    want = {"berner": "3000101", "longhike": "7000001"}
    # 先给大区编号（伯尔尼高地 = 3000101），再按目录顺序给其他条目编号
    order = [x for x in nodes if x[0].get("kd") == "大区"] + [x for x in nodes if x[0].get("kd") != "大区"]
    for n, d, p in order:
        if d == 0: continue
        ty, sub, extra = typ(n, p)
        i = ids.get("swiss", "n", n["id"], ty, want.get(n["id"]))
        KMAP["swiss"][("n", n["id"])] = i
        if i not in E:
            E[i] = new_entry(i, ty, **({"subtype": sub} if sub else {}), **extra)
        E[i]["books"]["swiss"] = {"key": n["id"]}
    for k in TERMS:
        if ("n", k) not in KMAP["swiss"]:
            ty = "food" if TERMS[k].get("k") == "美食" else "dict"
            i = ids.get("swiss", "t", k, ty); KMAP["swiss"][("t", k)] = i
            E.setdefault(i, new_entry(i, ty))["books"]["swiss"] = {"key": k}
    # 内容
    for n, d, p in nodes:
        if d == 0:
            tree["root"] = "swiss:root"; tree["nodes"]["swiss:root"] = {"key": "root", "c": [KMAP["swiss"][("n", c["id"])] for c in n.get("c", [])]}
            continue
        i = KMAP["swiss"][("n", n["id"])]; e = E[i]
        e["parent"] = KMAP["swiss"][("n", p["id"])] if p is not None and p["id"] != "root" else None
        tree["nodes"][i] = {"key": n["id"], "kd": n.get("kd"), "f": n.get("f"), "c": [KMAP["swiss"][("n", c["id"])] for c in n.get("c", [])]}
        absorb(e, "swiss", "node", n, SWISS["node"])
    rootn = nodes[0][0]
    for k, t in TERMS.items():
        i = KMAP["swiss"].get(("n", k)) or KMAP["swiss"][("t", k)]
        tree["terms"].append(i); absorb(E[i], "swiss", "term", t, SWISS["term"])
        if E[i]["type"] == "dict" and not E[i].get("category"): E[i]["category"] = t.get("k")
    for k, v in PLAN.items():
        i = KMAP["swiss"][("n", k)]; tree["plan"].append(i)
        E[i]["geo"] = dict(E[i]["geo"] or {}, lat=v[0], lon=v[1])
        E[i]["practical"]["visit_min"] = v[2]
        E[i]["ext"].setdefault("swiss", {})["plan"] = {"code": v[3]}
    for k, M in MULTI.items():
        i = KMAP["swiss"][("n", k)]; tree["multi"].append(i)
        absorb(E[i], "swiss", "multi", M, SWISS["multi"])
    # 图片：CARDIMG 的键保持旧键（引擎按键查），文件改名为 编号_cover
    for k, c in CARD.items():
        i = KMAP["swiss"].get(("n", k)) or KMAP["swiss"].get(("t", k))
        fn0 = urllib.parse.unquote(c["src"].split("/", 1)[1])
        db = IMGDB.get(k, {})
        extra = {"w": db.get("w"), "h": db.get("h")} if db else {}
        role = "cover" if not E[i]["icon"] and not any(IMG.get(f, {}).get("role") == "cover" for f in E[i]["images"]) else "02"
        fn = add_img("swiss", k, i, role, commons_rec(c, extra, "swiss", k), next((d for d in (f"{SW_DIR}/img_legacy/{fn0}", f"{SW_DIR}/site/img/{fn0}") if os.path.exists(d)), ""))
        tree["cardimg"].append([k, fn])
    # 封面：ph 指向的图片（自己没有照片的面借用代表景点的照片，不复制，只记录引用）
    for n, d, p in nodes:
        if d == 0 or not n.get("ph"): continue
        e = E[KMAP["swiss"][("n", n["id"])]]
        fn = IMG_OF.get(("swiss", n["ph"]))
        if fn: e["cover"] = fn
    fill_geo(tree, "swiss")
    return tree, C, rootn

# =====================================================================
# 京都
# =====================================================================
def kyoto():
    fx = os.path.join(ROOT, "legacy", "kyoto_v69_src.json")
    if not os.path.exists(fx):
        subprocess.run(["node", os.path.join(ROOT, "tools", "extract_kyoto.js"), f"{KY_DIR}/index.html", fx], check=True, capture_output=True)
    K = json.load(open(fx))
    B, D, T = K["BOOK"], K["DEEP"], K["TERMS"]
    nodes = []
    def walk(n, d, p):
        nodes.append((n, d, p))
        for c in n.get("c", []): walk(c, d + 1, n)
    walk(B, 0, None)
    bid = {n["id"]: (n, d, p) for n, d, p in nodes}
    LINES = {"tetsugaku": ("walk", False), "yamashina-sosui": ("walk", False), "torokko": ("train", True), "nagasaka": ("hike", False)}
    EVENTS = {"gionmatsuri", "biwakohanabi", "yodogawa"}
    def grand(n): return any(c.get("c") for c in n.get("c", []))
    def typ(n, d, p):
        k = n["id"]
        if d == 1: return "region", {}
        if k in LINES: return "line", dict(mode=LINES[k][0], is_transport=LINES[k][1])
        if k in EVENTS or re.search(r"花火|祭$|祭·", n["n"]): return "event", {}
        if d == 2 and grand(n): return "area", {}
        pt = typ_of.get(p["id"])
        if pt in ("spot", "line", "event"): return "subspot", {}
        return "spot", {}
    typ_of = {}
    want = {"kinkakuji": "1000001", "tetsugaku": "2000001", "gionmatsuri": "6000001"}
    tree = {"root": "kyoto:root", "root_order": list(B.keys()), "nodes": {}, "deep": [], "deepc": {}, "terms": [], "plan": [], "cardimg": [], "imgs": []}
    order = [x for x in nodes if x[0]["id"] in want] + [x for x in nodes if x[0]["id"] not in want]
    for n, d, p in sorted(nodes, key=lambda x: x[1]):     # 按深度先算类型（子项类型取决于父项）
        if d == 0: continue
        typ_of[n["id"]] = typ(n, d, p)[0]
    for n, d, p in order:
        if d == 0: continue
        ty, extra = typ(n, d, p)
        i = ids.get("kyoto", "n", n["id"], ty, want.get(n["id"]))
        KMAP["kyoto"][("n", n["id"])] = i
        E.setdefault(i, new_entry(i, ty, **extra))["books"]["kyoto"] = {"key": n["id"]}
    # DEEP 里的子景点（及只在 DEEP 出现的键）
    subpar = {}
    for k, v in D.items():
        for c in v.get("c", []): subpar[c["id"]] = k
    for k in list(subpar) + [k for k in D if k not in bid and k not in subpar]:
        if ("n", k) in KMAP["kyoto"]: continue
        i = ids.get("kyoto", "n", k, "subspot"); KMAP["kyoto"][("n", k)] = i
        E.setdefault(i, new_entry(i, "subspot", tier=3))["books"]["kyoto"] = {"key": k}
    for k, t in T.items():
        if ("n", k) in KMAP["kyoto"] and bid.get(k, ({},))[0].get("n") == t["n"]: continue
        ty = "food" if t.get("k") == "美食" else "dict"
        i = ids.get("kyoto", "t", k, ty); KMAP["kyoto"][("t", k)] = i
        E.setdefault(i, new_entry(i, ty))["books"]["kyoto"] = {"key": k}
    # 内容
    for n, d, p in nodes:
        if d == 0:
            tree["nodes"]["kyoto:root"] = {"key": "root", "c": [KMAP["kyoto"][("n", c["id"])] for c in n.get("c", [])]}
            continue
        i = KMAP["kyoto"][("n", n["id"])]
        E[i]["parent"] = KMAP["kyoto"][("n", p["id"])] if d > 1 else None
        tree["nodes"][i] = {"key": n["id"], "c": [KMAP["kyoto"][("n", c["id"])] for c in n.get("c", [])]}
        absorb(E[i], "kyoto", "book", n, KYOTO["book"])
    for k, v in D.items():
        i = KMAP["kyoto"][("n", k)]; tree["deep"].append(i)
        absorb(E[i], "kyoto", "deep", v, KYOTO["deep"])
        if "c" in v:
            tree["deepc"][i] = []
            for c in v["c"]:
                ci = KMAP["kyoto"][("n", c["id"])]; tree["deepc"][i].append(ci)
                if E[ci]["parent"] is None: E[ci]["parent"] = i
                absorb(E[ci], "kyoto", "sub", c, KYOTO["sub"])
    for k, t in T.items():
        i = KMAP["kyoto"].get(("t", k)) or KMAP["kyoto"][("n", k)]
        tree["terms"].append(i); absorb(E[i], "kyoto", "term", t, KYOTO["term"])
    for k, v in K["PLANDATA"].items():
        i = KMAP["kyoto"][("n", k)]; tree["plan"].append(i)
        E[i]["geo"] = dict(E[i]["geo"] or {}, lat=v[0], lon=v[1])
        E[i]["practical"]["visit_min"] = v[2]
        E[i]["ext"].setdefault("kyoto", {})["plan"] = {"code": v[3]}
    # 子景点挂在父项下
    for i, e in E.items():
        if "kyoto" in e["books"] and i not in tree["nodes"] and e["type"] != "dict" and e["type"] != "food":
            tree["nodes"][i] = {"key": e["books"]["kyoto"]["key"], "c": [], "deep_only": True}
    for pi, cs in tree["deepc"].items():
        for ci in cs:
            if tree["nodes"].get(ci, {}).get("deep_only"):
                tree["nodes"][pi].setdefault("subs", []).append(ci)
    # ---------- 图片归属 ----------
    CARD, IMGS = K["CARDIMG"], K["IMGS"]
    owner = {}   # card key -> (entry id, role)
    def claim(key, i, role):
        if key and key in CARD and key not in owner: owner[key] = (i, role)
    roles = {}
    def nextrole(i):
        roles[i] = roles.get(i, 1) + 1; return "%02d" % roles[i]
    for k, v in D.items():
        i = KMAP["kyoto"][("n", k)]
        claim(v.get("ph"), i, "cover")
        for c in v.get("c", []): claim(c.get("ph"), KMAP["kyoto"][("n", c["id"])], "cover")
    for k, v in D.items():
        i = KMAP["kyoto"][("n", k)]
        for s_ in v.get("season", []):
            if s_.get("img"): claim(s_["img"], i, "cover_" + SEASON.get(s_["t"], s_["t"]))
    def cards(i, lst):
        for c in lst or []:
            if c.get("img") in CARD and c["img"] not in owner: owner[c["img"]] = (i, nextrole(i))
    for k, v in D.items():
        i = KMAP["kyoto"][("n", k)]; cards(i, v.get("cards"))
        for c in v.get("c", []): cards(KMAP["kyoto"][("n", c["id"])], c.get("cards"))
    for k, t in T.items():
        i = KMAP["kyoto"].get(("t", k)) or KMAP["kyoto"][("n", k)]
        if t.get("img") in CARD and t["img"] not in owner: owner[t["img"]] = (i, "cover")
    for key in CARD:
        if key in owner: continue
        m = re.match(r"(h|h2|h3|s|f|o|r)-(.+)$", key)
        base = m.group(2) if m else key
        if m and m.group(1) == "s": base = base.rsplit("-", 1)[0]
        i = KMAP["kyoto"].get(("n", base)) or KMAP["kyoto"].get(("t", base))
        if not i:
            cands = [k for k in bid if k.startswith(base) or base.startswith(k)]
            i = KMAP["kyoto"][("n", cands[0])] if cands else KMAP["kyoto"][("n", "kyoto")]
        role = "cover" if m and m.group(1) == "h" else nextrole(i)
        owner[key] = (i, role)
    for key, c in CARD.items():
        i, role = owner[key]
        if role == "cover" and any(IMG[f]["role"] == "cover" for f in E[i]["images"]): role = nextrole(i)
        season = role.split("_", 1)[1] if role.startswith("cover_") else None
        fn = add_img("kyoto", key, i, role, commons_rec(c, None, "kyoto", key, season), f"{KY_DIR}/{urllib.parse.unquote(c['src'])}")
        tree["cardimg"].append([key, fn])
    # 地图图片（插画导览图、航空照片境内图）
    mapowner = {}
    for n, d, p in nodes:
        if n.get("img"): mapowner.setdefault(n["img"], KMAP["kyoto"][("n", n["id"])] if d else None)
    for k, v in D.items():
        if v.get("img"): mapowner.setdefault(v["img"], KMAP["kyoto"][("n", k)])
    for key, src in IMGS.items():
        i = mapowner.get(key)
        air = key.endswith("AIR")
        if i is None:  # 封面总图
            fn = "kyoto_map" + os.path.splitext(src)[1]
            IMG[fn] = dict(kind="illustration", source="作者绘制", author="Yang Shi", license="作者所有", commercial=True,
                           attribution=None, season=None, quality="featured", url=None, owner=None, role="map", legacy={"kyoto": {"key": key, "src": src}})
            shutil.copy2(f"{KY_DIR}/{src}", os.path.join(ASSETS, fn)); IMG_OF[("kyoto", "IMGS:" + key)] = fn
        else:
            dsrc = D.get(E[i]["books"]["kyoto"]["key"], {}).get("air", {}).get("credit")
            rec = dict(kind="photo" if air else "illustration",
                       source="国土地理院 地理院タイル" if air else "作者绘制", author=None if air else "Yang Shi",
                       license="国土地理院コンテンツ利用規約（出典明示）" if air else "作者所有", commercial=True,
                       attribution=dsrc if air else None, season=None, quality="normal", url="https://maps.gsi.go.jp/" if air else None,
                       legacy={"kyoto": {"key": key, "src": src}})
            fn = add_img("kyoto", "IMGS:" + key, i, "map", rec, f"{KY_DIR}/{src}")
        tree["imgs"].append([key, fn])
    # 封面字段
    for k, v in D.items():
        fn = IMG_OF.get(("kyoto", v.get("ph")))
        if fn: E[KMAP["kyoto"][("n", k)]]["cover"] = fn
    fill_geo(tree, "kyoto")
    return tree, K

# =====================================================================
def tier(e):
    if e["type"] == "subspot": return 3
    if e.get("featured") or "hot" in e["tags"]: return 1
    return 2

def main():
    if os.path.exists(os.path.join(DB, "entries.json")) and "--force" not in sys.argv:
        sys.exit("资料库已存在：迁移只做一次，之后以资料库为准。确实要从旧书重新生成，请加 --force（会覆盖资料库里的修改）。")
    if os.path.exists(ASSETS): shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)
    # 先占用规范里举例的编号：1000001 金阁寺、2000001 哲学之道、3000101 伯尔尼高地、6000001 祇园祭、7000001 长线徒步
    for b, k, t, w in (("kyoto", "kinkakuji", "spot", "1000001"), ("kyoto", "tetsugaku", "line", "2000001"),
                       ("swiss", "berner", "region", "3000101"), ("kyoto", "gionmatsuri", "event", "6000001"),
                       ("swiss", "longhike", "chapter", "7000001"), ("kyoto", "ujitea", "food", "5000001")):
        ids.get(b, "t" if t in ("food", "dict") else "n", k, t, w)
    st, SC, sroot = swiss()
    kt, K = kyoto()
    for e in E.values():
        e["tier"] = tier(e)
        if e.get("cover"): e["icon"] = None
        if e["type"] in ("food", "dict") and not e.get("category"):
            for b in e["ext"].values():
                if "term" in b and b["term"].get("k"): e["category"] = b["term"]["k"]
        e["books"] = dict(sorted(e["books"].items()))
    # 京都的参考资料表
    jdump(os.path.join(DB, "sources.json"), {"kyoto": K["SRC"], "swiss": {}})
    jdump(os.path.join(DB, "entries.json"), dict(sorted(E.items())))
    jdump(os.path.join(DB, "images.json"), dict(sorted(IMG.items())))
    ids.save()
    import books_config
    sw = books_config.swiss(SC, sroot, E, st)
    ky = books_config.kyoto(K, E, kt)
    for b, cfg, tr in (("swiss", sw, st), ("kyoto", ky, kt)):
        jdump(os.path.join(BOOKS, b, "book.json"), cfg)
        jdump(os.path.join(BOOKS, b, "tree.json"), tr)
        jdump(os.path.join(BOOKS, b, "layout.json"), LAYOUT[b])
    from collections import Counter
    print("entries", len(E), Counter(e["type"] for e in E.values()))
    print("images", len(IMG), "missing", sum(1 for r in IMG.values() if r.get("missing")))
    print("by book", Counter(b for e in E.values() for b in e["books"]))

if __name__ == "__main__":
    main()
