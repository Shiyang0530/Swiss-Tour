"""各书旧数据字段 ↔ 资料库字段的对照表（迁移和导出共用）。

每一类来源对象（瑞士节点、京都 BOOK 节点、京都 DEEP 等）有三组键：
  MAP     旧键 → (资料库字段路径, 转换方式)
  LAYOUT  只跟这本书的版面有关的键（插画地图坐标、标签位置…），存进 books/{书}/layout.json
  STRUCT  结构键（id、子节点列表），由导出程序按 tree.json 重建
其余没有对应字段的键原样存进条目的 ext.{书}.{来源}，保证导出结果与原书完全一致。
瑞士另有 DERIVED：由 build.py 自动计算的键（地图、图例、数字…），不进资料库。
"""

SWISS = {
    "node": dict(
        MAP={
            "n": ("name.zh", None), "ja": ("name.local", None), "d": ("detail", None), "t": ("tags", None),
            "i": ("practical.info", None), "tip": ("practical.tip", None), "u": ("practical.url", None),
            "pass": ("practical.pass", None), "stay": ("practical.stay", None), "go": ("practical.go", None),
            "buy": ("practical.buy", None), "notes": ("practical.notes", None),
            "star": ("featured", None), "ext": ("search_link", None), "sm": ("season.months", None),
            "term": ("dictionary", "ref1"), "route": ("geo.path", None), "archtx": ("architecture_text", None),
            "sights": ("stops_text", None),
        },
        LAYOUT=set(),
        STRUCT={"id", "c"},
        DERIVED={"f", "kd", "x", "y", "mk", "ty", "bg", "lbl", "sb", "lg", "lm", "rm", "mn", "num", "trn", "via", "col",
                 "oldtown", "multi", "kindx", "phrep", "hotref", "ph"},
        PARTIAL={"tm": ("k", "t", "s")},  # tm 里只有 k/t/s 是内容，svg/prof/lg/mk 由 build.py 画
    ),
    "term": dict(
        MAP={
            "n": ("name.zh", None), "ja": ("name.local", None), "k": ("category", None), "d": ("detail", None),
            "a": ("aliases", None), "w": ("related_spots", "refs"), "q": ("search_query", None),
            "sm": ("season.months", None), "buy": ("practical.buy", None), "u": ("practical.url", None),
            "notes": ("practical.notes", None),
        },
        LAYOUT=set(), STRUCT=set(), DERIVED={"img"}, PARTIAL={},
    ),
    "multi": dict(
        MAP={"stages": ("stages", None), "sum": ("route_summary", None), "plans": ("route_plans", None),
             "alerts": ("alerts", None), "src": ("sources_links", None), "t": ("route_title", None)},
        LAYOUT=set(), STRUCT=set(), DERIVED={"map"}, PARTIAL={},
    ),
}

KYOTO = {
    "book": dict(
        MAP={"n": ("name.zh", None), "ja": ("name.local", None), "t": ("tags", None), "d": ("summary", None),
             "i": ("practical.info", None), "tip": ("practical.tip", None), "u": ("practical.url", None),
             "star": ("featured", None)},
        LAYOUT={"x", "y", "px", "py", "lbl", "r", "img", "w", "edge", "banner", "f", "route"},
        STRUCT={"id", "c"},
    ),
    "deep": dict(
        MAP={"d": ("detail", None), "hl": ("highlights", None), "hist": ("history", None),
             "arch": ("architecture", None), "src": ("sources", None), "sm": ("season.marks", None),
             "ext": ("search_link", None), "i": ("practical.info", None)},
        LAYOUT={"px", "py", "side", "img", "air", "plan", "edge"},
        STRUCT={"c"},
    ),
    "sub": dict(
        MAP={"n": ("name.zh", None), "ja": ("name.local", None), "t": ("tags", None), "d": ("detail", None)},
        LAYOUT={"x", "y", "px", "py", "side", "f"},
        STRUCT={"id"},
    ),
    "term": dict(
        MAP={"n": ("name.zh", None), "ja": ("name.local", None), "k": ("category", None), "a": ("aliases", None),
             "d": ("detail", None), "rel": ("related", "trefs"), "q": ("search_query", None),
             "w": ("related_spots", "refs"), "sm": ("season.months", None), "pref": ("origin_pref", None)},
        LAYOUT=set(), STRUCT=set(),
    ),
}

MISSING = object()

def getp(d, path, default=MISSING):
    for p in path.split("."):
        if not isinstance(d, dict) or p not in d: return default
        d = d[p]
    return d

def setp(d, path, v):
    ps = path.split(".")
    for p in ps[:-1]:
        if not isinstance(d.get(p), dict): d[p] = {}
        d = d[p]
    d[ps[-1]] = v
