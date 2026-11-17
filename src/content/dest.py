# 新结构：大区 → 目的地（城市或地区）→ 子地点 → 景点
# spots 中 "@片区id" 表示该片区（重组前）剩下的全部景点；base 表示沿用原片区节点（保留介绍、住宿交通、热门路线）
def D(id, n=None, ja=None, d=None, base=None, spots=(), subs=()):
    return dict(id=id, n=n, ja=ja, d=d, base=base, spots=list(spots), subs=list(subs))

RAND_D = "这里收录本大区里不属于任何一个目的地、但值得专程或顺路一去的地点，可以在两个目的地之间移动时安排。"

DEST = {
 "berner": [
  D("jungfrauregion", "少女峰与因特拉肯地区", "Jungfrau Region · Interlaken",
    "少女峰地区是伯尔尼高地的核心：北边的因特拉肯夹在图恩湖和布里恩茨湖之间，是交通枢纽和住宿大本营；往南进山，格林德瓦和劳特布龙嫩两条山谷分别通往艾格、僧侣、少女峰三座名峰脚下，山谷之间由小沙伊德格的山口和少女峰铁路相连。这里有齿轨铁路、缆车和大量平缓的全景步道，适合住上三到五天慢慢玩。",
    subs=[D("interlaken", base="interlaken", spots=["@interlaken"]),
          D("grindelwald", base="grindelwald", spots=["@grindelwald"]),
          D("jungfrau", base="jungfrau", spots=["@jungfrau"]),
          D("lauterbrunnen", n="劳特布龙嫩谷", ja="Lauterbrunnental · Wengen · Mürren", base="lauterbrunnen", spots=["@lauterbrunnen", "@muerren"])]),
  D("thunbrienz", base="thunbrienz", spots=["@thunbrienz"]),
  D("kandersteg", base="kandersteg", spots=["@kandersteg"]),
  D("gstaad", base="gstaad", spots=["@gstaad"]),
 ],
 "wallis": [
  D("zermatt", n="马特洪峰地区", ja="Zermatt · Matterhorn", base="zermatt", spots=["@zermatt"]),
  D("saasfee", base="saasfee", spots=["@saasfee"]),
  D("aletsch", base="aletsch", spots=["@aletsch"]),
  D("sion", n="罗讷河谷", ja="Rhonetal · Sion · Leukerbad", base="sion", spots=["valere", "wine", "leukerbad", "gemmi"]),
  D("wallisski", "瓦莱滑雪胜地", "Verbier · Crans-Montana",
    "韦尔比耶和克兰-蒙塔纳是瓦莱州罗讷河谷两侧的两大滑雪胜地：韦尔比耶属于「四山谷」大雪场，以陡坡和野雪闻名；克兰-蒙塔纳建在朝南的阳光高台上，坡度平缓，正对瓦莱阿尔卑斯群峰。",
    spots=["verbier", "cransmontana"]),
  D("chamonix", n="勃朗峰地区", ja="Massif du Mont-Blanc · Monte Bianco", base="chamonix", spots=["tmb"],
    subs=[D("chamonixsub", "夏蒙尼", "Chamonix-Mont-Blanc",
            "夏蒙尼位于法国，是勃朗峰北麓的登山之都，1924 年举办了第一届冬季奥运会。山谷两侧分别是勃朗峰群和红针峰群，几条大型缆车和齿轨铁路把游客送到冰川与雪峰之间。这里使用欧元，瑞士通票基本不适用。",
            spots=["chamonixvillage", "aiguilledumidi", "montenvers", "lacblanc", "grandbalcon", "brevent", "valleeblanche", "chamonixski"]),
          D("courmayeur", "库马约尔与奥斯塔", "Courmayeur · Valle d'Aosta",
            "库马约尔在意大利一侧的勃朗峰南麓，通过勃朗峰隧道和天空之路缆车与夏蒙尼相连。往东顺着奥斯塔谷而下，是罗马古城奥斯塔和一连串中世纪城堡。这里使用欧元，说意大利语和法语。",
            spots=["courmayeurvillage", "skyway", "valferretit", "aosta"]),
          D("champexsub", "尚佩与瑞士费雷谷", "Champex-Lac · Val Ferret",
            "勃朗峰的瑞士一侧，是环勃朗峰徒步经过的安静山村：尚佩湖边的小村和长长的费雷谷，从马蒂尼坐火车和邮政巴士就能到。",
            spots=["champex", "valferretch"])]),
  D("wallisrand", "瓦莱周边与沿途", "Wallis · unterwegs", RAND_D, spots=["grandstbernard", "lavey", "saillon"]),
 ],
 "luzern": [
  D("luzerncity", n="琉森市区", base="luzerncity", spots=["@luzerncity"]),
  D("luzernsee", "琉森湖区", "Vierwaldstättersee",
    "琉森湖（四森林州湖）形状曲折，周围环绕着瑞吉山、皮拉图斯山、施坦塞峰和斯托斯等一座座观景山，湖船、齿轨铁路和缆车把它们连成一张网，坐船上山、坐车下山是这里最经典的玩法。南岸的吕特利草地和施维茨、阿尔特多夫一带是瑞士建国传说的发生地。",
    spots=["seeboat"],
    subs=[D("rigi", base="rigi", spots=["@rigi"]), D("pilatus", base="pilatus", spots=["@pilatus"]),
          D("stanserhorn", base="stanserhorn", spots=["@stanserhorn"]),
          D("stoos", n="斯托斯与吕特利", base="stoos", spots=["@stoos"])]),
  D("titlis", base="titlis", spots=["@titlis"]),
  D("luzernrand", "琉森周边与沿途", "Zentralschweiz · unterwegs", RAND_D, spots=["schrattenfluh"]),
 ],
 "graubuenden": [
  D("engadin", "恩加丁地区", "Engadin",
    "恩加丁是因河上游一条海拔 1600 到 1800 米的高山长谷，上恩加丁湖泊相连、阳光充足，圣莫里茨和蓬特雷西纳是中心；往南翻过伯尔尼纳山口就是意大利语的波斯基亚沃谷；往下游的下恩加丁则是刮画装饰的古村、温泉和瑞士国家公园。冬天滑雪、夏天徒步，秋天落叶松一片金黄。",
    subs=[D("stmoritz", base="stmoritz", spots=["@stmoritz"]), D("bernina", base="bernina", spots=["@bernina"]),
          D("unterengadin", base="unterengadin", spots=["@unterengadin"])]),
  D("davos", base="davos", spots=["@davos"]),
  D("chur", n="库尔与阿罗萨", base="chur", spots=["@chur"]),
  D("flimslaax", base="flimslaax", spots=["caumasee", "ruinaulta", "laaxski"]),
  D("albula", n="阿尔布拉线", base="albula", spots=["landwasser", "berguen"]),
  D("grrand", "格劳宾登周边与沿途", "Graubünden · unterwegs", RAND_D, spots=["vals", "viamala"]),
 ],
 "ticino": [
  D("luganolake", "卢加诺湖区", "Lago di Lugano",
    "卢加诺湖弯弯曲曲地伸进群山之间，北岸是提契诺最大的城市卢加诺，湖边点缀着莫尔科特、甘德里亚这样的石头小村，南边的门德里西奥一带有吉内罗索山和葡萄酒乡。夏天很有地中海的味道。",
    subs=[D("lugano", n="卢加诺", base="lugano", spots=["lagolugano", "riforma", "sansalvatore"]),
          D("morcotesub", "莫尔科特与甘德里亚", "Morcote · Gandria",
            "卢加诺湖边最美的两座石头小村：一南一北，都能坐湖船到达，村里只有台阶和小巷。", spots=["morcote", "gandria"]),
          D("mendrisio", base="mendrisio", spots=["@mendrisio"])]),
  D("maggiore", "马焦雷湖区", "Lago Maggiore",
    "马焦雷湖北端属于瑞士，洛迦诺和阿斯科纳是湖边的两座度假小城，气候温暖、棕榈成行；往北的韦尔扎斯卡谷和马贾谷是清澈的溪流、石头村庄和瀑布。",
    subs=[D("locarno", n="洛迦诺与阿斯科纳", base="locarno", spots=["@locarno"]),
          D("verzasca", base="verzasca", spots=["@verzasca"])]),
  D("bellinzona", n="贝林佐纳", base="bellinzona", spots=["castelli", "tamaro"]),
  D("tirand", "提契诺周边与沿途", "Ticino · in viaggio", RAND_D, spots=["gottardo"]),
 ],
 "leman": [
  D("geneve", n="日内瓦市区", base="geneve", spots=["@geneve"]),
  D("lausanne", n="洛桑市区", base="lausanne", spots=["@lausanne"]),
  D("montreux", n="蒙特勒与拉沃", ja="Montreux · Vevey · Lavaux", base="montreux", spots=["lavauxwalk", "@montreux"]),
  D("gruyeres", base="gruyeres", spots=["@gruyeres"]),
  D("lemanrand", "日内瓦湖区周边与沿途", "Région lémanique · en route", RAND_D, spots=["glacier3000"]),
 ],
 "zuerich": [
  D("zurichcity", n="苏黎世市区", base="zurichcity", spots=["bahnhofstrasse", "uetliberg", "landesmuseum", "lindthome", "corbusierzh"]),
  D("schaffhausen", base="schaffhausen", spots=["@schaffhausen"]),
  D("appenzell", n="阿彭策尔地区", ja="Appenzellerland · St. Gallen", base="appenzell", spots=["@appenzell", "stiftsbibliothek"]),
  D("walensee", base="walensee", spots=["@walensee"]),
  D("liechtenstein", base="liechtenstein", spots=["@liechtenstein"]),
  D("zrand", "东北部周边与沿途", "Ostschweiz · unterwegs", RAND_D, spots=["fortyseven", "bodensee"]),
 ],
 "bernbasel": [
  D("berncity", n="伯尔尼市区", base="berncity", spots=["@berncity"]),
  D("basel", n="巴塞尔市区", base="basel", spots=["baselaltstadt", "beyeler", "kunstmuseumbasel", "fasnacht"]),
  D("jura", base="jura", spots=["@jura"]),
  D("bbrand", "西北部周边与沿途", "Nordwestschweiz · unterwegs", RAND_D, spots=["emmentalbruecke", "vitra"]),
 ],
}
LONG = ["viaalpina", "hauteroute"]   # 移到「长线徒步」专题
ALIAS = {"muerren": "lauterbrunnen", "martigny": "wallisrand", "lavaux": "montreux", "stgallen": "appenzell", "emmental": "bbrand",
         "diablerets": "lemanrand", "mendrisio": "mendrisio"}
# 景点类型（地图图例）：town 小镇 / old 老城区 / out 户外 / cul 人文
TOWN_T = set("""höheweg wengen muerrenvillage zermattvillage saasfeevillage gstaadvillage chamonixvillage courmayeurvillage stmoritzvillage
poschiavo guarda davostown heididorf morcote gandria ascona piazzagrande gruyerestown steinamrhein appenzelltown murten spiez brienz
iseltwald stursanne vaduztown""".split())
OLD_T = set("bernaltstadt baselaltstadt bahnhofstrasse vieilleville altstadt riforma churaltstadt aosta chauxdefonds".split())
