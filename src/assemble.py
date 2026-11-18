import re, os, json, base64, hashlib, io, subprocess
W = "/home/claude/work"; OUT = "/home/claude/swiss/out"
app = open(W + "/app.js", encoding="utf-8").read()
css = open(W + "/css_nofont.css", encoding="utf-8").read()
head = open(W + "/head.html", encoding="utf-8").read()
body = open(W + "/body.html", encoding="utf-8").read()
tail = open(W + "/tail.html", encoding="utf-8").read()
data = open(OUT + "/data.js", encoding="utf-8").read()

def rep(s, old, new, count=1, name=""):
    n = s.count(old)
    assert n == count, f"{name or old[:60]!r}: expected {count}, found {n}"
    return s.replace(old, new)

# ---------------- app.js ----------------
PASSJS = r"""function viaBlock(n){const V=(n.via||[]).filter(v=>NODES[v[0]]);if(!V.length)return "";return `<div class="sec">途经这里的徒步路线</div><div class="vias">${V.map(([id,l])=>`<button class="mylink" data-go="${id}">${esc(NODES[id].n)}${l?` <small>${esc(l)}</small>`:""} →</button>`).join("")}</div>`}
function rmBlock(n){const L=n.rm;return `<div class="tmhead"><span class="eyebrow">线路图</span></div><div class="lmwrap"><svg class="map lmap" viewBox="0 0 600 440" role="img" aria-label="${esc(n.n)}线路图"><rect width="600" height="440" style="fill:var(--land)"/>${L.svg.replace("__HY__",HYPSO)}</svg>${lgHtml(L.lg)}<p class="tmnote">彩色线为列车大致走向，标出了起终点和沿途主要车站（位置为近似值）。下方总图中，这条线路会被加粗显示。</p></div>`}
function lmBlock(n){const L=n.lm;return `<div class="tmhead"><span class="eyebrow">${n.ty==="old"?"老城区地图":"小镇地图"}</span></div><div class="lmwrap"><svg class="map lmap" viewBox="0 0 600 440" role="img" aria-label="${esc(n.n)}地图"><rect width="600" height="440" style="fill:var(--land)"/>${L.svg.replace("__HY__",HYPSO)}</svg>${lgHtml(L.lg)}${L.near&&L.near.length?`<div class="lmnear">${L.near.filter(x=>NODES[x[0]]).map(([id])=>`<button data-go="${id}">${esc(NODES[id].n)}</button>`).join("")}</div>`:""}<p class="tmnote">地图上标出附近收录的景点、车站与缆车。联网时默认叠加瑞士国家地图（swisstopo），可显示街道、步道和等高线；点地图右上角的 ◩ 可在示意图、地形图、街道图（OpenStreetMap）之间切换。看过的区域会缓存，离线时也能显示。</p></div>`}
const WILDK=t=>t&&(t.k==="野生动物"||t.k==="高山植物"||t.k==="地质与地貌");
function wildInfo(t){let h="";const pct=x=>((x-1)/12*100).toFixed(2);
if(t.sm&&t.sm.length)h+=`<div class="scal"><div class="sec">季节</div><div class="scgrid"><div class="scrow"><span class="scl">较易见到</span><div class="sctrack">${t.sm.map(([a,b,l])=>`<i class="sc-food" style="left:${pct(a)}%;width:${Math.max(1.2,(Math.min(b,13)-a)/12*100).toFixed(2)}%"${l?` title="${esc(l)}"`:""}></i>`).join("")}</div></div><div class="scrow scm"><span class="scl"></span><div class="sctrack">${[1,2,3,4,5,6,7,8,9,10,11,12].map(m=>`<span style="left:${((m-0.5)/12*100).toFixed(2)}%">${m}</span>`).join("")}</div></div></div><ul class="evl">${t.sm.map(([a,b,l])=>`<li><b>${esc(l||"")}</b><span>${b-a>=11.5?"全年":mlabel(a)+"–"+mlabel(Math.min(b,12.99)-0.01)}</span></li>`).join("")}</ul></div>`;
const w=(t.w||[]).filter(x=>NODES[x]);if(w.length)h+=`<div class="sec">${t.k==="地质与地貌"?"在这些地方能看到":"较常见的地区"}</div><div class="cloud">${w.map(x=>`<button class="tag" data-go="${x}">${esc(NODES[x].n)}</button>`).join("")}</div>${t.k==="地质与地貌"?"":`<p class="scnote">野生动植物出没和花期每年不同，这里只列出较常见的地区，不保证一定能见到。</p>`}`;
if(t.q&&t.k!=="地质与地貌")h+=`<p class="foodlinks"><a href="https://www.inaturalist.org/observations?place_id=6939&q=${encodeURIComponent(t.q.split(" ").slice(0,2).join(" "))}" target="_blank" rel="noopener">iNaturalist 瑞士观察记录 ↗</a><a href="https://commons.wikimedia.org/w/index.php?search=${encodeURIComponent(t.q)}" target="_blank" rel="noopener">更多照片（维基共享资源） ↗</a></p>`;
return h}
function localWild(n){if(!n.depth||!n.parent||["trains","transport","food","wild","geology"].includes(n.folders&&NODES[n.id]&&(()=>{let x=n;while(x.depth>1)x=x.parent;return x.id})()))return "";const up=new Set();let x=n;while(x){up.add(x.id);x=x.parent}const down=new Set(n.depth>=2?subtree(n).map(c=>c.id):[]);
const all=Object.entries(TERMS_).filter(([,t])=>WILDK(t)&&(t.w||[]).some(i=>up.has(i)||down.has(i)));if(!all.length)return "";const gs=all.filter(([,t])=>t.k==="地质与地貌"),fs=all.filter(([,t])=>t.k!=="地质与地貌");const geoH=gs.length?`<div class="sec">在这里能看到的地貌</div><div class="foods">${gs.map(([id,t])=>{const c=t.img&&CIMG[t.img];return `<button class="food" data-route="term-${id}">${c?`<img src="${c.src}" alt="" loading="lazy">`:`<span class="noimg">岩</span>`}<b>${esc(t.n)}</b><small>地质与地貌</small></button>`}).join("")}</div>`:"";if(!fs.length)return geoH;const mo=new Date().getMonth()+1;
return geoH+`<div class="sec">可能见到的动植物</div><div class="foods">${fs.map(([id,t])=>{const c=t.img&&CIMG[t.img];const on=(t.sm||[]).some(([a,b])=>mo>=Math.floor(a)&&mo<=Math.floor(Math.min(b,12.99)));return `<button class="food" data-route="term-${id}">${c?`<img src="${c.src}" alt="" loading="lazy">`:`<span class="noimg">${t.k==="野生动物"?"兽":"花"}</span>`}<b>${esc(t.n)}</b><small>${esc(t.k)}${on?" · 当季":""}</small></button>`}).join("")}</div>`}
function apAuto(){if(!AP_RES||AP_RES.err)return;const cl=x=>JSON.parse(JSON.stringify(x||{}));PLAN=cl(AP_RES.plan);let id=Object.keys(PV.v).find(k=>PV.v[k].auto);const opt=Object.assign({},AP_RES.opt,{baseRes:AP_RES.base});if(id){Object.assign(PV.v[id],{ts:Date.now(),plan:cl(PLAN),meta:AP_RES.meta||{},opt});PV.cur=id;pvSave()}else{id=pvNew("自动行程（草稿）",PLAN,AP_RES.meta,opt);PV.v[id].auto=1;pvSave()}savePlan()}
function nSpots(c){return c.c&&c.c.length?(c.kind==="多日路线"?1:(c.kind==="老城区"?1:0)+c.c.reduce((a,x)=>a+nSpots(x),0)):1}
const DAYC=["#C4432B","#2F6DB5","#3F7A34","#8E5BC8","#D0841B","#16878A","#B5487A","#6B6B2E"];
function planMapHtml(ds){let lines="",mk="";const all=[];ds.forEach((d,i)=>{const col=DAYC[i%DAYC.length];const xy=(PLAN[d]||[]).filter(id=>PXY[id]&&NODES[id]).map(id=>[id,PXY[id][0],PXY[id][1]]);if(xy.length>1)lines+=`<path d="M${xy.map(p=>p[1]+" "+p[2]).join(" L")}" fill="none" stroke="${col}" stroke-width="2.2" stroke-dasharray="5 4" stroke-linecap="round" opacity=".85"/>`;xy.forEach((p,j)=>{all.push([p[1],p[2]]);mk+=`<g class="pmk" data-go="${p[0]}" role="link" tabindex="0" aria-label="第${i+1}天 ${esc(NODES[p[0]].n)}"><title>第${i+1}天 · ${j+1}. ${esc(NODES[p[0]].n)}</title><circle cx="${p[1]}" cy="${p[2]}" r="7.5" fill="${col}" stroke="#fff" stroke-width="1.8"/><text x="${p[1]}" y="${p[2]}" text-anchor="middle" dominant-baseline="central" font-size="9" font-weight="700" fill="#fff">${i+1}</text></g>`})});if(!all.length)return "";
let x0=Math.min(...all.map(p=>p[0])),x1=Math.max(...all.map(p=>p[0])),y0=Math.min(...all.map(p=>p[1])),y1=Math.max(...all.map(p=>p[1]));let w=Math.max(x1-x0+80,110),h=Math.max(y1-y0+70,w*440/600);w=Math.max(w,h*600/440);h=w*440/600;const fx=Math.max(0,Math.min(600-w,(x0+x1)/2-w/2)),fy=Math.max(0,Math.min(440-h,(y0+y1)/2-h/2));
return `<div class="sec">行程地图</div><svg class="map planall" viewBox="0 0 600 440" data-fit="${fx.toFixed(1)} ${fy.toFixed(1)} ${Math.min(600,w).toFixed(1)}" role="img" aria-label="行程地图"><rect width="600" height="440" style="fill:var(--land)"/>${(BOOK.bg||"").replace("__HY__",HYPSO)}${lines}${mk}</svg><div class="pmlg">${ds.map((d,i)=>`<button data-planmap="${d}" title="只看这一天"><i style="background:${DAYC[i%DAYC.length]}"></i>第${i+1}天 · ${PLAN[d].length} 处</button>`).join("")}</div><p class="scnote">圆点颜色代表日期，数字是第几天，虚线按当天顺序连接；点圆点进入景点页，点下方的日期只看那一天。</p>`}
function syncBack(){const bb=document.getElementById("backBtn");if(!bb)return;const h=[...HIST].reverse().find(r=>r!==cur);bb.disabled=!h;let nm="";try{const q=h&&parseRoute(h);nm=q&&q.node?q.node.n:(h==="plan"?"旅行计划":h==="mytags"?"我的标签":"上一个页面")}catch(e){nm="上一个页面"}bb.title=h?"回到："+nm:"还没有浏览过其他页面"}
const LVN={e:"轻松",m:"适中",h:"进阶"};
function hotBlock(n){const H=n.hot;if(!H||!H.length)return "";return `<div class="sec">热门徒步路线 · 多来源统计</div><p class="scnote">按推荐这条路线的榜单和指南数量排序；来源包括 Lonely Planet、徒步网站、旅游局推荐等，统计于 2026 年 11 月。</p><ol class="hot">${H.map((r,i)=>`<li><div class="hh"><b class="hr">${i+1}</b><span class="hn">${esc(r.n)}</span><span class="tag ${({e:"easy",m:"moderate",h:"hard"})[r.lv]}">${LVN[r.lv]}</span><span class="hsc" title="推荐来源数">${"●".repeat(Math.min(r.sc,8))} ${r.sc} 个来源</span></div><div class="ho">${esc(r.o)}</div><div class="hst">${esc(r.s)}</div>${r.note?`<div class="hwarn">⚠ ${esc(r.note)}</div>`:""}<details class="hsrc"><summary>推荐依据</summary>${r.src.map(([l,u,k])=>`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(l)}</a> <i>${esc(k)}</i>`).join("<br>")}</details>${r.node&&NODES[r.node]?`<button class="mylink" data-go="${r.node}">查看「${esc(NODES[r.node].n)}」页面${NODES[r.node].tm?"与路线图":""} →</button>`:""}</li>`).join("")}</ol>`}
function stayBlock(n){let S=n.stay?n:null;let sub="";if(!S&&n.parent&&n.parent.stay&&!n.c.length&&(n.mk==="hike"||n.t.includes("hike")||n.hotref)){S=n.parent;sub=`（${esc(n.parent.n)}一带）`}if(!S)return "";return `<div class="sec">住宿与交通${sub}</div><dl class="stay"><dt>推荐住宿区域</dt><dd>${lk(S.stay)}</dd><dt>交通</dt><dd>${lk(S.go)}</dd></dl><p class="scnote">班次、运营季节和价格以官方时刻表与官网为准。</p>`}
function multiBlock(n){const ks=n.multi||[];if(!ks.length)return "";const leaf=!n.c.length||n.kind==="多日路线";return `<div class="sec">多日徒步 · 推荐分段</div>${ks.map(k=>{const M=MULTI[k];if(!M)return "";const tot=M.stages.reduce((s,x)=>s+(+x[2]||0),0);return `<details class="multi"${leaf?" open":""}><summary><b>${esc(M.t)}</b><span>${M.stages.length} 段 · 合计约 ${Math.round(tot)} km</span></summary><p class="msum">${lk(M.sum)}</p>${M.alerts.map(x=>`<div class="hwarn">⚠ ${esc(x)}</div>`).join("")}${M.map?`<div class="mmap" data-mk="${k}"><svg class="map tmap" viewBox="0 0 600 440" role="img" aria-label="${esc(M.t)}分段地图"><rect width="600" height="440" style="fill:var(--land)"/>${M.map.svg.replace("__HY__",HYPSO)}</svg>${M.map.prof?`<svg class="tmprof" viewBox="0 0 600 100" role="img" aria-label="海拔剖面">${M.map.prof}</svg>`:""}</div>`:""}<p class="scnote">点表格中的任一段，地图和海拔剖面会高亮这一段；再点一次取消。</p><div class="mtab"><table><thead><tr><th>段</th><th>起点 → 终点</th><th>km</th><th>↑ / ↓ m</th><th>最高点</th><th>缩短与交通</th></tr></thead><tbody>${M.stages.map((s,i)=>`<tr class="stgrow" data-mk="${k}" data-s="${i+1}"><td>${s[0]}</td><td>${esc(s[1])}${s[5]?`<small> · ${esc(s[5])}</small>`:""}</td><td>${s[2]}</td><td>${s[3]} / ${s[4]}</td><td>${esc(s[6]||"")}</td><td>${esc(s[7]||"")}</td></tr>`).join("")}</tbody></table></div><div class="mplans"><b>推荐分段方案</b><ol>${M.plans.map(([h,p])=>`<li><b>${esc(h)}</b>：${lk(p)}</li>`).join("")}</ol></div><p class="scnote">数据来源：${M.src.map(([l,u])=>`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(l)}</a>`).join(" · ")}。山屋和住宿旺季需提前预订，山口积雪和封路情况以当地发布为准。</p></details>`}).join("")}`}
function setStage(mk,s){const on=!document.querySelector(`.stgrow[data-mk="${mk}"][data-s="${s}"].on`);document.querySelectorAll(`[data-mk="${mk}"] .stg,[data-mk="${mk}"] .pstg,[data-mk="${mk}"] .pstl,.stgrow[data-mk="${mk}"]`).forEach(e=>e.classList.toggle("on",on&&e.dataset.s===String(s)));if(on){const m=[...document.querySelectorAll(`[data-mk="${mk}"] svg.map`)].find(e=>e.getBoundingClientRect().width>0);if(m){const r=m.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)m.scrollIntoView({behavior:"smooth",block:"center"})}}}
document.addEventListener("click",e=>{const r=e.target.closest(".stgrow");if(r){setStage(r.dataset.mk,r.dataset.s);return}const p=e.target.closest(".stg,.pstg");if(p){const w=p.closest("[data-mk]");if(w)setStage(w.dataset.mk,p.dataset.s)}});
function hotRef(n){const h=n.hotref;if(!h||!NODES[h[0]])return "";return `<div class="hotref">🔥 热门度：在「${esc(NODES[h[0]].n)}」热门徒步路线中排第 ${h[1]}，有 ${h[2]} 个榜单或指南推荐。<button class="mylink" data-go="${h[0]}">查看排行 →</button></div>`}
function zoomify(svg){if(svg.__z||svg.closest(".cover-img"))return;svg.__z=1;const b=svg.viewBox.baseVal,W0=b.width,H0=b.height;let v={x:0,y:0,w:W0,h:H0};const w=document.createElement("div");w.className="zw";svg.parentNode.insertBefore(w,svg);w.appendChild(svg);const c=document.createElement("div");c.className="zc";c.innerHTML='<button type="button" data-z="in" aria-label="放大" title="放大">+</button><button type="button" data-z="out" aria-label="缩小" title="缩小">−</button><button type="button" data-z="reset" aria-label="还原" title="还原">⤢</button>'+(svg.querySelector("g.geoP")?'<button type="button" data-z="bm" aria-label="切换底图" title="切换底图：示意图 / 地形图 / 街道图" class="bmb">◩</button>':'');w.appendChild(c);
const set=n=>{n.w=Math.max(W0/8,Math.min(W0,n.w));n.h=n.w*H0/W0;n.x=Math.max(0,Math.min(W0-n.w,n.x));n.y=Math.max(0,Math.min(H0-n.h,n.y));v=n;svg.setAttribute("viewBox",`${n.x.toFixed(2)} ${n.y.toFixed(2)} ${n.w.toFixed(2)} ${n.h.toFixed(2)}`);const z=n.w<W0-.5;svg.classList.toggle("zoomed",z);w.classList.toggle("zoomed",z);cs(n.w/W0);svg.__v=n;tilesSoon(svg)};
let ZL=null;const ctr=e=>{if(e.tagName==="circle")return[+e.getAttribute("cx"),+e.getAttribute("cy")];try{const b=e.getBBox();return[b.x+b.width/2,b.y+b.height/2]}catch(_){return null}};
const MKS=".tnm,.pkm,.psm,.stn";const GRP="g.mk,g.tst,g.twp,g.lfn,g.ill,g.pmk,g.lmk";
const cs=k=>{if(!ZL){ZL=[];svg.querySelectorAll(GRP).forEach(g=>{const s=g.querySelector("circle,rect,path");const a=g.dataset.cx?[+g.dataset.cx,+g.dataset.cy]:s&&ctr(s);if(a)ZL.push([g,a])});svg.querySelectorAll(MKS).forEach(e=>{if(e.closest(GRP))return;const a=ctr(e);if(a)ZL.push([e,a])});svg.querySelectorAll("text").forEach(t=>{if(t.closest(GRP+",.sbar"))return;const p=t.previousElementSibling;let a=p&&p.matches(MKS)?ctr(p):null;if(!a){const x=parseFloat(t.getAttribute("x")),y=parseFloat(t.getAttribute("y"));if(isNaN(x)||isNaN(y))return;a=[x,y]}ZL.push([t,a])})}
ZL.forEach(([e,[x,y]])=>{if(k>.999)e.removeAttribute("data-zt"),e.style.transform="";else e.style.transform=`translate(${x}px,${y}px) scale(${k.toFixed(4)}) translate(${-x}px,${-y}px)`})};
const pt=(cx,cy)=>{const r=svg.getBoundingClientRect();return[v.x+(cx-r.left)/r.width*v.w,v.y+(cy-r.top)/r.height*v.h]};
const zoomAt=(f,px,py)=>{const nw=Math.max(W0/8,Math.min(W0,v.w/f)),k=nw/v.w;set({x:px-(px-v.x)*k,y:py-(py-v.y)*k,w:nw})};
c.addEventListener("click",e=>{const t=e.target.closest("button");if(!t)return;e.stopPropagation();const m=t.dataset.z;if(m==="bm"){bmCycle(svg);return}if(m==="reset")set({x:0,y:0,w:W0});else zoomAt(m==="in"?1.6:1/1.6,v.x+v.w/2,v.y+v.h/2)});
svg.addEventListener("dblclick",e=>{e.preventDefault();const[p,q]=pt(e.clientX,e.clientY);zoomAt(e.shiftKey?1/2:2,p,q)});
svg.addEventListener("wheel",e=>{if(!e.ctrlKey&&!e.metaKey&&!svg.classList.contains("zoomed"))return;e.preventDefault();const[p,q]=pt(e.clientX,e.clientY);zoomAt(Math.exp(-e.deltaY*(e.deltaMode?.05:.002)),p,q)},{passive:false});
const P=new Map;let moved=0,start=null,pinch=null;
svg.addEventListener("pointerdown",e=>{P.set(e.pointerId,{x:e.clientX,y:e.clientY});if(P.size===1){moved=0;start={x:e.clientX,y:e.clientY,v:{...v}}}else if(P.size===2){const[a,d]=[...P.values()];pinch={d:Math.hypot(a.x-d.x,a.y-d.y),v:{...v},m:pt((a.x+d.x)/2,(a.y+d.y)/2)};moved=1}});
svg.addEventListener("pointermove",e=>{if(!P.has(e.pointerId))return;P.set(e.pointerId,{x:e.clientX,y:e.clientY});const r=svg.getBoundingClientRect();if(P.size>=2&&pinch){const[a,d]=[...P.values()];const dd=Math.hypot(a.x-d.x,a.y-d.y);if(!pinch.d)return;const f=dd/pinch.d,nw=Math.max(W0/8,Math.min(W0,pinch.v.w/f)),mx=(a.x+d.x)/2,my=(a.y+d.y)/2;set({x:pinch.m[0]-(mx-r.left)/r.width*nw,y:pinch.m[1]-(my-r.top)/r.height*nw*H0/W0,w:nw});e.preventDefault()}else if(P.size===1&&start&&start.v.w<W0-.5){const dx=e.clientX-start.x,dy=e.clientY-start.y;if(!moved&&Math.hypot(dx,dy)<5)return;if(!moved){moved=1;try{svg.setPointerCapture(e.pointerId)}catch(_){}}set({x:start.v.x-dx/r.width*start.v.w,y:start.v.y-dy/r.height*start.v.h,w:start.v.w});e.preventDefault()}});
const up=e=>{P.delete(e.pointerId);if(P.size<2)pinch=null;if(P.size===1){const[a]=[...P.values()];start={x:a.x,y:a.y,v:{...v}}}if(!P.size)start=null};
["pointerup","pointercancel","pointerleave"].forEach(t=>svg.addEventListener(t,up));
svg.addEventListener("click",e=>{if(moved){e.stopPropagation();e.preventDefault();moved=0}},true);if(svg.dataset.fit){const f=svg.dataset.fit.split(" ").map(Number);set({x:f[0],y:f[1],w:f[2]})}else{svg.__v=v;tilesSoon(svg)}}
const BMS={topo:{u:"https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",mz:18,a:"底图 © swisstopo",n:"地形图"},osm:{u:"https://tile.openstreetmap.org/{z}/{x}/{y}.png",mz:19,a:"底图 © OpenStreetMap 贡献者",n:"街道图"}};
let BMPREF=null;try{BMPREF=localStorage.getItem("bm")}catch(_){}
function bmOf(svg){if(svg.__bm!==undefined)return svg.__bm;const p=svg.querySelector("g.geoP");if(!p)return "off";if(BMPREF==="off")return "off";const[cx,cy,cl,k]=p.dataset.p.split(" ").map(Number);return (BMPREF&&BMS[BMPREF]&&k*cl>900)?BMPREF:(k*cl>900?"topo":"off")}
function bmCycle(svg){const o=["off","topo","osm"];const cur=bmOf(svg);const nx=o[(o.indexOf(cur)+1)%3];svg.__bm=nx;BMPREF=nx;try{localStorage.setItem("bm",nx)}catch(_){}
  const w=svg.closest(".zw");if(w){let t=w.querySelector(".bmtip");if(!t){t=document.createElement("div");t.className="bmtip";w.appendChild(t)}t.textContent=nx==="off"?"底图：示意图":"底图："+BMS[nx].n+(navigator.onLine===false?"（离线时只显示浏览过的区域）":"");t.classList.add("on");clearTimeout(t.__h);t.__h=setTimeout(()=>t.classList.remove("on"),1800)}
  drawTiles(svg)}
function tilesSoon(svg){clearTimeout(svg.__th);svg.__th=setTimeout(()=>drawTiles(svg),120)}
function drawTiles(svg){const p=svg.querySelector("g.geoP");if(!p)return;let L=svg.querySelector("g.tiles");const mode=bmOf(svg);svg.classList.toggle("bmon",mode!=="off");
  if(mode==="off"){if(L)L.remove();const a=svg.querySelector(".bmattr");if(a)a.remove();return}
  const S=BMS[mode];if(!L||L.dataset.m!==mode){if(L)L.remove();L=document.createElementNS("http://www.w3.org/2000/svg","g");L.setAttribute("class","tiles");L.dataset.m=mode;p.parentNode.insertBefore(L,p)}
  const[cx,cy,cl,k]=p.dataset.p.split(" ").map(Number);const vb=svg.viewBox.baseVal;const v={x:vb.x,y:vb.y,w:vb.width,h:vb.height};
  const lon=X=>cx+(X-300)/(cl*k),lat=Y=>cy-(Y-220)/k;const X=lo=>300+(lo-cx)*cl*k,Y=la=>220-(la-cy)*k;
  const r=svg.getBoundingClientRect();const pxw=Math.max(300,r.width||600)*(window.devicePixelRatio||1);
  const ppd=pxw/v.w*cl*k;let z=Math.round(Math.log2(ppd*360/256));z=Math.max(3,Math.min(S.mz,z));
  const lo0=lon(v.x),lo1=lon(v.x+v.w),la1=lat(v.y),la0=lat(v.y+v.h);
  const tx=(lo,z)=>(lo+180)/360*2**z,ty=(la,z)=>{const t=la*Math.PI/180;return(1-Math.log(Math.tan(t)+1/Math.cos(t))/Math.PI)/2*2**z};
  let xa,xb,ya,yb;for(;;){xa=Math.floor(tx(lo0,z));xb=Math.floor(tx(lo1,z));ya=Math.floor(ty(la1,z));yb=Math.floor(ty(la0,z));if((xb-xa+1)*(yb-ya+1)<=60||z<=3)break;z--}
  const ilo=(x,z)=>x/2**z*360-180,ila=(y,z)=>{const n=Math.PI*(1-2*y/2**z);return Math.atan(Math.sinh(n))*180/Math.PI};
  const want=new Set;const have=new Map;L.querySelectorAll("image").forEach(i=>have.set(i.dataset.t,i));
  for(let x=xa;x<=xb;x++)for(let y=ya;y<=yb;y++){const key=z+"/"+x+"/"+y;want.add(key);if(have.has(key))continue;
    const i=document.createElementNS("http://www.w3.org/2000/svg","image");const x0=X(ilo(x,z)),x1=X(ilo(x+1,z)),y0=Y(ila(y,z)),y1=Y(ila(y+1,z));
    i.setAttribute("x",x0.toFixed(2));i.setAttribute("y",y0.toFixed(2));i.setAttribute("width",(x1-x0+.4).toFixed(2));i.setAttribute("height",(y1-y0+.4).toFixed(2));i.setAttribute("preserveAspectRatio","none");i.dataset.t=key;i.dataset.z=z;
    i.addEventListener("error",()=>i.remove());i.setAttribute("href",S.u.replace("{z}",z).replace("{x}",x).replace("{y}",y));L.appendChild(i)}
  // keep lower-zoom tiles underneath until new ones load; drop tiles of other zooms that are far off
  have.forEach((i,key)=>{if(!want.has(key)&&+i.dataset.z!==z){if(+i.dataset.z>z||L.childNodes.length>160)i.remove()}else if(!want.has(key)&&L.childNodes.length>160)i.remove()});
  [...L.querySelectorAll("image")].sort((a,b)=>a.dataset.z-b.dataset.z).forEach(i=>L.appendChild(i));
  let a=svg.querySelector(".bmattr");if(!a){a=document.createElementNS("http://www.w3.org/2000/svg","text");a.setAttribute("class","bmattr");svg.appendChild(a)}a.setAttribute("x",(v.x+6).toFixed(1));a.setAttribute("y",(v.y+14*v.w/600).toFixed(1));a.setAttribute("font-size",(10*v.w/600).toFixed(2));a.textContent=S.a}
const zScan=r=>{(r.matches&&r.matches("svg.map")?[r]:[]).concat([...(r.querySelectorAll?r.querySelectorAll("svg.map"):[])]).forEach(zoomify)};
new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1&&!(n.classList&&n.classList.contains("zw")))zScan(n)}))).observe(document.documentElement,{childList:true,subtree:true});
document.addEventListener("DOMContentLoaded",()=>zScan(document));setTimeout(()=>zScan(document),0);
function passBlock(t){if(!t||(!t.buy&&!t.notes))return "";return `${t.buy&&t.buy.length?`<div class="sec">购票</div><div class="buy">${t.buy.map(([l,u])=>`<a class="buybtn" href="${esc(u)}" target="_blank" rel="noopener">${esc(l)} ↗</a>`).join("")}</div>`:""}${t.notes&&t.notes.length?`<div class="sec">注意事项</div><ol class="notes">${t.notes.map(x=>`<li>${lk(x)}</li>`).join("")}</ol><p class="scnote">票价与规则核对于 2026 年 11 月，每年可能调整，购买前请以官网为准。</p>`:""}`}
"""
MAPJS = r"""function mkShape(c,r){const k=c.mk,x=c.x,y=c.y;if(k==="ski")return `<rect class="sh ski" x="${(x-r*.84).toFixed(1)}" y="${(y-r*.84).toFixed(1)}" width="${(r*1.68).toFixed(1)}" height="${(r*1.68).toFixed(1)}" rx="2.5" transform="rotate(45 ${x} ${y})"/>`;if(k==="mtn")return `<rect class="sh mtn" x="${(x-r*.9).toFixed(1)}" y="${(y-r*.9).toFixed(1)}" width="${(r*1.8).toFixed(1)}" height="${(r*1.8).toFixed(1)}" rx="${(r*.42).toFixed(1)}"/>`;if(k==="vtown")return `<path class="sh town" d="M${(x-r*.95).toFixed(1)} ${(y+r*.85).toFixed(1)}V${(y-r*.15).toFixed(1)}L${x} ${(y-r*1.05).toFixed(1)}L${(x+r*.95).toFixed(1)} ${(y-r*.15).toFixed(1)}V${(y+r*.85).toFixed(1)}Z" stroke-linejoin="round"/>`;if(k==="vold")return `<path class="sh old" d="M${(x-r*.9).toFixed(1)} ${(y+r*.9).toFixed(1)}V${(y-r*.9).toFixed(1)}h${(r*.45).toFixed(1)}v${(r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(-r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(-r*.35).toFixed(1)}V${(y+r*.9).toFixed(1)}Z" stroke-linejoin="round"/>`;if(k==="vout")return `<circle class="sh out" cx="${x}" cy="${y}" r="${r}"/>`;if(k==="hike")return `<path class="sh hike" d="M${x} ${(y-r*1.25).toFixed(1)}L${(x+r*1.2).toFixed(1)} ${(y+r*.9).toFixed(1)}H${(x-r*1.2).toFixed(1)}Z" stroke-linejoin="round"/>`;return `<circle cx="${x}" cy="${y}" r="${r}"/>`}
const LGI={vout:["户外景点（山、湖、峡谷等）",c=>`<circle cx="13" cy="9" r="6.5" fill="#5f8a3a"/>`],vtown:["小镇",c=>`<path d="M7 15V8L13 3L19 8V15Z" fill="#b0763a"/>`],vold:["老城区",c=>`<path d="M7 15V3h3v2h3V3h3v2h3V15Z" fill="#8e3b46"/>`],vcul:["人文景点（博物馆、教堂、城堡、温泉等）",c=>`<circle cx="13" cy="9" r="6.5" fill="#C4432B"/>`],regions:["不同底色：本书划分的八个大区（范围示意）",c=>`<rect x="1" y="3" width="11" height="12" fill="#E07A5F" fill-opacity=".3" stroke="#E07A5F"/><rect x="14" y="3" width="11" height="12" fill="#3D85C6" fill-opacity=".3" stroke="#3D85C6"/>`],ill:["热门景点插画（位置示意）",c=>`<path d="M5 17 L13 3 L21 17Z" fill="#C9B79A" stroke="#4B566F" stroke-width="1" stroke-linejoin="round"/><path d="M10.3 7.8 L13 3 L15.7 7.8 L13 9.4Z" fill="#fff" stroke="#4B566F" stroke-width=".8"/>`],spot:["景点",c=>`<circle cx="13" cy="9" r="6.5" fill="#C4432B"/>`],area:["目的地 / 子地点（点击进入，数字为景点数）",c=>`<circle cx="13" cy="9" r="6.5" fill="#C4432B"/>`],
hike:["徒步路线",c=>`<path d="M13 1.5L20.5 15H5.5Z" fill="#3f7a34" stroke-linejoin="round"/>`],ski:["滑雪场",c=>`<rect x="8" y="4" width="10" height="10" rx="1.5" fill="#2f6db5" transform="rotate(45 13 9)"/>`],
mtn:["山地交通（缆车 / 齿轨 / 观光列车）",c=>`<rect x="6.5" y="2.5" width="13" height="13" rx="4" fill="#6d5a99"/>`],trainroute:["观景列车线路（每条线一种颜色）",c=>`<path d="M2 6H24" stroke="#C4432B" stroke-width="3"/><path d="M2 12H24" stroke="#2E6FB7" stroke-width="3"/>`],stn:["起终点 / 沿途主要车站",c=>`<circle cx="7" cy="9" r="5" fill="#C4432B" stroke="#fff" stroke-width="1.5"/><circle cx="19" cy="9" r="3.5" fill="#fff" stroke="#C4432B" stroke-width="1.8"/>`],
peak:["山峰与海拔（米）",c=>`<path d="M13 3L19 14H7Z" fill="#7b6a55"/>`],town:["城镇与海拔（米）",c=>`<circle cx="13" cy="9" r="3.6" fill="#fff" stroke="#3b2a1a" stroke-width="1.6"/>`],
rail:["铁路",c=>`<path d="M1 9H25" stroke="#3b2a1a" stroke-width="2.6" opacity=".55"/><path d="M1 9H25" stroke="#fff" stroke-width="1.1" stroke-dasharray="4 4"/>`],
water:["湖泊 / 河流",c=>`<rect x="2" y="3" width="13" height="12" rx="3" fill="#a9c8d8"/><path d="M15 12C19 12 20 6 25 6" stroke="#a9c8d8" stroke-width="2.4" fill="none"/>`],
border:["国界",c=>`<path d="M1 9H25" stroke="#8b7b68" stroke-width="1.2" stroke-dasharray="5 4"/>`],
route_hike:["徒步路线（白色箭头为推荐方向）",c=>`<path d="M1 9H25" stroke="#3f7a34" stroke-width="3.6" stroke-linecap="round"/><path d="M11 6L14 9L11 12" stroke="#fff" stroke-width="1.5" fill="none"/>`],
route_ski:["滑雪 / 雪橇路线",c=>`<path d="M1 9H25" stroke="#2f6db5" stroke-width="3.6" stroke-linecap="round"/><path d="M11 6L14 9L11 12" stroke="#fff" stroke-width="1.5" fill="none"/>`],
start:["起点 / 终点",c=>`<circle cx="13" cy="9" r="7.5" fill="${c}" stroke="#fff" stroke-width="1.5"/>`],via:["途经点（编号见下表）",c=>`<circle cx="13" cy="9" r="6" fill="#fff" stroke="${c}" stroke-width="2"/>`],
skiarea:["滑雪区域大致范围",c=>`<rect x="2" y="2" width="22" height="14" rx="4" fill="#2f6db5" fill-opacity=".12" stroke="#2f6db5" stroke-dasharray="4 3"/>`],
lift_g:["吊厢 / 空中缆车",c=>`<path d="M3 9H23" stroke="#3b2a1a" stroke-width="2"/><rect x="1" y="6.5" width="5" height="5" fill="#fff" stroke="#3b2a1a" stroke-width="1.4"/><rect x="20" y="6.5" width="5" height="5" fill="#fff" stroke="#3b2a1a" stroke-width="1.4"/>`],
lift_c:["吊椅",c=>`<path d="M1 9H25" stroke="#3b2a1a" stroke-width="2" stroke-dasharray="6 3"/>`],
lift_f:["缆索铁路 / 登山铁路",c=>`<path d="M1 9H25" stroke="#3b2a1a" stroke-width="4"/><path d="M1 9H25" stroke="#fff" stroke-width="1.5" stroke-dasharray="4 4"/>`],
trail:["徒步路线走向（示意）",c=>`<path d="M1 9H25" stroke="#3f7a34" stroke-width="2.4" stroke-dasharray="5 3"/>`],trail_ski:["滑雪 / 雪橇路线（示意）",c=>`<path d="M1 9H25" stroke="#2f6db5" stroke-width="2.4" stroke-dasharray="5 3"/>`],
lift:["缆车 / 登山铁路（示意）",c=>`<path d="M3 9H23" stroke="#3b2a1a" stroke-width="1.5"/><rect x="1" y="6.5" width="5" height="5" fill="#fff" stroke="#3b2a1a" stroke-width="1.2"/><rect x="20" y="6.5" width="5" height="5" fill="#fff" stroke="#3b2a1a" stroke-width="1.2"/>`],
pass:["山口与海拔（米）",c=>`<path d="M8 3Q12 9 8 15M18 3Q14 9 18 15" stroke="#3b2a1a" stroke-width="1.6" fill="none"/>`],
hypso:["海拔分层（示意）：1000 / 2000 / 3000 米以上",c=>`<rect x="0" y="4" width="8" height="10" fill="rgb(192,172,116)" opacity=".6"/><rect x="9" y="4" width="8" height="10" fill="rgb(150,120,78)" opacity=".75"/><rect x="18" y="4" width="8" height="10" fill="rgb(236,238,242)" stroke="#bbb" stroke-width=".6"/>`],
station:["主要站点与海拔",c=>`<circle cx="13" cy="9" r="4.6" fill="#2f6db5" stroke="#fff" stroke-width="1.6"/>`]};
function lgHtml(ks,col){return ks&&ks.length?`<div class="maplg" aria-label="图例"><b>图例</b>${ks.map(k=>LGI[k]?`<span><svg viewBox="0 0 26 18" width="26" height="18" aria-hidden="true">${LGI[k][1](col||"#3f7a34")}</svg>${LGI[k][0]}</span>`:"").join("")}</div>`:""}
function tmBlock(n){const T=n.tm,col=T.k==="ski"?"#2f6db5":"#3f7a34",area=!!T.st;
  const lab=area?"雪场示意图":T.k==="ski"?"滑雪 / 雪橇路线示意图":"徒步路线示意图";
  const list=area?`<div class="tml2"><div><span class="eyebrow">缆车与登山铁路</span><ol>${T.list.map(([i,nm,ty])=>`<li><b>${i}</b>${esc(nm)} <small>${ty}</small></li>`).join("")}</ol></div><div><span class="eyebrow">主要站点</span><ul>${T.st.map(([z,o,e])=>`<li>${esc(z)} <i>${esc(o)}</i> <small>${e} m</small></li>`).join("")}</ul></div></div>`
    :`<ol class="tml">${T.list.map(([i,z,o,e,r])=>{const se=r==="s"||r==="e"||r==="loop";return `<li><b class="${se?"se":""}">${r==="s"?"起":r==="e"?"终":r==="loop"?"起终":i}</b><span>${esc(z)}${o?` <i>${esc(o)}</i>`:""}</span><small>${e} m</small></li>`}).join("")}</ol>`;
  return `<div class="tm ${T.k}${area?" area":""}"${T.mk?` data-mk="${T.mk}"`:""}><div class="tmh"><span class="eyebrow">${lab}</span><b>${esc(T.t)}</b><small>${esc(T.s)}</small></div>
  <svg class="map tmap" viewBox="0 0 600 440" role="img" aria-label="${esc(T.t)}"><rect width="600" height="440" style="fill:var(--land)"/>${T.svg.replace("__HY__",HYPSO)}<g transform="translate(570 34)"><path d="M0 -14 L5.5 5 L0 1 L-5.5 5Z" style="fill:var(--ink)"/><text y="18" text-anchor="middle" style="fill:var(--ink);font:600 10px var(--f-mono)">N</text></g></svg>${T.prof?`<svg class="tmprof" viewBox="0 0 600 100" role="img" aria-label="海拔剖面">${T.prof}</svg>`:""}${lgHtml(T.lg,col)}${list}
  <p class="tmnote">示意图：线路走向、站点位置与海拔为近似值，${area?"实际雪道与开放情况请以雪场官方雪道图为准":"出发前请以官方地图、现场路标和当天天气为准"}。</p></div>`}
"""
a = app
a = rep(a, 'n.kind=depth===0?"总览":depth===1?"地区":(uk?["","","区域","景点","看点"][depth]:["","","景点","看点"][depth]);',
  'n.kind=depth===0?"总览":depth===1?((n.c[0]&&n.c[0].c&&n.c[0].c.length)?"大区":"专题"):(depth===2&&n.c.length?"片区":depth>=3&&n.c.length?(n.oldtown?"老城区":"多日路线"):p&&p.depth>=3&&!p.oldtown?"分段":(p&&p.depth===1&&!(p.c[0].c||[]).length?"条目":"景点"));')
