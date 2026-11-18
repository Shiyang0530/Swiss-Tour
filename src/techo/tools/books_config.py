"""书的配置文件（规范第六部分“书的配置文件”）。"""

def _regions(E, tree, admin, stays):
    out = []
    for i in tree["nodes"][tree["root"]]["c"]:
        e = E[i]
        if e["type"] != "region": continue
        key = e["books"][next(iter(e["books"]))]["key"]
        out.append(dict(id=i, name=e["name"].get("zh"), admin=admin.get(key, []), stays=stays.get(key, [])))
    return out

def swiss(C, root, E, tree):
    admin = {
        "berner": ["CH-BE（南部：图恩、因特拉肯-上哈斯利、弗鲁蒂根-下西门塔尔、上西门塔尔-萨嫩）"],
        "wallis": ["CH-VS", "FR-74（勃朗峰地区）", "IT-AO（奥斯塔谷，勃朗峰地区）"],
        "luzern": ["CH-LU", "CH-UR", "CH-SZ", "CH-OW", "CH-NW", "CH-ZG"],
        "graubuenden": ["CH-GR"], "ticino": ["CH-TI"], "leman": ["CH-GE", "CH-VD", "CH-FR"],
        "zuerich": ["CH-ZH", "CH-SH", "CH-TG", "CH-SG", "CH-AR", "CH-AI", "CH-GL", "LI"],
        "bernbasel": ["CH-BE（北部）", "CH-BS", "CH-BL", "CH-SO", "CH-AG", "CH-JU", "CH-NE"],
    }
    stays = {k: [v[2]] for k, v in C["AP_TOPDATA"].items()}
    chapters = [i for i in tree["nodes"][tree["root"]]["c"] if E[i]["type"] == "chapter"]
    return dict(
        book_id="swiss", title="瑞士旅行手帖", subtitle="SWISS · TRAVEL NOTEBOOK",
        scope=dict(countries=["CH", "LI"], border_areas=["FR-74", "IT-AO"], note="瑞士全境，加勃朗峰法意两侧"),
        languages=["zh"], min_tier=3, max_depth=5,
        seasons=[dict(key="ski", name="滑雪季", months=[12, 4]), dict(key="hike", name="徒步季", months=[6, 9]),
                 dict(key="autumn", name="秋色", months=[9, 10])],
        theme_tab=dict(name="滑雪和徒步", tags=["ski", "hike"]),
        dict_categories=["交通", "地质与地貌", "美食", "野生动物", "高山植物", "概念"],
        filter_facets={"transport": [["", ["mtn", "train", "boat", "rail", "bus"]]],
                       "hike": [["难度", ["easy", "moderate", "hard"]], ["时长", ["d4h", "d1", "dmulti"]]]},
        regions=_regions(E, tree, admin, stays), chapters=chapters,
        country_info=dict(currency="CHF", languages=["德语", "法语", "意大利语", "罗曼什语"], plug="J 型（C 型可用）",
                          emergency="112 / 144（急救）/ 1414（Rega 直升机救援）"),
        upsells=[],
        engine=dict(TAGS=C["TAGS"]),
        root={k: v for k, v in root.items() if k in ("n", "ja", "d", "t", "i", "tip")},
    )

def kyoto(K, E, tree):
    admin = {"kyoto": ["JP-26（京都市）"], "nara": ["JP-29"], "shiga": ["JP-25"], "osaka": ["JP-27"],
             "uminokyoto": ["JP-26（丹后、中丹）"], "morinokyoto": ["JP-26（南丹、中丹的山区）"]}
    root = {k: v for k, v in K["BOOK"].items() if k != "c"}
    return dict(
        book_id="kyoto", title="京都旅行手帖", subtitle="KYOTO · TRAVEL NOTEBOOK",
        scope=dict(countries=["JP"], note="京都府、奈良县、滋贺县、大阪府"),
        languages=["zh"], min_tier=3, max_depth=5,
        seasons=[dict(key="sakura", name="樱花", months=[3, 4]), dict(key="momiji", name="红叶", months=[11, 12]),
                 dict(key="snow", name="雪景", months=[12, 2]), dict(key="matsuri", name="祭典节庆", months=None)],
        theme_tab=None,
        dict_categories=sorted({t.get("k") for t in K["TERMS"].values() if t.get("k")}),
        filter_facets={},
        regions=_regions(E, tree, admin, {}),
        chapters=[],
        country_info=dict(currency="JPY", languages=["日语"], plug="A 型 100 V", emergency="110（警察）/ 119（急救、消防）"),
        upsells=[],
        engine=dict(TAGS=K["TAGS"], TAG_PARENT=K["TAG_PARENT"], DIAG_NUKI=K["DIAG_NUKI"]),
        root=root,
    )
