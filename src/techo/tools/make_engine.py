"""一次性：把京都 v69 的页面程序和瑞士的改动合并成一个通用引擎（techo/engine/）。

输入：京都 v69 的 app.js（/home/claude/work/app.js，与京都仓库 v69 完全相同）和瑞士 assemble.py 打完补丁后的结果
      （/tmp/sw_parts.pkl，由 assemble.py 生成）。
输出：
  engine/app.js             通用页面程序；书与书之间的差别全部改成读 CFG（书的配置）
  engine/planner/single.js  自动行程：单一住宿城市（京都）
  engine/planner/multi.js   自动行程：多个大区轮换住宿（瑞士）
  engine/base.css、head.html、body.html、tail.html、sw.js  页面模板
  books/{书}/engine.json    这本书的引擎配置（CFG）
引擎生成后以 engine/ 里的文件为准，以后直接改这些文件；本脚本只作记录。
"""
import json, os, pickle, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT, BOOKS, jdump

ENG = os.path.join(ROOT, "engine")
K = open("/home/claude/work/app.js", encoding="utf-8").read()
SW = pickle.load(open("/tmp/sw_parts.pkl", "rb"))
S = SW["a"]

def split(a):
    i = a.index("/* ===== 自动生成行程 ===== */"); j = a.index("function pvBar")
    return a[:i], a[i:j], a[j:]
kpre, kpl, kpost = split(K)
spre, spl, spost = split(S)

def rep(s, old, new, count=1):
    n = s.count(old)
    assert n == count, (n, count, old[:120])
    return s.replace(old, new)

def lit(text, name, at=None):
    """取出 const NAME=<字面量> 的字面量文本（括号配对，跳过字符串）。"""
    i = text.index(at) if at else text.index(f"const {name}=") + len(f"const {name}=")
    depth, j, q = 0, i, None
    while True:
        ch = text[j]
        if q:
            if ch == "\\": j += 2; continue
            if ch == q: q = None
        elif ch in "\"'`": q = ch
        elif ch in "{[(": depth += 1
        elif ch in "}])":
            depth -= 1
            if depth == 0: return text[i:j + 1]
        elif depth == 0 and ch in ";\n": return text[i:j]
        j += 1

def js_eval(expr):
    out = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({expr}))"], capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def lit_to_cfg(text, name, cfgpath):
    v = js_eval(lit(text, name))
    return text.replace(f"const {name}={lit(text, name)}", f"const {name}={cfgpath}", 1), v

# ================= 页面程序（除自动行程以外） =================
c = spre + "/*@@PLANNER@@*/" + spost
c = rep(c, 'n.disp=depth===0?[]:[...(p&&p.disp||[]),n.n];', 'n.disp=CFG.feat.disp?(depth===0?[]:[...(p&&p.disp||[]),n.n]):fs;')
c = rep(c, 'n.kind=depth===0?"总览":n.kd?n.kd:depth===1?((n.c[0]&&n.c[0].c&&n.c[0].c.length)?"大区":"专题"):(depth===2&&n.c.length?"片区":depth>=3&&n.c.length?(n.oldtown?"老城区":"多日路线"):p&&p.depth>=3&&!p.oldtown?"分段":(p&&p.depth===1&&!(p.c[0].c||[]).length?"条目":"景点"));',
        'n.kind=depth===0?"总览":n.kd?n.kd:depth===1?"地区":(uk?["","","区域","景点","看点"][depth]:["","","景点","看点"][depth]);')
