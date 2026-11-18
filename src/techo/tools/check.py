"""资料库检查：字段、图片许可、链接。  python3 check.py [--links] [--book kyoto|swiss]

  字段检查   编号格式与类型、上级是否存在、必填字段、标签是否在书的标签表里、词条和图片引用是否存在、旧键是否重复
  图片检查   许可是否可商用、署名、来源网址、所属条目、文件是否存在、分辨率
  链接检查   （加 --links）逐个访问官网、购票和参考资料链接，列出打不开的；需要能上网的环境
结果写到 reports/check-日期.md，并在屏幕上打印摘要。退出码：有错误为 1。
"""
import datetime, json, os, re, sys, urllib.request, urllib.error, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT, DB, BOOKS, jload

DIGIT = {"spot": "1", "subspot": "1", "line": "2", "region": "3", "area": "3", "dict": "4", "decor": "4", "food": "5", "event": "6", "chapter": "7"}
FREE = re.compile(r"^(CC0|Public domain|CC BY(-SA)? [0-9.]+( [a-z]{2})?|AI 插画|作者所有|国土地理院.*)$")
ATTR = re.compile(r"^CC BY")

def site_img(book):
    return {"kyoto": "/home/claude/kyoto-techo/img", "swiss": "/home/claude/swiss/site/img"}.get(book)

