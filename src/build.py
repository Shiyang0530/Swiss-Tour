import sys, os, json, math, re, importlib
sys.path.insert(0, "/home/claude/swiss/content")
from shapely.geometry import shape, box, mapping, LineString
from shapely.ops import unary_union

TREE = "/home/claude/swiss/tree"
OUT = "/home/claude/swiss/out"
os.makedirs(OUT, exist_ok=True)

def folders(path):
    return sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])

def clean(fname):
    s = re.sub(r"^\d\d_", "", fname)
    s = re.sub(r"（[^）]*）", "", s).strip()
    return s

NAME = {
 "altstadt": "琉森老城", "bernaltstadt": "伯尔尼老城", "swissminiatur": "瑞士小人国", "narcisses": "蒙特勒水仙花季",
 "fraumuenster": "圣母大教堂", "grossmuenster": "苏黎世大教堂", "lagobianco": "伯尔尼纳白湖", "lacblanc": "白湖",
 "rothornzermatt": "罗特洪峰", "desalpe": "格吕耶尔牧牛下山节", "alpabfahrt": "阿彭策尔牧牛下山节",
 "rigipanorama": "瑞吉全景步道", "rigisled": "瑞吉雪橇道", "glaciercave": "铁力士冰川洞", "rathausbasel": "巴塞尔市政厅",
 "zytglogge": "伯尔尼钟楼", "vinorama": "拉沃葡萄酒品鉴", "baslermuenster": "巴塞尔大教堂", "doubs": "杜河瀑布",
 "rigibahn": "瑞吉铁路", "pilatusbahn": "皮拉图斯铁路", "stoosbahn": "斯托斯缆索铁路", "chaeserrugg": "沙瑟鲁格",
 "panoramic": "勃朗峰全景吊厢", "kapellenweg": "萨斯费小教堂之路", "landesmuseum": "瑞士国家博物馆",
 "zermattski": "采尔马特雪场", "zuerichsee": "苏黎世湖游船", "lagolugano": "卢加诺湖游船",
 "chauxdefonds": "拉绍德封与力洛克", "valere": "锡永瓦莱尔与图尔比永城堡", "gianadda": "吉亚纳达基金会",
 "cathedrallausanne": "洛桑大教堂", "vieilleville": "日内瓦老城与圣皮埃尔大教堂", "seeboat": "琉森湖游船",
 "lakeboat": "图恩湖与布里恩茨湖游船", "eigertrail": "艾格北壁步道", "royalwalk": "曼利兴–小沙伊德格全景步道",
 "stp": "瑞士通票", "halffare": "瑞士半价卡", "tellpass": "琉森旅行通票", "flixbus": "FlixBus 长途巴士", "mbmultipass": "勃朗峰多日通票", "berneroberlandpass": "伯尔尼高地通票", "jungfraupass": "少女峰通票",
}

TAGS = dict(hot="热门景点", unesco="世界遗产", ski="滑雪季", hike="徒步", autumn="赏秋", xmas="圣诞市集", matsuri="节庆活动",
  mtn="山地交通", cog="齿轨铁路", funi="缆索铁路", cable="缆车", train="观景列车", boat="湖船",
  arch="建筑", alps="阿尔卑斯山", rhine="莱茵河", view="观景台", glacier="冰川", lake="湖景", waterfall="瀑布", nature="自然", spa="温泉",
  town="小镇与老城区", castle="城堡", church="教堂修道院", museum="博物馆", art="艺术", history="历史", literature="文学", myth="神话传说",
  food="美食", cheese="奶酪", chocolate="巧克力", shopping="购物",
  family="亲子", elderly="适合老人", couple="适合情侣", free="免门票", crossborder="跨境",
  easy="轻松", moderate="适中", hard="进阶")
LV = {"e": "easy", "m": "moderate", "h": "hard"}

regions = [importlib.import_module(f"r0{i}").REGION for i in range(1, 9)]
r9 = importlib.import_module("r09")

top = folders(TREE)
assert len(top) == 13, top

def mk(id, n, ja, f, d, t, **kw):
    node = dict(id=id, n=n, ja=ja, f=f, d=d, t=list(dict.fromkeys(t)))
    for k, v in kw.items():
        if v not in (None, {}, [], ""): node[k] = v
    return node

IDS = set()
PLANDATA = {}
LEAVES = []
sys.path.insert(0, "/home/claude/swiss/content")
from topo import HIKE as _HK
import hot as _HOT
HIKE_ROUTES = {k for k, v in _HK.items() if not (len(v) > 3 and v[3] == "ski")}
HIKE_ROUTES |= {r["node"] for v in _HOT.HOT.values() for r in v if r["node"]}
HIKE_ROUTES -= {"brevent", "glacierparadise", "rochersdenaye", "niesen", "wine", "truebsee"}
HIKE_ROUTES |= {"hauteroute", "viaalpina", "tmb"}
HIKE_ROUTES |= {"seealpsee", "lauenensee", "engstligen", "drachenweg", "emmentalbruecke", "truebsee"}

VILLAGE = {"wengen", "muerrenvillage", "gimmelwald", "iseltwald", "brienz", "spiez", "gstaadvillage", "zermattvillage",
           "saasfeevillage", "riederalp", "bettmeralp", "chamonixvillage", "courmayeurvillage", "stmoritzvillage", "poschiavo",
           "scuol", "guarda", "davostown", "heididorf", "gandria", "morcote", "ascona", "gruyerestown", "steinamrhein",
           "appenzelltown", "stursanne", "murten"}
def leaf(s, f):
    assert s["id"] not in IDS, s["id"]; IDS.add(s["id"])
    t = list(s["t"])
    if s["lv"]: t.append(LV[s["lv"]])
    sm = s["sm"] or {}
    for k in ("ski", "autumn", "xmas", "matsuri"):
        if k in sm and k not in t: t.append(k)
    # 「徒步」只标在具体徒步路线上
    if s["id"] in HIKE_ROUTES:
        if "hike" not in t: t.insert(min(1, len(t)), "hike")
    else:
        t = [x for x in t if x != "hike"]
    if any(x in t for x in ("cog", "funi", "cable")) and "mtn" not in t: pass
    t = [x for x in t if x not in ("garden", "music")]
    if s["id"] in _EX2.ARCH and "arch" not in t: t.insert(min(1, len(t)), "arch")
    t = [x for x in t if x not in ("town", "village")]
    if s["id"] in _PR.TOWN: t.insert(min(1, len(t)), "town")
    _txt = (s["n"] or "") + s["ja"] + s["d"]
    if "莱茵" in _txt or "Rhein" in s["ja"] or "Rhin" in s["ja"]: t.append("rhine")

    n = s["n"] or NAME.get(s["id"]) or clean(f)
    q = s["ja"]
    node = mk(s["id"], n, s["ja"], f, s["d"], t, i=s["i"], tip=s["tip"], u=s["u"], star=s["star"] or None, sm=sm or None,
              ext="https://www.google.com/search?tbm=isch&q=" + q.replace(" ", "+"))
    node["g"] = s["g"]
    if s["id"] in _EX2.ARCH: node["archtx"] = _EX2.ARCH[s["id"]]
    fl = "".join(s["fl"].split())
    PLANDATA[s["id"]] = [round(s["g"][0], 4), round(s["g"][1], 4), s["dur"], fl]
    LEAVES.append(node)
    return node

BOOK = mk("root", "瑞士及周边", "Schweiz · Suisse · Svizzera · Svizra", "",
 "瑞士国土面积约 4.1 万平方公里，比中国的台湾稍大，却浓缩了阿尔卑斯山最精华的风景：48 座四千米以上的雪峰、一千五百多个湖泊和欧洲最长的冰川。全国有德语、法语、意大利语和罗曼什语四种官方语言，翻过一座山口，语言、建筑和饮食就会随之改变。瑞士的公共交通准点而密集，火车、湖船、齿轨铁路和缆车组成一张网，不开车也能到达几乎所有山顶。这本书把瑞士分成八个大区，并把勃朗峰周边的法国、意大利以及列支敦士登一并收入，另附交通、长线徒步、美食、野生动植物、地质与地貌五个专题。",
 ["unesco"], i={"a": "苏黎世机场和日内瓦机场是两大国际门户，巴塞尔机场位于法国境内"},
 tip="瑞士四季分明：12 月至次年 4 月是滑雪季，6 月至 9 月是徒步季，9 月底至 10 月是赏秋季节；4 月底至 5 月和 11 月是山区淡季，许多缆车停运检修。")
BOOK["c"] = []

