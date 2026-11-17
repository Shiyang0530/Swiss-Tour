# 瑞士通票 (STP) / 半价卡 (HF) —— free / 50 / 25 / part / no
# 依据：Swiss Travel System 官方 FAQ（Rigi、Stoos、Stanserhorn 免费，多数山地交通 5 折）、各线路官网与 STS 优惠表，核对于 2026 年 11 月
P = {
 # 观景列车与普通铁路
 "glacierexpress": ("free", "50", "座位预订费另付"), "berninaexpress": ("free", "50", "座位预订费另付；通票免费到瑞士边境"),
 "goldenpass": ("free", "50", "座位预订费另付"), "gotthardpanorama": ("free", "50", "列车与游船都含；预订费另付"),
 "voralpen": ("free", "50", ""), "luzerninterlaken": ("free", "50", "座位预订可选"),
 "montblancexpress": ("part", "part", "只适用于瑞士境内段（马蒂尼—法国边境）"), "centovalli": ("part", "part", "只适用于瑞士境内段"),
 "brusio": ("free", "50", "雷蒂亚铁路伯尔尼纳线"), "landwasser": ("free", "50", "雷蒂亚铁路阿尔布拉线"), "ruinaulta": ("free", "50", "雷蒂亚铁路"),
 "uetliberg": ("free", "50", "S10 苏黎世—于特利山"),
 # 湖船
 "lakeboat": ("free", "50", ""), "seeboat": ("free", "50", ""), "ruetli": ("free", "50", "琉森湖游船"), "lagolugano": ("free", "50", ""),
 "ouchy": ("free", "50", "日内瓦湖 CGN 游船"), "walenseelake": ("free", "50", ""), "bodensee": ("free", "50", "瑞士公司的游船"),
 "rheinfaehre": ("no", "no", "私营小渡船，现场付费"),
 # 通票免费的山
 "rigibahn": ("free", "50", ""), "cabrio": ("free", "50", "冬季停运"), "stoosbahn": ("free", "50", ""),
 # 部分优惠
 "jungfraubahn": ("part", "part", "通票免费到格林德瓦或文根，再往上约 25% 折扣"), "eigerexpress": ("part", "50", "去少女峰站的联票约 25% 折扣"),
 "schilthorn": ("part", "50", "通票免费到米伦，往上 5 折"),
 # 5 折
 "harder": ("50", "50", ""), "schynige": ("50", "50", ""), "first": ("50", "50", ""), "niesen": ("50", "50", ""), "rothorn": ("50", "50", ""),
 "gornergrat": ("50", "50", ""), "glacierparadise": ("50", "50", ""), "sunnegga": ("50", "50", ""), "allalin": ("50", "50", ""),
 "eggishorn": ("50", "50", ""), "gemmi": ("50", "50", ""), "pilatusbahn": ("50", "50", ""), "rotair": ("50", "50", ""),
 "corvatsch": ("50", "50", ""), "muottasmuragl": ("50", "50", ""), "diavolezza": ("50", "50", ""), "parsenn": ("50", "50", ""),
 "weisshorn": ("50", "50", ""), "sansalvatore": ("50", "50", ""), "generoso": ("50", "50", ""), "cardada": ("50", "50", ""),
 "tamaro": ("50", "50", ""), "rochersdenaye": ("50", "50", ""), "glacier3000": ("50", "50", ""), "saentis": ("50", "50", ""),
 "aescher": ("50", "50", "埃本阿尔卑缆车"), "chaeserrugg": ("50", "50", ""),
 # 法国 / 意大利
 "aiguilledumidi": ("no", "no", "可用勃朗峰多日通票"), "montenvers": ("no", "no", "可用勃朗峰多日通票"), "brevent": ("no", "no", "可用勃朗峰多日通票"),
 "skyway": ("no", "no", "意大利段，单独购票"),
 "flixbus": ("no", "no", "不属于瑞士公共交通网"),
}