def main():
    links = "--links" in sys.argv
    only = sys.argv[sys.argv.index("--book") + 1] if "--book" in sys.argv else None
    E = jload(os.path.join(DB, "entries.json")); I = jload(os.path.join(DB, "images.json"))
    ids = jload(os.path.join(DB, "ids.json"))
    err, warn = [], []
    E_ = lambda i: f"{i} {E[i]['name'].get('zh', '')}" if i in E else i
    # ---------- 编号 ----------
    seen = {}
    for k, v in ids["map"].items():
        if v in seen and seen[v].split(":")[0] == k.split(":")[0]: err.append(f"编号 {v} 在同一本书里对应两个旧键：{seen[v]}、{k}")
        seen[v] = k
    books = {b: jload(os.path.join(BOOKS, b, "engine.json")) for b in os.listdir(BOOKS) if os.path.exists(os.path.join(BOOKS, b, "engine.json"))}
    tags = {b: set(jload(os.path.join(BOOKS, b, "book.json"))["engine"]["TAGS"]) for b in books}
    keys = {}
    NS = {}
    for k, v in ids["map"].items():
        b, ns, _ = k.split(":", 2); NS[(b, v)] = ns
    for i, e in E.items():
        if only and only not in e["books"]: continue
        if not re.fullmatch(r"\d{7}", i): err.append(f"{E_(i)}：编号不是 7 位数字")
        elif DIGIT.get(e["type"]) != i[0]: err.append(f"{E_(i)}：类型 {e['type']} 应以 {DIGIT.get(e['type'])} 开头")
        if e["type"] not in DIGIT: err.append(f"{E_(i)}：未知类型 {e['type']}")
        if not e["name"].get("zh"): err.append(f"{i}：缺中文名称")
        if e.get("parent") and e["parent"] not in E: err.append(f"{E_(i)}：上级 {e['parent']} 不存在")
        if e.get("tier") not in (1, 2, 3): err.append(f"{E_(i)}：tier 应为 1–3")
        if e["type"] in ("spot", "line", "event", "area") and not e.get("geo"): warn.append(f"{E_(i)}：没有经纬度")
        if e["type"] in ("spot", "subspot", "line", "area", "event") and not (e.get("detail") or e.get("summary")): warn.append(f"{E_(i)}：没有正文")
        if e["type"] == "line" and e.get("subtype") != "stage" and "mode" not in e: warn.append(f"{E_(i)}：线没有标交通方式")
        if e["type"] == "food" and not e.get("season"): warn.append(f"{E_(i)}：美食没有时令（规范要求必填）")
        for b, bk in e["books"].items():
            kk = (b, NS.get((b, i), "n"), bk["key"])
            if kk in keys: err.append(f"{b} 的旧键 {bk['key']} 同时属于 {keys[kk]} 和 {i}")
            keys[kk] = i
            bad = [t for t in e.get("tags", []) if b in tags and t not in tags[b]]
            if bad: warn.append(f"{E_(i)}：标签 {bad} 不在《{books[b]['title']}》的标签表里")
        for f in ("dictionary", "related", "related_spots"):
            for r in e.get(f) or []:
                if r not in E: err.append(f"{E_(i)}：{f} 指向不存在的 {r}")
        for f in e.get("images", []) + ([e["cover"]] if e.get("cover") else []):
            if f not in I: err.append(f"{E_(i)}：图片 {f} 没有图片记录")
        if e.get("verified") is None: pass
        elif not re.fullmatch(r"\d{4}-\d\d-\d\d", str(e["verified"])): err.append(f"{E_(i)}：核实日期格式应为 YYYY-MM-DD")
    # ---------- 图片 ----------
    lic = {"可商用": 0, "不可商用": 0}
    for fn, r in I.items():
        if only and only not in r.get("legacy", {}): continue
        if not re.fullmatch(r"(\d{7}|[a-z]+)_[a-z0-9_]+\.(webp|png|jpg)", fn): err.append(f"图片 {fn}：文件名不符合「编号_用途」")
        if r.get("owner") and r["owner"] not in E: err.append(f"图片 {fn}：所属条目 {r['owner']} 不存在")
        L = r.get("license") or ""
        if not L: err.append(f"图片 {fn}：没有许可信息")
        elif not FREE.match(L): warn.append(f"图片 {fn}：许可「{L}」需要人工确认")
        if r.get("commercial") is False: err.append(f"图片 {fn}：标为不可商用（{L}）")
        lic["可商用" if r.get("commercial") else "不可商用"] += 1
        if ATTR.match(L) and not (r.get("author") and r.get("attribution")): err.append(f"图片 {fn}：{L} 需要署名，但缺作者或署名")
        if r.get("kind") == "photo" and not r.get("url"): warn.append(f"图片 {fn}：照片没有来源网址")
        if r.get("kind") not in ("photo", "illustration", "link_only"): err.append(f"图片 {fn}：kind 应为 photo / illustration / link_only")
        if r.get("w") and r["w"] < 800: warn.append(f"图片 {fn}：原图宽度只有 {r['w']} 像素")
        here = [d for d in (os.path.join(ROOT, "assets", "img"), *(site_img(b) for b in r.get("legacy", {}))) if d and os.path.exists(os.path.join(d, fn))]
        if not here and (os.path.isdir(os.path.join(ROOT, "assets", "img")) or any(site_img(b) and os.path.isdir(site_img(b)) for b in r.get("legacy", {}))):
            err.append(f"图片 {fn}：找不到文件")
    # ---------- 链接 ----------
    bad_links = []
    if links:
        urls = {}
        for i, e in E.items():
            if only and only not in e["books"]: continue
            p = e.get("practical", {})
            for u in [p.get("url")] + [x[1] for x in p.get("buy") or [] if isinstance(x, list) and len(x) > 1]:
                if u and u.startswith("http"): urls.setdefault(u, []).append(i)
        for b, S in jload(os.path.join(DB, "sources.json"), {}).items():
            for k, v in S.items():
                if isinstance(v, list) and len(v) > 1 and str(v[1]).startswith("http"): urls.setdefault(v[1], []).append(f"{b}:{k}")
        def probe(u):
            for m in ("HEAD", "GET"):
                try:
                    rq = urllib.request.Request(u, method=m, headers={"User-Agent": "Mozilla/5.0 techo-linkcheck"})
                    with urllib.request.urlopen(rq, timeout=15) as r: return r.status
                except urllib.error.HTTPError as x:
                    if m == "GET" or x.code not in (403, 405, 429): return x.code
                except Exception as x:
                    if m == "GET": return str(x)[:60]
        with cf.ThreadPoolExecutor(8) as ex:
            for u, st in zip(urls, ex.map(probe, urls)):
                if not (isinstance(st, int) and st < 400): bad_links.append((u, st, urls[u]))
    # ---------- 报告 ----------
    day = datetime.date.today().isoformat()
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    out = os.path.join(ROOT, "reports", f"check-{day}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# 资料库检查 {day}\n\n条目 {len(E)} · 图片 {len(I)}（可商用 {lic['可商用']}，不可商用 {lic['不可商用']}）\n\n")
        f.write(f"## 错误（{len(err)}）\n\n" + "".join(f"- {x}\n" for x in err) + "\n")
        f.write(f"## 提醒（{len(warn)}）\n\n" + "".join(f"- {x}\n" for x in warn) + "\n")
        if links: f.write(f"## 打不开的链接（{len(bad_links)}）\n\n" + "".join(f"- {u} → {st}（{', '.join(E_(x) if x in E else x for x in w[:3])}）\n" for u, st, w in bad_links))
    print(f"错误 {len(err)} · 提醒 {len(warn)}" + (f" · 打不开的链接 {len(bad_links)}" if links else "") + f" → {out}")
    for x in err[:15]: print("  ✗", x)
    return 1 if err else 0

if __name__ == "__main__":
    sys.exit(main())
