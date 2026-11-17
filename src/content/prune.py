# 2026-11-17 删减：70 处景点（并入或删除），热门/精选保留 50 处，小镇与老城区标签名单
DEL = set("""beatus maennlichen kleinescheidegg wab wengenski muerrenski birg allmendhubel oberhofen giessbach gletscherschlucht adelbodenski gstaadski
rothornzermatt kapellenweg riederalp bettmeralp maerjelensee haengebruecke aletschski gianadda panoramic tmb_tram fenis courmayeurski trient
musegg weggis rigikulm rigisled dragonride fraekmuentegg cliffwalk glaciercave stoosski bundesbrief telldenkmal
piznair jakobshorn schatzalp baerenland arosaski alpgruem lagobianco
gimmelwald montebre foxtown swissminiatur brissago castagne
horlogefleurie lavauxexpress vinorama narcisses fourchette desalpe villarsski
zuerichsee lindenhof appenzellerkaese alpabfahrt seerenbach flumserberg hofkellerei kunstmuseum malbun
gurten emmentalerkaese rathausbasel doubs""".split())

MERGE = {
 "royalwalk": "起点曼利兴（Männlichen）有缆车从格林德瓦和文根上来；终点小沙伊德格（Kleine Scheidegg）是去少女峰的换车站，正对艾格北壁。",
 "jungfraubahn": "从劳特布龙嫩或格林德瓦要先坐文根阿尔卑铁路（WAB）上到小沙伊德格，再换乘少女峰铁路。",
 "schilthorn": "缆车中途站比格（Birg）有一段悬在峭壁外的悬崖步道，可以顺路下车走一走。",
 "muerrenvillage": "从米伦沿小路往下走约半小时，就是悬崖边更安静的吉梅尔瓦尔德（Gimmelwald）小村，缆车也停这一站。村子上方的阿门德胡贝尔（Allmendhubel）有缆索铁路直达，夏天有平缓的花之步道，适合带小孩。",
 "thuncastle": "图恩湖北岸还有带湖畔花园的奥贝霍芬城堡（Schloss Oberhofen），坐船可以顺路一游。",
 "grindelski": "少女峰滑雪区包括格林德瓦–菲斯特、小沙伊德格–曼利兴（格林德瓦–文根）和米伦–雪朗峰三块雪场，可以买一张少女峰滑雪通票通用。",
 "sunnegga": "从苏内加再坐缆车可以上到罗特洪峰（Rothorn），从另一个角度看马特洪峰。",
 "aletschglacier": "冰川南侧的高原上有里德阿尔卑（Riederalp）和贝特默阿尔卑（Bettmeralp）两个无车村，是住宿和出发的基地；夏天可以从贝拉尔普走吊桥过马萨峡谷到里德阿尔卑，或者走到冰川边的马耶伦湖。",
 "aiguilledumidi": "夏季在南针峰还可以换乘勃朗峰全景吊厢（Panoramic Mont-Blanc），横越冰川到意大利一侧的赫尔布罗纳峰。",
 "tmb": "想轻松体验一小段，可以从圣热尔韦坐勃朗峰电车（Tramway du Mont-Blanc）上山，再接上环勃朗峰的路线。",
 "aosta": "奥斯塔谷沿途还有费尼斯城堡（Castello di Fénis）等多座中世纪城堡。",
 "rigibahn": "山顶瑞吉库尔姆（Rigi Kulm）是看日出的经典地点，住一晚山顶酒店最方便；也可以从湖边的韦吉斯（Weggis）坐缆车上山，冬天还有雪橇道。",
 "pilatusbahn": "从克林斯（Kriens）一侧可以坐吊厢和大型缆车「龙骑」（Dragon Ride）上下山，和齿轨铁路组成「金色环游」；半山腰的 Fräkmüntegg 有夏季滑道和绳索公园。",
 "rotair": "峰顶站还有铁力士悬崖吊桥（Cliff Walk）和冰川洞，都包含在登山票里。",
 "ruetli": "附近的施维茨有收藏 1291 年联邦宪章的博物馆，阿尔特多夫的广场上立着威廉·退尔纪念碑。",
 "altstadt": "老城北面保存着一段穆塞格城墙（Museggmauer），夏天可以登上几座塔楼俯瞰全城。",
 "stmoritzski": "主雪场科尔维利亚（Corviglia）一直连到皮兹内尔峰（Piz Nair），峰顶视野开阔。",
 "davosski": "其中的雅各布斯峰（Jakobshorn）雪场以单板公园著称。",
 "diavolezza": "沿伯尔尼纳山口再往南，还有伯尔尼纳白湖（Lago Bianco）和阿尔卑格吕姆（Alp Grüm）观景站，伯尔尼纳快车都会经过。",
 "weisshorn": "阿罗萨雪场与伦策海德相连，统称阿罗萨–伦策海德滑雪区。",
 "lavauxwalk": "走累了可以坐观光小火车（Lavaux Express）代步，也可以在村里的酒窖或 Lavaux Vinorama 品鉴当地葡萄酒。",
 "vieilleville": "湖边的英国公园里有用鲜花拼成的花钟。",
 "gruyerestown": "格吕耶尔地区秋天有牧牛下山节（Désalpe），牛群戴着花冠和大铃铛走下山来。",
 "bahnhofstrasse": "老城西侧的林登霍夫（Lindenhof）小山是俯瞰利马特河和老城的好地方；夏天还可以在码头坐苏黎世湖游船。",
 "appenzelltown": "这里也是阿彭策尔奶酪的产地，附近有展示奶酪制作的工坊；秋天有热闹的牧牛下山节。",
 "vaduztown": "城里还有列支敦士登美术馆，城外的王室酒庄（Hofkellerei）可以品尝本地葡萄酒。",
 "emmentalbruecke": "附近的埃门塔尔奶酪厂展示带孔大奶酪的制作过程。",
 "baslermuenster": "大教堂附近的市场广场上有红色的巴塞尔市政厅，是老城最显眼的建筑。",
}

HOT50 = set("""jungfraubahn sphinx first bachalpsee royalwalk staubbach schilthorn oeschinensee lakeboat
matterhorn gornergrat zermattvillage sunnegga riffelsee aletschglacier aiguilledumidi leukerbad tmb
kapellbruecke altstadt seeboat rigibahn pilatusbahn rotair stoosbahn
stmoritzvillage diavolezza landwasser caumasee muottasmuragl
pontedeisalti castelli riforma ascona
jetdeau vieilleville lavauxwalk chillon gruyerestown
bahnhofstrasse rheinfall stiftsbibliothek aescher steinamrhein lindthome
bernaltstadt baslermuenster creuxduvan
glacierexpress berninaexpress""".split())

TOWN = set("""bernaltstadt baselaltstadt bahnhofstrasse vieilleville altstadt riforma höheweg
zermattvillage saasfeevillage wengen muerrenvillage gruyerestown murten steinamrhein appenzelltown morcote ascona piazzagrande spiez stmoritzvillage""".split())