c = re.sub(r'const TAG_PARENT=\{[^;]*\};', 'const TAG_PARENT=CFG.TAG_PARENT||{};', c, count=1)
c = rep(c, "if(!SEEN||!TRE)return e.replace(OGRE,'<span class=\"og\">（$1）</span>');", "if(!SEEN||!TRE)return e.replace(OGRE,OGR);")
c = rep(c, ").replace(OGRE,'<span class=\"og\">（$1）</span>')}", ").replace(OGRE,OGR)}")
c = rep(c, "const OGRE=", "const OGR=CFG.feat.og?'<span class=\"og\">（$1）</span>':'（$1）';const OGRE=")
c = rep(c, 'duck:["DuckDuckGo","https://duckduckgo.com/?q="]};', 'yahoojp:["Yahoo! JAPAN","https://search.yahoo.co.jp/search?p="],duck:["DuckDuckGo","https://duckduckgo.com/?q="]};(CFG.engines_off||[]).forEach(k=>delete ENGINES[k]);')
c = re.sub(r'"swiss-([a-z][a-z\-]*)"', r'(CFG.id+"-\1")', c)
c = rep(c, 'const SHARE_BASE="https://shiyang0530.github.io/swiss-techo/";', 'const SHARE_BASE=CFG.shareBase;')
c = rep(c, "在《瑞士旅行手帖》里打开", "在《${CFG.title}》里打开")
c = rep(c, '<div class="ps-brand">瑞士旅行手帖</div>', '<div class="ps-brand">${CFG.title}</div>')
c = rep(c, "Math.min(6,Math.max(1,apDays(AP.start,AP.end).length))", "Math.min(CFG.ap.regMax[k]||CFG.ap.regMax._,Math.max(1,apDays(AP.start,AP.end).length))")
c = rep(c, "AP_RES=apGenerate();apAuto();", "AP_RES=apGenerate();if(CFG.feat.autoDraft)apAuto();", 2)
c = rep(c, "apAuto();const id=Object.keys(PV.v).find(k=>PV.v[k].auto);if(id){PV.v[id].name=nm;delete PV.v[id].auto;pvSave()}",
        "if(CFG.feat.autoDraft){apAuto();const id=Object.keys(PV.v).find(k=>PV.v[k].auto);if(id){PV.v[id].name=nm;delete PV.v[id].auto;pvSave()}}else{PLAN=JSON.parse(JSON.stringify(AP_RES.plan));pvNew(nm,PLAN,AP_RES.meta,Object.assign({},AP_RES.opt,{baseRes:AP_RES.base}));savePlan();}")
c = rep(c, '${PLANDATA[n.id]?`<div class="mrow prow">', '${(CFG.feat.planRowData?PLANDATA[n.id]:n.depth>=2)?`<div class="mrow prow">')
c = rep(c, 'const UPPER=n=>n.c.some(c=>["大区","目的地","子地点"].includes(c.kind));', 'const UPPER=n=>CFG.upper.ids?CFG.upper.ids.includes(n.id):n.c.some(c=>CFG.upper.kinds.includes(c.kind));')
c = rep(c, 'const cntIn=(c,k)=>[c,...subtree(c)].filter(x=>(x.kind==="多日路线"||x.kind==="老城区"||!x.c.length)&&matchTag(x,k)).length;',
        'const cntIn=(c,k)=>CFG.feat.countMarkers?[c,...subtree(c)].filter(x=>(x.kind==="多日路线"||x.kind==="老城区"||!x.c.length)&&matchTag(x,k)).length:subtree(c).filter(x=>matchTag(x,k)).length+(matchTag(c,k)?1:0);')