a = rep(a, 'indexedDB.open("kyoto-book",1)', 'indexedDB.open("swiss-book",1)')
a = a.replace('"kyoto-', '"swiss-')
a = rep(a, 'const TAG_PARENT={sengoku:"history",meiji:"history",myth:"history",literature:"history",unesco:"history",genji:"literature"};',
  'const TAG_PARENT={cog:"mtn",funi:"mtn",cable:"mtn",mtn:"transport",train:"transport",boat:"transport",rail:"transport",bus:"transport",myth:"history",literature:"history",cheese:"food",chocolate:"food"};')
a = rep(a, 'yahoojp:["Yahoo! JAPAN","https://search.yahoo.co.jp/search?p="],', '')
a = re.sub(r'const PREFJA=\{kyoto:.*?\};\n', 'const PREFJA={},PREFZH={};\n', a, count=1, flags=re.S)
# planner
a = re.sub(r'const AP_BASES=\{auto:\{n:"帮我推荐"\},kyotost:.*?\};\n', lambda m: 'const AP_BASES={auto:{n:"帮我推荐"},zurich:{n:"苏黎世",g:[47.3779,8.5402]},luzern:{n:"琉森",g:[47.0502,8.3093]},interlaken:{n:"因特拉肯",g:[46.6905,7.8690]},grindelwald:{n:"格林德瓦",g:[46.6243,8.0414]},zermatt:{n:"采尔马特",g:[46.0242,7.7486]},bern:{n:"伯尔尼",g:[46.9490,7.4392]},basel:{n:"巴塞尔",g:[47.5476,7.5897]},montreux:{n:"蒙特勒",g:[46.4350,6.9100]},lausanne:{n:"洛桑",g:[46.5167,6.6290]},geneve:{n:"日内瓦",g:[46.2102,6.1424]},lugano:{n:"卢加诺",g:[46.0050,8.9470]},stmoritz:{n:"圣莫里茨",g:[46.4980,9.8460]},chur:{n:"库尔",g:[46.8530,9.5290]},chamonix:{n:"夏蒙尼（法国）",g:[45.9237,6.8694]}};\n', a, count=1, flags=re.S)
assert '"夏蒙尼（法国）"' in a
a = re.sub(r'const AP_TAG_G=\[\["时令".*?\]\];\n', lambda m: 'const AP_TAG_G=[["时令","ski autumn xmas matsuri"],["徒步","hike d4h d1 dmulti"],["适合人群","elderly couple family"],["交通","transport mtn train boat rail"],["自然风景","alps rhine view glacier lake waterfall nature spa"],["历史文化","history unesco arch castle church museum art"],["吃喝玩乐","hot food cheese chocolate town shopping"],["实用","free crossborder"]];\n', a, count=1, flags=re.S)
a = rep(a, 'const AP_SEASON=["sakura","momiji","snow","matsuri","newyear"];', 'const AP_SEASON=["ski","hike","autumn","xmas","matsuri"];')
a = re.sub(r'const AP_REG_TOP=\{kyoto:"京都".*?\};\nconst AP_REG_SUB=\{.*?\};\n', lambda m: '''const AP_REG_TOP=Object.fromEntries(Object.entries(AP_TOPDATA).map(([k,v])=>[k,v[0]]));
const AP_SUBPICK=["grindelwald","lauterbrunnen","muerren","zermatt","saasfee","aletsch","chamonix","luzerncity","titlis","stmoritz","bernina","davos","lugano","locarno","geneve","montreux","gruyeres","zurichcity","appenzell","liechtenstein","basel","berncity"];
const AP_REG_SUB=Object.fromEntries(AP_SUBPICK.filter(k=>AP_SUBDATA[k]).map(k=>[k,AP_SUBDATA[k][0]]));
const AP_HUB=Object.fromEntries([...Object.entries(AP_TOPDATA),...Object.entries(AP_SUBDATA)].map(([k,v])=>[k,v[1]]));
const AP_HUBN=Object.fromEntries([...Object.entries(AP_TOPDATA),...Object.entries(AP_SUBDATA)].map(([k,v])=>[k,v[2]]));
let AP_CURREG=null,DAYHUBN="";
''', a, count=1, flags=re.S)
assert "AP_SUBPICK" in a
a = rep(a, 'const apRegion=id=>{let n=NODES[id];while(n){if(AP.regions[n.id])return n.id;n=n.parent}return ""};',
  'const apRegion=id=>{const R=AP_CURREG||AP.regions;let n=NODES[id];while(n){if(R[n.id])return n.id;n=n.parent}return ""};\nfunction apAutoRegs(S,days){if(days.length<3)return{};const sc={};Object.values(S).forEach(x=>{let n=NODES[x.id];while(n&&n.depth>1)n=n.parent;if(!n||!AP_REG_TOP[n.id])return;(sc[n.id]=sc[n.id]||[]).push(x.s)});const rank=Object.entries(sc).map(([k,v])=>[k,v.sort((p,q)=>q-p).slice(0,6).reduce((p,q)=>p+q,0)]).sort((p,q)=>q[1]-p[1]);const m=Math.max(1,Math.min(4,Math.round(days.length/2.5)));const top=rank.slice(0,m);const o={};let left=days.length;top.forEach(([k])=>{const q=Math.max(1,Math.round(days.length/m));o[k]=Math.min(q,left);left-=o[k]});if(left>0&&top.length)o[top[0][0]]+=left;return o}')