import routes as _RT
import extra2 as _EX2
import prune as _PR
import oldtown as _OT
# 勃朗峰区域：夏蒙尼 + 库马约尔与奥斯塔谷 + 尚佩、瑞士段费雷谷、特里安
for R in regions:
    ids = [A["id"] for A in R["c"]]
    if "chamonix" in ids and "courmayeur" in ids:
        A_ch = R["c"][ids.index("chamonix")]; A_co = R["c"][ids.index("courmayeur")]; A_ma = R["c"][ids.index("martigny")]
        mv = [x for x in A_ma["c"] if x["id"] in ("champex", "valferretch", "trient")]
        A_ma["c"] = [x for x in A_ma["c"] if x not in mv]
        A_ch["c"] = A_ch["c"] + A_co["c"] + mv
        R["c"].remove(A_co)
        A_ch["n"] = "勃朗峰区域"; A_ch["ja"] = "Massif du Mont-Blanc · Monte Bianco"
        A_ch["d"] = ("勃朗峰是阿尔卑斯山的最高峰，海拔约 4806 米，山体横跨法国、意大利和瑞士三国。本书把环绕它的三处山谷合成一个区域："
                     "北麓法国的夏蒙尼（Chamonix）是登山之都，南麓意大利的库马约尔（Courmayeur）通过天空之路缆车和勃朗峰隧道与它相连，"
                     "东侧瑞士的尚佩（Champex）、费雷谷和特里安则是环勃朗峰徒步经过的安静山村。往东顺着奥斯塔谷而下，还有罗马古城奥斯塔和中世纪城堡。"
                     "法国和意大利一侧使用欧元，瑞士通票基本不适用。")
for R in regions:
    for A in R["c"]:
        if A["id"] in _RT.EXTRA: A["c"].append(_RT.EXTRA[A["id"]])
        if A["id"] in _EX2.EXTRA2: A["c"].extend(_EX2.EXTRA2[A["id"]])
        A["c"] = [x for x in A["c"] if x["id"] not in _PR.DEL]
        for aid_, pid_, kids_, nm_ in _OT.OT:
            if A["id"] != aid_: continue
            pool = {x["id"]: x for x in A["c"]}
            pool.update({k: v for k, v in _OT.NEW.items()})
            ids_ = [i for i, x in enumerate(A["c"]) if x["id"] in kids_ + [pid_]]
            par = pool[pid_]; par["kids"] = [pool[k] for k in kids_]; par["n"] = nm_
            rest = [x for x in A["c"] if x["id"] not in kids_ + [pid_]]
            pos = sum(1 for i, x in enumerate(A["c"]) if i < min(ids_) and x["id"] not in kids_ + [pid_])
            rest.insert(pos, par); A["c"] = rest
        for x in A["c"]:
            if x["id"] in _PR.MERGE and _PR.MERGE[x["id"]] not in x["d"]: x["d"] = x["d"] + _PR.MERGE[x["id"]]
for ri, R in enumerate(regions):
    rf = top[ri]
    rnode = mk(R["id"], R["n"] or clean(rf), R["ja"], rf, R["d"], R["t"], i=R["i"], tip=R["tip"])
    assert R["id"] not in IDS; IDS.add(R["id"])
    rnode["hub"] = R["hub"]; rnode["hubn"] = R["hubn"]
    rnode["c"] = []
    afs = folders(os.path.join(TREE, rf))
    assert len(afs) == len(R["c"]), (rf, len(afs), len(R["c"]))
    for ai, A in enumerate(R["c"]):
        af = afs[ai]
        anode = mk(A["id"], A["n"] or clean(af), A["ja"], af, A["d"], A["t"], i=A["i"], tip=A["tip"])
        assert A["id"] not in IDS, A["id"]; IDS.add(A["id"])
        sfs = folders(os.path.join(TREE, rf, af))
        assert len(sfs) == len(A["c"]), (af, len(sfs), len(A["c"]), sfs)
        anode["c"] = []
        for si, s in enumerate(A["c"]):
            ln = leaf(s, sfs[si])
            if s.get("kids"):
                kfs = folders(os.path.join(TREE, rf, af, sfs[si]))
                assert len(kfs) == len(s["kids"]), (sfs[si], kfs)
                ln["c"] = [leaf(k, kfs[ki]) for ki, k in enumerate(s["kids"])]
                ln["oldtown"] = 1; LEAVES.remove(ln)
            anode["c"].append(ln)
        # area tags: union of frequent child tags (unesco, crossborder)
        for k in ("unesco", "crossborder"):
            if any(k in c["t"] for c in anode["c"]) and k not in anode["t"]: anode["t"].append(k)
        rnode["c"].append(anode)
    BOOK["c"].append(rnode)

