"""瑞士：build.py 算完结构和地图之后，用资料库的内容覆盖节点（在 build.py 末尾调用）。

资料库是内容的唯一来源：名称、正文、标签、实用信息、通票、经纬度、多日路线分段、图片署名都以 db 为准。
地图、图例、数字、交通方块等派生数据仍由 build.py 计算。
注意：覆盖发生在画地图之后，所以在 db 里改名称或经纬度，地图上的文字和位置要等 content/*.py 同步后才会变；
正文、标签、实用信息等改动会直接生效。
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT
import export
from schema import SWISS

ASSETS = os.path.join(ROOT, "assets", "img")
SITE_IMG = "/home/claude/swiss/site/img"
_D = None
def _db():
    global _D
    if _D is None:
        if not os.path.exists(os.path.join(ROOT, "db", "entries.json")): return None
        _D = export.load("swiss")
        _D["k2i"] = {e["books"]["swiss"]["key"]: i for i, e in _D["E"].items() if "swiss" in e["books"]}
        _D["card"] = dict(_D["tree"]["cardimg"])
    return _D

def has_img(key):
    """build.py 判断某个键有没有照片：资料库已登记，或 site/img 里有旧文件名的新照片。"""
    D = _db()
    if D and key in D["card"]: return True
    return os.path.exists(f"{SITE_IMG}/{key}.webp")

def apply(BOOK, TERMS, PLANDATA, MULTI, CARDIMG, TAGS=None, legacy_img=False):
    D = _db()
    if D is None: return {"skipped": True}
    E, lay, k2i, cfg = D["E"], D["lay"], D["k2i"], D["cfg"]
    stat = {"nodes": 0, "new": [], "terms": 0, "plan": 0, "img": 0, "img_new": []}
    def node(n):
        if n["id"] == "root":
            n.update(cfg["root"])
        else:
            i = k2i.get(n["id"])
            if i is None or "node" not in E[i]["ext"].get("swiss", {}): stat["new"].append(n["id"])
            else:
                e = E[i]
                out = export.emit(E, lay, "swiss", SWISS["node"], e, "node", {"id": n["id"], "c": n.get("c")})
                for k, v in out.items():
                    if k in ("id", "c"): continue
                    if k in SWISS["node"]["PARTIAL"]:
                        n.setdefault(k, {}).update(v)
                    else: n[k] = v
                stat["nodes"] += 1
        for c in n.get("c", []): node(c)
    node(BOOK)
    for k, t in TERMS.items():
        i = k2i.get(k)
        if i and "term" in E[i]["ext"].get("swiss", {}):
            t.update(export.emit(E, lay, "swiss", SWISS["term"], E[i], "term", {})); stat["terms"] += 1
    for k in list(PLANDATA):
        i = k2i.get(k)
        if i and E[i].get("geo") and "plan" in E[i]["ext"].get("swiss", {}):
            e = E[i]; PLANDATA[k] = [e["geo"]["lat"], e["geo"]["lon"], e["practical"]["visit_min"], e["ext"]["swiss"]["plan"]["code"]]
            stat["plan"] += 1
    for k, M in MULTI.items():
        i = k2i.get(k)
        if i and "multi" in E[i]["ext"].get("swiss", {}):
            M.update(export.emit(E, lay, "swiss", SWISS["multi"], E[i], "multi", {}))
    if TAGS is not None: TAGS.update(cfg["engine"]["TAGS"])
    # 图片：改用 编号_用途 文件名，并同步到 site/img
    os.makedirs(SITE_IMG, exist_ok=True)
    for k, c in CARDIMG.items():
        fn = D["card"].get(k)
        if not fn: stat["img_new"].append(k); continue
        c.clear(); c.update(export.card(D["I"], fn, "swiss", legacy=legacy_img))
        stat["img"] += 1
        if legacy_img: continue
        dst = os.path.join(SITE_IMG, fn)
        if not os.path.exists(dst): shutil.copy2(os.path.join(ASSETS, fn), dst)
    return stat

def ingest():
    """旧工具（fetch_img.py 等）仍按旧键把照片存成 site/img/{键}.webp 并写 imgdb.json。
    build.py 开始时调用本函数：把这些照片登记进资料库、改成编号文件名，再把旧文件移到 img_legacy/。"""
    import json, re, urllib.parse
    from tdb import DB, BOOKS, jload, jdump
    D = _db()
    if D is None or not os.path.isdir(SITE_IMG): return []
    news = [f[:-5] for f in os.listdir(SITE_IMG) if f.endswith(".webp") and not re.match(r"^\d{7}_", f)]
    if not news: return []
    IMGDB = jload("/home/claude/techo/books/swiss/src/imgdb.json", {})
    E, I, tree = D["E"], D["I"], D["tree"]
    card = dict(tree["cardimg"]); done = []
    for key in news:
        i = D["k2i"].get(key); info = IMGDB.get(key)
        if not i or not info: continue
        rec = dict(kind="photo", source="Wikimedia Commons", author=info.get("by"), license=info.get("lic"),
                   commercial=not re.search(r"\bNC\b|\bND\b", info.get("lic") or ""),
                   attribution=f'{info.get("by")} / {info.get("lic")} / Wikimedia Commons', season=None, quality="normal",
                   url=info.get("page"), title=info.get("title"), w=info.get("w"), h=info.get("h"),
                   legacy={"swiss": {"key": key, "src": "img/" + urllib.parse.quote(key) + ".webp", "fields": ["src", "by", "lic", "u", "t"], "card": {}}})
        fn = card.get(key)
        if fn: rec.update(owner=I[fn].get("owner"), role=I[fn].get("role"))
        else:
            role = "cover" if not any(I.get(f, {}).get("role") == "cover" for f in E[i]["images"]) else "%02d" % (len(E[i]["images"]) + 1)
            fn = f"{i}_{role}.webp"; rec.update(owner=i, role=role)
            E[i]["images"].append(fn); tree["cardimg"].append([key, fn]); card[key] = fn
        I[fn] = rec
        shutil.copy2(os.path.join(SITE_IMG, key + ".webp"), os.path.join(ASSETS, fn))
        shutil.copy2(os.path.join(SITE_IMG, key + ".webp"), os.path.join(SITE_IMG, fn))
        os.makedirs("/home/claude/swiss/img_legacy", exist_ok=True)
        shutil.move(os.path.join(SITE_IMG, key + ".webp"), f"/home/claude/swiss/img_legacy/{key}.webp")
        done.append((key, fn))
    if done:
        jdump(os.path.join(DB, "entries.json"), E); jdump(os.path.join(DB, "images.json"), dict(sorted(I.items())))
        jdump(os.path.join(BOOKS, "swiss", "tree.json"), tree)
        D["card"] = card
    return done

def early(BOOK, LEAVES=()):
    """在 build.py 画地图之前调用：名称和经纬度先用资料库的，地图上的文字和位置就会跟着资料库变。"""
    D = _db()
    if D is None: return 0
    E, k2i = D["E"], D["k2i"]; n_ = 0
    def walk(n):
        nonlocal n_
        i = k2i.get(n["id"])
        if i:
            e = E[i]
            if e["name"].get("zh") and n.get("n") != e["name"]["zh"]: n["n"] = e["name"]["zh"]; n_ += 1
            g = e.get("geo") or {}
            if "g" in n and "lat" in g and not g.get("approx") and [g["lat"], g["lon"]] != list(n["g"])[:2]:
                n["g"] = [g["lat"], g["lon"]] + list(n["g"])[2:]; n_ += 1
        for c in n.get("c", []): walk(c)
    walk(BOOK)
    for s in LEAVES:                      # build.py 的叶子表另有一份经纬度
        i = k2i.get(s.get("id")); g = (E[i].get("geo") or {}) if i else {}
        if "g" in s and "lat" in g and not g.get("approx"): s["g"] = [g["lat"], g["lon"]] + list(s["g"])[2:]
    return n_