a = rep(a, 'if(T.includes("onsen")&&!AP.must.some(id=>(NODES[id].t||[]).includes("onsen"))){const far=x=>{const tt=apTravel([34.9858,135.7588],x.g,mode,x.remote);',
  'if(T.includes("spa")&&!AP.must.some(id=>(NODES[id].t||[]).includes("spa"))){const far=x=>{const tt=apTravel([46.8,8.2],x.g,mode,x.remote);')
a = rep(a, '.filter(x=>(NODES[x.id].t||[]).includes("onsen")).sort(', '.filter(x=>(NODES[x.id].t||[]).includes("spa")).sort(')
a = rep(a, 'for(const k of ["sakura","momiji","snow"]){if(has(k)&&inSeason(k))s+=10}', 'for(const k of ["ski","hike","autumn","xmas"]){if(has(k)&&inSeason(k))s+=10}')
a = rep(a, 'if(f.includes("s")&&!["sakura","momiji"].some(k=>has(k)&&inSeason(k))', 'if(f.includes("s")&&!["ski","hike","autumn","xmas"].some(k=>has(k)&&inSeason(k))')
a = rep(a, 'const B=AP_BASES[base].g;\n  const used=new Set();', 'const B0=AP_BASES[base].g;let B=B0;\n  const used=new Set();')
a = rep(a, 'const regDay={};{', 'const REGS=Object.keys(AP.regions||{}).length?AP.regions:apAutoRegs(S,days);AP_CURREG=REGS;const regDay={};{')
a = rep(a, 'Object.entries(AP.regions||{}).sort(', 'Object.entries(REGS).sort(')
a = rep(a, 'const KY=new Set(["kyoto",...Object.keys(AP_REG_SUB)]);', 'const KY=new Set();')
a = rep(a, 'days.forEach((d,di)=>{\n    const cx=apDayCtx(d,days,AP,B,pace0);', 'days.forEach((d,di)=>{\n    B=regDay[d]&&AP_HUB[regDay[d]]?AP_HUB[regDay[d]]:B0;\n    const cx=apDayCtx(d,days,AP,B,pace0);')
a = rep(a, 'const lbl={kyoto:"京都",nara:"奈良",osaka:"大阪",shiga:"滋贺",uminokyoto:"海之京都",morinokyoto:"森之京都"};', 'const lbl=AP_REG_TOP;AP_CURREG=null;')
a = rep(a, 'if(rg)note.unshift(`这一天专门安排「${AP_REGIONS[rg]}」`);', 'if(rg)note.unshift(`这一天专门安排「${AP_REGIONS[rg]}」，建议当晚住在${AP_HUBN[rg]||AP_REGIONS[rg]}附近`);')
a = re.sub(r'const AP_PLACES=\{kix:.*?\};\n', lambda m: 'const AP_PLACES={zrh:{n:"苏黎世机场",air:1,g:[47.4502,8.5618]},gva:{n:"日内瓦机场",air:1,g:[46.2370,6.1092]},bsl:{n:"巴塞尔机场",air:1,g:[47.5896,7.5299]},mxp:{n:"米兰马尔彭萨机场",air:1,g:[45.6306,8.7281]},zhb:{n:"苏黎世火车站",g:[47.3779,8.5402]},gvst:{n:"日内瓦火车站",g:[46.2102,6.1424]},bslst:{n:"巴塞尔火车站",g:[47.5476,7.5897]}};\n', a, count=1, flags=re.S)
assert "苏黎世机场" in a
a = rep(a, 'tr=P.t[z]', 'tr=apTravel(P.g,B,o.mode,false)', count=2)
a = a.replace('AP_PLACES.kix', 'AP_PLACES.zrh').replace('"kix"', '"zrh"')
a = rep(a, 'B=AP_BASES[r.base].g;', 'B=(r.meta[d]&&r.meta[d].rg&&AP_HUB[r.meta[d].rg])||AP_BASES[r.base].g;')
a = rep(a, 'Math.min(k==="kyoto"?10:4,', 'Math.min(6,')
a = rep(a, '选中后，京都、奈良、大阪等同一大区的日子会尽量排在一起', '选中后，同一大区的日子会尽量排在一起，减少换酒店')
a = rep(a, '[["一级区域",AP_REG_TOP],["京都细分",AP_REG_SUB]]', '[["大区",AP_REG_TOP],["热门片区",AP_REG_SUB]]')
a = rep(a, '想去的区域（可选 · 每点一次多排一天，点到上限后归零；没指定的日子自动安排）', '想去的区域（可选 · 每点一次多排一天，点到上限后归零；都不选时会按偏好自动分配到几个大区，每个大区建议住在对应的中心城镇）')
a = rep(a, 'const SHARE_BASE="https://shiyang0530.github.io/kyoto-techo/";', 'const SHARE_BASE="https://shiyang0530.github.io/swiss-techo/";')
a = a.replace("京都旅行手帖", "瑞士旅行手帖").replace("京都旅游", "瑞士旅游").replace("京都及周边", "瑞士及周边")
a = rep(a, 'const UPPER=n=>n.id==="root"||n.id==="kyoto";', 'const UPPER=n=>n.depth<=1&&n.c.some(c=>c.c.length);')
# maps
a = rep(a, '${P?planSVG(P):hills+water+rivers+geo}', '${P?planSVG(P):n.bg?n.bg+geo:hills+water+rivers+geo}')
a = rep(a, '"示意图 · 非实际比例"+(n.route?" · 虚线为推荐步行顺序":"")', '(n.bg?"地图数据：Natural Earth · 图钉位置为示意":"示意图 · 非实际比例")+(n.route?" · 虚线为推荐步行顺序":"")')
a = rep(a, 'h+=n.img?imgMap(n):mapSVG(n);', 'h+=n.img?imgMap(n):(n.bg||n.c.some(c=>c.x!=null))?mapSVG(n):photo(n,false);')
a = rep(a, 'const right=c.x<440;const tx=right?c.x+r+8:c.x-r-8;const b=badge(n,c);', 'const b=badge(n,c);const lw=[...(c.n+(b?" · "+b:""))].reduce((s,ch)=>s+(ch.charCodeAt(0)>255?13.5:7),0);const right=c.x+r+8+lw<596||c.x-r-8-lw<4;const tx=right?c.x+r+8:c.x-r-8;')
a = rep(a, 'n.folders=fs;n.key=fs.join("/");', 'n.folders=fs;n.disp=depth===0?[]:[...(p&&p.disp||[]),n.n];n.key=fs.join("/");')
a = a.replace('.folders.slice(', '.disp.slice(').replace('.folders[0]', '.disp[0]')
a = rep(a, '<circle cx="${c.x}" cy="${c.y}" r="${r}"/><text class="num"', '${mkShape(c,r)}<text class="num"')
a = rep(a, '<text class="num" x="${c.x}" y="${c.y}">${i+1}</text>', '<text class="num" x="${c.x}" y="${c.y}">${c.num||(c.c.length&&UPPER(n)?(FILTER?cntIn(c,FILTER):nSpots(c)):i+1)}</text>')
a = rep(a, 'text-anchor="${right?"start":"end"}">${esc(c.n)}${b?', 'text-anchor="${right?"start":"end"}">${esc(c.mn||c.n)}${b?')
a = rep(a, '${route}${marks}', '${route}${marks}${n.sb||""}')
a = rep(a, '${P?planSVG(P):n.bg?n.bg+geo:hills+water+rivers+geo}', '${P?planSVG(P):n.bg?n.bg.replace("__HY__",HYPSO)+geo:hills+water+rivers+geo}')
a = rep(a, 'function mapSVG(n,focus){', 'const HYPSO="data:image/webp;base64,' + base64.b64encode(open("/home/claude/swiss/out/hypso.webp","rb").read()).decode() + '";\nfunction mapSVG(n,focus){')
a = rep(a, 'function mapSVG(n,focus){', MAPJS + 'function mapSVG(n,focus){')
a = rep(a, '<div class="tagtitle">旅行计划</div>${pvBar()}', '<div class="tagtitle">旅行计划</div>${pvBar()}${planDates().length?planMapHtml(planDates()):""}')
a = rep(a, 'if(q("[data-apgo]")){AP_SEED=1;AP_RES=apGenerate();', 'if(q("[data-apgo]")){AP_SEED=1;AP_RES=apGenerate();apAuto();')
a = rep(a, 'if(q("[data-apre]")){AP_SEED++;AP_RES=apGenerate();', 'if(q("[data-apre]")){AP_SEED++;AP_RES=apGenerate();apAuto();')
a = rep(a, 'if(q("[data-apsave]")&&AP_RES&&!AP_RES.err){const nm=($("#ap-name").value||"自动行程").trim();PLAN=JSON.parse(JSON.stringify(AP_RES.plan));pvNew(nm,PLAN,AP_RES.meta,Object.assign({},AP_RES.opt,{baseRes:AP_RES.base}));savePlan();go("plan");return}', 'if(q("[data-apsave]")&&AP_RES&&!AP_RES.err){const nm=($("#ap-name").value||"自动行程").trim();apAuto();const id=Object.keys(PV.v).find(k=>PV.v[k].auto);if(id){PV.v[id].name=nm;delete PV.v[id].auto;pvSave()}go("plan");return}')
a = rep(a, '<button class="btn pri" data-apsave="1">保存为新版本并设为当前行程</button>', '<button class="btn pri" data-apsave="1">命名并打开旅行计划</button></div><p class="scnote">生成的行程已经自动放进「旅行计划」，作为当前版本「自动行程（草稿）」；再点「换一种排法」会覆盖这个草稿。想保留，就在这里起个名字。</p><div>')
a = rep(a, 'const cntIn=(c,k)=>subtree(c).filter(x=>matchTag(x,k)).length+(matchTag(c,k)?1:0);', 'const cntIn=(c,k)=>[c,...subtree(c)].filter(x=>(x.kind==="多日路线"||x.kind==="老城区"||!x.c.length)&&matchTag(x,k)).length;')
a = rep(a, 'function badge(n,c){return FILTER&&UPPER(n)?cntIn(c,FILTER):0}', 'function badge(n,c){return 0}')
a = rep(a, 'h+=localFood(n);', 'h+=localFood(n);h+=localWild(n);')
a = rep(a, '${t.k==="美食"?"时令 · 产地 · 餐厅搜索":"在书中出现的位置"}</span></div><h1>${esc(t.n)}</h1>${foodInfo(t)}', '${t.k==="美食"?"时令 · 产地 · 餐厅搜索":t.k==="地质与地貌"?"地貌 · 在哪里能看到":WILDK(t)?"季节 · 常见地区":"在书中出现的位置"}</span></div><h1>${esc(t.n)}</h1>${WILDK(t)?wildInfo(t):foodInfo(t)}')
a = rep(a, ':t.k==="美食"?"":`<p class="intro" style="margin-top:14px">目前书中还没有页面提到这个词条。</p>`', ':t.k==="美食"||WILDK(t)?"":`<p class="intro" style="margin-top:14px">目前书中还没有页面提到这个词条。</p>`')
a = rep(a, '  if(n.cards&&n.cards.length)h+=', '  if(n.archtx)h+=`<div class="sec">建筑看点</div><p class="archp">${lk(n.archtx)}</p>`;\n  if(n.cards&&n.cards.length)h+=')
a = rep(a, 'n.kind=depth===0?"总览":depth===1?', 'n.kind=depth===0?"总览":n.kd?n.kd:depth===1?')
a = rep(a, 'const UPPER=n=>n.depth<=1&&n.c.some(c=>c.c.length);', 'const UPPER=n=>n.c.some(c=>["大区","目的地","子地点"].includes(c.kind));')
a = rep(a, '${c.num||(c.c.length&&UPPER(n)?(FILTER?cntIn(c,FILTER):nSpots(c)):i+1)}', '${c.num||(n.kind==="多日路线"?i+1:(FILTER?cntIn(c,FILTER):nSpots(c)))}')
a = rep(a, 'function syncTab(){const tp=$("#tbPrev")', 'function syncTab(){syncBack();const tp=$("#tbPrev")')
a = rep(a, '$("#prevBtn").onclick=()=>{const p=parseRoute(cur);', '$("#prevBtn").onclick=()=>{const p=parseRoute(cur);if(p.terms||p.term){const L=TSEQ(),i=p.term?L.indexOf(p.term):-1;if(i>0)go("term-"+L[i-1],-1);else if(i===0)go("terms",-1);return}')
a = rep(a, '$("#nextBtn").onclick=()=>{const p=parseRoute(cur);', '$("#nextBtn").onclick=()=>{const p=parseRoute(cur);if(p.terms||p.term){const L=TSEQ(),i=p.term?L.indexOf(p.term):-1;if(i<L.length-1)go("term-"+L[i+1],1);return}')
a = rep(a, '  const i=p.node?p.node.page-1:-1;\n  $("#prevBtn").disabled=i<0;', '  if(p.terms||p.term){const L=TSEQ(),j=p.term?L.indexOf(p.term):-1;$("#prevBtn").disabled=!p.term;$("#nextBtn").disabled=j>=L.length-1;syncTab();$("#prevBtn").title=j>0?"上一页："+TERMS_[L[j-1]].n:j===0?"上一页：词典索引":"";$("#nextBtn").title=j<L.length-1?"下一页："+TERMS_[L[j+1]].n:"";return}\n  const i=p.node?p.node.page-1:-1;\n  $("#prevBtn").disabled=i<0;')
a = rep(a, 'function termIndex(){', 'const TSEQ=()=>TCATS.flatMap(c=>Object.keys(TERMS_).filter(id=>TERMS_[id].k===c));\nfunction termIndex(){')
a = rep(a, '$("#tbNext").onclick=()=>$("#nextBtn").click();', '$("#tbNext").onclick=()=>$("#nextBtn").click();$("#backBtn").onclick=()=>$("#tbPrev").click();')
a = rep(a, 'function termPages(id){', PASSJS + 'function termPages(id){')
a = rep(a, '<p class="intro" style="margin-top:14px">${esc(t.d)}</p>${foodBlock(t)}', '<p class="intro" style="margin-top:14px">${esc(t.d)}</p>${passBlock(t)}${foodBlock(t)}')
a = rep(a, '  h+=`<p class="intro">${lk(n.d)}</p>`;', '  h+=hotRef(n)+`<p class="intro">${lk(n.d)}</p>`+passBlock(n)+multiBlock(n)+hotBlock(n)+viaBlock(n)+stayBlock(n);')
a = rep(a, '?mapSVG(n):photo(n,false);', '?mapSVG(n)+lgHtml(n.lg):photo(n,false);')
a = rep(a, '"地图数据：Natural Earth · 图钉位置为示意"', '"地图数据：Natural Earth · 山峰城镇为本书标注 · 图钉位置为示意"')
a = rep(a, '} else if(pp){h+=(n.parent.air?', '} else if(pp){h+=(n.tm?tmBlock(n):"")+(n.lm?lmBlock(n):"")+(n.rm?rmBlock(n):"")+(n.parent.air?')
a = rep(a, 'function lk(s){const e=esc(s);if(!SEEN||!TRE)return e;return e.replace(TRE,m=>{const id=TMAP[m];if(SEEN.has(id))return m;SEEN.add(id);return `<button class="term" data-term="${id}">${m}</button>`})}',
  'const OGRE=/（([A-Za-zÀ-ž0-9\'’.\\-\\/&;#, ]+?)）/g;function lk(s){const e=esc(s);if(!SEEN||!TRE)return e.replace(OGRE,\'<span class="og">（$1）</span>\');return e.replace(TRE,m=>{const id=TMAP[m];if(SEEN.has(id))return m;SEEN.add(id);return `<button class="term" data-term="${id}">${m}</button>`}).replace(OGRE,\'<span class="og">（$1）</span>\')}')
