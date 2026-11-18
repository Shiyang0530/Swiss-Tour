"""从共享资料库导出各书引擎所需的数据。

  kyoto_consts(legacy=False) → 京都 index.html 的数据常量（TAGS、BOOK、DEEP、TERMS…）
  swiss_overlay(...)          → 在瑞士 build.py 算好结构之后，把资料库内容写回节点（见 overlay_swiss.py）
legacy=True 时图片仍用旧文件名，用于和原书逐项比对（往返测试）。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import DB, BOOKS, jload
from schema import SWISS, KYOTO, MISSING, getp

def load(book):
    return dict(E=jload(os.path.join(DB, "entries.json")), I=jload(os.path.join(DB, "images.json")),
                S=jload(os.path.join(DB, "sources.json")), cfg=jload(os.path.join(BOOKS, book, "book.json")),
                tree=jload(os.path.join(BOOKS, book, "tree.json")), lay=jload(os.path.join(BOOKS, book, "layout.json")))

def from_db(E, book, conv, v):
    if conv is None: return v
    key = lambda i: E[i]["books"][book]["key"]
    if conv == "ref1": return key(v[0])
    if conv in ("refs", "trefs"): return [key(i) for i in v]
    raise ValueError(conv)

def emit(E, lay, book, spec, e, src, struct, only=None):
    rec = e["ext"][book][src]
    out = {}
    L = lay.get(e["id"], {}).get(src, {})
    for k in rec["_o"]:
        if only is not None and k not in only: continue
        if k in struct: out[k] = struct[k]
        elif k in rec: out[k] = rec[k]
        elif k in L: out[k] = L[k]
        else:
            slot, conv = spec["MAP"][k]
            v = getp(e, slot)
            if v is MISSING: continue          # 资料库里删掉了这个字段
            out[k] = from_db(E, book, conv, v)
    return out

def card(I, fn, book, legacy):
    r = I[fn]
    lg = r["legacy"][book]
    v = {"src": lg["src"] if legacy else "img/" + fn, "by": r.get("author"), "lic": r.get("license"), "u": r.get("url"), "t": r.get("title")}
    v.update(lg.get("card", {}))
    return {k: v[k] for k in lg.get("fields", v)}

def kyoto_consts(legacy=False):
    D_ = load("kyoto"); E, I, cfg, tree, lay = D_["E"], D_["I"], D_["cfg"], D_["tree"], D_["lay"]
    key = lambda i: E[i]["books"]["kyoto"]["key"]
    def node(i):
        t = tree["nodes"][i]
        return emit(E, lay, "kyoto", KYOTO["book"], E[i], "book", {"id": key(i), "c": [node(c) for c in t["c"]]})
    root = dict(cfg["root"]); root["c"] = [node(c) for c in tree["nodes"][tree["root"]]["c"]]
    order = list(cfg["root"].keys())
    BOOK = {k: root[k] for k in order}; BOOK["c"] = root["c"]
    # 原书 c 在 d 之前还是之后：保持 book.json 记录的顺序
    BOOK = {k: BOOK[k] for k in tree["root_order"]}
    DEEP = {}
    for i in tree["deep"]:
        e = E[i]
        st = {}
        if i in tree["deepc"]:
            st["c"] = [emit(E, lay, "kyoto", KYOTO["sub"], E[c], "sub", {"id": key(c)}) for c in tree["deepc"][i]]
        DEEP[key(i)] = emit(E, lay, "kyoto", KYOTO["deep"], e, "deep", st)
    TERMS = {key(i): emit(E, lay, "kyoto", KYOTO["term"], E[i], "term", {}) for i in tree["terms"]}
    PLAN = {}
    for i in tree["plan"]:
        e = E[i]; PLAN[key(i)] = [e["geo"]["lat"], e["geo"]["lon"], e["practical"]["visit_min"], e["ext"]["kyoto"]["plan"]["code"]]
    CARD = {k: card(I, fn, "kyoto", legacy) for k, fn in tree["cardimg"]}
    IMGS = {k: (I[fn]["legacy"]["kyoto"]["src"] if legacy else "img/" + fn) for k, fn in tree["imgs"]}
    eng = cfg["engine"]
    return dict(TAGS=eng["TAGS"], BOOK=BOOK, DIAG_NUKI=eng["DIAG_NUKI"], SRC=D_["S"]["kyoto"], DEEP=DEEP, TERMS=TERMS,
                PLANDATA=PLAN, CARDIMG=CARD, IMGS=IMGS, TAG_PARENT=eng["TAG_PARENT"])