# special chapters
TERMS = {}
import wild as _WILD
import geo as _GEOC
for ci, CH in enumerate([r9.TRAINS, r9.TRANSPORT, r9.FOOD, _WILD.WILD, _GEOC.GEO]):
    cf = top[8 + ci]
    cnode = mk(CH["id"], CH["n"], CH["ja"], cf, CH["d"], [], tip=CH.get("tip"))
    IDS.add(CH["id"])
    sfs = folders(os.path.join(TREE, cf))
    assert len(sfs) == len(CH["c"]), (cf, len(sfs))
    cnode["c"] = []
    for si, T in enumerate(CH["c"]):
        f = sfs[si]
        assert T["id"] not in IDS, T["id"]; IDS.add(T["id"])
        n = NAME.get(T["id"]) or clean(f)
        node = mk(T["id"], n, T["ja"], f, T["d"], T["t"], i=T["i"], tip=T["tip"], u=T["u"], star=T["star"] or None, sm=T["sm"],
                  ext="https://www.google.com/search?tbm=isch&q=" + T["ja"].replace(" ", "+"), buy=T.get("buy"), notes=T.get("notes"))
        if T["route"]:
            node["route"] = T["route"]
            mid = T["route"][len(T["route"]) // 2]
            node["g"] = mid
        if CH["id"] == "transport":
            TERMS[T["id"]] = dict(n=n, ja=T["ja"], k="交通", d=T["d"], a=[n], node=T["id"])
            if T.get("buy"): TERMS[T["id"]]["buy"] = T["buy"]; TERMS[T["id"]]["u"] = T["u"]
            if T.get("notes"): TERMS[T["id"]]["notes"] = T["notes"]
            node["term"] = T["id"]
        if CH["id"] == "food":
            fd = T["food"]
            TERMS[T["id"]] = dict(n=n, ja=T["ja"], k="美食", d=T["d"], a=[n], w=fd["w"], q=fd["q"], node=T["id"])
            if fd.get("sm"): TERMS[T["id"]]["sm"] = fd["sm"]
            node["term"] = T["id"]
            node["t"] = ["food"] + (["cheese"] if T["id"] in ("fondue", "raclette") else []) + (["chocolate"] if T["id"] == "chocolate" else [])
        if CH["id"] in ("wild", "geology"):
            fd = T["food"]
            TERMS[T["id"]] = dict(n=n, ja=T["ja"], k=fd["k"], d=T["d"], a=[n], w=fd["w"], sm=fd["sm"], q=fd["q"], node=T["id"])
            if not fd["sm"]: TERMS[T["id"]].pop("sm")
            node["term"] = T["id"]; node["t"] = []
        cnode["c"].append(node)
    if CH["id"] == "trains": _TRAINNODE = cnode; continue
    if CH["id"] == "transport": cnode["c"] = _TRAINNODE["c"] + cnode["c"]; cnode["d"] = "这一章先介绍瑞士最有名的几条观光火车线路，每条都附有线路图；后面是山地交通的种类和各种交通通票。瑞士的公共交通准点而密集，火车、湖船、齿轨铁路和缆车组成一张网，不开车也能到达几乎所有山顶。" + cnode["d"]
    BOOK["c"].append(cnode)

# extra aliases for glossary linking
EXTRA_ALIAS = {"utal": ["U形谷", "U 形谷"], "haengetal": ["悬谷"], "moraine": ["冰碛"], "karst": ["喀斯特", "溶沟"], "bergsturz": ["山崩"], "overthrust": ["推覆构造"], "permafrost": ["永久冻土", "冻土"], "gneiss": ["片麻岩"], "glacierlake": ["冰斗湖", "冰碛湖"], "marmot": ["旱獭"], "ibex": ["羱羊", "野山羊"], "larchtree": ["落叶松"], "arolla": ["五针松", "阿尔沃松"], "blacknose": ["黑鼻羊"], "lammergeier": ["胡兀鹫"], "chough": ["黄嘴山鸦"], "cograil": ["齿轨铁路", "齿轨"], "funicular": ["缆索铁路"], "aerialcable": ["空中缆车"], "gondola": ["吊厢"], "chairlift": ["吊椅"],
  "stp": ["瑞士通票"], "halffare": ["半价卡"], "jungfraupass": ["少女峰通票"], "tellpass": ["退尔通票", "琉森旅行通票", "Tell-Pass", "Lucerne Travel Pass"], "flixbus": ["FlixBus", "Flixbus", "长途巴士"], "fondue": ["芝士火锅"], "raclette": ["烤奶酪"],
  "roesti": ["土豆饼"], "geschnetzeltes": ["苏黎世小牛肉"], "nusstorte": ["恩加丁坚果塔", "坚果塔"], "vermicelles": ["栗子泥甜点", "栗子蛋糕"],
  "gerstensuppe": ["大麦汤"], "revision": ["检修停运"], "mbmultipass": ["勃朗峰多日通票"], "berneroberlandpass": ["伯尔尼高地通票"]}
for k, al in EXTRA_ALIAS.items():
    TERMS[k]["a"] = list(dict.fromkeys(al + TERMS[k]["a"]))
TERMS["unesco_t"] = dict(n="世界遗产", ja="UNESCO-Welterbe", k="概念", a=["世界自然遗产", "世界文化遗产"],
  d="瑞士共有 13 处世界遗产（截至 2020 年代），本书收录了其中多处：伯尔尼老城、圣加仑修道院、贝林佐纳三城堡、雷蒂亚铁路阿尔布拉线与伯尔尼纳线、拉沃葡萄园梯田、拉绍德封与力洛克制表城等文化遗产，以及少女峰–阿莱奇等自然遗产。")
TERMS["glacier_t"] = dict(n="冰川", ja="Gletscher", k="概念", a=["冰舌", "冰裂缝"],
  d="冰川是由多年积雪压实成冰、在重力作用下缓慢流动的巨大冰体。瑞士约有 1400 条冰川，最大的是阿莱奇冰川。由于气候变暖，瑞士的冰川正在快速消退，在莫特拉奇、冰海等冰川旁的步道上，可以看到标出历年冰川位置的牌子。走上冰川必须由持证向导带领。")
TERMS["alpabzug"] = dict(n="牧牛下山节", ja="Alpabzug / Désalpe", k="概念", a=["牧牛下山"],
  d="每年 9 月到 10 月初，在高山牧场度过整个夏天的牛群被赶回山下的村庄，牧民给领头的牛戴上花冠和大铜铃，穿着传统服装列队下山，村里会举办集市和庆祝活动。阿彭策尔、格吕耶尔和瓦莱州的下山节最为有名。")
TERMS["romansh"] = dict(n="罗曼什语", ja="Rumantsch", k="概念", a=[],
  d="罗曼什语是瑞士的第四种官方语言，源于古罗马时期的通俗拉丁语，主要在格劳宾登州的山谷中使用，说这种语言的人约占瑞士人口的 0.5%。在恩加丁和格劳宾登的许多村庄，路牌和房屋上的题字都是罗曼什语。")

# ---------- geometry ----------
import mapx
from mapx import rail_svg, poi_layers, scalebar, Placer, marker_boxes, mk_kind, tw, topic_hike, topic_ski, esc
from topo import HIKE, SKI, SKI_USE
from gloss import GLOSS
mapx.HIKE_NODES.update(k for k, v in HIKE.items() if (v[3] if len(v) > 3 else "hike") == "hike")
mapx.SKI_NODES.update(k for k in SKI_USE if k not in ("glacier3000", "corvatsch", "piznair", "parsenn", "jakobshorn", "weisshorn", "glacierparadise"))
mapx.SKI_NODES.update(k for k, v in HIKE.items() if len(v) > 3 and v[3] == "ski")
G = lambda f: json.load(open("/home/claude/geo/" + f))
countries = [(ft["properties"]["ADM0_A3"], shape(ft["geometry"])) for ft in G("ne_10m_admin_0_countries.geojson")["features"]]
REG = box(4.5, 44.8, 11.8, 48.5)
countries = [(a, g.intersection(REG)) for a, g in countries if g.intersects(REG)]
LAKENAME = {"Lake Geneva": "日内瓦湖", "Bodensee": "博登湖", "Lago di Como": "科莫湖", "Walensee": "瓦伦湖", "Zugersee": "楚格湖", "Bielersee": "比尔湖",
  "Zürichsee": "苏黎世湖", "Neuchâtel": "纳沙泰尔湖", "MURTENSEE": "穆尔滕湖", "Vierwaldstättersee": "琉森湖", "Lago di Lugano - Ceresio": "卢加诺湖",
  "Brienzersee": "布里恩茨湖", "Thunersee": "图恩湖", "Lac d' Annecy": "安纳西湖", None: "马焦雷湖"}
lakes = []
for f in ("ne_10m_lakes.geojson", "ne_10m_lakes_europe.geojson"):
    for ft in G(f)["features"]:
        g = shape(ft["geometry"])
        if g.intersects(REG):
            nm = ft["properties"].get("name")
            lakes.append((LAKENAME.get(nm, ""), g.intersection(REG)))
from geo_extra import SMALL_LAKES as _SL
from shapely.geometry import Point as _Pt
from shapely import affinity as _aff
_NSL = 0
for zh, la, lo, A_, B_, ang in _SL:
    if any(g.contains(_Pt(lo, la)) for _, g in lakes): continue
    e = _Pt(0, 0).buffer(1, 32)
    e = _aff.scale(e, A_ / 2, B_ / 2)
    e = _aff.rotate(e, ang, origin=(0, 0))
    e = _aff.scale(e, 1 / (111.32 * math.cos(math.radians(la))), 1 / 111.32, origin=(0, 0))
    lakes.append(("", _aff.translate(e, lo, la))); _NSL += 1
print("small lakes added", _NSL)
rivers = []
for ft in G("ne_10m_rivers_lake_centerlines.geojson")["features"]:
    g = shape(ft["geometry"])
    if g.intersects(REG): rivers.append(g.intersection(REG))
CNAME = {"FRA": "法国", "DEU": "德国", "ITA": "意大利", "AUT": "奥地利", "LIE": "列支敦士登", "CHE": "瑞士"}

W, H = 600, 440

class Proj:
    def __init__(self, pts, minspan=0.04, pad=(70, 55)):
        lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
        la0, la1, lo0, lo1 = min(lats), max(lats), min(lons), max(lons)
        cl = math.cos(math.radians((la0 + la1) / 2)); self.cl = cl
        sy = max(la1 - la0, minspan); sx = max((lo1 - lo0) * cl, minspan * 1.3)
        k = min((W - 2 * pad[0]) / sx, (H - 2 * pad[1]) / sy); self.k = k
        self.cy = (la0 + la1) / 2; self.cx = (lo0 + lo1) / 2
    def xy(self, lat, lon):
        return (W / 2 + (lon - self.cx) * self.cl * self.k, H / 2 - (lat - self.cy) * self.k)
    def window(self, m=30):
        lo0 = self.cx - (W / 2 + m) / (self.cl * self.k); lo1 = self.cx + (W / 2 + m) / (self.cl * self.k)
        la1 = self.cy + (H / 2 + m) / self.k; la0 = self.cy - (H / 2 + m) / self.k
        return box(lo0, la0, lo1, la1)

def path_of(geom, P):
    tol = 0.8 / (P.k)  # degrees ~ 0.8px
    g = geom.simplify(tol, preserve_topology=False)
    out = []
    def ring(coords, close):
        pts = [P.xy(y, x) for x, y in coords]
        if len(pts) < 2: return ""
        s = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        return s + ("Z" if close else "")
    def walk(g):
        t = g.geom_type
        if t == "Polygon":
            out.append(ring(g.exterior.coords, True))
            for r in g.interiors: out.append(ring(r.coords, True))
        elif t == "LineString": out.append(ring(g.coords, False))
        elif t in ("MultiPolygon", "MultiLineString", "GeometryCollection"):
            for x in g.geoms: walk(x)
    walk(g)
    return "".join(out)

def bg_svg(P, routes=None, labels=True):
    win = P.window()
    s = []
    for a3, g in countries:
        gi = g.intersection(win)
        if gi.is_empty: continue
        fill = "#F6F4EA" if a3 in ("CHE", "LIE") else "#E4E1D2"
        s.append(f'<path d="{path_of(gi, P)}" fill="{fill}" stroke="none"/>')
    if P.k < 2000:
        x0, y0 = P.xy(48.5, 4.5); x1, y1 = P.xy(44.8, 11.8)
        s.append(f'<image href="__HY__" x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" preserveAspectRatio="none"/>')
    for a3, g in countries:
        gi = g.boundary.intersection(win)
        if gi.is_empty: continue
        s.append(f'<path d="{path_of(gi, P)}" fill="none" style="stroke:var(--muted)" stroke-width="1" stroke-dasharray="5 4" opacity=".7"/>')
    for g in rivers:
        gi = g.intersection(win)
        if gi.is_empty: continue
        s.append(f'<path d="{path_of(gi, P)}" fill="none" style="stroke:var(--water)" stroke-width="2.2" stroke-linecap="round"/>')
    for nm, g in lakes:
        gi = g.intersection(win)
        if gi.is_empty: continue
        s.append(f'<path d="{path_of(gi, P)}" style="fill:var(--water)"/>')
    s.append(rail_svg(P, path_of))
    s.append(f'<g class="geoP" data-p="{P.cx:.6f} {P.cy:.6f} {P.cl:.6f} {P.k:.3f}"></g>')
    if routes:
        for r in routes:
            if isinstance(r, dict):
                pts = [P.xy(a, b) for a, b in r["r"]]; d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
                s.append(f'<path d="{d}" fill="none" style="stroke:var(--page)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
                         f'<path class="rt" data-rt="{r["id"]}" d="{d}" fill="none" style="stroke:{r["col"]}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
                continue
            pts = [P.xy(a, b) for a, b in r]
            s.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" fill="none" style="stroke:var(--shu)" stroke-width="3" stroke-dasharray="7 5" stroke-linecap="round" opacity=".75"/>')
    lbl = []
    if labels:
        for a3, g in countries:
            if a3 not in CNAME or a3 == "CHE": continue
            gi = g.intersection(P.window(-40))
            if gi.is_empty: continue
            if gi.area * P.k * P.k * P.cl < 6000 and a3 != "LIE": continue
            if a3 == "LIE" and P.k < 150: continue
            pt = gi.representative_point(); x, y = P.xy(pt.y, pt.x)
            lbl.append(dict(t=CNAME[a3], x=round(x), y=round(y)))
        for nm, g in lakes:
            if not nm: continue
            gi = g.intersection(P.window(-20))
            if gi.is_empty or gi.area * P.k * P.k * P.cl < 900: continue
            pt = gi.representative_point(); x, y = P.xy(pt.y, pt.x)
            from geo_extra import LAKE_ELEV
            lbl.append(dict(t=nm + (f" {LAKE_ELEV[nm]}" if nm in LAKE_ELEV else ""), x=round(x), y=round(y) + 4))
    return "".join(s), lbl

def centroid(node):
    if "g" in node: return node["g"]
    pts = [centroid(c) for c in node.get("c", []) if centroid(c)]
    if not pts: return None
    g = [sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)]
    return g

OUTT = set("hike ski mtn cog funi cable glacier lake waterfall view nature alps train boat".split())
def spot_mk(c):
    ty = c.get("ty")
    if ty == "town": return "vtown"
    if ty == "old": return "vold"
    if ty == "cul": return "vcul"
    return mk_kind(c) or "vout"
def layout(node, minspan, extra=None, routes=None, only=None):
    kids = [c for c in node["c"] if centroid(c) and (only is None or only(c))]
    if not kids: return
    pts = [centroid(c) for c in kids] + (extra or [])
    if routes:
        for r in routes: pts += r["r"] if isinstance(r, dict) else r
    P = Proj(pts, minspan)
    pos = {c["id"]: list(P.xy(*centroid(c))) for c in kids}
    # repel overlapping markers (label-aware: labels sit to the right of pins)
    lw = {c["id"]: sum(13.5 if ord(ch) > 255 else 7 for ch in c.get("mn", c["n"])) for c in kids}
    ids = list(pos)
    for _ in range(400):
        moved = False
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = pos[ids[i]], pos[ids[j]]
                ax0, ax1 = a[0] - 14, a[0] + 22 + lw[ids[i]]; bx0, bx1 = b[0] - 14, b[0] + 22 + lw[ids[j]]
                if ax1 < bx0 or bx1 < ax0: continue
                dy = b[1] - a[1]
                if abs(dy) >= 26: continue
                push = (26 - abs(dy)) / 2 + 0.3
                sgn = 1 if dy >= 0 else -1
                if abs(dy) < 0.01: sgn = 1 if a[0] <= b[0] else -1
                a[1] -= sgn * push; b[1] += sgn * push; moved = True
        for p in pos.values():
            p[0] = min(W - 24, max(24, p[0])); p[1] = min(H - 30, max(26, p[1]))
        if not moved: break
    for c in kids:
        c["x"], c["y"] = round(pos[c["id"]][0], 1), round(pos[c["id"]][1], 1)
    bg, lbl = bg_svg(P, routes)
    placer = Placer()
    for l in lbl:
        w = tw(l["t"], 12); placer.add((l["x"] - w / 2, l["y"] - 12, l["x"] + w / 2, l["y"] + 3))
    marker_boxes(placer, kids, lw)
    ov, okeys = mapx.overlay(P, path_of, HIKE, SKI) if node["id"] != "root" else ("", [])
    ill = ""
    ilids = IL.ROOT if node["id"] == "root" else IL.REGION.get(node["id"], [])
    sz = 34 if node["id"] == "root" else 38
    for lid in ilids:
        g = GEO.get(lid)
        if not g: continue
        x, y = P.xy(*g)
        if not (16 < x < W - 16 and 16 < y < H - 36): continue
        bx = (x - sz / 2, y - sz / 2, x + sz / 2, y + sz / 2)
        if placer.ok(bx): placer.add(bx); cx, cy = x, y
        else:
            pos = None
            for gp, s2 in ((3, sz), (12, sz), (6, sz * .82), (20, sz * .82)):
                pos = placer.place(x, y, s2, s2, gap=gp)
                if pos: break
            if not pos: continue
            cx, cy = pos[0] + s2 / 2, pos[1] + s2 / 2
            ill += IL.icon(IL.KIND[lid], cx, cy, s2); continue
        ill += IL.icon(IL.KIND[lid], cx, cy, sz)
    poi, keys = poi_layers(P, placer, avoid_pts=[(c["x"], c["y"]) for c in kids], skip_names={c["n"] for c in kids})
    rf = region_fill(P) if node["id"] == "root" else ""
    node["bg"] = bg + rf + ov + poi + ill
    if ill: okeys = okeys + ["ill"]
    node["lbl"] = lbl
    node["sb"] = scalebar(P)
    kinds = []; hasarea = False
    for c in kids:
        if c.get("kd") in ("目的地", "子地点", "大区", "专题") or (c.get("c") and not c.get("kd")):
            hasarea = True; continue
        k = spot_mk(c); c["mk"] = k
        if k not in kinds: kinds.append(k)
    leafy = bool(kinds)
    lg = (["area"] if hasarea else []) + [k for k in ("vout", "hike", "ski", "mtn", "vtown", "vold", "vcul") if k in kinds]
    if routes: lg.append("trainroute")
    lg += okeys + [k for k in ("peak", "pass", "town") if k in keys] + ["rail", "water", "border"] + (["hypso"] if P.k < 2000 else [])
    node["lg"] = lg
    return P


# ---------- 热门 / 精选：只保留 50 处 ----------
def _hot(n):
    for c in n.get("c", []):
        if not c.get("c") or c.get("multi") or c.get("oldtown") or c["id"] in ("tmb", "hauteroute", "viaalpina"):
            c["t"] = [k for k in c["t"] if k != "hot"]
            if c["id"] in _PR.HOT50: c["t"].insert(0, "hot"); c["star"] = 1
            else: c.pop("star", None)
        _hot(c)
_hot(BOOK)
# ---------- 阿尔卑斯山 tag：阿尔卑斯山区片区里与山有关的景点 ----------
NONALP = {"basel", "berncity", "jura", "emmental", "zurichcity", "schaffhausen", "stgallen", "geneve", "lausanne", "lavaux",
          "luzerncity", "lugano", "mendrisio", "locarno", "bellinzona", "gruyeres"}
for R in BOOK["c"]:
    for A in R.get("c", []):
        if A["id"] in NONALP or R["id"] in ("trains", "transport", "food", "wild", "geology"): continue
        for n in A.get("c", []):
            if any(x in n["t"] for x in ("hike", "ski", "glacier", "mtn", "cog", "cable", "funi")) or re.search(r"山|峰|冰川|山口|阿尔卑", n["n"]):
                if "alps" not in n["t"]: n["t"].insert(1, "alps")
# ---------- multi-day routes -> route node with stage children ----------
import multi as MULTIM, urllib.parse
from topo import HIKE as _HKX
def _hav(a, b):
    R_ = 6371; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_ * math.asin(math.sqrt(h))
def _find(n, id_):
    if n["id"] == id_: return n
    for c in n.get("c", []):
        r = _find(c, id_)
        if r: return r
ROUTE_NODES = []
for mk_, M in MULTIM.MULTI.items():
    rid = _RT.ROUTE_OF[mk_]; rn = _find(BOOK, rid)
    pts = M.get("pts") or _HKX[M["hike"]][2]
    names = [p[2] if len(p) >= 6 else None for p in pts]
    LEAVES.remove(rn); PLANDATA.pop(rid, None)
    rf = rn["f"]; rdir = None
    for root_, dirs, _f in os.walk(TREE):
        if os.path.basename(root_) == rf: rdir = root_; break
    assert rdir, rf
    short = {"tmb": "环勃朗峰", "hauteroute": "瑞士高山之路", "viaalpina": "Via Alpina "}[mk_]
    prev = 0; kids = []
    for si, st in enumerate(M["stages"]):
        nm = M["ends"][si]
        j = len(pts) - 1 if si == len(M["stages"]) - 1 else next(k for k in range(prev + 1, len(pts)) if names[k] == nm)
        seg = [list(p) for p in pts[prev:j + 1]]
        named = [p for p in seg if len(p) >= 6]
        for p in named: p[5] = "w"
        named[0][5] = "s"; named[-1][5] = "e"
        o0, o1 = named[0][3], named[-1][3]
        num, route, km, up, dn, tm_, hi, sc = st
        km = float(km)
        # stage midpoint by distance
        cum = [0]
        for a_, b_ in zip(seg, seg[1:]): cum.append(cum[-1] + _hav(a_, b_))
        half = cum[-1] / 2; k_ = next(i for i, c in enumerate(cum) if c >= half)
        g = [round(seg[k_][0], 4), round(seg[k_][1], 4)]
        hrs = None
        mt = re.match(r"(\d+(?:\.\d+)?)", tm_ or "")
        if mt: hrs = float(mt.group(1))
        else: hrs = round(km / 4 + up / 500, 1)
        lv = "h" if (up >= 1200 or km >= 22) else "m" if up >= 600 or km >= 12 else "e"
        sid = f"{rid}-s{si + 1}"
        title = f"第 {num} 段 · {route}"
        d = (f"{short}第 {num} 段，从{named[0][2]}走到{named[-1][2]}，约 {km:g} 公里，爬升约 {up} 米、下降约 {dn} 米"
             + (f"，一般需要 {tm_.replace('h', '小时').strip()}" if tm_ else f"，按距离和爬升估算约需 {round(hrs * 2) / 2:g} 小时") + "。"
             + (f"最高点是{hi}。" if hi else "")
             + (f"{sc.rstrip('。')}。" if sc else ""))
        stats = f"约 {km:g} km · ↑{up} m ↓{dn} m" + (f" · {tm_}" if tm_ else "")
        t = []  # 分段不单独进标签列表，标签只挂在整条路线上
        f = f"{si + 1:02d}_第{num}段 {route}".replace("/", "-")
        os.makedirs(os.path.join(rdir, f), exist_ok=True)
        sn = mk(sid, title, f"{o0} → {o1}", f, d, t, i={"l": stats, "h": rn.get("i", {}).get("h")}, sm=rn.get("sm"),
                ext="https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote(f"{o0} {o1} hike"))
        sn["g"] = g
        sn["tm"] = topic_hike((title, stats, [tuple(p) for p in seg]), Proj, bg_svg, path_of)
        sn["mk"] = "hike"; sn["mn"] = named[-1][2]; sn["num"] = str(num).split("–")[0]
        PLANDATA[sid] = [g[0], g[1], int(hrs * 60), ""]
        LEAVES.append(sn); kids.append(sn); IDS.add(sid)
        prev = j
    rn["c"] = kids; rn["multi"] = [mk_]
    rn["kindx"] = "多日路线"
    ROUTE_NODES.append((rn, [(p[0], p[1]) for p in pts]))

REGCOL = {"berner": "#E07A5F", "wallis": "#3D85C6", "luzern": "#6FAE8A", "graubuenden": "#9B6BD6", "ticino": "#E2B04A",
          "leman": "#3FA7B8", "zuerich": "#D877A8", "bernbasel": "#9AA33B"}
def region_fill(P):
    from shapely.ops import voronoi_diagram
    from shapely.geometry import MultiPoint, Point as Pt_
    pts = {}; owner = {}
    def walk(n, rid):
        if "g" in n and not n.get("c"):
            k = (round(n["g"][1], 3), round(n["g"][0], 3))
            if k not in owner: owner[k] = rid
        for c in n.get("c", []): walk(c, rid)
    for R in BOOK["c"]:
        if R["id"] in REGCOL: walk(R, R["id"])
    mp = MultiPoint([Pt_(*k) for k in owner])
    vd = voronoi_diagram(mp, envelope=box(4.5, 44.8, 11.8, 48.5))
    che = unary_union([g for a, g in countries if a in ("CHE", "LIE")])
    out_w = [Pt_(*k) for k, r in owner.items() if r == "wallis" and not che.contains(Pt_(*k))]
    clip = unary_union([che, MultiPoint(out_w).convex_hull.buffer(0.09)]) if out_w else che
    cells = {r: [] for r in REGCOL}
    for cell in vd.geoms:
        for k, r in owner.items():
            if cell.contains(Pt_(*k)): cells[r].append(cell); break
    s = []
    for r, cs in cells.items():
        if not cs: continue
        g = unary_union(cs).intersection(clip).buffer(0.015).buffer(-0.015)
        g = g.intersection(P.window())
        if g.is_empty: continue
        d = path_of(g, P)
        s.append(f'<path class="rgf" d="{d}" fill="{REGCOL[r]}" fill-opacity=".09" stroke="{REGCOL[r]}" stroke-opacity=".45" stroke-width="1.1"/>')
    return '<g class="regions">' + "".join(s) + '</g>'
# ================= 重组：大区 → 目的地 → 子地点 → 景点 =================
import dest as _DS
SPECIAL = ("trains", "transport", "food", "wild", "geology")
OLDPATH = {}
def _op(n, p):
    for c in n.get("c", []):
        OLDPATH[c["id"]] = p + [c["f"]]; _op(c, p + [c["f"]])
_op(BOOK, [])
AREAS = {}; SPOTS = {}
for R in BOOK["c"]:
    if R["id"] in SPECIAL: continue
    for A in R["c"]:
        AREAS[A["id"]] = A
        for c in A["c"]: SPOTS[c["id"]] = c
_used = set()
_EXPL = set()
def _ex(s):
    _EXPL.update(x for x in s["spots"] if not x.startswith("@"))
    for t in s["subs"]: _ex(t)
for _l in _DS.DEST.values():
    for _s in _l: _ex(_s)
def _take(lst):
    out = []
    for x in lst:
        if x.startswith("@"):
            out += [c for c in AREAS[x[1:]]["c"] if c["id"] not in _used and c["id"] not in _DS.LONG and c["id"] not in _EXPL and c not in out]
        else: out.append(SPOTS[x])
    for c in out:
        assert c["id"] not in _used, c["id"]; _used.add(c["id"])
    return out
def _mkdest(spec, kd):
    if spec["base"]:
        node = AREAS[spec["base"]]
        if spec["n"]: node["n"] = spec["n"]
        if spec["ja"]: node["ja"] = spec["ja"]
        if spec["d"]: node["d"] = spec["d"]
    else:
        node = mk(spec["id"], spec["n"], spec["ja"], "", spec["d"], [])
    for k in ("bg", "lbl", "sb", "lg", "x", "y", "mk"): node.pop(k, None)
    node["c"] = [_mkdest(s, "子地点") for s in spec["subs"]] + _take(spec["spots"])
    node["kd"] = kd
    for k in ("unesco", "crossborder"):
        if any(k in c.get("t", []) for c in node["c"]) and k not in node["t"]: node["t"].append(k)
    return node
for R in BOOK["c"]:
    if R["id"] in _DS.DEST:
        R["c"] = [_mkdest(s, "目的地") for s in _DS.DEST[R["id"]]]
_left = set(SPOTS) - _used - set(_DS.LONG)
assert not _left, _left
LH = mk("longhike", "长线徒步", "Fernwanderwege", "",
        "瑞士有好几条跨越多个地区的长线徒步路线，适合用一到三周慢慢走完，也可以只挑其中几段。这一章收录三条：横穿瑞士北阿尔卑斯的 Via Alpina、从勃朗峰走到马特洪峰的瑞士高山之路，以及穿越法国、意大利和瑞士三国的环勃朗峰徒步（TMB）。各段途经的目的地页面也会列出相关路线。", ["hike"])
LH["c"] = [SPOTS[i] for i in _DS.LONG]; LH["kd"] = "专题"
BOOK["c"].insert([R["id"] for R in BOOK["c"]].index("transport"), LH)
# kd / ty for every node
def _kd(n, depth, parent):
    for c in n.get("c", []):
        if depth == 0: c["kd"] = c.get("kd") or ("专题" if c["id"] in SPECIAL else "大区")
        elif c.get("kd") in ("目的地", "子地点", "专题"): pass
        elif c.get("oldtown"): c["kd"] = "老城区"
        elif c.get("multi") and c.get("c"): c["kd"] = "多日路线"
        elif parent.get("kd") == "多日路线": c["kd"] = "分段"
        elif parent.get("kd") == "专题" and c.get("route"): c["kd"] = "观光火车"
        elif parent.get("kd") == "专题" and parent["id"] in SPECIAL and parent["id"] != "trains": c["kd"] = "条目"
        else: c["kd"] = "景点"
        if c["kd"] in ("景点", "老城区", "多日路线"):
            t = set(c.get("t", []))
            c["ty"] = ("old" if (c["id"] in _DS.OLD_T or c.get("oldtown")) else "town" if c["id"] in _DS.TOWN_T
                       else "out" if (t & OUTT or c["kd"] == "多日路线") else "cul")
        _kd(c, depth + 1, c)
_kd(BOOK, 0, BOOK)
# folder names from final order
def _fn(n):
    for i, c in enumerate(n.get("c", [])):
        if c["id"] in SPECIAL or n["id"] in SPECIAL or n["id"] in ("trains",): pass
        nm = c["n"].replace("/", "-").replace("\\", "-").replace(":", "：")
        c["f"] = f"{i + 1:02d}_{nm}" if n["id"] != "root" or True else c["f"]
        _fn(c)
_fn(BOOK)
NEWPATH = {}
def _np(n, p):
    for c in n.get("c", []):
        NEWPATH[c["id"]] = p + [c["f"]]; _np(c, p + [c["f"]])
_np(BOOK, [])
json.dump({"old": {k: "/".join(v) for k, v in OLDPATH.items()}, "new": {k: "/".join(v) for k, v in NEWPATH.items()}},
          open(OUT + "/folder_map.json", "w"), ensure_ascii=False, indent=0)
sys.path.insert(0, "/home/claude/techo/tools")
import overlay_swiss as _OV0
print("db early (名称/经纬度)", _OV0.early(BOOK, LEAVES))
import illus as IL
GEO = {n["id"]: n["g"] for n in LEAVES}
# root: regions placed at centroid, extend to cover Chamonix/Aosta
_ROOTP = layout(BOOK, 1.0, extra=[[45.75, 6.85], [47.75, 9.6]], only=lambda c: "hub" in c)
for R in BOOK["c"]:
    if R["id"] in ("food", "wild", "geology"): continue
    if R["id"] == "transport":
        import trainstops as _TS
        for c in R["c"]:
            if c["id"] in _TS.COL: c["col"] = _TS.COL[c["id"]]
        layout(R, 1.0, routes=[dict(r=c["route"], id=c["id"], col=c.get("col", "#C4432B")) for c in R["c"] if c.get("route")]); continue
    if R["id"] == "longhike":
        layout(R, 0.4); continue
    if R["id"] == "trains":
        layout(R, 1.0, routes=[c["route"] for c in R["c"]])
        continue
    layout(R, 0.25)
    def _lay(n):
        for c in n.get("c", []):
            if c.get("kd") == "目的地": layout(c, 0.06 if any(x.get("kd") == "子地点" for x in c["c"]) else 0.035)
            elif c.get("kd") == "子地点": layout(c, 0.03)
            elif c.get("kd") == "专题": layout(c, 0.3)
            _lay(c)
    _lay(R)
def _otl(n):
    for c in n.get("c", []):
        if c.get("oldtown"): layout(c, 0.008)
        _otl(c)
_otl(BOOK)
for rn, line in ROUTE_NODES:
    P_ = layout(rn, 0.02, extra=line)
    xy = [P_.xy(a, b) for a, b in line]
    dd = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    rn["bg"] += (f'<path d="{dd}" fill="none" style="stroke:var(--page)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
                 f'<path d="{dd}" fill="none" stroke="{mapx.HIKE_C}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    if "route_hike" not in rn["lg"]: rn["lg"].insert(1, "route_hike")

# ---------- 小镇地图（细节图） ----------
from shapely.geometry import Point as _P2, MultiPoint as _MP
ALLS = []
def _alls(n):
    for c in n.get("c", []):
        if "g" in c and c.get("kd") in ("景点", "老城区", "多日路线"): ALLS.append(c)
        _alls(c)
_alls(BOOK)
TYC = {"out": "#5f8a3a", "town": "#b0763a", "old": "#8e3b46", "cul": "#C4432B"}
def town_map(n):
    g = n["g"]
    P = Proj([g], 0.022)
    bg, _ = bg_svg(P, labels=False)
    win = P.window(-10)
    placer = Placer()
    x0, y0 = P.xy(*g)
    placer.add((x0 - 14, y0 - 14, x0 + 14, y0 + 14))
    near = [s for s in ALLS if s is not n and win.contains(_P2(s["g"][1], s["g"][0]))]
    marks = []; labs = []; lst = []
    for s in near:
        x, y = P.xy(*s["g"]); placer.add((x - 7, y - 7, x + 7, y + 7))
    ov, okeys = mapx.overlay(P, path_of, HIKE, SKI)
    for s in near:
        x, y = P.xy(*s["g"])
        w = tw(s["n"], 12); pos = placer.place(x, y, w, 15, gap=11)
        lab = f'<text class="tsl" x="{pos[0]:.1f}" y="{pos[1] + 12:.1f}">{esc(s["n"])}</text>' if pos else ""
        marks.append(f'<g class="lmk" data-go="{s["id"]}" data-cx="{x:.1f}" data-cy="{y:.1f}"><circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{TYC.get(s.get("ty"), "#C4432B")}" stroke="#fff" stroke-width="2"/>{lab}</g>')
        lst.append([s["id"]])
    w = tw(n["n"], 14); pos = placer.place(x0, y0, w, 18, gap=19)
    me = (f'<g class="lmk me" data-cx="{x0:.1f}" data-cy="{y0:.1f}"><path d="M{x0-11:.1f} {y0+10:.1f}V{y0-2:.1f}L{x0:.1f} {y0-12:.1f}L{x0+11:.1f} {y0-2:.1f}V{y0+10:.1f}Z" fill="{TYC.get(n.get("ty"))}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/>'
          + (f'<text class="tsl" x="{pos[0]:.1f}" y="{pos[1] + 14:.1f}" style="font-size:14px;font-weight:700">{esc(n["n"])}</text>' if pos else "") + '</g>')
    poi, keys = poi_layers(P, placer, avoid_pts=[(x0, y0)] + [P.xy(*s["g"]) for s in near], skip_names={s["n"] for s in near})
    lg = ["v" + n.get("ty")] + ["v" + t for t in ("out", "town", "old", "cul") if t != n.get("ty") and any(s.get("ty") == t for s in near)] + okeys + [k for k in ("peak", "pass", "town") if k in keys] + ["rail", "water"]
    return dict(svg=bg + ov + poi + "".join(marks) + me + scalebar(P), lg=[k for k in lg if k], near=lst)
NTM = 0
for s in ALLS:
    if s.get("ty") in ("town", "old") and not s.get("c") and not s.get("tm"):
        s["lm"] = town_map(s); NTM += 1
print("town maps", NTM)
# ---------- 徒步路线跨目的地显示 ----------
ROUTEX = {}
for k, spec in HIKE.items():
    if len(spec) > 3 and spec[3] == "ski": continue
    ROUTEX[k] = (None, [(p[0], p[1]) for p in spec[2]])
for mk_, M in MULTIM.MULTI.items():
    rid = {"tmb": "tmb", "hauteroute": "hauteroute", "viaalpina": "viaalpina"}[mk_]
    pts = M.get("pts") or HIKE[M["hike"]][2]
    names = [p[2] if len(p) >= 6 else None for p in pts]
    segs = []; prev = 0
    for si, st in enumerate(M["stages"]):
        j = len(pts) - 1 if si == len(M["stages"]) - 1 else next(q for q in range(prev + 1, len(pts)) if names[q] == M["ends"][si])
        segs.append((str(st[0]), [(p[0], p[1]) for p in pts[prev:j + 1]])); prev = j
    ROUTEX[rid] = (segs, [(p[0], p[1]) for p in pts])
NV = 0
def _desc(n):
    out = set()
    for c in n.get("c", []): out.add(c["id"]); out |= _desc(c)
    return out
def _via(n):
    global NV
    for c in n.get("c", []):
        if c.get("kd") in ("目的地", "子地点"):
            gs = [s["g"] for s in ALLS if s["id"] in _desc(c)]
            if gs:
                hull = _MP([(g[1], g[0]) for g in gs]).convex_hull.buffer(0.02)
                dd = _desc(c); vv = []
                for rid, (segs, line) in ROUTEX.items():
                    if rid in dd or rid not in NODEMAP: continue
                    if segs:
                        hit = [lab for lab, sp in segs if any(hull.contains(_P2(lo, la)) for la, lo in sp)]
                        if hit: vv.append([rid, "第 " + "、".join(hit) + " 段"])
                    elif any(hull.contains(_P2(lo, la)) for la, lo in line): vv.append([rid, ""])
                if vv: c["via"] = vv; NV += len(vv)
        _via(c)
# ---------- 观光火车线路图（高亮线路） ----------
def train_map(n):
    rt = n["route"]
    P = Proj(rt, 0.12, pad=(80, 70))
    bg, _ = bg_svg(P, labels=False)
    xy = [P.xy(a, b) for a, b in rt]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    placer = Placer()
    for x, y in xy: placer.add((x - 4, y - 4, x + 4, y + 4))
    import trainstops as _TS
    col = _TS.COL.get(n["id"], "#C4432B")
    line = (f'<path d="{d}" fill="none" style="stroke:var(--page)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity=".95"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    stops = _TS.STOPS.get(n["id"]) or [("", rt[0][0], rt[0][1], True), ("", rt[-1][0], rt[-1][1], True)]
    sp = []
    for nm, la, lo, big in stops:
        x, y = P.xy(la, lo); r = 7 if big else 4.6
        placer.add((x - r - 2, y - r - 2, x + r + 2, y + r + 2)); sp.append((nm, x, y, big, r))
    ends = ""
    for nm, x, y, big, r in sp:
        ends += (f'<circle class="stn" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col if big else "#fff"}" stroke="{"#fff" if big else col}" stroke-width="{2.5 if big else 2.2}"/>')
    labs = ""
    for nm, x, y, big, r in sorted(sp, key=lambda t: not t[3]):
        if not nm: continue
        w = sum(14.5 if ord(ch) > 255 else 7.5 for ch in nm) * (1.08 if big else 0.92)
        pos = placer.place(x, y, w, 15 if big else 13, gap=r + 6)
        if not pos:
            print("NOPLACE", n["id"], nm); continue
        tx, ty = pos
        labs += (f'<text class="tstop{" big" if big else ""}" x="{tx:.1f}" y="{ty + (11.5 if big else 10):.1f}">{esc(nm)}</text>')
    poi, keys = poi_layers(P, placer, avoid_pts=xy)
    lg = ["trainroute", "stn"] + [k for k in ("peak", "pass", "town") if k in keys] + ["rail", "water", "border"]
    return dict(svg=bg + line + ends + poi + labs + scalebar(P), lg=lg)
# ---- 观景列车：只保留 8 条线路；登山铁路归入山地交通；沿途看点与车站对应 ----
import trainstops as _TS, trainsights as _TG, re as _re2
_ALLN = {}
def _all(n):
    _ALLN[n["id"]] = n
    for c in n.get("c", []): _all(c)
_all(BOOK)
for _n in _ALLN.values():
    t = _n.get("t", [])
    if "train" in t and _n["id"] not in _TS.COL:
        t.remove("train")
        if any(k in t for k in ("cog", "funi", "cable")) or _n["id"] in ("jungfraubahn", "rothorn", "gornergrat", "montenvers", "rigibahn", "pilatusbahn", "generoso", "rochersdenaye"):
            if "mtn" not in t: t.append("mtn")
            if "cog" not in t and _n["id"] in ("jungfraubahn", "rothorn", "gornergrat", "montenvers", "rigibahn", "pilatusbahn", "generoso", "rochersdenaye"): t.append("cog")
def _mins(txt):
    m = _re2.search(r"约\s*(\d+(?:\.\d+)?)\s*小时(?:\s*(\d+)\s*分钟)?", txt) or _re2.search(r"约\s*(\d+)\s*分钟", txt)
    if not m: return 0
    return float(m.group(1)) * 60 + int(m.group(2) or 0) if "小时" in m.group(0) else int(m.group(1))
def _km(a, b):
    import math
    return math.hypot((a[0] - b[0]) * 111.2, (a[1] - b[1]) * 111.2 * math.cos(math.radians(a[0])))
NTH = 0
for tid, col in _TS.COL.items():
    T = _ALLN.get(tid)
    if not T: continue
    T["sights"] = [[nm, d, (lid if lid in _ALLN else None)] for nm, d, lid in _TG.SIGHTS.get(tid, [])]
    rt = T["route"]; cum = [0]
    for i in range(1, len(rt)): cum.append(cum[-1] + _km(rt[i - 1], rt[i]))
    L = cum[-1]; tot = _mins((T.get("i") or {}).get("l", "").split("；")[0])
    st = _TS.STOPS[tid]; a0, aZ = st[0][0], st[-1][0]
    for nm, la, lo, big in st:
        did = _TG.STATION_DEST.get(nm)
        if not did or did not in _ALLN: continue
        j = min(range(len(rt)), key=lambda k: _km(rt[k], (la, lo)))
        f = cum[j] / L if L else 0
        go = []
        if f > 0.02: go.append([a0.replace("（乘船）", ""), int(round(tot * f / 5) * 5)])
        if f < 0.98: go.append([aZ.replace("（乘船）", ""), int(round(tot * (1 - f) / 5) * 5)])
        D = _ALLN[did].setdefault("trn", [])
        if not any(x["id"] == tid for x in D):
            D.append(dict(id=tid, n=T["n"], col=col, st=nm.replace("（乘船）", ""), go=go)); NTH += 1
print("train-at-destination", NTH)
NTR = 0
for R in BOOK["c"]:
    if R["id"] == "transport":
        for c in R["c"]:
            if c.get("route"): c["rm"] = train_map(c); NTR += 1
print("train maps", NTR)
# planner: region hubs and sub-areas
AP_TOP = {R["id"]: [R["n"], R["hub"], R["hubn"]] for R in BOOK["c"] if "hub" in R}
AP_SUB = {}
def _aps(n):
    for A in n.get("c", []):
        if A.get("kd") in ("目的地", "子地点"):
            g = centroid(A)
            if g: AP_SUB[A["id"]] = [A["n"], g, A["n"]]
            _aps(A)
for R in BOOK["c"]:
    if "hub" in R: _aps(R)

IMGDB = json.load(open("/home/claude/swiss/imgdb.json")) if os.path.exists("/home/claude/swiss/imgdb.json") else {}
# 共享资料库（/home/claude/techo）：内容与图片以资料库为准，见 techo/tools/overlay_swiss.py
sys.path.insert(0, "/home/claude/techo/tools")
import overlay_swiss as _OV
_ING = _OV.ingest()
if _ING: print("新照片已登记进资料库", _ING[:5], len(_ING))
CARDIMG = {}
import urllib.parse
def attach(n):
    e = IMGDB.get(n["id"])
    if e and _OV.has_img(n["id"]):
        n["ph"] = n["id"]
        CARDIMG[n["id"]] = dict(src="img/" + urllib.parse.quote(n["id"]) + ".webp", by=e["by"], lic=e["lic"], u=e["page"], t=e["title"])
    for c in n.get("c", []): attach(c)
attach(BOOK)
# 用户提供的 AI 插画（Microsoft Copilot 生成）
USERIMG = {"oeschinensee": "厄希嫩湖", "grindelwald": "格林德瓦", "luzerncity": "琉森", "stmoritz": "圣莫里茨", "chamonix": "勃朗峰区域"}
def _setu(n):
    if n["id"] in USERIMG and _OV.has_img(n["id"]):
        n["ph"] = n["id"]
        CARDIMG[n["id"]] = dict(src="img/" + n["id"] + ".webp", by="Microsoft Copilot 生成（作者提供）", lic="AI 插画", ai=1)
    for c in n.get("c", []): _setu(c)
_setu(BOOK)
# 大区、片区和多日路线没有自己的照片时，借用其中最有代表性的景点照片
def _rep(n):
    for c in n.get("c", []): _rep(c)
    if not n.get("c") or n.get("ph") or n["id"] in ("root",): return
    cands = []
    def walk(x, d):
        if (not x.get("c") or x.get("oldtown")) and x.get("ph") and not CARDIMG.get(x["ph"], {}).get("ai"):
            cands.append((-(2 if x.get("star") else 0) - (1 if "hot" in x.get("t", []) else 0), d, x["ph"]))
        for c in x.get("c", []): walk(c, d + 1)
    walk(n, 0)
    if cands:
        cands.sort(); n["ph"] = cands[0][2]; n["phrep"] = 1
_rep(BOOK)
TERMIMG = {"karst": "schrattenfluh", "jurafold": "creuxduvan", "permafrost": "matterhorn", "gorge": "viamala"}
for _k, _t in TERMS.items():
    if _k in CARDIMG: _t["img"] = _k
    elif TERMIMG.get(_k) in CARDIMG: _t["img"] = TERMIMG[_k]

def strip(n):
    n = dict(n)
    n.pop("g", None); n.pop("hub", None); n.pop("hubn", None)
    if "c" in n: n["c"] = [strip(c) for c in n["c"]]
    return n

# ---------- hot hikes, stay & transport ----------
import hot as HOTM
NODEMAP = {}
def _nm(n):
    NODEMAP[n["id"]] = n
    for c in n.get("c", []): _nm(c)
_nm(BOOK)
NH = 0
for aid0, routes in HOTM.HOT.items():
    aid = _DS.ALIAS.get(aid0, aid0) if aid0 not in NODEMAP else aid0
    assert aid in NODEMAP, aid
    out = []
    for r in routes:
        keys = list(dict.fromkeys(k for k, _ in r["src"]))
        src = []
        for k, rk in r["src"]:
            lab, url = HOTM.SRC[k]
            src.append([lab, url, rk])
        d = dict(n=r["n"], o=r["o"], s=r["s"], lv=r["lv"], sc=len(keys), src=src)
        if r["node"] and r["node"] in NODEMAP: d["node"] = r["node"]
        if r["note"]: d["note"] = r["note"]
        out.append(d)
    out = NODEMAP[aid].get("hot", []) + out
    out.sort(key=lambda d: -d["sc"])
    NODEMAP[aid]["hot"] = out
    for i, d in enumerate(out):
        if d.get("node"):
            NODEMAP[d["node"]]["hotref"] = [aid, i + 1, d["sc"]]
    NH += len(out)
for aid0, (st, go) in HOTM.STAY.items():
    aid = aid0 if aid0 in NODEMAP else _DS.ALIAS.get(aid0, aid0)
    assert aid in NODEMAP, aid
    if NODEMAP[aid].get("stay"): continue
    NODEMAP[aid]["stay"] = st; NODEMAP[aid]["go"] = go
for lid, (st, go) in HOTM.SKISTAY.items():
    if lid not in NODEMAP: continue
    NODEMAP[lid]["stay"] = st; NODEMAP[lid]["go"] = go
print("hot routes", NH)
_via(BOOK); print("via links", NV)
import multi as MULTIM


# ---------- topic maps ----------
LEAFMAP = {n["id"]: n for n in LEAVES}
NT = 0
_MSTG = {M["hike"]: (mk_, M["ends"]) for mk_, M in MULTIM.MULTI.items() if M.get("hike")}
for k, spec in HIKE.items():
    if k in LEAFMAP:
        e = _MSTG.get(k)
        LEAFMAP[k]["tm"] = topic_hike(spec, Proj, bg_svg, path_of, ends=e[1] if e else None, mk=e[0] if e else None); NT += 1
    else: print("WARN hike id not a leaf", k)
for k, sk in SKI_USE.items():
    if k in LEAFMAP: LEAFMAP[k]["tm"] = topic_ski(SKI[sk], Proj, bg_svg, path_of); NT += 1
print("topic maps", NT)

# ---------- original-language names in intros ----------
GL = dict(GLOSS)
def _auto(n, depth):
    if depth in (1, 2, 3) and n.get("ja") and re.search(r"[A-Za-z]", n["ja"]) and n["id"] not in ("trains", "transport", "food", "wild", "geology"):
        GL.setdefault(n["n"], n["ja"])
    for c in n.get("c", []): _auto(c, depth + 1)
for R in BOOK["c"]:
    if R["id"] in ("trains", "transport", "food", "wild", "geology"): continue
    _auto(R, 1)
for k in [k for k in GL if len(k) < 2]: GL.pop(k)
TRC = set("阿埃艾安奥巴贝比波布采策达德迪多杜厄恩法菲费弗福盖戈格古哈海汉赫胡霍基吉加卡凯坎科克库拉莱兰朗劳勒雷里利林卢鲁伦罗洛马迈曼梅蒙米莫穆纳奈尼努诺帕佩皮普齐奇切萨塞桑森沙施什舍斯索苏塔泰特提图瓦韦维温沃乌西希谢辛休雅亚扬耶伊因英尤扎泽兹茨蒂尔蓬隆措楚肯廷丁宾芬滕根登贡察默柯黎乔琴蕾娜妮丽莎尚肖翁旺姆伯吕弗朗班邦拜博柏彭珀琉佐祖苔凡梵")
for _c in "达加安西海因亚多利法普英": TRC.discard(_c)
TRN = set("尔斯特德恩格兹茨夫纳诺拉")
GRE = re.compile("|".join(re.escape(k) for k in sorted(GL, key=len, reverse=True)))
ANN = 0
def annotate(text):
    global ANN
    done = set(); out = []; i = 0; depth = 0
    for m in GRE.finditer(text):
        a, b = m.span(); k = m.group(0); orig = GL[k]
        seg = text[i:a]; depth += seg.count("（") - seg.count("）"); out.append(seg); i = a
        prev = text[a - 1] if a else ""; nxt = text[b] if b < len(text) else ""
        if (orig in done or k in done or prev in TRC or nxt in TRN or nxt in "（(" or re.match(r"\s?[A-Za-zÀ-ÿ]", text[b:b + 2])
                or orig.lower() == k.lower()):
            out.append(k); i = b; continue
        done.add(k); done.add(orig); ANN += 1
        out.append(k + (f" {orig}" if depth > 0 else f"（{orig}）")); i = b
    out.append(text[i:])
    return "".join(out)
def ann_tree(n):
    if n["id"] in ("transport", "food", "wild", "geology"): return
    if n.get("d"): n["d"] = annotate(n["d"])
    for c in n.get("c", []): ann_tree(c)
ann_tree(BOOK)
print("annotated names", ANN)

# ---- 徒步时长 / 交通子类 / 体力标签只留给徒步 ----
import dur as _DUR
_RAIL = {"stp", "halffare", "berneroberlandpass", "tellpass"}
_MTN = {"jungfraupass", "mbmultipass", "revision"}
NDUR = {}
def _tagfix(n):
    t = n.setdefault("t", [])
    if "hike" in t and n.get("kd") not in ("专题",):
        d = _DUR.dur_tag(n) or ("d4h" if not n.get("c") else None)
        if d and d not in t: t.append(d); NDUR[d] = NDUR.get(d, 0) + 1
    elif n.get("kd") not in ("分段",):
        for k in ("easy", "moderate", "hard"):
            if k in t: t.remove(k)
    if n["id"] in _RAIL and "rail" not in t: t.append("rail")
    if n["id"] in _MTN and "mtn" not in t: t.append("mtn")
    if n["id"] == "flixbus" and "bus" not in t: t.append("bus")
    for c in n.get("c", []): _tagfix(c)
_tagfix(BOOK)
print("durations", NDUR)
import passinfo as _PI
def _pass(n):
    if n["id"] in _PI.P: n["pass"] = list(_PI.P[n["id"]])
    for c in n.get("c", []): _pass(c)
_pass(BOOK)
TAGS.update(transport="交通", rail="瑞士铁路", bus="FlixBus 长途巴士", d4h="4 小时内", d1="单日", dmulti="多日")
_ovs = _OV.apply(BOOK, TERMS, PLANDATA, MULTIM.MULTI, CARDIMG, TAGS)
print("db overlay", {k: (v if not isinstance(v, list) else (len(v), v[:5])) for k, v in _ovs.items()})
book = strip(BOOK)
total = 0
def cnt(n):
    global total; total += 1
    for c in n.get("c", []): cnt(c)
cnt(book)
for k, t in TERMS.items(): t.pop("node", None)
js = "const TAGS=" + json.dumps(TAGS, ensure_ascii=False) + ";\n"
js += "const BOOK=" + json.dumps(book, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const PLANDATA=" + json.dumps(PLANDATA, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const TERMS=" + json.dumps(TERMS, ensure_ascii=False, separators=(",", ":")) + ";\n"
_RP = _ROOTP
js += "const PXY=" + json.dumps({k: [round(v, 1) for v in _RP.xy(d[0], d[1])] for k, d in PLANDATA.items()}, separators=(",", ":")) + ";\n"
js += "const AP_TOPDATA=" + json.dumps(AP_TOP, ensure_ascii=False) + ";\nconst AP_SUBDATA=" + json.dumps(AP_SUB, ensure_ascii=False) + ";\n"
for mk_, M in MULTIM.MULTI.items():
    if M.get("pts") or M.get("hike"):
        M["map"] = topic_hike((M["t"], "", M.get("pts") or HIKE[M["hike"]][2]), Proj, bg_svg, path_of, ends=M["ends"], mk=mk_, labels=[str(x[0]) for x in M["stages"]])
        M["map"].pop("list", None)
js += "const MULTI=" + json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ("where", "pts", "ends", "hike")} for k, v in MULTIM.MULTI.items()}, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const SRC={},DEEP={},IMGS={};\nconst CARDIMG=" + json.dumps(CARDIMG, ensure_ascii=False) + ";\n"
open(OUT + "/data.js", "w").write(js)
# folder tree text for PS command / checks
print("photos", len(CARDIMG), "nodes", total, "leaves", len(LEAVES), "plandata", len(PLANDATA), "terms", len(TERMS), "data.js", len(js))