a = rep(a, 'const pp=!n.c.length&&n.parent&&(n.parent.air||n.parent.plan);', 'const pp=!n.c.length&&n.parent&&(n.parent.air||n.parent.plan||(n.parent.bg&&n.x!=null));')
a = rep(a, 'if(n.depth>=2){const host=', 'if(n.depth>=2&&!n.term){const host=')
a = rep(a, '${n.depth>=2?`<div class="mrow prow">', '${PLANDATA[n.id]?`<div class="mrow prow">')
# pages
a = rep(a, 'const kindLabel={总览:"总览",地区:"地区",区域:"区域",景点:"景点",看点:"看点"}[n.kind];', 'const kindLabel=n.kind;')
a = rep(a, '"关西 · 冬日"', '"阿尔卑斯 · 四季"')
a = rep(a, 'const INFO={p:"门票",h:"时间",a:"交通"};', 'const INFO={e:"海拔",h:"开放 / 运营",p:"门票",s:"通票",l:"路线",a:"交通"};')
a = rep(a, '  if(n.cards&&n.cards.length)h+=', '  if(n.term&&TERMS_[n.term]&&TERMS_[n.term].k==="美食")h+=foodInfo(TERMS_[n.term]);\n  if(n.term&&WILDK(TERMS_[n.term]))h+=wildInfo(TERMS_[n.term]);\n  if(n.cards&&n.cards.length)h+=')
a = rep(a, 'return ORDER.filter(m=>!fam.has(m.id)&&m.depth>=2)', 'return ORDER.filter(m=>!fam.has(m.id)&&m.depth>=2&&!m.c.length)')
# food links
a = rep(a, 'const kw=t.q,pj=PREFJA[t.pref]||"";', 'const kw=t.q,pj="Schweiz";')
a = re.sub(r'<a href="https://tabelog\.com/[^>]*>食べログ 评分排行 ↗</a>', lambda m: '<a href="https://www.tripadvisor.com/Search?q=${encodeURIComponent(kw+" Switzerland")}" target="_blank" rel="noopener">Tripadvisor ↗</a>', a, count=1)
assert "tabelog" not in a
a = a.replace('(PREFZH[t.pref]||"")+" "+t.n', '"瑞士 "+t.n')
a = rep(a, '出发前请先在 App 里把城市切换到京都或大阪，到了日本会自动定位。', '出发前请先在 App 里把城市切换到苏黎世、日内瓦等瑞士城市，到了瑞士会自动定位。')
a = rep(a, '" 人気店"', '" restaurant"')
a = rep(a, 'https://ja.wikipedia.org/w/index.php?search=', 'https://de.wikipedia.org/w/index.php?search=')
a = rep(a, '>日文 ↗</a>', '>德文 ↗</a>')
a = rep(a, '正文里带下划线的词都收录在这里：宗派、建筑样式、佛像、祭典，以及相关的人物和历史事件。', '正文里带下划线的词都收录在这里：山地交通的种类、各种交通通票、瑞士美食，以及世界遗产、冰川等概念。')
# seasons
a = rep(a, 'const SC_TAGS=["sakura","momiji","snow","matsuri","newyear"];', 'const SC_TAGS=["ski","hike","autumn","xmas","matsuri"];')
a = rep(a, 'function seasonCal(n){const tags=(n.t||[]).filter(t=>SC_TAGS.includes(t));', 'function seasonCal(n){const tags=[...new Set([...(n.t||[]),...Object.keys(n.sm||{})])].filter(t=>SC_TAGS.includes(t));')
a = rep(a, '<span class="scl">${esc((TAGS[t]||t))}</span>', '<span class="scl">${esc(t==="hike"&&!(n.t||[]).includes("hike")?"夏季开放":t==="hike"?"徒步季节":(TAGS[t]||t))}</span>')
a = rep(a, 'const has=k=>(n.t||[]).includes(k)', 'const has=k=>(n.t||[]).includes(k)||!!(n.sm&&n.sm[k])')
a = rep(a, 'const SC_DEF={sakura:[[3.7,4.2]],momiji:[[11.4,12.1]],snow:[[1.1,2.7]],newyear:[[12.97,13],[1,1.15]],matsuri:[]};', 'const SC_DEF={ski:[[12.4,13],[1,4.4]],hike:[[6.0,10.0]],autumn:[[9.6,10.9]],xmas:[[11.75,12.8]],matsuri:[]};')
a = re.sub(r'出发前请查当年的开花、红叶或活动公告。<b>浅色</b>表示该地点没有单独资料，按京都市区平均估计。\$\{t==="snow"\?"[^"]*":""\}',
  lambda m: '出发前请查当年雪场、步道或缆车的开放公告，以及活动日期。<b>浅色</b>表示该地点没有单独资料，按瑞士一般情况估计。', a, count=1)
assert "按瑞士一般情况估计" in a
a = rep(a, 'x>=12.5&&t!=="momiji"?x-12:x', 'x>=12.5&&t!=="autumn"?x-12:x')
# toc
a = rep(a, 'const open=new Set(["root","kyoto"]);', 'const open=new Set(["root"]);')
a = re.sub(r'const G=\[\["时令","sakura momiji snow matsuri newyear"\].*?\];\n', lambda m: 'const G=[["时令","ski hike autumn xmas matsuri"],["交通","transport"],["自然风景","alps rhine view glacier lake waterfall nature spa"],["历史文化","history unesco arch castle church museum art"],["适合人群","elderly couple family"],["吃喝玩乐","hot food town shopping"],["实用信息","free crossborder"]];\n', a, count=1, flags=re.S)
assert '["交通"' in a