c = rep(c, 'function badge(n,c){return 0}', 'function badge(n,c){return CFG.feat.countMarkers?0:(FILTER&&UPPER(n)?cntIn(c,FILTER):0)}')
c = re.sub(r'const SUBF=\{.*?\};\nconst SUBHIDE=new Set\(\[.*?\]\);', 'const SUBF=CFG.SUBF||{};\nconst SUBHIDE=new Set(CFG.SUBHIDE||[]);', c, count=1, flags=re.S)
c, n = re.subn(r'const HYPSO="data:image/webp;base64,[^"]*";', 'const HYPSO=typeof HYPSO_DATA!=="undefined"?HYPSO_DATA:"";', c); assert n == 1
c = rep(c, "const right=c.x+r+8+lw<596||c.x-r-8-lw<4;", "const right=CFG.feat.smartLabels?(c.x+r+8+lw<596||c.x-r-8-lw<4):c.x<440;")
c = rep(c, '${c.num||(n.kind==="多日路线"?i+1:(FILTER?cntIn(c,FILTER):nSpots(c)))}', '${CFG.feat.countMarkers?(c.num||(n.kind==="多日路线"?i+1:(FILTER?cntIn(c,FILTER):nSpots(c)))):i+1}')
c = re.sub(r'const SC_TAGS=\[[^\]]*\];', 'const SC_TAGS=CFG.SC_TAGS;', c, count=1)
c = re.sub(r'const SC_DEF=\{[^;]*\};', 'const SC_DEF=CFG.SC_DEF;', c, count=1)
c = rep(c, 'const tags=[...new Set([...(n.t||[]),...Object.keys(n.sm||{})])].filter(t=>SC_TAGS.includes(t));', 'const tags=(CFG.feat.smTags?[...new Set([...(n.t||[]),...Object.keys(n.sm||{})])]:(n.t||[])).filter(t=>SC_TAGS.includes(t));')
c = rep(c, '<span class="mono">瑞士旅游${', '<span class="mono">${CFG.folder}${')
c = rep(c, '图片文件夹：瑞士旅游\\\\${', '图片文件夹：${CFG.folder}\\\\${')
c = re.sub(r'const INFO=\{[^}]*\};', 'const INFO=CFG.INFO;', c, count=1)
c = rep(c, '&&m.depth>=2&&!m.c.length)', '&&m.depth>=2&&(!CFG.feat.relatedLeaves||!m.c.length))')
c = rep(c, 'h+=n.img?imgMap(n):(n.bg||n.c.some(c=>c.x!=null))?mapSVG(n)+lgHtml(n.lg):photo(n,false);', 'h+=n.img?imgMap(n):(!CFG.feat.photoNoMap||n.bg||n.c.some(c=>c.x!=null))?mapSVG(n)+lgHtml(n.lg):photo(n,false);')
c = rep(c, '"阿尔卑斯 · 四季"', 'CFG.eyebrow')
c = rep(c, '(n.id==="transport"?passTable():"")', '(n.id===CFG.passTableNode?passTable():"")')
c = rep(c, 'const PREFJA={},PREFZH={};', 'const PREFJA=CFG.PREFJA||{},PREFZH=CFG.PREFZH||{};')
c = rep(c, 'const kw=t.q,pj="Schweiz";', 'const kw=t.q,pj=CFG.food.pj!=null?CFG.food.pj:(PREFJA[t.pref]||"");')
c = rep(c, '<a href="https://www.tripadvisor.com/Search?q=${encodeURIComponent(kw+" Switzerland")}" target="_blank" rel="noopener">Tripadvisor ↗</a>',
        '${CFG.food.site==="tabelog"?`<a href="https://tabelog.com/${t.pref?t.pref+"/":""}rstLst/?sk=${encodeURIComponent(kw)}&SrtT=rt" target="_blank" rel="noopener">食べログ 评分排行 ↗</a>`:`<a href="https://www.tripadvisor.com/Search?q=${encodeURIComponent(kw+" "+CFG.food.en)}" target="_blank" rel="noopener">Tripadvisor ↗</a>`}')
c = rep(c, '("瑞士 "+t.n)', '((CFG.food.zh!=null?CFG.food.zh:(PREFZH[t.pref]||"")+" ")+t.n)', 2)
c = rep(c, '出发前请先在 App 里把城市切换到苏黎世、日内瓦等瑞士城市，到了瑞士会自动定位。', '${CFG.food.dpNote}')
c = rep(c, '" restaurant"', 'CFG.food.gq')
c = rep(c, 'https://de.wikipedia.org/w/index.php?search=', 'https://${CFG.wiki.lang}.wikipedia.org/w/index.php?search=')
c = rep(c, '>德文 ↗</a>', '>${CFG.wiki.label} ↗</a>')
c = rep(c, '正文里带下划线的词都收录在这里：山地交通的种类、各种交通通票、瑞士美食，以及世界遗产、冰川等概念。', '${CFG.termIntro}')
c = rep(c, 'if(p.terms||p.term){const L=TSEQ()', 'if(CFG.feat.termPaging&&(p.terms||p.term)){const L=TSEQ()', 3)
c = rep(c, '${planDates().length?planMapHtml(planDates()):""}', '${CFG.feat.planMap&&planDates().length?planMapHtml(planDates()):""}')
# 使用说明
gi, gj = c.index("function guidePages(){"), c.index("const R=`<div class=\"kicker\"><span class=\"kind\">使用说明</span>")
GUIDE = '''function guidePages(){
  const N=ORDER.filter(n=>n.depth>=2&&(!CFG.guide.leaves||!n.c.length)).length;
  const L=`<div class="gcover"><span class="eyebrow">${CFG.guide.eyebrow}</span><div class="cover-t">${CFG.title}</div><p class="cover-s">${CFG.guide.lead.replace("{N}",N)}</p>
  <div class="cover-img">${BOOK.img&&IMGS[BOOK.img]?`<img src="${IMGS[BOOK.img]}" alt="${esc(BOOK.n)}插画地图">`:mapSVG(BOOK)}</div><button class="btn pri" data-go="root">开始阅读 →</button></div>`;
  const S=CFG.guide.sections;
  '''
