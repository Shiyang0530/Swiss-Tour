from common import S
# 城市老城区：老城作为景点，下面是子景点
NEW = {
 "baselaltstadt": S("baselaltstadt", "Basler Altstadt", [47.5585, 7.5880], "town history church", "e",
   "巴塞尔老城沿莱茵河左岸的小山坡展开，从红砂岩的大教堂到红色的市政厅，中世纪的街巷、喷泉和城门保存得很完整。夏天可以坐靠水流和钢索摆渡的莱茵河渡船过河，或者像当地人一样带着防水袋顺流漂游；冬天大教堂广场和赤足广场上是瑞士最有名的圣诞市集之一。",
   {"a": "巴塞尔火车站坐 8 或 11 路电车到 Marktplatz，约 10 分钟"}, dur=180, fl="e", n="巴塞尔老城"),
 "stpierre": S("stpierre", "Cathédrale Saint-Pierre", [46.2011, 6.1485], "church history view", "e",
   "圣皮埃尔大教堂建于 12 至 13 世纪，宗教改革后成为加尔文布道的新教教堂，室内陈设十分朴素，至今还保留着他坐过的椅子。可以爬上塔楼俯瞰日内瓦湖和老城屋顶；教堂地下的考古遗址展示了从罗马时代到中世纪的层层遗迹。",
   {"a": "日内瓦老城中心，从湖边步行上坡约 10 分钟"}, u="https://www.cathedrale-geneve.ch/", dur=60, fl="e", n="圣皮埃尔大教堂"),
}
# (片区, 老城景点 id, 子景点 id 列表, 新名称)
OT = [
 ("berncity", "bernaltstadt", ["zytglogge", "baerenpark", "bundeshaus", "einsteinhaus"], "伯尔尼老城"),
 ("basel", "baselaltstadt", ["baslermuenster", "rheinfaehre", "baslerweihnacht"], "巴塞尔老城"),
 ("zurichcity", "bahnhofstrasse", ["grossmuenster", "fraumuenster"], "苏黎世老城与班霍夫大街"),
 ("geneve", "vieilleville", ["stpierre", "reformation"], "日内瓦老城"),
 ("luzerncity", "altstadt", ["kapellbruecke", "loewendenkmal"], "琉森老城"),
]
