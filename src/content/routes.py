from common import S
# 多日长线：作为独立景点，下面按官方/常见分段生成子节点（分段）
EXTRA = {
 "zermatt": S("hauteroute", "Walker's Haute Route", [46.0207, 7.7491], "hike hard crossborder", "h",
   "瑞士高山之路（Walker's Haute Route）从法国夏蒙尼走到采尔马特，约 200 公里，累计爬升约 1.4 万米，通常分 12 到 14 天走完。路线横穿勃朗峰和马特洪峰之间的瓦莱山区，翻越十多个山口，连续几天都在 2500 米以上，被认为是阿尔卑斯最难也最壮观的长线徒步之一。沿途住山屋和山村旅馆，不少路段可以坐巴士或缆车跳过。",
   {"l": "全程约 200 公里，12 至 14 天", "h": "通常 7 月初至 9 月中"},
   tip="山屋在 7、8 月非常紧张，要提前几个月预订；部分山口要跨越积雪或碎石坡，需要有高山徒步经验。", u="https://www.myswitzerland.com/", dur=480, fl="v s", sm={"hike": [[7.0, 9.6]]}, n="瑞士高山之路 Haute Route"),
 "kandersteg": S("viaalpina", "Via Alpina (Nationale Route 1)", [46.4950, 7.6740], "hike hard", "h",
   "Via Alpina 是瑞士国家徒步路线 1 号，从列支敦士登走到日内瓦湖边的蒙特勒，约 370 公里，翻越 14 个山口，全程通常要 3 周左右。本书把它放在伯尔尼高地，因为最精彩的一段——从英格堡经格林德瓦、劳特布龙嫩到坎德施泰格——都在这一带。每段的起点和终点几乎都通火车、巴士或缆车，很适合只挑其中几段来走。",
   {"l": "全程约 370 公里，约 3 周", "h": "通常 6 月底至 9 月"},
   tip="官方路标是带「1」字的红白或绿色指示牌；第 12、13 段最难，需要不恐高。", u="https://www.schweizmobil.ch/en/hiking-in-switzerland/route-01", dur=480, fl="v s", sm={"hike": [[6.8, 9.6]]}, n="Via Alpina 全程"),
}
ROUTE_OF = {"tmb": "tmb", "hauteroute": "hauteroute", "viaalpina": "viaalpina"}  # multi key -> node id
