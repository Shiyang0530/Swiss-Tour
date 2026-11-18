"""京都：用资料库重新生成 index.html 的数据部分，并把图片改成 编号_用途 文件名。

  python3 build_kyoto.py [仓库路径]
1. index.html 中数据 <script>（从 const TAGS= 到该段结束）的数据常量整体替换为资料库导出的结果；TAG_PARENT 同步替换。
2. img/ 下的旧文件名用 git mv 改成新文件名（保留历史）；资料库里有、仓库里没有的图片从 techo/assets/img 复制过去。
3. sw.js 的离线文件表按新文件名重建，缓存版本号按内容自动更新。
"""
import hashlib, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT
import export

REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/kyoto-techo"
ASSETS = os.path.join(ROOT, "assets", "img")
ORDER = ["TAGS", "BOOK", "DIAG_NUKI", "SRC", "DEEP", "TERMS", "PLANDATA", "CARDIMG", "IMGS"]

def js(v): return json.dumps(v, ensure_ascii=False, separators=(",", ":"))

def main():
    C = export.kyoto_consts(legacy=False)
    L = export.kyoto_consts(legacy=True)
    p = os.path.join(REPO, "index.html")
    s = open(p, encoding="utf-8").read()
    a = s.index("const TAGS="); b = s.index("</script>", a)   # 数据单独在一个 <script> 里
    head = "/* 以下数据由共享资料库生成（techo/tools/build_kyoto.py），请改资料库，不要直接改这里 */\n"
    data = head + "".join(f"const {k}={js(C[k])};\n" for k in ORDER)
    s = s[:a] + data + s[b:]
    s, n = re.subn(r"TAG_PARENT=\{[^;]*\};", "TAG_PARENT=" + js(C["TAG_PARENT"]) + ";", s, count=1)
    assert n == 1
    # 图片改名
    ren = {}
    for kind in ("CARDIMG", "IMGS"):
        for k, v in L[kind].items():
            old = v["src"] if kind == "CARDIMG" else v
            new = C[kind][k]["src"] if kind == "CARDIMG" else C[kind][k]
            ren[old] = new
    moved = copied = 0
    for old, new in ren.items():
        po, pn = os.path.join(REPO, old), os.path.join(REPO, new)
        if os.path.exists(pn): continue
        if os.path.exists(po):
            subprocess.run(["git", "-C", REPO, "mv", old, new], check=True); moved += 1
        else:
            shutil.copy2(os.path.join(ASSETS, os.path.basename(new)), pn); copied += 1
    leftover = [old for old in ren if os.path.exists(os.path.join(REPO, old)) and ren[old] != old]
    open(p, "w", encoding="utf-8").write(s)
    # sw.js
    files = sorted(set(ren.values()))
    sw = os.path.join(REPO, "sw.js")
    w = open(sw, encoding="utf-8").read()
    base = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"]
    h = hashlib.sha1(s.encode() + "".join(files).encode()).hexdigest()[:10]
    w = re.sub(r'const CACHE="[^"]*";const FILES=\[[^\]]*\];', f'const CACHE="kyoto-techo-{h}";const FILES={js(base + files)};', w, count=1)
    open(sw, "w", encoding="utf-8").write(w)
    print(f"index.html {len(s)} chars · 图片改名 {moved} · 复制 {copied} · 残留旧名 {len(leftover)} · sw 文件 {len(base) + len(files)} · CACHE kyoto-techo-{h}")

if __name__ == "__main__":
    main()