# ---- multi-base auto planner ----
AUTOFN = r"""function apAutoDays(S,days,mode,pace){
  const N=days.length;const Nf=N-(toMin(AP.depT)!=null&&N>1?1:0);const ar={};
  Object.values(S).forEach(x=>{const n=NODES[x.id];const a=n&&n.parent;if(!a||a.depth!==2||!AP_HUB[a.id])return;(ar[a.id]=ar[a.id]||[]).push(x)});
  const val={};Object.entries(ar).forEach(([k,xs])=>{const sc=xs.filter(x=>x.dur>=40||x.s>=1000).map(x=>x.s).sort((p,q)=>q-p);if(sc.length)val[k]=sc.slice(0,pace.max||3).reduce((p,q)=>p+q,0)});
  const alloc=(keys,n,extra)=>{const c={};for(let i=0;i<n;i++){let best=null;keys.forEach(k=>{const u=c[k]||0;const cap=Math.max(1,Math.ceil(ar[k].length/Math.max(2,pace.max||3)))+extra;if(u>=cap)return;const v=val[k]*Math.pow(0.55,u);if(!best||v>best[1])best=[k,v]});if(!best)break;c[best[0]]=(c[best[0]]||0)+1}return c};
  const tt=(a,b)=>apTravel(a,b,mode,false);
  const c1=alloc(Object.keys(val),Nf,0);const blocks=[];
  Object.keys(c1).sort((a,b)=>val[b]-val[a]).forEach(k=>{const g=AP_HUB[k];const bl=blocks.find(b=>tt(b.g,g)<=90);if(bl){bl.a.push(k);bl.v+=val[k]*c1[k]}else blocks.push({k,g,a:[k],v:val[k]*c1[k]})});
  const M=Math.max(1,Math.min(blocks.length,Math.round(Nf/2.6)||1));const A0=((AP_PLACES[AP.arrP]||AP_PLACES.zrh).g),Z0=((AP_PLACES[AP.depP]||AP_PLACES[AP.arrP]||AP_PLACES.zrh).g);blocks.forEach(b=>{b.w=b.v*Math.exp(-Math.max(0,tt(A0,b.g)+tt(b.g,Z0)-360)/240)});const kept=blocks.sort((p,q)=>q.w-p.w).slice(0,M);kept.forEach(b=>b.a=[]);
  const cand=Object.keys(val).filter(k=>kept.some(b=>tt(b.g,AP_HUB[k])<=90));const cnt=alloc(cand,Nf,1);
  Object.keys(cnt).forEach(k=>{const b=kept.slice().sort((p,q)=>tt(p.g,AP_HUB[k])-tt(q.g,AP_HUB[k]))[0];b.a.push(k)});
  const A=((AP_PLACES[AP.arrP]||AP_PLACES.zrh).g),Z=((AP_PLACES[AP.depP]||AP_PLACES[AP.arrP]||AP_PLACES.zrh).g);const bs=kept.filter(b=>b.a.length);
  const perms=a=>a.length<2?[a]:a.flatMap((x,i)=>perms([...a.slice(0,i),...a.slice(i+1)]).map(p=>[x,...p]));
  let ord=bs,bc=1e9;perms(bs).forEach(p=>{let c=tt(A,p[0].g)+tt(p[p.length-1].g,Z);for(let i=1;i<p.length;i++)c+=tt(p[i-1].g,p[i].g);if(c<bc){bc=c;ord=p}});
  const seq=[];ord.forEach(b=>{b.a.slice().sort((p,q)=>tt(b.g,AP_HUB[p])-tt(b.g,AP_HUB[q])).forEach(k=>{for(let j=0;j<cnt[k];j++)seq.push([k,b])})});
  const regDay={},dayBase={},dayBaseN={};days.forEach((d,i)=>{const x=seq[Math.min(i,seq.length-1)];if(!x)return;regDay[d]=x[0];dayBase[d]=x[1].g;dayBaseN[d]=AP_HUBN[x[1].k]});
  const segs=[];let i=0;while(i<days.length){const n=dayBaseN[days[i]];let j=i;while(j+1<days.length&&dayBaseN[days[j+1]]===n)j++;if(n)segs.push(`第${i+1}${j>i?"–"+(j+1):""}天 ${n}`);i=j+1}
  return {regDay,dayBase,dayBaseN,segs:segs.join(" → "),regs:Object.fromEntries(Object.keys(cnt).map(k=>[k,cnt[k]]))}}
"""
a = rep(a, 'function apGenerate(){', AUTOFN + 'function apGenerate(){')
a = rep(a, 'const REGS=Object.keys(AP.regions||{}).length?AP.regions:apAutoRegs(S,days);AP_CURREG=REGS;const regDay={};{',
  'const AUTO=!Object.keys(AP.regions||{}).length&&days.length>=2;const AD=AUTO?apAutoDays(S,days,mode,pace):null;const REGS=AUTO?AD.regs:(AP.regions||{});AP_CURREG=REGS;const regDay={};if(AUTO)Object.assign(regDay,AD.regDay);else{')
a = rep(a, 'const B0=AP_BASES[base].g;let B=B0;', 'const B0=AP_BASES[base].g;let B=B0,PREVB=null;')
a = rep(a, 'B=regDay[d]&&AP_HUB[regDay[d]]?AP_HUB[regDay[d]]:B0;\n    const cx=apDayCtx(d,days,AP,B,pace0);',
  'B=AD?(AD.dayBase[d]||B0):(regDay[d]&&AP_HUB[regDay[d]]?AP_HUB[regDay[d]]:B0);DAYHUBN=AD?(AD.dayBaseN[d]||""):"";\n    const cx=apDayCtx(d,days,AP,B,pace0);\n    if(di>0&&PREVB&&km(PREVB,B)>3){const tr=apTravel(PREVB,B,mode,false);const at=cx.start;cx.pre.push({mv:1,at,txt:`退房，前往${DAYHUBN||AP_HUBN[regDay[d]]||"新的住处"}，约 ${tr} 分钟，寄存行李`});const s0=Math.ceil((at+tr+20)/5)*5;cx.budget=Math.max(0,cx.budget-(s0-cx.start));cx.start=s0;if(cx.budget<75){cx.budget=0;cx.max=0}else cx.max=Math.max(1,Math.min(cx.max,Math.round(cx.max*cx.budget/pace0.budget+0.4)));cx.short=1}\n    PREVB=B;')
a = rep(a, 'meta[d]={rows,back,food,note,rg,dep};', 'meta[d]={rows,back,food,note,rg,dep,bg:B};')
a = rep(a, 'if(AP.few!==false){', 'if(AP.few!==false&&!AUTO){')
a = rep(a, 'return {days,plan,meta,base,baseWhy,warn,', 'return {days,plan,meta,base,baseWhy:AD?"按区域分段住宿，每段住在中心城镇；换住处的日子已预留路上的时间":baseWhy,segs:AD?AD.segs:"",warn,')
a = rep(a, '住宿：<b>${esc(AP_BASES[r.base].n)}</b>', '住宿：<b>${esc(r.segs||AP_BASES[r.base].n)}</b>')
a = rep(a, 'Object.assign(apDayCalc(ordered,eve,B,pace,mode,old.rg),{rg:old.rg})', 'Object.assign(apDayCalc(ordered,eve,B,pace,mode,old.rg),{rg:old.rg,bg:old.bg})')
a = rep(a, 'B=(r.meta[d]&&r.meta[d].rg&&AP_HUB[r.meta[d].rg])||AP_BASES[r.base].g;', 'B=(r.meta[d]&&r.meta[d].bg)||(r.meta[d]&&r.meta[d].rg&&AP_HUB[r.meta[d].rg])||AP_BASES[r.base].g;')
a = rep(a, 'B=((AP_BASES[o.baseRes]||AP_BASES[o.base]||{}).g)||AP_BASES.kawara.g;', 'B=(((v.meta||{})[d]||{}).bg)||((AP_BASES[o.baseRes]||AP_BASES[o.base]||{}).g)||AP_BASES.zurich.g;')
a = rep(a, 'const AP_REGIONS={...AP_REG_TOP,...AP_REG_SUB};', 'const AP_REGIONS={...Object.fromEntries(Object.entries(AP_SUBDATA).map(([k,v])=>[k,v[0]])),...AP_REG_TOP};')
a = rep(a, '建议当晚住在${AP_HUBN[rg]||AP_REGIONS[rg]}附近', '建议当晚住在${DAYHUBN||AP_HUBN[rg]||AP_REGIONS[rg]}附近')
a = rep(a, 'for(const k of ["ski","hike","autumn","xmas"]){if(has(k)&&inSeason(k))s+=10}', 'for(const k of ["ski","hike","autumn","xmas"]){if(has(k)&&inSeason(k))s+=10}{const sk=["ski","hike","autumn","xmas"].filter(has);if(sk.length&&!sk.some(inSeason))s-=7}')
a = rep(a, 'if(f.includes("s")&&!["ski","hike","autumn","xmas"].some(k=>has(k)&&inSeason(k))', 'if(f.includes("s")&&!["ski","hike","autumn","xmas","matsuri"].some(k=>has(k)&&inSeason(k))')
a = rep(a, 'if(arr!=null){const P=AP_PLACES[o.arrP]', 'if(arr!=null){c.arr=1;const P=AP_PLACES[o.arrP]')
a = rep(a, 'if(cx.pre&&cx.pre.length&&!ordered.length)note.unshift(', 'if(cx.arr&&!ordered.length)note.unshift(')
a = rep(a, 'pp?"境内图 · 位置":"图片"', 'pp?(n.tm?(n.tm.st?"雪场图 · 位置":n.tm.k==="ski"?"路线图 · 位置":"徒步路线图 · 位置"):n.parent.bg?"地图 · 位置":"境内图 · 位置"):"图片"')
# guide pages
GUIDE = r'''function guidePages(){
  const L=`<div class="gcover"><span class="eyebrow">阿尔卑斯 · 瑞士及周边</span><div class="cover-t">瑞士旅行手帖</div><p class="cover-s">一本可以翻页、搜索、按兴趣筛选的旅行电子书。八个大区加勃朗峰与列支敦士登，三个专题，${ORDER.filter(n=>n.depth>=2&&!n.c.length).length} 个景点与条目；滑雪季、徒步路线、赏秋一目了然。</p>
  <div class="cover-img">${mapSVG(BOOK)}</div><button class="btn pri" data-go="root">开始阅读 →</button></div>`;
  const S=[["翻页与层级","书按「总览 → 大区 → 片区 → 景点」一层层展开，每一层左边是地图，右边是介绍。点地图上的编号或右侧列表就能进入下一层。用两侧的 ‹ › 按钮或键盘 ← → 按书页顺序翻页，Backspace 回到上一层，顶部的路径可以随时跳回任何一层。顶部的「‹ 返回」按钮（手机上在底部）回到刚才看过的页面，例如从路线分段跳到词典后再回来，左右滑动或「下一页」按书页顺序翻页。"],
  ["读懂地图","地图按真实地理位置绘制：浅色是瑞士和列支敦士登，深色是周边国家，蓝色是湖泊和河流，虚线是国界，黑白相间的线是铁路，▲ 是山峰，)( 是山口，小圆点是城镇，名称后面的小号数字是海拔（米），湖泊名后面是湖面海拔；总览图和大区图上，由浅到深的底色是海拔分层：浅黄约 1000–2000 米，褐色约 2000–3000 米，近白色是 3000 米以上的高山雪区。这层底色是根据书中几百个已知海拔的点推算的示意图，只表示大致地势，不是精确地形；右下角有比例尺，每张地图下方都有图例。总览图上不同的底色是本书划分的八个大区；大区和片区圆点里的数字是其中收录的景点数，景点图上的数字是列表编号。热门景点旁有小插画，位置是示意。景点图钉的形状和颜色表示类型：红色圆形是一般景点，绿色三角是徒步路线，蓝色菱形是滑雪场，紫色方块是缆车、齿轨铁路等山地交通。几个景点挨得太近时，图钉会稍微错开，位置仅为示意。"],["路线图与雪场图","徒步路线和滑雪场的景点页左侧，有一张专门的示意地图。徒步路线图标出起点、终点、途经点和推荐方向，下面附有海拔剖面和途经点表（中文名、当地原名和海拔）。雪场图标出滑雪区域的大致范围、主要缆车和登山铁路，以及各站点的海拔。这些图里的线路和站点位置是近似值，出发前请以官方地图和现场路标为准。"],["地图缩放","每张地图右上角有 + − ⤢ 三个按钮，可以放大、缩小和还原。电脑上也可以双击放大（按住 Shift 双击缩小），或按住 Ctrl 滚动鼠标滚轮；手机上用两指张开放大。放大后可以拖动地图查看其他部分，这时右下角的比例尺会暂时隐藏。"],["当地原名","简介中的地名第一次出现时，括号里附有当地语言的原名（德语、法语、意大利语或罗曼什语），方便在当地看路牌、查车票或搜索地图。也可以直接用原名在右上角搜索。"],
  ["三个时令","每个景点都标了时令：「滑雪季」通常是 12 月到次年 4 月，徒步路线的适合季节通常是 6 月到 9 月，「赏秋」是 9 月底到 10 月的落叶松、葡萄采收和牧牛下山节。景点页下方的时令月历用色条标出大致时期；在目录的标签索引里点任一时令，可以看到全书该时令景点的月历总表。"],
  ["体力分级","每个景点都标了体力等级：「轻松」表示坐车或缆车可以直达，步行很少，适合老人和小孩；「适中」是 2 到 3 小时的平缓步道；「进阶」是爬升大、路程长或需要不恐高的路线。用地图上方的筛选可以只看某一等级。"],
  ["按兴趣筛选","地图上方有一排标签，例如「齿轨铁路」「冰川」「适合老人」「免门票」。选一个标签，地图和列表只保留符合的景点。在总览和大区页选标签，会显示每个片区有几处符合。翻页后筛选自动清除。"],
  ["搜索与标签索引","右上角搜索框可以搜景点名（中文或当地名称），也可以搜标签，按 / 键快速聚焦。打开「目录」，下方的「标签索引」按时令、体力、山地交通、自然、历史文化、吃喝玩乐分组，点任意一行进入该标签的全部景点。"],
  ["我的标签","每个景点标题下都有「我的标签」：点「♡ 收藏」「想去」「已去过」，或输入自己的标签（例如「第二天」「带父母」）。所有保存的景点汇总在「我的标签」页，可以导出后在别的设备导入。标签只保存在你自己的浏览器里。"],
  ["旅行计划","景点页的「我的标签」下方有「旅行计划」：选一个日期，点「加入行程」即可把景点排进那一天。顶部的「旅行计划」按钮打开行程单，按日期列出每天的景点并可调整顺序；点「在地图上看」，地图只显示当天的景点。行程页上方还有一张行程地图，用不同颜色标出每天的景点并按顺序连线。"],
  ["自动生成行程","在「旅行计划」页或目录里点「✨ 自动生成行程」：填出发和结束日期、到达和离开的机场或车站、节奏、交通方式和偏好标签，也可以指定必去景点。瑞士的行程通常要在几个大区之间移动：你可以在「想去的区域」里点选大区或热门片区，每点一次多排一天；都不选时，系统会按你的偏好自动把日子分配到几个大区，并在每天的提示里写出建议住宿的中心城镇。时令类偏好（滑雪季、徒步、赏秋、圣诞市集、节庆）只在出行日期对得上时生效，只在某个季节开放的缆车和雪场也会自动避开淡季。"],
  ["多版本与分享","旅行计划顶部的「行程版本」可以保存多套方案。点「📤 分享行程」可以复制链接发给朋友，对方打开就能一键导入；「复制文字版」适合贴进微信；「打印 / 存为 PDF」会生成一份干净的行程单。"],
  ["词典与美食","正文中带虚下划线的词（齿轨铁路、缆索铁路、瑞士通票、芝士火锅等）可以点击，先弹出小卡片，再点「查看词条」进入词典页。美食词条附有时令和产地，以及 Google 地图、Tripadvisor 和大众点评的搜索链接，本书不推荐具体店家。"],
  ["门票与官网","景点页列出海拔、运营时间、通票优惠和交通的参考信息。山地交通的票价和运营日期每年都会调整，每年 4 月底到 5 月、11 月前后许多缆车停运检修，请以官方发布为准：有官网的景点可以直接打开，其他景点可以用你选择的搜索引擎搜索。"],
  ["照片","书中的照片都来自 Wikimedia Commons，均为允许商业使用的授权（CC BY、CC BY-SA、CC0 或公有领域），每张照片下方注明了作者和授权。没有找到合适授权照片的景点，会显示一个图片搜索链接。你也可以把自己拍的照片放进电脑上「瑞士旅游」文件夹里对应的景点子文件夹，再在「图片素材」里选择整个文件夹，照片就会出现在对应页面上，并保存在这台设备的浏览器里。"],
  ["离线使用","整本书是一个 HTML 文件，地图、字体和文字都已内置。把文件保存到电脑或手机，用浏览器打开即可离线阅读；只有官网和搜索链接需要联网。在 iPhone 上请用 Safari 打开，而不是在「文件」里预览。"]];
  const R=`<div class="kicker"><span class="kind">使用说明</span><span>第一次阅读请看这里</span></div><h1>怎样使用这本书</h1>${S.map(([h,p],i)=>`<div class="guide"><span class="gn">${String(i+1).padStart(2,"0")}</span><div><b>${h}</b><p>${p}</p></div></div>`).join("")}<span class="folio">ii</span>`;
  return [L,R];
}
'''
i0 = a.index("function guidePages(){"); i1 = a.index("let CLEAR_ARMED=false;")
a = a[:i0] + GUIDE + a[i1:]
# ---- compound tag filters: 交通 / 徒步 sub-filters ----
a = rep(a, 'const matchTag=(n,k)=>', 'const matchTag=(n,k)=>k&&k.includes("&")?k.split("&").every(p=>matchTag(n,p)):')
a = rep(a, 'const tagLabel=k=>', 'const tagLabel=k=>k&&k.includes("&")?k.split("&").map(p=>TAGS[p]).join(" · "):')
a = rep(a, 'function filterBar(n){', """const SUBF={transport:[["",["mtn","train","boat","rail","bus"]]],hike:[["难度",["easy","moderate","hard"]],["时长",["d4h","d1","dmulti"]]]};
const SUBHIDE=new Set(["mtn","cog","funi","cable","train","boat","rail","bus","easy","moderate","hard","d4h","d1","dmulti"]);
const fBase=()=>FILTER&&!isMy(FILTER)&&!isPlan(FILTER)?FILTER.split("&")[0]:null;
function subBar(pool,F=FILTER,attr="data-filter"){const b=F&&!isMy(F)&&!isPlan(F)?F.split("&")[0]:null;if(!b||!SUBF[b])return "";const cur=F.split("&").slice(1);
  return `<div class="fsub" role="toolbar" aria-label="${esc(TAGS[b])}细分">${SUBF[b].map(([lab,ks])=>{const other=cur.filter(x=>!ks.includes(x));
    const cs=ks.map(k=>{const on=cur.includes(k);const key=[b,...other,...(on?[]:[k])].join("&");const c=pool.filter(x=>matchTag(x,[b,...other,k].join("&"))).length;if(!c&&!on)return "";return `<button class="fchip sub${on?" on":""}" ${attr}="${esc(key)}">${esc(TAGS[k])}<small>${c}</small></button>`}).join("");
    return cs?`<span class="fsg">${lab?`<b>${lab}</b>`:""}${cs}</span>`:""}).join("")}</div>`}
function filterBar(n){""")
a = rep(a, 'function tagPages(t){\n  const list=ORDER.filter(n=>hasTag(n,t));', 'function tagPages(T){\n  const t=T.split("&")[0],list=ORDER.filter(n=>matchTag(n,T));')
a = rep(a, '</button>`).join(" ")}</p>`:""}<p style="color:var(--ink-2)">共 ${list.length} 处，分布在', '</button>`).join(" ")}</p>`:""}${subBar(ORDER.filter(n=>hasTag(n,t)),T,"data-tag")}<p style="color:var(--ink-2)">共 ${list.length} 处，分布在')
a = rep(a, '${Object.keys(TAGS).filter(k=>TAGCOUNT[k]).map(k=>`<button class="tag${k===t?" cur":""}"', '${Object.keys(TAGS).filter(k=>TAGCOUNT[k]&&(!SUBHIDE.has(k)||k===t)).map(k=>`<button class="tag${k===t?" cur":""}"')
a = rep(a, '<h1>${esc(TAGS[t])}</h1><div class="kids" style="margin-top:14px">', '<h1>${esc(tagLabel(T))}</h1><div class="kids" style="margin-top:14px">')
a = rep(a, 'if(r.startsWith("tag-")&&TAGS[r.slice(4)])return{tag:r.slice(4)};', 'if(r.startsWith("tag-")&&TAGS[r.slice(4).split("&")[0]])return{tag:r.slice(4)};')
a = rep(a, 'if(SC_TAGS.includes(t))return seasonTagPages(t,list);', 'if(SC_TAGS.includes(t))return seasonTagPages(t,list,T);')
a = rep(a, 'function seasonTagPages(t,list){', 'function seasonTagPages(t,list,T=t){')
a = rep(a, 'const L=`<span class="eyebrow">时令</span><div class="tagtitle">${esc(TAGS[t])}</div><p style="color:var(--ink-2)">', 'const L=`<span class="eyebrow">时令</span><div class="tagtitle">${esc(tagLabel(T))}</div>${subBar(ORDER.filter(n=>hasTag(n,t)),T,"data-tag")}<p style="color:var(--ink-2)">')
a = a.replace('<span class="cur">标签 · ${esc(TAGS[p.tag])}</span>', '<span class="cur">标签 · ${esc(tagLabel(p.tag))}</span>')
a = rep(a, 'const rest=Object.keys(TAGS).filter(k=>!used.has(k)&&TAGCOUNT[k]&&!TAG_PARENT[k]);', 'const rest=Object.keys(TAGS).filter(k=>!used.has(k)&&TAGCOUNT[k]&&!TAG_PARENT[k]&&!SUBHIDE.has(k));')
# ================= autoplan v2 =================
a = rep(a, 'const AP_SUBPICK=["grindelwald","lauterbrunnen","muerren","zermatt","saasfee","aletsch","chamonix","luzerncity","titlis","stmoritz","bernina","davos","lugano","locarno","geneve","montreux","gruyeres","zurichcity","appenzell","liechtenstein","basel","berncity"];',
  'if(AP_SUBDATA.luzerncity)AP_SUBDATA.luzernx=["琉森",AP_SUBDATA.luzerncity[1],"琉森"];\nconst AP_SUBPICK=["zurichcity","jungfrauregion","luzernx","zermatt","chamonix","geneve"];const AP_SUBLBL={zurichcity:"苏黎世",jungfrauregion:"因特拉肯与少女峰",luzernx:"琉森",zermatt:"马特洪峰",chamonix:"勃朗峰",geneve:"日内瓦"};\nconst AP_ALIAS={luzerncity:"luzernx",luzernsee:"luzern"+"x"};\nconst AP_PLREG={zrh:"zurichcity",zhb:"zurichcity",gva:"geneve",gvst:"geneve",bsl:"basel",bslst:"basel",mxp:"lugano"};')
