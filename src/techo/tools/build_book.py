"""用通用引擎生成一本书：  python3 build_book.py kyoto|swiss [输出目录]

页面 = engine/head.html + 字体子集 + engine/base.css + engine/body.html
     + <script> CFG（books/{书}/engine.json）+ 书的数据 </script>
     + <script> engine/app.js（插入 engine/planner/{single|multi}.js）</script> + engine/tail.html
另外生成 sw.js（离线缓存表）和 manifest.webmanifest。
书的数据：京都从资料库导出（export.kyoto_consts）；瑞士用 swiss/build.py 的输出 out/data.js（已叠加资料库）。
"""
import base64, hashlib, json, os, re, subprocess, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT, BOOKS, jload

ENG = os.path.join(ROOT, "engine")
SITE = {"kyoto": "/home/claude/kyoto-techo", "swiss": "/home/claude/swiss/site"}
FONTS = "/home/claude/fonts"
KY_ORDER = ["TAGS", "BOOK", "DIAG_NUKI", "SRC", "DEEP", "TERMS", "PLANDATA", "CARDIMG", "IMGS"]

def rd(p): return open(p, encoding="utf-8").read()
def js(v): return json.dumps(v, ensure_ascii=False, separators=(",", ":"))

def book_data(book):
    if book == "kyoto":
        import export
        C = export.kyoto_consts()
        txt = "/* 以下数据由共享资料库生成（techo/tools/build_book.py），请改资料库，不要直接改这里 */\n" + "".join(f"const {k}={js(C[k])};\n" for k in KY_ORDER)
        return txt + plan_proj(C["PLANDATA"])
    if book == "swiss":
        d = rd("/home/claude/swiss/out/data.js")
        hy = base64.b64encode(open("/home/claude/swiss/out/hypso.webp", "rb").read()).decode()
        return d + f'const HYPSO_DATA="data:image/webp;base64,{hy}";\n'
    raise SystemExit("未知的书：" + book)

def plan_proj(PLAN):
    """没有地理底图的书（京都是插画地图）：给行程地图算一个经纬度投影，联网时叠加在线街道底图。"""
    import math
    la = [v[0] for v in PLAN.values()]; lo = [v[1] for v in PLAN.values()]
    cy, cx = (min(la) + max(la)) / 2, (min(lo) + max(lo)) / 2; cl = math.cos(math.radians(cy))
    k = min(560 / ((max(lo) - min(lo)) * cl), 400 / (max(la) - min(la)))
    pxy = {i: [round(300 + (v[1] - cx) * cl * k, 1), round(220 - (v[0] - cy) * k, 1)] for i, v in PLAN.items()}
    bg = f'<g class="geoP" data-p="{cx:.6f} {cy:.6f} {cl:.6f} {k:.3f}"></g>'
    return f"const PXY={js(pxy)};\nconst PLANBG={js(bg)};\n"

def subset(src, out, textfile):
    subprocess.run(["pyftsubset", src, f"--text-file={textfile}", f"--output-file={out}", "--flavor=woff", "--layout-features=*"], check=True)
    return base64.b64encode(open(out, "rb").read()).decode()

def main(book, out=None):
    out = out or SITE[book]
    cfg = jload(os.path.join(BOOKS, book, "engine.json"))
    page = cfg["page"]
    app = rd(os.path.join(ENG, "app.js")).replace("/*@@PLANNER@@*/", rd(os.path.join(ENG, "planner", cfg["ap"]["planner"] + ".js")), 1)
    css = rd(os.path.join(ENG, "base.css"))
    head = rd(os.path.join(ENG, "head.html")).replace("{{DESC}}", page["desc"]).replace("{{SHORT}}", cfg["short"]).replace("{{TITLE}}", cfg["title"])
    back = '<button class="btn back" id="backBtn" disabled aria-label="回到刚才浏览的页面">‹ 返回</button>' if cfg["feat"].get("back") else ""
    body = (rd(os.path.join(ENG, "body.html")).replace("{{SEAL}}", page["seal"]).replace("{{BACK}}", back)
            .replace("{{TITLE}}", cfg["title"]).replace("{{FOLDER}}", cfg["folder"]).replace("{{SEARCH_PH}}", page["search_ph"]))
    ecfg = {k: v for k, v in cfg.items() if k != "page"}
    data = "const CFG=" + js(ecfg) + ";\n" + book_data(book)
    # 离线文件表
    imgs = sorted("img/" + urllib.parse.quote(f) for f in os.listdir(os.path.join(out, "img")) if f.endswith(".webp"))
    FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"] + imgs
    tail = rd(os.path.join(ENG, "tail.html")).replace("{{ID}}", cfg["id"])
    # 字体子集
    tmp = f"/tmp/techo_{book}"; os.makedirs(tmp, exist_ok=True)
    alltext = app + body + head + data + css
    chars = set(c for c in alltext if ord(c) > 0x7F) | set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ·–—…“”‘’（）《》「」、。，：；！？%/+-")
    open(f"{tmp}/chars.txt", "w").write("".join(sorted(chars)))
    open(f"{tmp}/msz.txt", "w").write(cfg["title"])
    msz = subset(f"{FONTS}/MaShanZheng-Regular.ttf", f"{tmp}/msz.woff", f"{tmp}/msz.txt")
    nss = subset(f"{FONTS}/NotoSerifSC[wght].ttf", f"{tmp}/nss.woff", f"{tmp}/chars.txt")
    FONTCSS = ("<style>\n/* Fonts: Ma Shan Zheng (c) The Ma Shan Zheng Project Authors; Noto Serif SC (c) Adobe & Google. All licensed under the SIL Open Font License 1.1 (https://openfontlicense.org). Subsetted for this book. */\n"
               f'@font-face{{font-family:"Ma Shan Zheng";src:url(data:font/woff;base64,{msz}) format("woff");font-weight:400;font-style:normal;font-display:swap}}\n'
               f'@font-face{{font-family:"Noto Serif SC";src:url(data:font/woff;base64,{nss}) format("woff");font-weight:600 900;font-style:normal;font-display:swap}}\n')
    assert css.lstrip().startswith("<style>")
    css_body = css.lstrip()[len("<style>"):]
    a_body = re.sub(r"<[/a-z]*$", "", app.lstrip()[len("<script>"):].rstrip()) + "\n</script>\n"
    html = head + FONTCSS + css_body + body + "<script>\n" + data + "</script>\n" + "<script>" + a_body + tail
    html = html.replace("__N__", str(len(FILES))).replace("__CV__", json.dumps(str(len(FILES))))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    ver = hashlib.sha1(html.encode()).hexdigest()[:10]
    sw = rd(os.path.join(ENG, "sw.js")).replace("{{ID}}", cfg["id"]).replace("{{VER}}", ver).replace("{{FILES}}", json.dumps(FILES))
    open(os.path.join(out, "sw.js"), "w", encoding="utf-8").write(sw)
    man = {"name": cfg["title"], "short_name": cfg["short"], "description": page["desc"].split("：")[0], "start_url": "./", "scope": "./", "display": "standalone",
           "background_color": page["manifest_bg"], "theme_color": page["manifest_bg"], "lang": "zh-Hans",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    open(os.path.join(out, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1))
    print(f"{book}: index.html {len(html)} 字符 · 离线文件 {len(FILES)} · CACHE {cfg['id']}-techo-{ver}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