c = c[:gi] + GUIDE + c[gj:]
c = rep(c, 'x>=12.5&&t!=="autumn"?x-12:x', 'x>=12.5&&t!==CFG.SC_WRAP?x-12:x')
c = rep(c, '出发前请查当年雪场、步道或缆车的开放公告，以及活动日期。<b>浅色</b>表示该地点没有单独资料，按瑞士一般情况估计。', '${CFG.SC_NOTE}${(CFG.SC_NOTE_T||{})[t]||""}')
c = rep(c, '<button data-go="root">瑞士及周边</button>', '<button data-go="root">${esc(BOOK.n)}</button>', 7)
c = rep(c, 'const open=new Set(["root"]);', 'const open=new Set(CFG.tocOpen);')
c = re.sub(r'const G=\[\["时令",.*?\]\];\n', 'const G=CFG.tocGroups;\n', c, count=1, flags=re.S)
c = rep(c, '$("#backBtn").onclick=()=>$("#tbPrev").click();', 'if($("#backBtn"))$("#backBtn").onclick=()=>$("#tbPrev").click();')
c = rep(c, 'new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1&&!(n.classList&&n.classList.contains("zw")))zScan(n)}))).observe(document.documentElement,{childList:true,subtree:true});\ndocument.addEventListener("DOMContentLoaded",()=>zScan(document));setTimeout(()=>zScan(document),0);',
        'if(CFG.feat.zoom){new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1&&!(n.classList&&n.classList.contains("zw")))zScan(n)}))).observe(document.documentElement,{childList:true,subtree:true});\ndocument.addEventListener("DOMContentLoaded",()=>zScan(document));setTimeout(()=>zScan(document),0);}')
c = rep(c, 'const uk=underKyoto||n.id==="kyoto";', 'const uk=underKyoto||(CFG.kindSplit||[]).includes(n.id);')
for bad in ["swiss", "瑞士旅行手帖", "瑞士及周边", "瑞士旅游", "kyoto", "京都"]:
    hits = [c[max(0, m.start() - 40):m.start() + 30].replace("\n", " ") for m in re.finditer(bad, c)]
    if hits: print("仍含", bad, len(hits), hits[:4])

# ================= 自动行程模块 =================
def planner(t, keys):
    t = re.sub(r'"(?:kyoto|swiss)-([a-z][a-z\-]*)"', r'(CFG.id+"-\1")', t)
    cfg = {}
    for k in keys:
        t, cfg[k] = lit_to_cfg(t, k, f"CFG.ap.{k}")
    return t, cfg
single, ky_ap = planner(kpl, ["AP_BASES", "AP_TAG_G", "AP_REG_TOP", "AP_REG_SUB", "AP_PLACES"])
single = rep(single, 'const AP_SEASON=["sakura","momiji","snow","matsuri","newyear"];', 'const AP_SEASON=CFG.ap.AP_SEASON;')
ky_ap["AP_SEASON"] = ["sakura", "momiji", "snow", "matsuri", "newyear"]
multi, sw_ap = planner(spl, ["AP_BASES", "AP_TAG_G", "AP_SUBPICK", "AP_SUBLBL", "AP_ALIAS", "AP_PLREG", "AP_PLACES"])
multi = rep(multi, 'const AP_SEASON=["ski","hike","autumn","xmas","matsuri"];', 'const AP_SEASON=CFG.ap.AP_SEASON;')
sw_ap["AP_SEASON"] = ["ski", "hike", "autumn", "xmas", "matsuri"]

os.makedirs(os.path.join(ENG, "planner"), exist_ok=True)
open(os.path.join(ENG, "app.js"), "w", encoding="utf-8").write(c)
open(os.path.join(ENG, "planner", "single.js"), "w", encoding="utf-8").write(single)
open(os.path.join(ENG, "planner", "multi.js"), "w", encoding="utf-8").write(multi)