a = rep(a, 'const AP_REG_SUB=Object.fromEntries(AP_SUBPICK.filter(k=>AP_SUBDATA[k]).map(k=>[k,AP_SUBDATA[k][0]]));', 'const AP_REG_SUB=Object.fromEntries(AP_SUBPICK.filter(k=>AP_SUBDATA[k]).map(k=>[k,AP_SUBLBL[k]||AP_SUBDATA[k][0]]));')
a = rep(a, 'const apRegion=id=>{const R=AP_CURREG||AP.regions;let n=NODES[id];while(n){if(R[n.id])return n.id;n=n.parent}return ""};', 'const apRegion=id=>{const R=AP_CURREG||AP.regions;let n=NODES[id];while(n){if(R[n.id])return n.id;const al=AP_ALIAS[n.id];if(al&&R[al])return al;n=n.parent}return ""};')
a = rep(a, 'if(!AP.regions||typeof AP.regions!=="object")AP.regions={};', 'if(!AP.regions||typeof AP.regions!=="object")AP.regions={};Object.keys(AP.regions).forEach(k=>{if(!AP_REG_TOP[k]&&!AP_REG_SUB[k])delete AP.regions[k]});AP.tags=(AP.tags||[]).filter(k=>!["ski","hike","d4h","d1","dmulti","easy","moderate","hard"].includes(k));if(!Array.isArray(AP.hikeDur))AP.hikeDur=["d4h","d1"];')
a = rep(a, 'const AP_TAG_G=[["时令","ski autumn xmas matsuri"],["徒步","hike d4h d1 dmulti"],', 'const AP_TAG_G=[["时令","autumn xmas matsuri"],')
# scenic trains
a = rep(a, 'function apAutoDays(S,days,mode,pace){', """const AP_TRAINS=(()=>{const o=[];const P=n=>{const m=/约\\s*(\\d+)\\s*小时(?:\\s*(\\d+)\\s*分钟)?/.exec(n)||/约\\s*(\\d+)\\s*分钟/.exec(n);if(!m)return 0;return /小时/.test(m[0])?+m[1]*60+ +(m[2]||0):+m[1]};
  ORDER.forEach(n=>{if(!n.route||!(n.t||[]).includes("train")||!n.i||!n.i.l||n.route.length<2)return;const min=P(n.i.l.split(/[；;]/)[0]);if(!min)return;let L=0;const cum=[0];for(let i=1;i<n.route.length;i++){L+=km(n.route[i-1],n.route[i]);cum.push(L)}o.push({id:n.id,n:n.n,r:n.route,cum,L,min})});return o})();
function apTrain(a,b){let best=null;AP_TRAINS.forEach(T=>{const near=g=>{let bi=-1,bd=1e9;T.r.forEach((p,i)=>{const d=km(g,p);if(d<bd){bd=d;bi=i}});return bd<=22?bi:-1};const i=near(a),j=near(b);if(i<0||j<0||i===j)return;const seg=Math.abs(T.cum[j]-T.cum[i]);if(seg<T.L*0.35||seg<35)return;const m=Math.round(T.min*seg/T.L/5)*5;if(m>apTravel(a,b,"public",false)*2.3)return;if(!best||seg>best.seg)best={id:T.id,n:T.n,min:m,seg}});return best}
function apAutoDays(S,days,mode,pace){""")
a = rep(a, 'let ord=bs,bc=1e9;perms(bs).forEach(p=>{let c=tt(A,p[0].g)+tt(p[p.length-1].g,Z);', 'let ord=bs,bc=1e9;perms(bs).forEach(p=>{let c=tt(A,p[0].g)*1.3+tt(p[p.length-1].g,Z);')
a = rep(a, "const regDay={},dayBase={},dayBaseN={};days.forEach((d,i)=>{const x=seq[Math.min(i,seq.length-1)];", """const fixEnd=(pl,atStart)=>{const P=AP_PLACES[pl]||AP_PLACES.zrh;const r=AP_PLREG[pl]||"zurichcity";if(!AP_HUB[r]||seq.length<3)return;const x=atStart?seq[0]:seq[seq.length-1];if(!x||x[0]===r||tt(P.g,x[1].g)<=100)return;
    const c={};seq.forEach(q=>c[q[0]]=(c[q[0]]||0)+1);let rm=-1;const ks=Object.keys(c).filter(k=>c[k]>1).sort((p,q)=>c[q]-c[p]);if(ks.length){for(let i=seq.length-1;i>=0;i--)if(seq[i][0]===ks[0]){rm=i;break}}else{let lo=1e18;seq.forEach((q,i)=>{if((val[q[0]]||0)<lo&&i!==(atStart?seq.length-1:0)){lo=val[q[0]]||0;rm=i}})}
    if(rm<0)return;const k0=seq[rm][0];seq.splice(rm,1);cnt[k0]--;if(!cnt[k0])delete cnt[k0];const e=[r,{g:AP_HUB[r],k:r}];if(atStart)seq.unshift(e);else seq.push(e);cnt[r]=(cnt[r]||0)+1};
  if(seq.length>=3){fixEnd(AP.arrP||"zrh",true);fixEnd(AP.depP||AP.arrP||"zrh",false)}
  const regDay={},dayBase={},dayBaseN={};days.forEach((d,i)=>{const x=seq[Math.min(i,seq.length-1)];""")
# manual region ordering by geography
a = rep(a, "const order=[];for(let j=0;j<want.length;j++){if(pi>=pref.length){warn.push(`日期不够，「${AP_REGIONS[want[j]]}」少排了 1 天`);continue}order.push([pref[pi++],want[j]])}\n    order.sort((a,b)=>a[0]<b[0]?-1:1);const seen={};order.forEach(([d,r])=>{regDay[d]=r});}",
  """const dsel=[];for(let j=0;j<want.length;j++){if(pi>=pref.length){warn.push(`日期不够，「${AP_REGIONS[want[j]]}」少排了 1 天`);continue}dsel.push(pref[pi++])}dsel.sort();
    const A=(AP_PLACES[AP.arrP]||AP_PLACES.zrh).g,Z=(AP_PLACES[AP.depP]||AP_PLACES[AP.arrP]||AP_PLACES.zrh).g,tt=(p,q)=>apTravel(p,q,mode,false),hub=k=>AP_HUB[k]||B0;
    const ks=[...new Set(want)];const perms=x=>x.length<2?[x]:x.flatMap((y,i)=>perms([...x.slice(0,i),...x.slice(i+1)]).map(p=>[y,...p]));let ord=ks,bc=1e18;(ks.length<=7?perms(ks):[ks]).forEach(p=>{let c=tt(A,hub(p[0]))*1.3+tt(hub(p[p.length-1]),Z);for(let i=1;i<p.length;i++)c+=tt(hub(p[i-1]),hub(p[i]));if(c<bc){bc=c;ord=p}});
    const seqR=ord.flatMap(k=>want.filter(x=>x===k));dsel.forEach((d,i)=>{if(seqR[i])regDay[d]=seqR[i]});}""")
# hike / ski gating
a = rep(a, "for(const id of ids){const n=NODES[id],[la,lo,dur,f]=PLANDATA[id];const has=k=>(n.t||[]).includes(k)||!!(n.sm&&n.sm[k]);",
  """const inSeasonAny=k=>ms.some(m=>segHit(SC_DEF[k],m));
  for(const id of ids){const n=NODES[id],[la,lo,dur,f]=PLANDATA[id];const has=k=>(n.t||[]).includes(k)||!!(n.sm&&n.sm[k]);const MUST=AP.must.includes(id);
    if(n.kind==="多日路线"&&!MUST)continue;
    if(n.mk==="hike"&&!MUST){if(!AP.hike)continue;if(!ms.some(m=>segHit((n.sm&&n.sm.hike)||SC_DEF.hike,m)))continue;if(AP.hikeDur.length&&!AP.hikeDur.some(k=>(n.t||[]).includes(k)))continue}
    if(n.mk==="ski"&&!MUST){if(!AP.ski)continue;if(!ms.some(m=>segHit((n.sm&&n.sm.ski)||SC_DEF.ski,m)))continue}""")
a = rep(a, "    if(AP.must.includes(id))s+=1000;\n", "    if(AP.must.includes(id))s+=1000;\n    if(AP.hike&&n.mk===\"hike\")s+=20;if(AP.ski&&n.mk===\"ski\")s+=25;\n")
a = rep(a, "  const reserved=new Set();Object.values(fixed).forEach(a=>a.forEach(x=>reserved.add(x.id)));", """  if(AP.hike&&!inSeasonAny("hike"))warn.push("出行日期不在徒步季（大致 6 月至 10 月），没有安排徒步路线");
  if(AP.ski&&!inSeasonAny("ski"))warn.push("出行日期不在滑雪季（大致 12 月中旬至次年 4 月中旬），没有安排滑雪");
  const reserved=new Set();Object.values(fixed).forEach(a=>a.forEach(x=>reserved.add(x.id)));""")
# base change with scenic train
a = rep(a, "if(di>0&&PREVB&&km(PREVB,B)>3){const tr=apTravel(PREVB,B,mode,false);const at=cx.start;cx.pre.push({mv:1,at,txt:`退房，前往${DAYHUBN||AP_HUBN[regDay[d]]||\"新的住处\"}，约 ${tr} 分钟，寄存行李`});",
  "if(di>0&&PREVB&&km(PREVB,B)>3){let tr=apTravel(PREVB,B,mode,false);const at=cx.start;const dest=DAYHUBN||AP_HUBN[regDay[d]]||\"新的住处\";const TR=AP.scenic!==false&&mode!==\"car\"?apTrain(PREVB,B):null;if(TR){tr=Math.max(tr,TR.min);cx.pre.push({mv:1,at,go:TR.id,txt:`退房，乘坐观景列车「${TR.n}」前往${dest}，约 ${durTx(tr)}（多数需预订座位），到后寄存行李`})}else cx.pre.push({mv:1,at,txt:`退房，前往${dest}，约 ${tr} 分钟，寄存行李`});")
a = a.replace('`<li class="lunch mv"><time>${hm(r.at)}</time><span>${esc(r.txt)}</span></li>`', '`<li class="lunch mv"><time>${hm(r.at)}</time><span>${esc(r.txt)}${r.go&&NODES[r.go]?` <button class="mylink" data-go="${r.go}">查看列车 →</button>`:""}</span></li>`')
# UI
a = rep(a, '   <label>换宿</label><div class="aprow wrap">', """   <label>徒步与滑雪（不勾选就不安排；勾选后也只在当季安排）</label><div class="aprow wrap"><button class="fchip${AP.hike?" on":""}" data-apck="hike" aria-pressed="${!!AP.hike}">${AP.hike?"☑":"☐"} 徒步</button>${AP.hike?["d4h","d1"].map(k=>`<button class="fchip sub${AP.hikeDur.includes(k)?" on":""}" data-aphd="${k}">${esc(TAGS[k])}</button>`).join(""):""}<button class="fchip${AP.ski?" on":""}" data-apck="ski" aria-pressed="${!!AP.ski}">${AP.ski?"☑":"☐"} 滑雪</button></div>
   <label>换住处时的交通</label><div class="aprow wrap"><button class="fchip${AP.scenic!==false?" on":""}" data-apck="scenic" aria-pressed="${AP.scenic!==false}">${AP.scenic!==false?"☑":"☐"} 有观景列车时坐观景列车</button><span class="scnote" style="margin:0">冰川快车、黄金山口快车等，算进路上时间，不算游玩项目</span></div>
   <label>换宿</label><div class="aprow wrap">""")
a = rep(a, '  if(q("[data-apfew]")){AP.few=AP.few===false;apSave();render(cur,false);return}', '  if(q("[data-apfew]")){AP.few=AP.few===false;apSave();render(cur,false);return}\n  if(b=q("[data-apck]")){const k=b.dataset.apck;if(k==="scenic")AP.scenic=AP.scenic===false;else AP[k]=!AP[k];apSave();render(cur,false);return}\n  if(b=q("[data-aphd]")){const k=b.dataset.aphd;AP.hikeDur=AP.hikeDur.includes(k)?AP.hikeDur.filter(x=>x!==k):[...AP.hikeDur,k];apSave();render(cur,false);return}')
a = rep(a, "const REGS=AUTO?AD.regs:(AP.regions||{});", "const REGS=AUTO?AD.regs:{...(AP.regions||{})};")
a = rep(a, "  const KY=new Set();const regSet", """  if(!AUTO&&Object.keys(regDay).length){const tt=(p,q)=>apTravel(p,q,mode,false);days.forEach((d,i)=>{if(regDay[d]||fixed[d])return;const nb=days.slice(0,i).reverse().find(x=>regDay[x])||days.slice(i+1).find(x=>regDay[x]);let r=nb?regDay[nb]:null;
    const end=i===0?(AP.arrP||"zrh"):i===days.length-1?(AP.depP||AP.arrP||"zrh"):null;if(end){const P=AP_PLACES[end]||AP_PLACES.zrh,er=AP_PLREG[end];if(er&&AP_HUB[er]&&(!r||!AP_HUB[r]||tt(P.g,AP_HUB[r])>100))r=er}
    if(r){regDay[d]=r;REGS[r]=(REGS[r]||0)+1}})}
  const KY=new Set();const regSet""")
