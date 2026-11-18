"""往返测试：资料库导出的结果必须与原书数据逐项一致（图片文件名除外）。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export
from tdb import ROOT

def diff(a, b, p="", out=None, lim=15):
    out = [] if out is None else out
    if len(out) >= lim: return out
    if type(a) != type(b): out.append(f"{p}: 类型 {type(a).__name__} ≠ {type(b).__name__}"); return out
    if isinstance(a, dict):
        if list(a) != list(b):
            ka, kb = set(a), set(b)
            if ka != kb: out.append(f"{p}: 键不同 多 {sorted(ka-kb)[:5]} 少 {sorted(kb-ka)[:5]}")
            else: out.append(f"{p}: 键顺序不同")
        for k in a:
            if k in b: diff(a[k], b[k], f"{p}.{k}", out, lim)
    elif isinstance(a, list):
        if len(a) != len(b): out.append(f"{p}: 长度 {len(a)} ≠ {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)): diff(x, y, f"{p}[{i}]", out, lim)
    elif a != b: out.append(f"{p}: {str(a)[:60]!r} ≠ {str(b)[:60]!r}")
    return out

def kyoto():
    src = json.load(open(ROOT + "/legacy/kyoto_v69_src.json"))
    got = export.kyoto_consts(legacy=True)
    bad = 0
    for k in ["TAGS", "BOOK", "DIAG_NUKI", "SRC", "DEEP", "TERMS", "PLANDATA", "CARDIMG", "IMGS", "TAG_PARENT"]:
        d = diff(got[k], src[k], k)
        print(("ok  " if not d else "DIFF"), k, *d[:8], sep="\n   " if d else " ")
        bad += bool(d)
    return bad


def swiss(path=None):
    """瑞士：把资料库叠加到 build.py 的原始输出上，结果必须不变。"""
    import copy
    from tdb import js_consts
    import overlay_swiss
    C = js_consts(open(path or ROOT + "/legacy/swiss_data_pre_db.js", encoding="utf-8").read())
    G = copy.deepcopy(C)
    st = overlay_swiss.apply(G["BOOK"], G["TERMS"], G["PLANDATA"], G["MULTI"], G["CARDIMG"], G["TAGS"], legacy_img=True)
    print("overlay", {k: (v if not isinstance(v, list) else len(v)) for k, v in st.items()})
    bad = 0
    for k in ["TAGS", "BOOK", "TERMS", "PLANDATA", "MULTI", "CARDIMG"]:
        d = diff(G[k], C[k], k)
        print(("ok  " if not d else "DIFF"), k, *d[:8], sep="\n   " if d else " ")
        bad += bool(d)
    return bad


def edit():
    """改资料库里的一个字段，导出结果必须跟着变（京都：金阁寺正文；瑞士：何维克街提示）。"""
    import copy, tempfile, shutil
    import overlay_swiss
    from tdb import DB, js_consts
    tmp = tempfile.mkdtemp(); shutil.copytree(DB, tmp, dirs_exist_ok=True)
    E = json.load(open(os.path.join(tmp, "entries.json")))
    E["1000001"]["detail"] = "测试正文"
    sw = next(i for i, e in E.items() if e["books"].get("swiss", {}).get("key") == "höheweg")
    E[sw]["practical"]["tip"] = "测试提示"; E[sw]["tags"] = E[sw]["tags"] + ["xmas"]
    json.dump(E, open(os.path.join(tmp, "entries.json"), "w"), ensure_ascii=False)
    old = export.DB; export.DB = tmp; overlay_swiss._D = None
    try:
        K = export.kyoto_consts()
        ok1 = K["DEEP"]["kinkakuji"]["d"] == "测试正文"
        C = js_consts(open(ROOT + "/legacy/swiss_data_pre_db.js", encoding="utf-8").read())
        overlay_swiss.apply(C["BOOK"], C["TERMS"], C["PLANDATA"], C["MULTI"], C["CARDIMG"], legacy_img=True)
        def f(n):
            if n["id"] == "höheweg": return n
            for c in n.get("c", []):
                r = f(c)
                if r: return r
        h = f(C["BOOK"]); ok2 = h["tip"] == "测试提示" and "xmas" in h["t"]
    finally:
        export.DB = old; overlay_swiss._D = None; shutil.rmtree(tmp)
    print("ok  " if ok1 and ok2 else "FAIL", "修改资料库后导出随之变化", ok1, ok2)
    return 0 if ok1 and ok2 else 1

if __name__ == "__main__":
    sys.exit(kyoto() + swiss() + edit())