# ================= 页面模板 =================
kb = open("/home/claude/work/body.html", encoding="utf-8").read()
kh = open("/home/claude/work/head.html", encoding="utf-8").read()
KSEAL = re.search(r'<span class="seal">.*?</span>', kb, re.S).group(0)
SSEAL = re.search(r'<span class="seal">.*?</span>', SW["b"], re.S).group(0)
b = SW["b"].replace(SSEAL, "{{SEAL}}")
b = rep(b, '<button class="btn back" id="backBtn" disabled aria-label="回到刚才浏览的页面">‹ 返回</button>', "{{BACK}}")
b = b.replace("瑞士旅行手帖", "{{TITLE}}").replace("瑞士旅游", "{{FOLDER}}")
b = rep(b, "搜索景点或标签，如 少女峰、齿轨铁路、滑雪季", "{{SEARCH_PH}}")
h = SW["h"]
h = rep(h, "瑞士及周边互动旅行电子书：地图、时令与体力标签、搜索、我的标签与自动行程，可离线阅读。", "{{DESC}}")
h = rep(h, '<meta name="apple-mobile-web-app-title" content="瑞士手帖">', '<meta name="apple-mobile-web-app-title" content="{{SHORT}}">')
h = h.replace("<title>京都旅行手帖</title>", "<title>{{TITLE}}</title>")
assert "{{TITLE}}" in h, h[:400]
t = SW["t"].replace('"swiss-techo-"', '"{{ID}}-techo-"').replace('"swiss-offline"', '"{{ID}}-offline"')
assert "swiss" not in t, [m.start() for m in re.finditer("swiss", t)]
for name, txt in (("body.html", b), ("head.html", h), ("tail.html", t), ("base.css", SW["css"])):
    open(os.path.join(ENG, name), "w", encoding="utf-8").write(txt)
asm = open("/home/claude/swiss/assemble.py", encoding="utf-8").read()
swt = asm[asm.index("'''self.addEventListener(\"install\"") + 3: asm.index("''')\nman = ")]
swt = 'const CACHE="{{ID}}-techo-{{VER}}";const FILES={{FILES}};\n' + swt.replace('"swiss-tiles"', '"{{ID}}-tiles"')
assert "swiss" not in swt
open(os.path.join(ENG, "sw.js"), "w", encoding="utf-8").write(swt)