a = rep(a, "if(AP.few!==false&&!AUTO){", "if(false){")
a = re.sub(r'   <label>换宿</label><div class="aprow wrap"><button class="fchip\$\{AP\.few.*?</div>\n', '', a, count=1, flags=re.S)
a = rep(a, "    if(!list.length&&pace.max){let best=null;const P=pool();", """    if(!list.length&&pace.max&&AP.ski&&!cx.short){const sk=Object.values(S).filter(x=>!used.has(x.id)&&NODES[x.id].mk==="ski"&&apTravel(B,x.g,mode,x.remote)<=90).sort((p,q)=>apTravel(B,p.g,mode,p.remote)-apTravel(B,q.g,mode,q.remote))[0];if(sk){list.push({...sk,ev:"滑雪一整天"});used.add(sk.id)}}
    if(!list.length&&pace.max){let best=null;const P=pool();""")
a = rep(a, 'baseWhy:AD?"按区域分段住宿，每段住在中心城镇；换住处的日子已预留路上的时间":baseWhy,segs:AD?AD.segs:"",', 'baseWhy:AD||Object.keys(regDay).length?"按区域分段住宿，每段住在中心城镇；换住处的日子已预留路上的时间":baseWhy,segs:AD?AD.segs:(()=>{const nm=d=>AP_SUBLBL[regDay[d]]||AP_HUBN[regDay[d]]||AP_REGIONS[regDay[d]]||"";const o=[];let i=0;while(i<days.length){const n=nm(days[i]);let j=i;while(j+1<days.length&&nm(days[j+1])===n)j++;if(n)o.push(`第${i+1}${j>i?"–"+(j+1):""}天 ${n}`);i=j+1}return o.join(" → ")})(),')
a = rep(a, 'days.forEach((d,i)=>{if(!(plan[d]||[]).length&&', 'days.forEach((d,i)=>{if(!(plan[d]||[]).length&&!(meta[d]&&meta[d].rows.some(r=>r.go))&&')
# ---- 瑞士通票 / 半价卡 标注 ----
a = rep(a, 'function rightPage(n){', """const PSTP={free:"免费",50:"5 折",25:"75 折",part:"部分路段",no:"不适用"},PHF={50:"5 折",part:"部分路段",no:"不适用"};
const pcls=v=>v==="free"?"pf":v==="no"?"pn":"pd";
function passMini(c){const p=c.pass;if(!p)return "";return `<span class="pmini"><i class="${pcls(p[0])}">通票 ${PSTP[p[0]]}</i><i class="${pcls(p[1])}">半价卡 ${PHF[p[1]]}</i></span>`}
function passBadge(n){const p=n.pass;if(!p)return "";return `<div class="passb"><span class="${pcls(p[0])}"><small>瑞士通票</small>${PSTP[p[0]]}</span><span class="${pcls(p[1])}"><small>半价卡</small>${PHF[p[1]]}</span>${p[2]?`<em>${esc(p[2])}</em>`:""}</div>`}
function passTable(){const G=[["观景列车与铁路",n=>n.t.includes("train")||n.t.includes("rail")],["湖船",n=>n.t.includes("boat")],["山地交通",n=>true]];const used=new Set();
  const rows=G.map(([g,f])=>{const L=ORDER.filter(n=>n.pass&&!used.has(n.id)&&f(n));L.forEach(n=>used.add(n.id));return L.length?`<tr class="pg"><th colspan="3">${g}</th></tr>`+L.map(n=>`<tr><td><button class="mylink" data-go="${n.id}">${esc(n.n)}</button></td><td class="${pcls(n.pass[0])}">${PSTP[n.pass[0]]}</td><td class="${pcls(n.pass[1])}">${PHF[n.pass[1]]}</td></tr>`).join(""):""}).join("");
  return `<div class="sec">瑞士通票与半价卡 · 一览</div><div class="mtab"><table class="ptab"><thead><tr><th>线路 / 景点</th><th>瑞士通票</th><th>半价卡</th></tr></thead><tbody>${rows}</tbody></table></div><p class="scnote">「免费」指持瑞士通票不用另外买票（观景列车的座位预订费另付）；「5 折」「75 折」指票价折扣。整理自 Swiss Travel System 和各线路官网，核对于 2026 年 11 月，每年可能调整，以官网为准。</p>`}
function rightPage(n){""")
a = rep(a, '  if(n.t.length)h+=`<div class="chips">${n.t.map(t=>chip(t)).join("")}</div>`;\n  if(n.depth>=1)h+=mineBlock(n);', '  if(n.t.length)h+=`<div class="chips">${n.t.map(t=>chip(t)).join("")}</div>`;\n  h+=passBadge(n);\n  if(n.depth>=1)h+=mineBlock(n);')
a = rep(a, "h+=hotRef(n)+`<p class=\"intro\">${lk(n.d)}</p>`+passBlock(n)", "h+=hotRef(n)+`<p class=\"intro\">${lk(n.d)}</p>`+(n.id===\"transport\"?passTable():\"\")+passBlock(n)")
a = rep(a, '${esc(c.n)}</b><small>${esc(c.d)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`}).join("")}</div>`;', '${esc(c.n)}</b>${passMini(c)}<small>${esc(c.d)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`}).join("")}</div>`;')
a = rep(a, '${mkShape(c,r)}<text class="num"', '${c.col?mkShape(c,r).replace(/class="sh /,`style="fill:${c.col}" class="sh `):mkShape(c,r)}<text class="num"')
a = rep(a, '${P?planSVG(P):n.bg?n.bg.replace("__HY__",HYPSO)+geo:hills+water+rivers+geo}', '${P?planSVG(P):n.bg?rtFocus(n.bg.replace("__HY__",HYPSO),focus)+geo:hills+water+rivers+geo}')
a = rep(a, 'function mkShape(c,r){', 'function rtFocus(b,f){if(!f||!b.includes(`data-rt="${f}"`))return b;const m=b.match(new RegExp(`<path class="rt" data-rt="${f}"[^>]*/>`));return m?b+`<path d="${/ d="([^"]+)"/.exec(m[0])[1]}" fill="none" style="stroke:var(--page)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`+m[0].replace(`class="rt"`,`class="rt on"`):b}\nfunction mkShape(c,r){')
a = rep(a, 'return `<svg class="map${P?" plan":""}" viewBox="0 0 600 440"', 'return `<svg class="map${P?" plan":""}${focus&&n.bg&&n.bg.includes(`data-rt="${focus}"`)?" rtf":""}" viewBox="0 0 600 440"')
a = rep(a, '+passBlock(n)+multiBlock(n)', '+passBlock(n)+trainSights(n)+trainsHere(n)+multiBlock(n)')
a = rep(a, 'function rightPage(n){', """const mtx=m=>m>=60?`约 ${Math.floor(m/60)} 小时${m%60?` ${m%60} 分`:""}`:`约 ${m} 分钟`;
function trainSights(n){if(!n.sights||!n.sights.length)return "";return `<div class="sec">沿途看点</div><ol class="tsights" style="--tc:${n.col||"var(--shu)"}">${n.sights.map(([nm,d,id])=>`<li><b>${id&&NODES[id]?`<button class="mylink" data-go="${id}">${esc(nm)} →</button>`:esc(nm)}</b><span>${esc(d)}</span></li>`).join("")}</ol>`}
function trainsHere(n){if(!n.trn||!n.trn.length)return "";return `<div class="sec">可以乘坐的观景列车</div><ul class="trhere">${n.trn.map(t=>`<li style="--tc:${t.col}"><button class="mylink" data-go="${t.id}">${esc(t.n)}</button><span class="trst">${esc(t.st)}站</span><span class="trgo">${t.go.map(([d,m])=>`→ ${esc(d)}，${mtx(m)}`).join("<br>")}</span></li>`).join("")}</ul><p class="scnote">时间按全程时长和距离估算，实际以时刻表为准；多数观景列车需要预订座位。</p>`}
function rightPage(n){""")
a = rep(a, "const ks=Object.keys(cnt).sort(", "const ks=Object.keys(cnt).filter(k=>!SUBHIDE.has(k)).sort(")
a = rep(a, 'const chip=(k,i)=>`<button class="fchip${FILTER===k?" on":""}${i>=LIM&&FILTER!==k?" extra":""}"', 'const chip=(k,i)=>`<button class="fchip${fBase()===k?" on":""}${i>=LIM&&fBase()!==k?" extra":""}"')
a = rep(a, """${more?`<button class="fmore" data-fmore="1">${FBAR_OPEN?"收起 ▴":`更多 ${ks.length-LIM} ▾`}</button>`:""}</div>`;""", """${more?`<button class="fmore" data-fmore="1">${FBAR_OPEN?"收起 ▴":`更多 ${ks.length-LIM} ▾`}</button>`:""}</div>${subBar(pool)}`;""")
for bad in ["京都", "关西", "kyoto-", "食べログ"]:
    if bad in a: print("WARN app still contains", bad, [m.start() for m in re.finditer(bad, a)][:5])

# ---------------- body / head / tail ----------------
SEAL = '<span class="seal"><svg aria-hidden="true" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#C4432B"/><path d="M8 78 L34 40 L46 56 L60 30 L92 78 Z" fill="#fff" opacity=".95"/><path d="M52 44 L60 30 L68 44 L63 41 L60 46 L56 41 Z" fill="#C4432B" opacity=".55"/><rect x="45" y="12" width="10" height="26" rx="1.5" fill="#fff"/><rect x="37" y="20" width="26" height="10" rx="1.5" fill="#fff"/><rect x="14" y="84" width="72" height="3" rx="1.5" fill="#fff" opacity=".8"/></svg></span>'
b = body
b = re.sub(r'<span class="seal">.*?</span>', lambda m: SEAL, b, count=1, flags=re.S)
b = b.replace("京都旅行手帖", "瑞士旅行手帖").replace("京都旅游", "瑞士旅游")
b = rep(b, '<button class="btn" id="tocBtn">目录</button>', '<button class="btn back" id="backBtn" disabled aria-label="回到刚才浏览的页面">‹ 返回</button><button class="btn" id="tocBtn">目录</button>')
b = rep(b, "搜索景点或标签，如 清水寺、佛寺、跨年", "搜索景点或标签，如 少女峰、齿轨铁路、滑雪季")
h = head
h = rep(h, "京都及周边互动旅行电子书：插画地图、标签筛选、搜索与我的标签，可离线阅读。", "瑞士及周边互动旅行电子书：地图、时令与体力标签、搜索、我的标签与自动行程，可离线阅读。")
h = rep(h, '<meta name="apple-mobile-web-app-title" content="京都手帖">', '<meta name="apple-mobile-web-app-title" content="瑞士手帖">')
import urllib.parse as _up
FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"] + sorted("img/" + _up.quote(f) for f in os.listdir("/home/claude/swiss/site/img") if f.endswith(".webp"))
t = tail
t = rep(t, "const N=379,", f"const N={len(FILES)},")
t = rep(t, 'k.startsWith("kyoto-techo-")', 'k.startsWith("swiss-techo-")')
t = rep(t, 'localStorage.getItem("kyoto-offline")', 'localStorage.getItem("swiss-offline")')
t = rep(t, 'localStorage.setItem("kyoto-offline",String(N))', 'localStorage.setItem("swiss-offline",String(N))')
import re as _re
_i = t.index('<script>if("serviceWorker"'); _j = t.index('</script>', _i) + len('</script>')
t = t[:_i] + """<script>if("serviceWorker" in navigator&&/^https?:/.test(location.protocol)){addEventListener("load",()=>{
 const t=document.createElement("div");t.id="offst";t.style.cssText="position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:40;background:#1F2B45;color:#fff;font:13px/1.4 system-ui,sans-serif;padding:7px 14px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:opacity .4s;pointer-events:none;white-space:nowrap";t.hidden=true;document.body.appendChild(t);
 const hide=(ms)=>setTimeout(()=>{t.style.opacity=0;setTimeout(()=>t.hidden=true,500)},ms);
 navigator.serviceWorker.register("sw.js").then(()=>{let last=-1,still=0,tries=0;const N=__N__;
  const ck=async()=>{try{tries++;const ks=(await caches.keys()).filter(k=>k.startsWith("swiss-techo-"));let n=0,ok=false;
   for(const k of ks){const c=await caches.open(k);if(await c.match("__offline_done__"))ok=true;n=Math.max(n,(await c.keys()).length)}
   let done=false;try{done=localStorage.getItem("swiss-offline")===CACHEV}catch(e){}
   if(ok){if(!done){t.textContent="✓ 已下载完成，断网也能使用";t.hidden=false;t.style.opacity=1;hide(4000);try{localStorage.setItem("swiss-offline",CACHEV)}catch(e){}}else{t.hidden=true}return}
   if(n===last)still++;else{still=0;last=n}
   if(still>=24||tries>200){if(!done){t.textContent="离线内容未能全部下载，联网时可正常使用";t.hidden=false;hide(5000)}return}
   if(!done&&tries>1){t.hidden=false;t.style.opacity=1;t.textContent="正在下载离线内容 "+Math.min(n,N)+" / "+N+"，请保持联网…"}
   setTimeout(ck,2500)}catch(e){t.hidden=true}};setTimeout(ck,1500)}).catch(()=>{});
 const CACHEV=__CV__;})}</script>""" + t[_j:]

# ---------------- css additions ----------------
css = css.rstrip()
assert css.endswith("</style>")
css = css[:-len("</style>")] + """
.sc-ski{background:#6f9cc8}.sc-hike{background:#6c8a4a}.sc-autumn{background:#d4902f}.sc-xmas{background:#b23a3a}
.tag.easy{border-color:#9fbf88;color:#4e6f35}.tag.moderate{border-color:#e0b468;color:#8a5f12}.tag.hard{border-color:#d78a7a;color:#9a3a26}
.cover-img svg.map{width:100%;height:auto;border-radius:10px;display:block}
svg.map .mk .sh{stroke:var(--page);stroke-width:3}svg.map .sh.ski{fill:#2f6db5}svg.map .sh.hike{fill:#3f7a34}svg.map .sh.mtn{fill:#6d5a99}svg.map .sh.out{fill:#5f8a3a}svg.map .sh.town{fill:#b0763a}svg.map .sh.old{fill:#8e3b46}
svg.map .pk{font:600 11.5px var(--f-body);fill:var(--ink-2);paint-order:stroke;stroke:var(--halo);stroke-width:3.5px;stroke-linejoin:round}
svg.map .pk .el{font:500 10px var(--f-mono);fill:var(--muted)}svg.map .pkm{fill:#7b6a55;stroke:var(--halo);stroke-width:1.2}
svg.map .tstop{font:600 12px var(--f-body);fill:var(--ink);paint-order:stroke;stroke:var(--halo);stroke-width:4px;stroke-linejoin:round}svg.map .tstop.big{font:700 14px var(--f-body)}
svg.map.rtf .rt{opacity:.28}svg.map .rt.on{opacity:1;stroke-width:6.5px}
svg.map .tn{font:500 11.5px var(--f-body);fill:var(--ink);paint-order:stroke;stroke:var(--halo);stroke-width:3.5px;stroke-linejoin:round}
svg.map .tnm{fill:var(--page);stroke:var(--ink);stroke-width:1.6}svg.map .tn .el{font:500 10px var(--f-mono);fill:var(--muted)}svg.map .psm{fill:none;stroke:var(--ink);stroke-width:1.6}
svg.map .sbar text{font:10px var(--f-mono);fill:var(--ink-2);paint-order:stroke;stroke:var(--halo);stroke-width:3px}
svg.map .tst text,svg.map .twp text,svg.map .lfn text{font:700 11px var(--f-body);text-anchor:middle;dominant-baseline:central}
svg.map .tst text{fill:#fff}svg.map .lfn circle{fill:var(--ink);stroke:var(--page);stroke-width:1.5}svg.map .lfn text{fill:var(--page);font-size:10px}
svg.map .tsl{font:700 13px var(--f-display);fill:var(--ink);paint-order:stroke;stroke:var(--halo);stroke-width:4px;stroke-linejoin:round}
svg.map .tse{font:500 10.5px var(--f-mono);fill:var(--ink-2);paint-order:stroke;stroke:var(--halo);stroke-width:3px;stroke-linejoin:round}
.maplg{display:flex;flex-wrap:wrap;gap:3px 14px;margin:8px 2px 6px;font-size:12px;line-height:1.5;color:var(--ink-2)}
.maplg b{font:600 11px var(--f-mono);letter-spacing:.08em;color:var(--muted);margin-right:2px}.maplg span{display:inline-flex;align-items:center;gap:5px}
.tm{margin:0 0 18px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.tmh{display:flex;flex-direction:column;gap:2px;margin:2px 0 8px}.tmh b{font:700 18px var(--f-display);color:var(--ink)}.tmh small{color:var(--ink-2);font-size:12.5px}
svg.tmprof{width:100%;height:auto;display:block;border:1px solid var(--line);border-top:0;border-radius:0 0 4px 4px}
svg.tmprof .pf{font:10px var(--f-mono);fill:var(--muted)}
.tml{list-style:none;padding:0;margin:8px 0;columns:2;column-gap:18px;font-size:13px}
.tml li{break-inside:avoid;padding:3px 0;display:flex;gap:7px;align-items:baseline}
.tml li span{flex:1}.tml b{flex:none;display:inline-grid;place-items:center;min-width:22px;height:20px;border-radius:10px;border:2px solid #3f7a34;color:#3f7a34;font:700 10.5px var(--f-body);padding:0 2px;box-sizing:border-box}
.tml b.se{background:#3f7a34;color:#fff}.tm.ski .tml b{border-color:#2f6db5;color:#2f6db5}.tm.ski .tml b.se{background:#2f6db5;color:#fff}
.tml i,.tml2 i{color:var(--muted);font-style:italic}.tml small,.tml2 small{color:var(--muted);font-family:var(--f-mono);white-space:nowrap}
.tml2{display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:13px;margin:8px 0}
.tml2 ol,.tml2 ul{margin:4px 0;padding-left:0;list-style:none}.tml2 li{padding:2px 0}
.tml2 ol b{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:9px;background:var(--ink);color:var(--page);font:700 10px var(--f-mono);margin-right:5px}
.tmnote{font-size:11.5px;color:var(--muted);margin:6px 0 0}
ol.hot{list-style:none;padding:0;margin:8px 0 6px}ol.hot li{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0;background:var(--page)}
.hh{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px}.hr{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:11px;background:var(--shu);color:#fff;font:700 12px var(--f-mono)}
.hn{font:700 16px var(--f-display);color:var(--ink)}.hsc{margin-left:auto;font:11px var(--f-mono);color:var(--shu);letter-spacing:.5px}
.ho{font-size:12.5px;color:var(--muted);font-style:italic;margin:2px 0 0 30px}.hst{font-size:13.5px;color:var(--ink-2);margin:4px 0 0 30px}
.hwarn{margin:6px 0 0 30px;font-size:13px;color:#9a3a26}.hsrc{margin:6px 0 0 30px;font-size:12.5px;line-height:1.7}.hsrc summary{cursor:pointer;color:var(--ink-2)}.hsrc a{color:var(--ink-2)}.hsrc i{color:var(--muted);font-style:normal;font-family:var(--f-mono);font-size:11.5px}
ol.hot .mylink{margin:6px 0 0 30px}
svg .stg{fill:none;stroke:transparent;stroke-width:14;stroke-linecap:round;stroke-linejoin:round;cursor:pointer;pointer-events:stroke}svg .stg:hover{stroke:rgba(242,194,0,.35)}svg .stg.on{stroke:rgba(242,194,0,.8)}
svg .pstg{fill:transparent;cursor:pointer}svg .pstg:hover{fill:rgba(242,194,0,.15)}svg .pstg.on{fill:rgba(242,194,0,.38)}svg .pstl{display:none;font:600 10px var(--f-body);fill:var(--ink)}svg .pstl.on{display:block}
tr.stgrow{cursor:pointer}tr.stgrow:hover td{background:rgba(242,194,0,.12)}tr.stgrow.on td{background:rgba(242,194,0,.32)}
.mmap{margin:8px 0}
details.multi{border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:8px 0;background:var(--page)}details.multi summary{cursor:pointer;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}details.multi summary b{font:700 16px var(--f-display);color:var(--ink)}details.multi summary span{font-size:12.5px;color:var(--muted)}
.msum{font-size:14px;line-height:1.75;margin:8px 0}.mtab{overflow-x:auto;margin:6px 0}.mtab table{border-collapse:collapse;font-size:12.5px;min-width:560px;width:100%}.mtab th{text-align:left;font-weight:600;color:var(--muted);border-bottom:1px solid var(--line);padding:4px 6px;white-space:nowrap}.mtab td{border-bottom:1px dashed var(--line);padding:5px 6px;vertical-align:top}.mtab td:first-child{font:700 12px var(--f-mono);color:var(--shu)}.mtab td:nth-child(3),.mtab td:nth-child(4){font-family:var(--f-mono);white-space:nowrap}.mtab small{color:var(--muted)}
.mplans{font-size:13.5px;line-height:1.7;margin:8px 0}.mplans ol{margin:4px 0;padding-left:1.4em}.mplans li{margin:4px 0}
dl.stay{margin:6px 0;font-size:14px;line-height:1.75}dl.stay dt{font-weight:700;color:var(--ink-2);font-size:12.5px;margin-top:6px}dl.stay dd{margin:2px 0 0}
.hotref{background:rgba(196,67,43,.07);border-left:3px solid var(--shu);padding:7px 10px;font-size:13px;margin:8px 0;border-radius:0 6px 6px 0}.hotref .mylink{margin-left:6px}
.buy{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}.buybtn{display:inline-block;padding:7px 13px;border:1px solid var(--shu);color:var(--shu);border-radius:999px;font-size:13.5px;text-decoration:none;background:var(--page)}.buybtn:hover{background:var(--shu);color:#fff}
ol.notes{margin:6px 0 4px;padding-left:1.4em;font-size:14px;line-height:1.75}ol.notes li{margin:3px 0}
.og{color:var(--muted);font-style:italic;font-size:.9em;letter-spacing:.01em}
@media(max-width:640px){.tml{columns:1}.tml2{grid-template-columns:1fr}}
.zw{position:relative}
.zw>svg.map{touch-action:pan-x pan-y;cursor:zoom-in;user-select:none;-webkit-user-select:none}
.zw>svg.map.zoomed{touch-action:none;cursor:grab}
.zw>svg.map.zoomed:active{cursor:grabbing}
svg.map.zoomed .sbar{display:none}
svg.map.zoomed path,svg.map.zoomed circle,svg.map.zoomed line,svg.map.zoomed polyline,svg.map.zoomed ellipse,svg.map.zoomed rect{vector-effect:non-scaling-stroke}
svg.map.zoomed g.mk,svg.map.zoomed text,svg.map.zoomed .tnm,svg.map.zoomed .pkm,svg.map.zoomed .psm{transform-box:view-box;transform-origin:0 0}
.zc{position:absolute;right:8px;top:8px;display:flex;flex-direction:column;gap:4px;z-index:2}
.zc button{width:30px;height:30px;border-radius:7px;border:1px solid var(--line,#ccc);background:var(--paper,#fff);color:var(--ink,#222);font:600 17px/1 system-ui,sans-serif;cursor:pointer;opacity:.88;box-shadow:0 1px 3px rgba(0,0,0,.15);padding:0}
.zc button:hover{opacity:1}
.zc .bmb{font-size:15px}
.passb{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 4px}
.passb span{display:inline-flex;flex-direction:column;padding:4px 10px;border-radius:8px;font-weight:700;font-size:14px;line-height:1.2}
.passb span small{font-weight:500;font-size:10.5px;opacity:.75}
.passb em{font-style:normal;font-size:12px;color:var(--muted)}
.pf{background:#E3F0DC;color:#2F6420}.pd{background:#FBEFD6;color:#8A5A0E}.pn{background:#EEE;color:#777}
.pmini{display:inline-flex;gap:4px;margin-left:6px;vertical-align:1px}.pmini i{font-style:normal;font-size:10.5px;padding:1px 6px;border-radius:5px;font-weight:600}
.ptab td.pf,.ptab td.pd,.ptab td.pn{font-weight:700;text-align:center;font-size:13px}.ptab tr.pg th{text-align:left;padding-top:12px;font-size:12px;color:var(--muted)}
.tsights{list-style:none;counter-reset:ts;padding:0;margin:8px 0 14px;border-left:3px solid var(--tc);padding-left:16px}
.tsights li{counter-increment:ts;position:relative;margin:0 0 12px;line-height:1.6}
.tsights li::before{content:"";position:absolute;left:-23px;top:7px;width:11px;height:11px;border-radius:50%;background:var(--page);border:2.5px solid var(--tc)}
.tsights li:first-child::before,.tsights li:last-child::before{background:var(--tc);border-color:var(--page);box-shadow:0 0 0 1.5px var(--tc)}
.tsights b{display:block;font-size:15px}.tsights span{color:var(--ink-2);font-size:14px}
.trhere{list-style:none;padding:0;margin:8px 0}.trhere li{display:grid;grid-template-columns:auto 1fr;column-gap:10px;row-gap:2px;padding:9px 0 9px 12px;border-left:4px solid var(--tc);margin-bottom:8px;background:rgba(0,0,0,.02);border-radius:0 6px 6px 0}
.trhere .mylink{font-weight:700;font-size:15px}.trhere .trst{color:var(--muted);font-size:13px;align-self:center}.trhere .trgo{grid-column:1 / -1;font-size:14px;color:var(--ink-2)}
.mtab table.ptab{min-width:0;width:100%;table-layout:fixed}.ptab th:first-child,.ptab td:first-child{width:46%;text-align:left;white-space:normal}.ptab td .mylink{white-space:normal;text-align:left;line-height:1.35}
@media(max-width:760px){.crumbs{flex-wrap:wrap!important;overflow-x:visible!important;white-space:normal!important;row-gap:0}
.mtab table:not(.ptab){min-width:0}.mtab table:not(.ptab) thead{display:none}
.mtab table:not(.ptab) tr{display:grid;grid-template-columns:2.4em 1fr;column-gap:8px;padding:8px 0;border-bottom:1px dashed var(--line)}
.mtab table:not(.ptab) td{display:block;border:0;padding:1px 0;white-space:normal!important;grid-column:2}
.mtab table:not(.ptab) td:first-child{grid-column:1;grid-row:1 / span 6}
.mtab table:not(.ptab) td:empty{display:none}
.mtab table:not(.ptab) td:nth-child(3)::before{content:"距离 ";font-family:var(--f-body);color:var(--muted)}.mtab table:not(.ptab) td:nth-child(3)::after{content:" km"}
.mtab table:not(.ptab) td:nth-child(4)::before{content:"爬升 / 下降 ";font-family:var(--f-body);color:var(--muted)}.mtab table:not(.ptab) td:nth-child(4)::after{content:" m"}
.mtab table:not(.ptab) td:nth-child(5)::before{content:"最高点 ";color:var(--muted)}
.mtab table:not(.ptab) td:nth-child(6)::before{content:"缩短与交通 ";color:var(--muted)}}
@media(max-width:520px){.ptab td.pf,.ptab td.pd,.ptab td.pn{font-size:12px;padding-left:2px;padding-right:2px}}
.fsub{display:flex;flex-wrap:wrap;gap:6px 14px;margin:-4px 0 10px;padding:7px 10px;border-radius:8px;background:rgba(0,0,0,.035)}
.fsub .fsg{display:flex;flex-wrap:wrap;gap:5px;align-items:center}
.fsub .fsg b{font:600 11px var(--f-mono,monospace);color:var(--muted);margin-right:2px}
.fchip.sub{font-size:12px;padding:3px 9px}
.zw .bmtip{position:absolute;right:46px;top:8px;background:rgba(30,30,30,.82);color:#fff;font:12px/1.4 system-ui,sans-serif;padding:5px 9px;border-radius:6px;opacity:0;transition:opacity .25s;pointer-events:none;z-index:3}
.zw .bmtip.on{opacity:1}
svg.map .bmattr{fill:#333;text-anchor:start;paint-order:stroke;stroke:#fff;stroke-width:3px;font-family:system-ui,sans-serif}
svg.map.bmon g.tiles image{opacity:.93}
.zc button[data-z=reset]{font-size:14px}
.zw:not(.zoomed) .zc button[data-z=out],.zw:not(.zoomed) .zc button[data-z=reset]{opacity:.35}
@media print{.zc{display:none}}
.vias{display:flex;flex-direction:column;gap:4px;margin:4px 0 8px}.vias small{color:var(--muted)}
.lmnear{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.lmnear button{border:1px solid var(--line);background:var(--page);border-radius:99px;padding:3px 10px;font-size:12px;cursor:pointer;color:var(--ink)}
svg.map g.lmk{cursor:pointer}svg.map g.lmk text{font-size:12px;paint-order:stroke;stroke:var(--halo);stroke-width:3px;fill:var(--ink)}svg.map g.lmk.me text{font-weight:700;font-size:14px}
.archp{line-height:1.85;color:var(--ink-2);margin:4px 0 6px}
.pmlg{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px}.pmlg button{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--page);color:var(--ink);border-radius:99px;padding:3px 10px;font-size:12px;cursor:pointer}.pmlg i{width:10px;height:10px;border-radius:50%;display:inline-block}
svg.map g.pmk{cursor:pointer}svg.map.planall .regions{opacity:.4}svg.map.planall{margin-top:6px}
.btn.back[disabled]{opacity:.38;cursor:default}
@media (max-width:860px){#backBtn{display:none}}

</style>
"""

# ---------------- fonts ----------------
alltext = a + b + h + data + css
chars = set(c for c in alltext if ord(c) > 0x7F)
chars |= set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ·–—…“”‘’（）《》「」、。，：；！？%/+-")
open("/home/claude/swiss/out/chars.txt", "w").write("".join(sorted(chars)))
def subset(src, out, extra=[], tf="/home/claude/swiss/out/chars.txt"):
    subprocess.run(["pyftsubset", src, f"--text-file={tf}", f"--output-file={out}", "--flavor=woff", "--layout-features=*"] + extra, check=True)
    return base64.b64encode(open(out, "rb").read()).decode()
open("/home/claude/swiss/out/msz.txt","w").write("瑞士旅行手帖京都")
msz = subset("/home/claude/fonts/MaShanZheng-Regular.ttf", "/home/claude/swiss/out/msz.woff", tf="/home/claude/swiss/out/msz.txt")
nss = subset("/home/claude/fonts/NotoSerifSC[wght].ttf", "/home/claude/swiss/out/nss.woff")
FONTCSS = ("<style>\n/* Fonts: Ma Shan Zheng (c) The Ma Shan Zheng Project Authors; Noto Serif SC (c) Adobe & Google. All licensed under the SIL Open Font License 1.1 (https://openfontlicense.org). Subsetted for this book. */\n"
  f'@font-face{{font-family:"Ma Shan Zheng";src:url(data:font/woff;base64,{msz}) format("woff");font-weight:400;font-style:normal;font-display:swap}}\n'
  f'@font-face{{font-family:"Noto Serif SC";src:url(data:font/woff;base64,{nss}) format("woff");font-weight:600 900;font-style:normal;font-display:swap}}\n')
assert css.lstrip().startswith("<style>")
css_body = css.lstrip()[len("<style>"):]
a_body = re.sub(r"<[/a-z]*$", "", a.lstrip()[len("<script>"):].rstrip()) + "\n</script>\n"
html = h + FONTCSS + css_body + b + "<script>\n" + data + "</script>\n" + "<script>" + a_body + t
html = html.replace("<title>京都旅行手帖</title>", "<title>瑞士旅行手帖</title>")
for bad in ["京都"]:
    idx = [m.start() for m in re.finditer(bad, html)]
    if idx: print("WARN html contains", bad, len(idx), [html[i-40:i+20] for i in idx[:4]])
D = "/home/claude/swiss/site"; os.makedirs(D, exist_ok=True)
html = html.replace("__N__", str(len(FILES))).replace("__CV__", json.dumps(str(len(FILES))))
open(D + "/index.html", "w", encoding="utf-8").write(html)
ver = hashlib.sha1(html.encode()).hexdigest()[:10]
open(D + "/sw.js", "w").write(f'const CACHE="swiss-techo-{ver}";const FILES={json.dumps(FILES)};\n' + '''self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(async c=>{let i=0;const one=async f=>{try{const r=await fetch(f,{cache:"reload"});if(r.ok)await c.put(f,r)}catch(_){}};const q=[...FILES];await Promise.all([0,1,2,3,4,5].map(async()=>{while(q.length)await one(q.shift())}));await c.put("__offline_done__",new Response("1"))}));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!=="swiss-tiles").map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);if(u.host==="wmts.geo.admin.ch"||u.host==="tile.openstreetmap.org"){e.respondWith(caches.open("swiss-tiles").then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==="opaque")c.put(r,res.clone());return res}))));return}if(u.origin!==location.origin)return;
  if(r.mode==="navigate"){e.respondWith(fetch(r).then(res=>{const c=res.clone();caches.open(CACHE).then(x=>x.put("index.html",c));return res}).catch(()=>caches.match("index.html")));return}
  e.respondWith(caches.match(r).then(m=>m||fetch(r)))});
''')
man = {"name": "瑞士旅行手帖", "short_name": "瑞士手帖", "description": "瑞士及周边互动旅行电子书", "start_url": "./", "scope": "./", "display": "standalone",
  "background_color": "#E3E5DC", "theme_color": "#E3E5DC", "lang": "zh-Hans",
  "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
open(D + "/manifest.webmanifest", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1))
print("index.html", len(html), "chars", len(chars), "msz", len(msz), "nss", len(nss))