# ================= 两本书的引擎配置 =================
def evS(text, name): return js_eval(lit(text, name))
kq = kpost
KG = kq[kq.index("function guidePages(){"):kq.index("let CLEAR_ARMED")]
SG = spost[spost.index("function guidePages(){"):spost.index("let CLEAR_ARMED")]
def guide_sections(g): return js_eval(lit(g, "S"))
kyoto = dict(
    id="kyoto", title="京都旅行手帖", short="京都手帖", folder="京都旅游", eyebrow="关西 · 冬日",
    shareBase="https://shiyang0530.github.io/kyoto-techo/", engines_off=[],
    PREFJA=js_eval("{kyoto:'京都',nara:'奈良',shiga:'滋賀',osaka:'大阪',hyogo:'兵庫'}"),
    PREFZH=js_eval("{kyoto:'京都',nara:'奈良',shiga:'滋贺',osaka:'大阪',hyogo:'兵库'}"),
    upper=dict(ids=["root", "kyoto"]), kindSplit=["kyoto"],
    SC_TAGS=["sakura", "momiji", "snow", "matsuri", "newyear"],
    SC_DEF={"sakura": [[3.7, 4.2]], "momiji": [[11.4, 12.1]], "snow": [[1.1, 2.7]], "newyear": [[12.97, 13], [1, 1.15]], "matsuri": []},
    SC_WRAP="momiji",
    SC_NOTE="出发前请查当年的开花、红叶或活动公告。<b>浅色</b>表示该地点没有单独资料，按京都市区平均估计。",
    SC_NOTE_T={"snow": "京都市区一个冬天通常只积雪几次、每次一两天，色条表示可能遇到的时段。"},
    INFO={"p": "门票", "h": "时间", "a": "交通"},
    food=dict(site="tabelog", pj=None, zh=None, en="Japan", gq=" 人気店", dpNote="出发前请先在 App 里把城市切换到京都或大阪，到了日本会自动定位。"),
    wiki=dict(lang="ja", label="日文"),
    termIntro="正文里带下划线的词都收录在这里：宗派、建筑样式、佛像、祭典，以及相关的人物和历史事件。",
    tocOpen=["root", "kyoto"],
    tocGroups=js_eval(lit(kq, "G", at='[["时令"')),
    SUBF={}, SUBHIDE=[], passTableNode=None,
    guide=dict(eyebrow="关西 · 京都及周边", leaves=False, lead="一本可以翻页、搜索、按兴趣筛选的旅行电子书。六个章节，从京都城中到日本海边，{N} 个景点与看点。", sections=guide_sections(KG)),
    ap=dict(planner="single", regMax={"_": 4, "kyoto": 10}, **ky_ap),
    feat=dict(disp=False, og=False, countMarkers=False, smartLabels=False, smTags=False, planRowData=False, relatedLeaves=False,
              photoNoMap=False, termPaging=False, planMap=False, autoDraft=False, zoom=False, back=False),
    page=dict(desc="京都及周边互动旅行电子书：插画地图、标签筛选、搜索与我的标签，可离线阅读。", search_ph="搜索景点或标签，如 清水寺、佛寺、跨年", seal=KSEAL,
              manifest_bg="#E3E5DC"),
)
swiss = dict(
    id="swiss", title="瑞士旅行手帖", short="瑞士手帖", folder="瑞士旅游", eyebrow="阿尔卑斯 · 四季",
    shareBase="https://shiyang0530.github.io/swiss-techo/", engines_off=["yahoojp"],
    PREFJA={}, PREFZH={},
    upper=dict(kinds=["大区", "目的地", "子地点"]),
    SC_TAGS=["ski", "hike", "autumn", "xmas", "matsuri"],
    SC_DEF={"ski": [[12.4, 13], [1, 4.4]], "hike": [[6.0, 10.0]], "autumn": [[9.6, 10.9]], "xmas": [[11.75, 12.8]], "matsuri": []},
    SC_WRAP="autumn",
    SC_NOTE="出发前请查当年雪场、步道或缆车的开放公告，以及活动日期。<b>浅色</b>表示该地点没有单独资料，按瑞士一般情况估计。", SC_NOTE_T={},
    INFO={"e": "海拔", "h": "开放 / 运营", "p": "门票", "s": "通票", "l": "路线", "a": "交通"},
    food=dict(site="tripadvisor", pj="Schweiz", zh="瑞士 ", en="Switzerland", gq=" restaurant", dpNote="出发前请先在 App 里把城市切换到苏黎世、日内瓦等瑞士城市，到了瑞士会自动定位。"),
    wiki=dict(lang="de", label="德文"),
    termIntro="正文里带下划线的词都收录在这里：山地交通的种类、各种交通通票、瑞士美食，以及世界遗产、冰川等概念。",
    tocOpen=["root"],
    tocGroups=js_eval(lit(spost, "G", at='[["时令"')),
    SUBF={"transport": [["", ["mtn", "train", "boat", "rail", "bus"]]], "hike": [["难度", ["easy", "moderate", "hard"]], ["时长", ["d4h", "d1", "dmulti"]]]},
    SUBHIDE=["mtn", "cog", "funi", "cable", "train", "boat", "rail", "bus", "easy", "moderate", "hard", "d4h", "d1", "dmulti"],
    passTableNode="transport",
    guide=dict(eyebrow="阿尔卑斯 · 瑞士及周边", leaves=True, lead="一本可以翻页、搜索、按兴趣筛选的旅行电子书。八个大区加勃朗峰与列支敦士登，三个专题，{N} 个景点与条目；滑雪季、徒步路线、赏秋一目了然。", sections=guide_sections(SG)),
    ap=dict(planner="multi", regMax={"_": 6}, **sw_ap),
    feat=dict(disp=True, og=True, countMarkers=True, smartLabels=True, smTags=True, planRowData=True, relatedLeaves=True,
              photoNoMap=True, termPaging=True, planMap=True, autoDraft=True, zoom=True, back=True),
    page=dict(desc="瑞士及周边互动旅行电子书：地图、时令与体力标签、搜索、我的标签与自动行程，可离线阅读。", search_ph="搜索景点或标签，如 少女峰、齿轨铁路、滑雪季", seal=SSEAL,
              manifest_bg="#E3E5DC"),
)
# 原书里的标签父子关系
kyoto["TAG_PARENT"] = js_eval(lit(K, "TAG_PARENT"))
swiss["TAG_PARENT"] = js_eval(lit(S, "TAG_PARENT"))
for b_, cfg in (("kyoto", kyoto), ("swiss", swiss)):
    jdump(os.path.join(BOOKS, b_, "engine.json"), cfg)
print("engine", len(c), "single", len(single), "multi", len(multi))
