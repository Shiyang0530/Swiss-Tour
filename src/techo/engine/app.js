<script>
(()=>{
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
(function merge(n){if(typeof DEEP!=="undefined"&&DEEP[n.id])Object.assign(n,DEEP[n.id]);(n.c||[]).forEach(merge)})(BOOK);
const NODES={},ORDER=[],PATH={};
(function walk(n,p,depth,folders,underKyoto){
  n.parent=p;n.depth=depth;n.c=n.c||[];n.t=n.t||[];
  const fs=depth===0?[]:[...folders,n.f||n.n];n.folders=fs;n.disp=CFG.feat.disp?(depth===0?[]:[...(p&&p.disp||[]),n.n]):fs;n.key=fs.join("/");PATH[n.key]=n;
  const uk=underKyoto||(CFG.kindSplit||[]).includes(n.id);
  n.kind=depth===0?"总览":n.kd?n.kd:depth===1?"地区":(uk?["","","区域","景点","看点"][depth]:["","","景点","看点"][depth]);
  NODES[n.id]=n;n.page=ORDER.push(n);
  n.c.forEach(c=>walk(c,n,depth+1,fs,uk));
})(BOOK,null,0,[],false);
const total=ORDER.length;
const TAG_PARENT=CFG.TAG_PARENT||{};
const TAG_KIDS={};Object.entries(TAG_PARENT).forEach(([c,p])=>(TAG_KIDS[p]=TAG_KIDS[p]||[]).push(c));
const DESC=k=>[k,...(TAG_KIDS[k]||[]).flatMap(DESC)];
const hasTag=(n,k)=>DESC(k).some(x=>n.t.includes(x));
const TAGCOUNT={};Object.keys(TAGS).forEach(k=>{const c=ORDER.filter(n=>hasTag(n,k)).length;if(c)TAGCOUNT[k]=c});
const pg=n=>String(n).padStart(3,"0");
/* ---------- glossary ---------- */
const CIMG=typeof CARDIMG!=="undefined"?CARDIMG:{};
const TERMS_=typeof TERMS!=="undefined"?TERMS:{},SRCS=typeof SRC!=="undefined"?SRC:{};
const TALIAS=[];Object.entries(TERMS_).forEach(([id,t])=>{if(!t.nl)t.a.forEach(a=>TALIAS.push([a,id]))});TALIAS.sort((a,b)=>b[0].length-a[0].length);
const TMAP=Object.fromEntries(TALIAS);
const TRE=TALIAS.length?new RegExp(TALIAS.map(x=>x[0].replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|"),"g"):null;
const TCATS=[...new Set(Object.values(TERMS_).map(t=>t.k))];
let SEEN=null;
const OGR=CFG.feat.og?'<span class="og">（$1）</span>':'（$1）';const OGRE=/（([A-Za-zÀ-ž0-9'’.\-\/&;#, ]+?)）/g;function lk(s){const e=esc(s);if(!SEEN||!TRE)return e.replace(OGRE,OGR);return e.replace(TRE,m=>{const id=TMAP[m];if(SEEN.has(id))return m;SEEN.add(id);return `<button class="term" data-term="${id}">${m}</button>`}).replace(OGRE,OGR)}
const nodeText=n=>[n.d,n.tip,...(n.hl||[]),...(n.hist||[]).map(x=>x[1]),...(n.arch||[]).map(x=>x[1]),...(n.cards||[]).flatMap(c=>[c.h,c.p])].filter(Boolean).join("\n");
const BACK={};if(TRE)ORDER.forEach(n=>{new Set(nodeText(n).match(TRE)||[]).forEach(m=>{const id=TMAP[m];(BACK[id]=BACK[id]||[]);if(!BACK[id].includes(n))BACK[id].push(n)})});
const srcOf=n=>n.src?n.src:(n.parent&&n.parent.src&&!n.c.length?n.parent.src:null);
function srcBlock(n){const s=srcOf(n);if(!s)return"";return `<div class="srcs"><span class="eyebrow">资料来源</span><ol>${s.map(k=>{const v=SRCS[k];return v?`<li><a href="${esc(v[1])}" target="_blank" rel="noopener">${esc(v[0])}</a></li>`:""}).join("")}</ol><p>内容依据以上资料整理；开放时间、票价和公开日期以官方发布为准。</p></div>`}

/* ---------- images (IndexedDB, per browser) ---------- */
const IMG={};
function dbOpen(){return new Promise((res,rej)=>{try{const r=indexedDB.open((CFG.id+"-book"),1);r.onupgradeneeded=()=>r.result.createObjectStore("img");r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)}catch(e){rej(e)}})}
function nodeForDir(segs){
  for(let i=0;i<segs.length;i++){const k=segs.slice(i).join("/");if(k&&PATH[k])return PATH[k]}
  return segs.length===1?BOOK:null;
}
function addImg(rel,blob){
  const segs=rel.split("/").slice(0,-1);const n=nodeForDir(segs);if(!n)return false;
  (IMG[n.id]=IMG[n.id]||[]).push({name:rel,url:URL.createObjectURL(blob)});return true;
}
function sortImgs(){Object.values(IMG).forEach(a=>a.sort((x,y)=>x.name.localeCompare(y.name,"zh")))}
async function loadStored(){
  try{const db=await dbOpen();const tx=db.transaction("img");const st=tx.objectStore("img");
    const [keys,vals]=await Promise.all([req(st.getAllKeys()),req(st.getAll())]);
    keys.forEach((k,i)=>addImg(k,vals[i]));sortImgs();if(keys.length)render(cur,false);
  }catch(e){}
}
const req=r=>new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});
$("#dirInput").addEventListener("change",async e=>{
  const files=[...e.target.files].filter(f=>(/^image\//.test(f.type)||/\.(jpe?g|png|webp|gif|avif)$/i.test(f.name))&&!/map|地图/i.test(f.name));
  Object.keys(IMG).forEach(k=>delete IMG[k]);
  let ok=0;files.forEach(f=>{if(addImg(f.webkitRelativePath||f.name,f))ok++});sortImgs();
  $("#imgStatus").textContent=`已匹配 ${ok} 张图片（共 ${files.length} 张）`;
  render(cur,false);
  try{const db=await dbOpen();const tx=db.transaction("img","readwrite");const st=tx.objectStore("img");st.clear();
    files.forEach(f=>st.put(f,f.webkitRelativePath||f.name));}catch(err){$("#imgStatus").textContent+="，本次未能保存到浏览器"}
});
$("#clearImg").onclick=async()=>{Object.keys(IMG).forEach(k=>delete IMG[k]);try{const db=await dbOpen();db.transaction("img","readwrite").objectStore("img").clear()}catch(e){}
  $("#imgStatus").textContent="已清除";render(cur,false)};

/* ---------- map rendering ---------- */
function seed(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619);return()=>((h=Math.imul(h^h>>>15,2246822507)^Math.imul(h^h>>>13,3266489909))>>>0)/4294967296}
const ENGINES={google:["Google","https://www.google.com/search?q="],bing:["Bing","https://www.bing.com/search?q="],baidu:["百度","https://www.baidu.com/s?wd="],yahoojp:["Yahoo! JAPAN","https://search.yahoo.co.jp/search?p="],duck:["DuckDuckGo","https://duckduckgo.com/?q="]};(CFG.engines_off||[]).forEach(k=>delete ENGINES[k]);
let ENGINE="google";try{const e=localStorage.getItem((CFG.id+"-engine"));if(e&&ENGINES[e])ENGINE=e}catch(err){}
const searchURL=n=>ENGINES[ENGINE][1]+encodeURIComponent(ENGINE==="baidu"?n.n:(n.ja||n.n).split("（")[0]);
const PRESET=["收藏","想去","已去过"];
let PLAN={};try{PLAN=JSON.parse(localStorage.getItem((CFG.id+"-plan"))||"{}")||{}}catch(e){PLAN={}}
const savePlan=()=>{Object.keys(PLAN).forEach(d=>{PLAN[d]=(PLAN[d]||[]).filter(id=>NODES[id]);if(!PLAN[d].length)delete PLAN[d]});try{localStorage.setItem((CFG.id+"-plan"),JSON.stringify(PLAN))}catch(e){};try{pvSync()}catch(e){}};
const planDates=()=>Object.keys(PLAN).sort();
const datesOf=id=>planDates().filter(d=>PLAN[d].includes(id));
const WK="日一二三四五六";
const fmtD=(d,long)=>{const t=new Date(d+"T00:00:00");if(isNaN(t))return d;const s=(t.getMonth()+1)+"月"+t.getDate()+"日";return long?t.getFullYear()+"年"+s+" 周"+WK[t.getDay()]:s};
const dayNo=d=>planDates().indexOf(d)+1;
let LASTDATE="";try{LASTDATE=localStorage.getItem((CFG.id+"-plan-last"))||""}catch(e){}
/* ===== 旅行计划多版本 ===== */
let PV={cur:"",v:{}};
try{PV=JSON.parse(localStorage.getItem((CFG.id+"-plans"))||"null")||PV}catch(e){}
if(!PV.v)PV={cur:"",v:{}};
const pvSave=()=>{try{localStorage.setItem((CFG.id+"-plans"),JSON.stringify(PV))}catch(e){}};
const pvNew=(name,plan,meta,opt)=>{const id="v"+Date.now().toString(36);PV.v[id]={name,ts:Date.now(),plan:JSON.parse(JSON.stringify(plan||{})),meta:meta||{},opt:opt||null};PV.cur=id;pvSave();return id};
if(!PV.cur||!PV.v[PV.cur]){const ks=Object.keys(PV.v);if(ks.length)PV.cur=ks[0];else pvNew("我的行程",PLAN);}
function pvSync(){if(PV.v[PV.cur]){PV.v[PV.cur].plan=JSON.parse(JSON.stringify(PLAN));pvSave()}}
function pvSwitch(id){if(!PV.v[id])return;PV.cur=id;PLAN=JSON.parse(JSON.stringify(PV.v[id].plan||{}));savePlan();pvSave()}
const pvMeta=()=>(PV.v[PV.cur]&&PV.v[PV.cur].meta)||{};

/*@@PLANNER@@*/function pvBar(){const ks=Object.keys(PV.v);return `<div class="pvbar"><label>行程版本</label><select id="pv-sel">${ks.map(k=>`<option value="${k}"${k===PV.cur?" selected":""}>${esc(PV.v[k].name)}</option>`).join("")}</select>
  <div class="aprow wrap"><button class="btn sm pri" data-route="autoplan">✨ 自动生成行程</button><button class="btn sm" data-pvdup="1">复制为新版本</button><button class="btn sm" data-pvnew="1">新建空白版本</button><button class="btn sm" data-pvren="1">重命名</button><button class="btn sm${SH_OPEN?" on":""}" data-shopen="1">📤 分享行程</button>${ks.length>1?`<button class="btn sm" data-pvdel="1">${PV_DEL?"再点一次确认删除":"删除此版本"}</button>`:""}</div>
  ${shareBox()}${PV_REN?`<div class="aprow"><input id="pv-name" value="${esc(PV.v[PV.cur].name)}" maxlength="40"><button class="btn sm pri" data-pvrenok="1">确定</button></div>`:""}</div>`}
let PV_DEL=false,PV_REN=false;
document.addEventListener("focusin",e=>{const el=e.target;if(el.dataset&&(el.dataset.apaddin||el.dataset.plaaddin))setTimeout(()=>{try{el.scrollIntoView({block:"start",behavior:"smooth"})}catch(_){}},300)});
document.addEventListener("input",e=>{const el=e.target;if(el.dataset&&el.dataset.plaaddin){const d=el.dataset.plaaddin,box=document.querySelector(`[data-apsug="p${d}"]`);if(!box)return;
  box.innerHTML=apSugg(el.value,true).map(id=>{const N=NODES[id],has=PLAN[d].includes(id),other=planDates().filter(k=>k!==d&&PLAN[k].includes(id)).map(k=>"第"+dayNo(k)+"天");return `<button data-plaaddid="${d}|${id}"${has?" disabled":""}><b>${esc(N.n)}</b><small>${esc(N.disp.slice(0,-1).join(" › "))}${has?" · 已在这一天":other.length?" · 也在"+other.join("、"):""}</small></button>`}).join("")||(el.value.trim()?'<p class="scnote">没有找到匹配的景点</p>':"");return}
  if(!el.dataset||!el.dataset.apaddin)return;const d=el.dataset.apaddin;const box=document.querySelector(`[data-apsug="${d}"]`);if(!box)return;
  const used=new Set(Object.values(AP_RES?AP_RES.plan:{}).flat());
  box.innerHTML=apSugg(el.value).map(id=>{const where=Object.keys(AP_RES.plan).find(k=>AP_RES.plan[k].includes(id));return `<button data-apaddid="${d}|${id}"><b>${esc(NODES[id].n)}</b><small>${esc(NODES[id].ja||"")}${where?` · 已在第${AP_RES.days.indexOf(where)+1}天，点选会移到这天`:""}</small></button>`}).join("")||(el.value.trim()?'<p class="scnote">没有找到匹配的景点</p>':"")});
(function(){let sx=0,sy=0,li=null,dx=0;
  document.addEventListener("touchstart",e=>{const l=e.target.closest(".apsw");document.querySelectorAll(".apsw.open").forEach(x=>{if(x!==l)x.classList.remove("open")});if(!l)return;li=l;sx=e.touches[0].clientX;sy=e.touches[0].clientY;dx=0},{passive:true});
  document.addEventListener("touchmove",e=>{if(!li)return;dx=e.touches[0].clientX-sx;const dy=e.touches[0].clientY-sy;if(Math.abs(dy)>Math.abs(dx)){return}if(dx<-10)li.style.transform=`translateX(${Math.max(dx,-84)}px)`;else if(dx>10&&li.classList.contains("open"))li.style.transform=`translateX(${Math.min(-84+dx,0)}px)`},{passive:true});
  document.addEventListener("touchend",()=>{if(!li)return;li.style.transform="";if(dx<-40)li.classList.add("open");else if(dx>30)li.classList.remove("open");li=null},{passive:true});})();
/* ===== 分享行程 ===== */
const SHARE_BASE=CFG.shareBase;
let SH_OPEN=false,SH_URL="",SH_MSG="";const TRIP_C={};
const shBase=()=>location.protocol==="https:"&&/github\.io$/.test(location.hostname)?location.origin+location.pathname:SHARE_BASE;
const b64u=u8=>{let s="";for(let i=0;i<u8.length;i+=8192)s+=String.fromCharCode.apply(null,u8.subarray(i,i+8192));return btoa(s).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"")};
const ub64=s=>{s=s.replace(/-/g,"+").replace(/_/g,"/");while(s.length%4)s+="=";const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u};
async function zip(u8,inv){const cs=inv?new DecompressionStream("deflate-raw"):new CompressionStream("deflate-raw");const r=new Blob([u8]).stream().pipeThrough(cs);return new Uint8Array(await new Response(r).arrayBuffer())}
function tripObj(){const v=PV.v[PV.cur]||{},ds=planDates(),M=liveMeta();if(!ds.length)return null;
  const day0=new Date(ds[0]+"T00:00:00"),off=d=>Math.round((new Date(d+"T00:00:00")-day0)/864e5);
  const n=off(ds[ds.length-1])+1,d=[],m=[];for(let i=0;i<n;i++){d.push([]);m.push(0)}
  ds.forEach(x=>{const i=off(x);d[i]=PLAN[x].slice();const mm=M[x];if(mm&&mm.rows&&mm.rows.filter(r=>!r.lunch&&!r.mv).every(r=>PLAN[x].includes(r.id))&&PLAN[x].every(id=>mm.rows.some(r=>r.id===id)))
    m[i]=[mm.rows.map(r=>r.mv?[1,r.at,r.txt]:r.lunch?[0,r.at]:[r.id,r.at,r.dur,r.tr,r.ev||"",r.eve?1:0]),mm.back,mm.food||[],mm.note||[]]});
  return {v:1,n:v.name||"我的行程",s:ds[0],d,m}}
async function tripEncode(){const o=tripObj();if(!o)return "";const u=new TextEncoder().encode(JSON.stringify(o));
  try{if(window.CompressionStream)return "z"+b64u(await zip(u))}catch(e){}return "j"+b64u(u)}
async function tripDecode(c){const k=c[0],u=ub64(c.slice(1));const raw=k==="z"?await zip(u,true):u;const o=JSON.parse(new TextDecoder().decode(raw));
  const day0=new Date(o.s+"T00:00:00"),plan={},meta={};
  o.d.forEach((ids,i)=>{const ids2=ids.filter(id=>NODES[id]);if(!ids2.length)return;const t=new Date(day0.getTime()+i*864e5+12*36e5);const d=t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0");
    plan[d]=ids2;const mm=o.m&&o.m[i];if(mm)meta[d]={rows:mm[0].filter(r=>r[0]===0||r[0]===1||NODES[r[0]]).map(r=>r[0]===1?{mv:1,at:r[1],txt:r[2]}:r[0]===0?{lunch:1,at:r[1]}:{id:r[0],at:r[1],dur:r[2],tr:r[3],ev:r[4],eve:r[5]}),back:mm[1],food:(mm[2]||[]).filter(k=>TERMS_[k]),note:mm[3]||[]}});
  return {name:o.n,plan,meta}}
function tripDayHtml(d,meta,plan){return meta[d]?apSchedule(d,meta,plan):`<ol class="apday">${plan[d].map(id=>`<li><time>·</time><span><button class="mylink" data-go="${id}"><b>${esc(NODES[id].n)}</b></button></span></li>`).join("")}</ol>`}
function tripText(name,plan,meta,url){const ds=Object.keys(plan).sort();let s=`【${name}】${fmtD(ds[0])}–${fmtD(ds[ds.length-1])} · 共 ${ds.length} 天\n`;
  ds.forEach((d,i)=>{s+=`\n第${i+1}天 ${fmtD(d,true)}\n`;const M=meta[d];
    if(M&&M.rows)M.rows.forEach(r=>{s+=r.mv?`${hm(r.at)} ${r.txt}\n`:r.lunch?`${hm(r.at)} 午餐\n`:`${hm(r.at)} ${NODES[r.id].n}${r.ev?"（"+r.ev+"）":""}\n`});else plan[d].forEach(id=>{s+=`· ${NODES[id].n}\n`});
    if(M&&M.food&&M.food.length)s+=`当地美食：${M.food.map(k=>TERMS_[k].n).join("、")}\n`;if(M&&M.note&&M.note.length)s+=`提示：${M.note.join("；")}\n`});
  if(url)s+=`\n在《${CFG.title}》里打开（可一键导入行程）：\n${url}\n`;return s}
function shareBox(){if(!SH_OPEN)return "";const canShare=!!navigator.share;
  return `<div class="shbox"><label>分享当前版本</label>
  ${SH_URL?`<input id="sh-url" readonly value="${esc(SH_URL)}" aria-label="分享链接">`:`<p class="scnote">正在生成链接…</p>`}
  <div class="aprow wrap">${canShare?`<button class="btn sm pri" data-shsys="1">发送给…</button>`:""}<button class="btn sm${canShare?"":" pri"}" data-shcopy="url">复制链接</button><button class="btn sm" data-shcopy="text">复制文字版</button><button class="btn sm" data-shprint="1">打印 / 存为 PDF</button></div>
  ${SH_MSG?`<p class="shmsg">${esc(SH_MSG)}</p>`:""}
  <p class="scnote">对方点开链接会打开这本手帖，并可以把行程一键导入成自己的新版本；没装的人直接在浏览器里看。文字版适合发微信；PDF 适合打印或发给不用手机看的人。</p></div>`}
async function shOpen(){SH_OPEN=!SH_OPEN;SH_MSG="";SH_URL="";render(cur,false);if(!SH_OPEN)return;
  const c=await tripEncode();SH_URL=c?shBase()+"#trip-"+c:"";if(!c)SH_MSG="当前版本还是空的，先排几个景点再分享。";render(cur,false)}
async function shCopy(txt,ok){try{await navigator.clipboard.writeText(txt);SH_MSG=ok}catch(e){const ta=document.createElement("textarea");ta.value=txt;ta.style.cssText="position:fixed;opacity:0";document.body.appendChild(ta);ta.select();let r=false;try{r=document.execCommand("copy")}catch(_){}ta.remove();SH_MSG=r?ok:"复制没有成功，请长按上面的链接手动复制。"}render(cur,false)}
function shPrint(name,plan,meta){const ds=Object.keys(plan).sort();let el=document.getElementById("printsheet");if(!el){el=document.createElement("div");el.id="printsheet";document.body.appendChild(el)}
  el.innerHTML=`<header><div class="ps-brand">${CFG.title}</div><h1>${esc(name)}</h1><p>${fmtD(ds[0],true)} – ${fmtD(ds[ds.length-1],true)} · 共 ${ds.length} 天</p></header>`+
   ds.map((d,i)=>{const M=meta[d];return `<section><h2>第${i+1}天 <small>${fmtD(d,true)}</small></h2><table>${M&&M.rows?M.rows.map(r=>r.mv?`<tr class="l"><td>${hm(r.at)}</td><td>${esc(r.txt)}</td><td></td></tr>`:r.lunch?`<tr class="l"><td>${hm(r.at)}</td><td>午餐</td><td></td></tr>`:`<tr><td>${hm(r.at)}</td><td><b>${esc(NODES[r.id].n)}</b> <span>${esc(NODES[r.id].ja||"")}</span>${r.ev?` · ${esc(r.ev)}`:""}</td><td>游览约 ${r.dur} 分钟 · 前往约 ${r.tr} 分钟</td></tr>`).join(""):plan[d].map(id=>`<tr><td>·</td><td><b>${esc(NODES[id].n)}</b> <span>${esc(NODES[id].ja||"")}</span></td><td></td></tr>`).join("")}</table>
   ${M&&M.food&&M.food.length?`<p>当地美食：${M.food.map(k=>esc(TERMS_[k].n)).join("、")}</p>`:""}${M&&M.note&&M.note.length?`<p class="n">${M.note.map(esc).join("；")}</p>`:""}</section>`}).join("")+
   `<footer>时间为大致估算，开放时间与交通以官方信息为准 · ${esc(SH_URL?"在线版：":"")}${esc(SH_URL?shBase():"")}</footer>`;
  let ok=true;try{window.print()}catch(e){ok=false}
  SH_MSG=ok?"如果没有弹出打印窗口：手机上请用浏览器的「分享 → 打印」，或在电脑浏览器里打开再试；打印时选「存储为 PDF」。":"当前环境不支持打印，请在浏览器里打开这本手帖再试。";render(cur,false)}
function tripPages(code){const T=TRIP_C[code];
  if(!T){tripDecode(code).then(r=>{TRIP_C[code]=r;if(cur==="trip-"+code)render(cur,false)}).catch(()=>{TRIP_C[code]={err:1};if(cur==="trip-"+code)render(cur,false)});
    return [`<span class="eyebrow">分享</span><div class="tagtitle">收到的行程</div><p>正在读取…</p>`,`<h1>行程</h1>`]}
  if(T.err||!Object.keys(T.plan).length)return [`<span class="eyebrow">分享</span><div class="tagtitle">收到的行程</div><p>这个分享链接无法读取，可能复制不完整，或者是旧版本生成的。请让对方重新复制一次链接。</p>`,`<h1>行程</h1>`];
  const ds=Object.keys(T.plan).sort();
  const L=`<span class="eyebrow">分享</span><div class="tagtitle">收到的行程</div><h2 style="margin:6px 0 4px">${esc(T.name)}</h2>
  <p style="color:var(--ink-2)">${fmtD(ds[0],true)} – ${fmtD(ds[ds.length-1],true)} · 共 ${ds.length} 天 · ${ds.reduce((a,d)=>a+T.plan[d].length,0)} 处景点</p>
  <div class="aprow wrap" style="margin-top:12px"><button class="btn pri" data-tripimp="${esc(code)}">导入为我的新行程版本</button></div>
  <p class="scnote">导入后会成为一个新的行程版本，不会覆盖你已有的计划；之后可以在「旅行计划」里自由调整。点右边的景点名可以先看介绍。</p><span class="folio">TRIP</span>`;
  const R=`<div class="kicker"><span class="kind">行程单</span><span>${esc(T.name)}</span></div><h1>行程预览</h1>`+ds.map((d,i)=>`<div class="sec">第${i+1}天 · ${fmtD(d,true)}</div>${tripDayHtml(d,T.meta,T.plan)}`).join("")+`<span class="folio">TRIP</span>`;
  return [L,R]}
document.addEventListener("click",e=>{const q=s=>e.target.closest(s);let b;
  if(q("[data-shopen]")){shOpen();return}
  if(q("[data-shsys]")){const v=PV.v[PV.cur];navigator.share({title:v.name,text:tripText(v.name,PLAN,liveMeta(),""),url:SH_URL}).catch(()=>{});return}
  if(b=q("[data-shcopy]")){const v=PV.v[PV.cur];if(b.dataset.shcopy==="url")shCopy(SH_URL,"链接已复制，可以粘贴到微信、邮件里发给对方。");else shCopy(tripText(v.name,PLAN,liveMeta(),SH_URL),"文字版已复制（末尾附了链接）。");return}
  if(q("[data-shprint]")){const v=PV.v[PV.cur];shPrint(v.name,PLAN,liveMeta());return}
  if(b=q("[data-tripimp]")){const T=TRIP_C[b.dataset.tripimp];if(!T||T.err)return;PLAN=JSON.parse(JSON.stringify(T.plan));pvNew(T.name+"（收到的）",PLAN,T.meta,null);savePlan();SH_OPEN=false;go("plan");return}
});

document.addEventListener("change",e=>{
  if(e.target.id==="pv-sel"){pvSwitch(e.target.value);render(cur,false)}
  if(e.target.id==="ap-start"){AP.start=e.target.value;if(!AP.end||AP.end<AP.start)AP.end=AP.start;apSave();render(cur,false)}
  if(e.target.id==="ap-end"){AP.end=e.target.value;apSave()}
  if(e.target.id==="ap-base"){AP.base=e.target.value;apSave()}
  if(e.target.id==="ap-arrt"){AP.arrT=e.target.value;apSave()}if(e.target.id==="ap-dept"){AP.depT=e.target.value;apSave()}
  if(e.target.id==="ap-arrp"){AP.arrP=e.target.value;apSave()}if(e.target.id==="ap-depp"){AP.depP=e.target.value;apSave()}
});
document.addEventListener("click",e=>{
  const q=s=>e.target.closest(s);let b;
  if(b=q("[data-aptag]")){const k=b.dataset.aptag;AP.tags=AP.tags.includes(k)?AP.tags.filter(x=>x!==k):[...AP.tags,k];apSave();render(cur,false);return}
  if(b=q("[data-plaaddid]")){const [d,id]=b.dataset.plaaddid.split("|");if(PLAN[d]&&!PLAN[d].includes(id)){const M=planCalc(d),ev=M.rows.find(r=>r.eve);const i=ev?PLAN[d].indexOf(ev.id):-1;if(i>=0)PLAN[d].splice(i,0,id);else PLAN[d].push(id);savePlan()}render(cur,false);return}
  if(b=q("[data-aprm]")){const [d,id]=b.dataset.aprm.split("|");AP_RES.plan[d]=AP_RES.plan[d].filter(x=>x!==id);apResched(d);render(cur,false);return}
  if(b=q("[data-apaddid]")){const [d,id]=b.dataset.apaddid.split("|");if(!AP_RES.plan[d].includes(id)){Object.keys(AP_RES.plan).forEach(k=>{if(k!==d&&AP_RES.plan[k].includes(id)){AP_RES.plan[k]=AP_RES.plan[k].filter(x=>x!==id);apResched(k)}});AP_RES.plan[d].push(id);apResched(d)}render(cur,false);return}
  if(q("[data-apfew]")){AP.few=AP.few===false;apSave();render(cur,false);return}
  if(b=q("[data-apck]")){const k=b.dataset.apck;if(k==="scenic")AP.scenic=AP.scenic===false;else AP[k]=!AP[k];apSave();render(cur,false);return}
  if(b=q("[data-aphd]")){const k=b.dataset.aphd;AP.hikeDur=AP.hikeDur.includes(k)?AP.hikeDur.filter(x=>x!==k):[...AP.hikeDur,k];apSave();render(cur,false);return}
  if(b=q("[data-apreg]")){const k=b.dataset.apreg,c=AP.regions[k]||0,mx=Math.min(CFG.ap.regMax[k]||CFG.ap.regMax._,Math.max(1,apDays(AP.start,AP.end).length));if(c>=mx)delete AP.regions[k];else AP.regions[k]=c+1;apSave();render(cur,false);return}
  if(b=q("[data-apset]")){const [k,v]=b.dataset.apset.split("|");AP[k]=v;apSave();render(cur,false);return}
  if(q("[data-apmust]")){const v=($("#ap-must").value||"").trim();const id=Object.keys(PLANDATA).find(k=>NODES[k]&&NODES[k].n===v);if(id&&!AP.must.includes(id)){AP.must.push(id);apSave();render(cur,false)}return}
  if(b=q("[data-apmustrm]")){AP.must=AP.must.filter(x=>x!==b.dataset.apmustrm);apSave();render(cur,false);return}
  if(q("[data-apgo]")){AP_SEED=1;AP_RES=apGenerate();if(CFG.feat.autoDraft)apAuto();render(cur,false);if(!wide()){const r=document.getElementById("R");r&&r.scrollIntoView({behavior:"smooth"})}return}
  if(q("[data-apre]")){AP_SEED++;AP_RES=apGenerate();if(CFG.feat.autoDraft)apAuto();render(cur,false);return}
  if(q("[data-apsave]")&&AP_RES&&!AP_RES.err){const nm=($("#ap-name").value||"自动行程").trim();if(CFG.feat.autoDraft){apAuto();const id=Object.keys(PV.v).find(k=>PV.v[k].auto);if(id){PV.v[id].name=nm;delete PV.v[id].auto;pvSave()}}else{PLAN=JSON.parse(JSON.stringify(AP_RES.plan));pvNew(nm,PLAN,AP_RES.meta,Object.assign({},AP_RES.opt,{baseRes:AP_RES.base}));savePlan();}go("plan");return}
  if(q("[data-pvdup]")){const c=PV.v[PV.cur];pvNew((c?c.name:"行程")+"（副本）",PLAN,c?c.meta:{},c?c.opt:null);render(cur,false);return}
  if(q("[data-pvnew]")){PLAN={};pvNew("新行程 "+(Object.keys(PV.v).length+1),{});savePlan();render(cur,false);return}
  if(q("[data-pvren]")){PV_REN=!PV_REN;render(cur,false);return}
  if(q("[data-pvrenok]")){const v=($("#pv-name").value||"").trim();if(v){PV.v[PV.cur].name=v;pvSave()}PV_REN=false;render(cur,false);return}
  if(q("[data-pvdel]")){if(!PV_DEL){PV_DEL=true;render(cur,false);setTimeout(()=>{PV_DEL=false},4000);return}delete PV.v[PV.cur];PV_DEL=false;pvSwitch(Object.keys(PV.v)[0]);render(cur,false);return}
},true);

let PENDING_FILTER=null;
let MY={};try{MY=JSON.parse(localStorage.getItem((CFG.id+"-mytags"))||"{}")||{}}catch(e){MY={}}
function saveMy(){Object.keys(MY).forEach(k=>{if(!MY[k]||!MY[k].length)delete MY[k]});try{localStorage.setItem((CFG.id+"-mytags"),JSON.stringify(MY))}catch(e){}}
const myAll=()=>{const s=new Set(PRESET);Object.values(MY).forEach(a=>a.forEach(x=>s.add(x)));return [...s]};
const myCount=()=>Object.keys(MY).filter(k=>NODES[k]).length;
function mineBlock(n){const cur=MY[n.id]||[];
  return `<div class="mine" id="mine"><span class="eyebrow">我的标签</span><div class="mrow">${myAll().map(x=>`<button class="mt${cur.includes(x)?" on":""}" data-mytoggle="${esc(x)}" aria-pressed="${cur.includes(x)}">${x==="收藏"?(cur.includes(x)?"♥ ":"♡ "):""}${esc(x)}</button>`).join("")}<span class="madd"><input id="mytag-input" maxlength="12" placeholder="新标签…" aria-label="添加自己的标签"><button class="mt plus" data-myadd="1">添加</button></span></div>${(CFG.feat.planRowData?PLANDATA[n.id]:n.depth>=2)?`<div class="mrow prow"><span class="eyebrow">旅行计划</span>${datesOf(n.id).map(d=>`<span class="mt on pd">第${dayNo(d)}天 · ${fmtD(d)}<button class="px" data-planrm="${d}" aria-label="从${fmtD(d)}移除">×</button></span>`).join("")}<span class="madd"><input type="date" id="plan-date" value="${esc(LASTDATE)}" aria-label="选择日期"><button class="mt plus" data-planadd="1">加入行程</button></span><button class="mt" data-route="plan">查看行程单 →</button></div>`:""}</div>`}
function refreshMine(){const el=document.querySelector("#R .mine");const p=parseRoute(cur);if(el&&p.node)el.outerHTML=mineBlock(p.node);const c=document.getElementById("myCnt");if(c)c.textContent=myCount();try{syncTab()}catch(e){}}
let FILTER=null,FBAR_OPEN=false;
const UPPER=n=>CFG.upper.ids?CFG.upper.ids.includes(n.id):n.c.some(c=>CFG.upper.kinds.includes(c.kind));
const tiered=n=>!UPPER(n)&&n.c.length>5;
function subtree(n){const a=[];(function w(x){x.c.forEach(c=>{a.push(c);w(c)})})(n);return a}
const isMy=k=>k&&k.startsWith("my:");
const isPlan=k=>k&&k.startsWith("plan:");
const matchTag=(n,k)=>k&&k.includes("&")?k.split("&").every(p=>matchTag(n,p)):isPlan(k)?(k==="plan:*"?datesOf(n.id).length>0:(PLAN[k.slice(5)]||[]).includes(n.id)):isMy(k)?(k==="my:*"?!!(MY[n.id]&&MY[n.id].length):(MY[n.id]||[]).includes(k.slice(3))):hasTag(n,k);
const tagLabel=k=>k&&k.includes("&")?k.split("&").map(p=>TAGS[p]).join(" · "):isPlan(k)?(k==="plan:*"?"旅行计划":"行程 "+fmtD(k.slice(5))):isMy(k)?(k==="my:*"?"我的标签":k.slice(3)):TAGS[k];
const cntIn=(c,k)=>CFG.feat.countMarkers?[c,...subtree(c)].filter(x=>(x.kind==="多日路线"||x.kind==="老城区"||!x.c.length)&&matchTag(x,k)).length:subtree(c).filter(x=>matchTag(x,k)).length+(matchTag(c,k)?1:0);
function stateOf(n,c){if(!FILTER)return"show";if(UPPER(n))return cntIn(c,FILTER)?"show":"hide";if(matchTag(c,FILTER))return"show";return tiered(n)&&c.star?"fade":(tiered(n)?"hide":"hide")}
function badge(n,c){return CFG.feat.countMarkers?0:(FILTER&&UPPER(n)?cntIn(c,FILTER):0)}
const SUBF=CFG.SUBF||{};
const SUBHIDE=new Set(CFG.SUBHIDE||[]);
const fBase=()=>FILTER&&!isMy(FILTER)&&!isPlan(FILTER)?FILTER.split("&")[0]:null;
function subBar(pool,F=FILTER,attr="data-filter"){const b=F&&!isMy(F)&&!isPlan(F)?F.split("&")[0]:null;if(!b||!SUBF[b])return "";const cur=F.split("&").slice(1);
  return `<div class="fsub" role="toolbar" aria-label="${esc(TAGS[b])}细分">${SUBF[b].map(([lab,ks])=>{const other=cur.filter(x=>!ks.includes(x));
    const cs=ks.map(k=>{const on=cur.includes(k);const key=[b,...other,...(on?[]:[k])].join("&");const c=pool.filter(x=>matchTag(x,[b,...other,k].join("&"))).length;if(!c&&!on)return "";return `<button class="fchip sub${on?" on":""}" ${attr}="${esc(key)}">${esc(TAGS[k])}<small>${c}</small></button>`}).join("");
    return cs?`<span class="fsg">${lab?`<b>${lab}</b>`:""}${cs}</span>`:""}).join("")}</div>`}
function filterBar(n){
  const pool=UPPER(n)?subtree(n):n.c;
  const cnt={};pool.forEach(x=>Object.keys(TAGS).forEach(k=>{if(hasTag(x,k))cnt[k]=(cnt[k]||0)+1}));
  const myc={};pool.forEach(x=>{const a=MY[x.id]||[];if(a.length)myc["my:*"]=(myc["my:*"]||0)+1;a.forEach(v=>myc["my:"+v]=(myc["my:"+v]||0)+1)});
  const pc={};pool.forEach(x=>{const a=datesOf(x.id);if(a.length)pc["plan:*"]=(pc["plan:*"]||0)+1;a.forEach(d=>pc["plan:"+d]=(pc["plan:"+d]||0)+1)});
  const pks=Object.keys(pc).sort((a,b)=>(b==="plan:*")-(a==="plan:*")||a.localeCompare(b));
  const pchip=k=>`<button class="fchip plan${FILTER===k?" on":""}" data-filter="${esc(k)}">${k==="plan:*"?"📅 旅行计划":"第"+dayNo(k.slice(5))+"天 "+fmtD(k.slice(5))}<small>${pc[k]}</small></button>`;
  const mks=Object.keys(myc).sort((a,b)=>(b==="my:*")-(a==="my:*")||((PRESET.indexOf(a.slice(3))+1)||99)-((PRESET.indexOf(b.slice(3))+1)||99)||myc[b]-myc[a]);
  const ks=Object.keys(cnt).filter(k=>!SUBHIDE.has(k)).sort((a,b)=>(b==="hot")-(a==="hot")||cnt[b]-cnt[a]);if(!ks.length&&!mks.length&&!pks.length)return"";
  const LIM=8,more=ks.length>LIM;
  const chip=(k,i)=>`<button class="fchip${fBase()===k?" on":""}${i>=LIM&&fBase()!==k?" extra":""}" data-filter="${k}">${esc(TAGS[k])}<small>${cnt[k]}</small></button>`;
  const mchip=k=>`<button class="fchip my${FILTER===k?" on":""}" data-filter="${esc(k)}">${k==="my:*"?"♥ 我的标签":esc(k.slice(3))}<small>${myc[k]}</small></button>`;
  return `<div class="fbar${FBAR_OPEN?" open":""}" role="toolbar" aria-label="按标签筛选"><button class="fchip${FILTER?"":" on"}" data-filter="">全部</button>${pks.map(pchip).join("")}${mks.map(mchip).join("")}${ks.map(chip).join("")}${more?`<button class="fmore" data-fmore="1">${FBAR_OPEN?"收起 ▴":`更多 ${ks.length-LIM} ▾`}</button>`:""}</div>${subBar(pool)}`;
}
function planSVG(P){
  const T=(P.terrain||[]).map(d=>`<path d="${d}" style="fill:var(--hill)" opacity=".75"/>`).join("");
  const W=(P.water||[]).map(d=>`<path d="${d}" fill="none" style="stroke:var(--water)" stroke-width="6" stroke-linecap="round"/>`).join("");
  const A=(P.path||[]).map(d=>`<path d="${d}" fill="none" style="stroke:var(--muted)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/>`).join("");
  const B=(P.b||[]).map(([x,y,w,h,l,k])=>{const cx=x+w/2,cy=y+h/2;let g=`<rect class="bd ${k||"plain"}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${k==="tomb"?h/2:2}"/>`;
    if(k==="pagoda")g+=`<path class="bdl" d="M${x} ${y}L${x+w} ${y+h}M${x+w} ${y}L${x} ${y+h}"/>`;
    if(k==="kura")g+=`<path class="bdl" d="M${x} ${y+h/3}H${x+w}M${x} ${y+2*h/3}H${x+w}"/>`;
    if(k==="gate")g+=`<path class="bdl" d="M${x+4} ${y}V${y+h}M${x+w-4} ${y}V${y+h}"/>`;
    const big=k==="main";return g+`<text class="bdt${big?" big":""}" x="${cx}" y="${big?cy+5:y+h+12}" text-anchor="middle">${esc(l)}</text>`}).join("");
  const L=(P.lbl||[]).map(l=>`<text class="geo" x="${l.x}" y="${l.y}" text-anchor="middle">${esc(l.t)}</text>`).join("");
  return T+W+A+B+L;
}
const HYPSO=typeof HYPSO_DATA!=="undefined"?HYPSO_DATA:"";
function rtFocus(b,f){if(!f||!b.includes(`data-rt="${f}"`))return b;const m=b.match(new RegExp(`<path class="rt" data-rt="${f}"[^>]*/>`));return m?b+`<path d="${/ d="([^"]+)"/.exec(m[0])[1]}" fill="none" style="stroke:var(--page)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>`+m[0].replace(`class="rt"`,`class="rt on"`):b}
function mkShape(c,r){const k=c.mk,x=c.x,y=c.y;if(k==="ski")return `<rect class="sh ski" x="${(x-r*.84).toFixed(1)}" y="${(y-r*.84).toFixed(1)}" width="${(r*1.68).toFixed(1)}" height="${(r*1.68).toFixed(1)}" rx="2.5" transform="rotate(45 ${x} ${y})"/>`;if(k==="mtn")return `<rect class="sh mtn" x="${(x-r*.9).toFixed(1)}" y="${(y-r*.9).toFixed(1)}" width="${(r*1.8).toFixed(1)}" height="${(r*1.8).toFixed(1)}" rx="${(r*.42).toFixed(1)}"/>`;if(k==="vtown")return `<path class="sh town" d="M${(x-r*.95).toFixed(1)} ${(y+r*.85).toFixed(1)}V${(y-r*.15).toFixed(1)}L${x} ${(y-r*1.05).toFixed(1)}L${(x+r*.95).toFixed(1)} ${(y-r*.15).toFixed(1)}V${(y+r*.85).toFixed(1)}Z" stroke-linejoin="round"/>`;if(k==="vold")return `<path class="sh old" d="M${(x-r*.9).toFixed(1)} ${(y+r*.9).toFixed(1)}V${(y-r*.9).toFixed(1)}h${(r*.45).toFixed(1)}v${(r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(-r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(r*.35).toFixed(1)}h${(r*.45).toFixed(1)}v${(-r*.35).toFixed(1)}V${(y+r*.9).toFixed(1)}Z" stroke-linejoin="round"/>`;if(k==="vout")return `<circle class="sh out" cx="${x}" cy="${y}" r="${r}"/>`;if(k==="hike")return `<path class="sh hike" d="M${x} ${(y-r*1.25).toFixed(1)}L${(x+r*1.2).toFixed(1)} ${(y+r*.9).toFixed(1)}H${(x-r*1.2).toFixed(1)}Z" stroke-linejoin="round"/>`;return `<circle cx="${x}" cy="${y}" r="${r}"/>`}
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
function mapSVG(n,focus){
  const R=seed(n.id);let hills="";const P=n.plan;
  for(let i=0;i<7;i++){const x=R()*600,y=R()*440,rx=60+R()*110,ry=40+R()*70;
    hills+=`<ellipse cx="${x|0}" cy="${y|0}" rx="${rx|0}" ry="${ry|0}" style="fill:var(--hill)" opacity=".7"/>`;
    for(let k=1;k<3;k++)hills+=`<ellipse cx="${x|0}" cy="${y|0}" rx="${rx*(1-k*.28)|0}" ry="${ry*(1-k*.28)|0}" fill="none" style="stroke:var(--matcha)" stroke-width=".6" opacity=".35"/>`;}
  const grid=[...Array(11)].map((_,i)=>`<path d="M${i*60} 0V440" style="stroke:var(--line)"/>`).join("")+[...Array(8)].map((_,i)=>`<path d="M0 ${i*60}H600" style="stroke:var(--line)"/>`).join("");
  const water=(n.w||[]).map(d=>`<path d="${d}" style="fill:var(--water)"/>`).join("");
  const rivers=(n.r||[]).map(d=>`<path d="${d}" fill="none" style="stroke:var(--water)" stroke-width="12" stroke-linecap="round"/>`).join("");
  const geo=(n.lbl||[]).map(l=>`<text class="geo" x="${l.x}" y="${l.y}" text-anchor="middle">${esc(l.t)}</text>`).join("");
  const kids=n.c.filter(c=>c.x!=null);
  const route=n.route&&kids.length>1?`<path d="M${kids.map(c=>c.x+" "+c.y).join(" L")}" fill="none" style="stroke:var(--shu)" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round" opacity=".8"/>`:"";
  const marks=kids.map(c=>{const i=n.c.indexOf(c);const st=focus?(c.id===focus?"show":"fade"):stateOf(n,c);if(st==="hide")return"";const minor=tiered(n)&&!c.star;const r=minor?10:14;const b=badge(n,c);const lw=[...(c.n+(b?" · "+b:""))].reduce((s,ch)=>s+(ch.charCodeAt(0)>255?13.5:7),0);const right=CFG.feat.smartLabels?(c.x+r+8+lw<596||c.x-r-8-lw<4):c.x<440;const tx=right?c.x+r+8:c.x-r-8;
    return `<g class="mk${minor?" minor":""}${st==="fade"?" fade":""}" data-go="${c.id}" tabindex="0" role="link" aria-label="${esc(c.n)}">${c.col?mkShape(c,r).replace(/class="sh /,`style="fill:${c.col}" class="sh `):mkShape(c,r)}<text class="num" x="${c.x}" y="${c.y}">${CFG.feat.countMarkers?(c.num||(n.kind==="多日路线"?i+1:(FILTER?cntIn(c,FILTER):nSpots(c)))):i+1}</text><text class="lab" x="${tx}" y="${c.y+5}" text-anchor="${right?"start":"end"}">${esc(c.mn||c.n)}${b?` · ${b}`:""}</text></g>`}).join("");
  return `<svg class="map${P?" plan":""}${focus&&n.bg&&n.bg.includes(`data-rt="${focus}"`)?" rtf":""}" viewBox="0 0 600 440" role="img" aria-label="${esc(n.n)}${P?"境内":""}示意地图"><rect width="600" height="440" style="fill:var(--land)"/><g stroke-width=".5">${grid}</g>${P?planSVG(P):n.bg?rtFocus(n.bg.replace("__HY__",HYPSO),focus)+geo:hills+water+rivers+geo}${route}${marks}${n.sb||""}
  <g transform="translate(560 40)"><path d="M0 -18 L7 6 L0 1 L-7 6Z" style="fill:var(--ink)"/><text y="22" text-anchor="middle" style="fill:var(--ink);font:600 11px var(--f-mono)">N</text></g>
  <text x="14" y="428" style="fill:var(--muted);font:10px var(--f-mono)">${P?esc(P.note||"境内示意图 · 非实际比例"):(n.bg?"地图数据：Natural Earth · 山峰城镇为本书标注 · 图钉位置为示意":"示意图 · 非实际比例")+(n.route?" · 虚线为推荐步行顺序":"")}</text></svg>`;
}
function imgMap(n,focus){
  const pins=n.c.map(c=>{const st=focus?(c.id===focus?"show":"fade"):stateOf(n,c);if(st==="hide")return"";return (c.edge&&c.edge.dir==="down"?`<button class="pin edgearrow down" data-go="${c.id}" style="left:${c.px}%;top:${c.py}%" aria-label="${esc(c.n)}，${esc(c.edge.hint)}">${ARROWD}<em class="txt"><span>${esc(c.n)}</span><small>${esc(c.edge.hint)}</small></em></button>`:c.edge?`<button class="pin edgearrow" data-go="${c.id}" style="left:${c.px}%;top:${c.py}%" aria-label="${esc(c.n)}，${esc(c.edge.hint)}">${ARROW(c.edge.rot)}<span>${esc(c.n)}</span><small>${esc(c.edge.hint)}</small></button>`
    :`<button class="pin${tiered(n)&&!c.star?" minor":""}${c.side?" s"+c.side:""}" data-go="${c.id}" style="left:${c.px}%;top:${c.py}%"><span>${esc(c.n)}</span><i></i>${badge(n,c)?`<em class="cnt">${badge(n,c)}</em>`:""}</button>`).replace('class="pin',`class="pin${st==="fade"?" fade":""}`)}).join("");
  const A=n.air;const alb=A?(A.lbl||[]).map(([x,y,t])=>`<span class="alb" style="left:${x}%;top:${y}%">${esc(t)}</span>`).join("")+`<span class="acredit">${esc(A.credit||"航空照片：国土地理院")}</span>`:"";
  const ban=n.banner?`<div class="banner" style="left:${n.banner.x}%;top:${n.banner.y}%">${esc(n.n)}</div>`:"";
  return `<div class="imgwrap"><div class="imgmap${A?" aerial":""}${editing?" editing":""}" data-map="${n.id}"><img src="${IMGS[n.img]}" alt="${esc(n.n)}${A?"航空照片境内图":"插画地图"}" draggable="false">${alb}${ban}${pins}</div></div>
  <div class="edittools"><button class="btn sm" data-edit="1">${editing?"完成调整":"调整图钉"}</button>${editing?`<span>拖动图钉到正确位置</span><button class="btn sm" data-copypins="1">复制坐标发给 Claude</button><button class="btn sm" data-resetpins="${n.id}">恢复默认</button><span class="status" id="pinStatus"></span>`:""}</div>`;
}
function cap(c){return c.ai?`插画 · ${esc(c.by)}`:`${esc(c.by)} · <a href="${esc(c.u)}" target="_blank" rel="noopener">${esc(c.lic)}</a> · Wikimedia Commons`}
function engSel(){return `<label class="eng">用 <select data-eng aria-label="选择搜索引擎">${Object.entries(ENGINES).map(([k,v])=>`<option value="${k}"${k===ENGINE?" selected":""}>${v[0]}</option>`).join("")}</select></label>`}
function extURL(u){let q=u;try{const x=new URL(u);q=x.searchParams.get("q")||u}catch(e){}return ENGINE==="google"?"https://www.google.com/search?tbm=isch&q="+encodeURIComponent(q):ENGINE==="bing"?"https://www.bing.com/images/search?q="+encodeURIComponent(q):ENGINE==="baidu"?"https://image.baidu.com/search/index?tn=baiduimage&word="+encodeURIComponent(q):ENGINE==="yahoojp"?"https://search.yahoo.co.jp/image/search?p="+encodeURIComponent(q):"https://duckduckgo.com/?ia=images&iax=images&q="+encodeURIComponent(q)}
function extBox(u,label){return `<div class="extph"><b>暂无可商用的图片</b><a href="${esc(extURL(u))}" target="_blank" rel="noopener">请访问该链接查看${label?esc(label):""}照片 ↗</a>${engSel()}</div>`}
const SC_TAGS=CFG.SC_TAGS;
const SC_DEF=CFG.SC_DEF;
function seasonCal(n){const tags=(CFG.feat.smTags?[...new Set([...(n.t||[]),...Object.keys(n.sm||{})])]:(n.t||[])).filter(t=>SC_TAGS.includes(t));if(!tags.length)return "";
  const rows=tags.map(t=>{const seg=(n.sm&&n.sm[t])||SC_DEF[t];if(!seg||!seg.length)return "";
    return `<div class="scrow"><span class="scl">${esc(t==="hike"&&!(n.t||[]).includes("hike")?"夏季开放":t==="hike"?"徒步季节":(TAGS[t]||t))}</span><div class="sctrack">${seg.map(([a,b,nm,dt])=>`<i class="sc-${t}" style="left:${((a-1)/12*100).toFixed(2)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%"${nm?` title="${esc(nm+" "+(dt||""))}"`:""}></i>`).join("")}</div></div>${seg.some(x=>x[2])?`<ul class="evl">${[...seg].sort((x,y)=>x[0]-y[0]).filter(x=>x[2]).map(x=>`<li><b>${esc(x[2])}</b><span>${esc(x[3]||"")}</span></li>`).join("")}</ul>`:""}`}).join("");
  if(!rows)return "";
  let mk="";try{const ds=Object.keys(PLAN||{}).filter(d=>(PLAN[d]||[]).includes(n.id));mk=ds.map(d=>{const x=new Date(d);const m=x.getMonth()+1+(x.getDate()-1)/31;return `<b class="scplan" style="left:${((m-1)/12*100).toFixed(2)}%" title="行程 ${d}"></b>`}).join("")}catch(e){}
  return `<div class="scal"><div class="sec">时令月历</div><div class="scgrid">${rows}<div class="scrow scm"><span class="scl"></span><div class="sctrack">${[1,2,3,4,5,6,7,8,9,10,11,12].map(m=>`<span style="left:${((m-0.5)/12*100).toFixed(2)}%">${m}</span>`).join("")}${mk}</div></div></div><p class="scnote">月份为往年大致时期，每年会有前后浮动，请以当年发布为准。</p></div>`}
function seasonStrip(n){if(!n.season||!n.season.length)return "";
  return `<div class="season"><div class="sec">时令</div><div class="sgrid">${n.season.map(x=>{const lb=x.l||TAGS[x.t]||x.t;const c=x.img&&CIMG[x.img];
   return c?`<figure><img src="${c.src}" alt="${esc(n.n)} ${esc(lb)}" loading="lazy"><span class="stag">${esc(lb)}</span><figcaption>${cap(c)}</figcaption></figure>`:x.ext?`<figure class="noimg"><span class="stag">${esc(lb)}</span>${extBox(x.ext,lb)}</figure>`:""}).join("")}</div></div>`}
function photo(n,small){return photo0(n,small)+seasonStrip(n)+seasonCal(n)}
function photo0(n,small){
  const a=IMG[n.id]||[];
  if(!a.length&&n.ph&&CIMG[n.ph]){const c=CIMG[n.ph];return `<figure class="photo hero${small?" small":""}${c.ai?" ai":""}"><img src="${c.src}" alt="${esc(n.n)}"><figcaption>${c.ai?`插画 · ${esc(c.by)}`:`${esc(c.by)} · <a href="${esc(c.u)}" target="_blank" rel="noopener">${esc(c.lic)}</a> · Wikimedia Commons`}</figcaption></figure>`}
  if(!a.length&&n.ext)return `<div class="photo${small?" small":""} ext">${extBox(n.ext,"")}</div>`;
  if(!a.length)return `<div class="photo${small?" small":""}"><div class="ph">在这个文件夹放入照片<span class="mono">${CFG.folder}${n.key?"\\"+n.folders.join("\\"):""}</span></div></div>`;
  const i=n._pi||0;
  return `<div class="photo${small?" small":""}"><img src="${a[i].url}" alt="${esc(n.n)}"></div>${a.length>1?`<div class="thumbs">${a.map((im,k)=>`<button data-pi="${k}" class="${k===i?"on":""}"><img src="${im.url}" alt=""></button>`).join("")}</div>`:""}`;
}


const ARROW=rot=>`<svg class="needle" viewBox="0 0 120 40" style="transform:rotate(${rot}deg)" aria-hidden="true">
  <path d="M4 20 L46 6 L40 20 Z" fill="#3A2816"/><path d="M4 20 L40 20 L46 34 Z" fill="#C9A66B"/>
  <path d="M4 20 L46 6 L40 20 L46 34 Z" fill="none" stroke="#3A2816" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="M40 20 H96" stroke="#3A2816" stroke-width="2.2"/><path d="M44 16 H92 M44 24 H92" stroke="#3A2816" stroke-width=".7" opacity=".6"/>
  <path d="M96 20 L108 10 L104 20 L108 30 Z" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.4" stroke-linejoin="round"/>
  <path d="M86 20 L96 12 L94 20 L96 28 Z" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.2" stroke-linejoin="round"/>
  <circle cx="40" cy="20" r="3.2" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.2"/></svg>`;
const ARROWD=`<svg class="needle" viewBox="0 0 40 120" aria-hidden="true"><g transform="translate(0 120) rotate(-90)">
  <path d="M4 20 L46 6 L40 20 Z" fill="#3A2816"/><path d="M4 20 L40 20 L46 34 Z" fill="#C9A66B"/>
  <path d="M4 20 L46 6 L40 20 L46 34 Z" fill="none" stroke="#3A2816" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="M40 20 H96" stroke="#3A2816" stroke-width="2.2"/><path d="M44 16 H92 M44 24 H92" stroke="#3A2816" stroke-width=".7" opacity=".6"/>
  <path d="M96 20 L108 10 L104 20 L108 30 Z" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.4" stroke-linejoin="round"/>
  <path d="M86 20 L96 12 L94 20 L96 28 Z" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.2" stroke-linejoin="round"/>
  <circle cx="40" cy="20" r="3.2" fill="#E6D2A8" stroke="#3A2816" stroke-width="1.2"/></g></svg>`;
/* ---------- pin adjust mode ---------- */
let editing=false;
const DEF={};ORDER.forEach(n=>{if(n.px!=null)DEF[n.id]=[n.px,n.py]});
try{const o=JSON.parse(localStorage.getItem((CFG.id+"-pins"))||"{}");for(const k in o)if(NODES[k]){NODES[k].px=o[k][0];NODES[k].py=o[k][1]}}catch(e){}
function savePins(){const o={};ORDER.forEach(n=>{if(n.px!=null&&(n.px!==DEF[n.id][0]||n.py!==DEF[n.id][1]))o[n.id]=[n.px,n.py]});try{localStorage.setItem((CFG.id+"-pins"),JSON.stringify(o))}catch(e){}return o}
let drag=null;
document.addEventListener("pointerdown",e=>{const pin=e.target.closest(".imgmap.editing .pin");if(!pin)return;e.preventDefault();drag={pin,box:pin.parentElement.getBoundingClientRect()};pin.setPointerCapture(e.pointerId)});
document.addEventListener("pointermove",e=>{if(!drag)return;const b=drag.box;
  const x=Math.min(100,Math.max(0,(e.clientX-b.left)/b.width*100)),y=Math.min(100,Math.max(0,(e.clientY-b.top)/b.height*100));
  drag.pin.style.left=x+"%";drag.pin.style.top=y+"%";drag.x=x;drag.y=y});
document.addEventListener("pointerup",()=>{if(!drag)return;const n=NODES[drag.pin.dataset.go];if(drag.x!=null){n.px=+drag.x.toFixed(1);n.py=+drag.y.toFixed(1);savePins()}drag=null});
async function copyPins(){const o={};ORDER.forEach(n=>{if(n.px!=null)o[n.id]=[n.px,n.py]});const s="图钉坐标 "+JSON.stringify(o);const st=document.getElementById("pinStatus");
  try{await navigator.clipboard.writeText(s);st.textContent="已复制，粘贴到对话里即可"}catch(e){st.textContent="复制失败，请手动复制：";const p=document.createElement("code");p.textContent=s;p.style.cssText="display:block;user-select:all;font-size:11px;word-break:break-all";st.after(p)}}

/* ---------- pages ---------- */
const chip=(t,sm)=>`<button class="tag ${t}${sm?" sm":""}" data-tag="${t}">${esc(TAGS[t])}</button>`;
const INFO=CFG.INFO;
function related(n){
  const fam=new Set([n.id,n.parent?.id,...n.c.map(c=>c.id)]);
  return ORDER.filter(m=>!fam.has(m.id)&&m.depth>=2&&(!CFG.feat.relatedLeaves||!m.c.length)).map(m=>({m,s:m.t.filter(t=>n.t.includes(t)&&t!=="hot").length+(m.t.includes("hot")?.3:0)}))
    .filter(x=>x.s>=1).sort((a,b)=>b.s-a.s).slice(0,4).map(x=>x.m);
}
function leftPage(n){
  const pp=!n.c.length&&n.parent&&(n.parent.air||n.parent.plan||(n.parent.bg&&n.x!=null));
  let h=`<div class="maphead"><span class="eyebrow">${n.c.length?(n.air?"境内图 · 航空照片":n.img?"插画地图":n.plan?"境内图":"地图"):pp?(n.tm?(n.tm.st?"雪场图 · 位置":n.tm.k==="ski"?"路线图 · 位置":"徒步路线图 · 位置"):n.parent.bg?"地图 · 位置":"境内图 · 位置"):"图片"}</span><span class="eyebrow mono">${esc(n.ja||"")}</span></div>`;
  if(n.c.length){
    h+=filterBar(n);
    h+=n.img?imgMap(n):(!CFG.feat.photoNoMap||n.bg||n.c.some(c=>c.x!=null))?mapSVG(n)+lgHtml(n.lg):photo(n,false);
    h+=`<div class="legend">${n.c.map((c,i)=>{const st=stateOf(n,c);if(st==="hide")return"";return `<button data-go="${c.id}" class="${st==="fade"?"fade":""}${tiered(n)&&c.star?" star":""}"><span class="n">${n.img?"·":String(i+1).padStart(2,"0")}</span><b>${esc(c.n)}${badge(n,c)?` <small>${badge(n,c)}</small>`:""}</b></button>`}).join("")}</div>`;
  } else if(pp){h+=(n.tm?tmBlock(n):"")+(n.lm?lmBlock(n):"")+(n.rm?rmBlock(n):"")+(n.parent.air?imgMap(n.parent,n.id):mapSVG(n.parent,n.id))+`<div class="legend">${n.parent.c.map((c,i)=>`<button data-go="${c.id}" class="${c.id===n.id?"star":"fade"}"><span class="n">${String(i+1).padStart(2,"0")}</span><b>${esc(c.n)}</b></button>`).join("")}</div>`+photo(n,true)}
  else h+=photo(n,false);
  return h+`<span class="folio">${pg(n.page*2-1)}</span>`;
}
const PSTP={free:"免费",50:"5 折",25:"75 折",part:"部分路段",no:"不适用"},PHF={50:"5 折",part:"部分路段",no:"不适用"};
const pcls=v=>v==="free"?"pf":v==="no"?"pn":"pd";
function passMini(c){const p=c.pass;if(!p)return "";return `<span class="pmini"><i class="${pcls(p[0])}">通票 ${PSTP[p[0]]}</i><i class="${pcls(p[1])}">半价卡 ${PHF[p[1]]}</i></span>`}
function passBadge(n){const p=n.pass;if(!p)return "";return `<div class="passb"><span class="${pcls(p[0])}"><small>瑞士通票</small>${PSTP[p[0]]}</span><span class="${pcls(p[1])}"><small>半价卡</small>${PHF[p[1]]}</span>${p[2]?`<em>${esc(p[2])}</em>`:""}</div>`}
function passTable(){const G=[["观景列车与铁路",n=>n.t.includes("train")||n.t.includes("rail")],["湖船",n=>n.t.includes("boat")],["山地交通",n=>true]];const used=new Set();
  const rows=G.map(([g,f])=>{const L=ORDER.filter(n=>n.pass&&!used.has(n.id)&&f(n));L.forEach(n=>used.add(n.id));return L.length?`<tr class="pg"><th colspan="3">${g}</th></tr>`+L.map(n=>`<tr><td><button class="mylink" data-go="${n.id}">${esc(n.n)}</button></td><td class="${pcls(n.pass[0])}">${PSTP[n.pass[0]]}</td><td class="${pcls(n.pass[1])}">${PHF[n.pass[1]]}</td></tr>`).join(""):""}).join("");
  return `<div class="sec">瑞士通票与半价卡 · 一览</div><div class="mtab"><table class="ptab"><thead><tr><th>线路 / 景点</th><th>瑞士通票</th><th>半价卡</th></tr></thead><tbody>${rows}</tbody></table></div><p class="scnote">「免费」指持瑞士通票不用另外买票（观景列车的座位预订费另付）；「5 折」「75 折」指票价折扣。整理自 Swiss Travel System 和各线路官网，核对于 2026 年 11 月，每年可能调整，以官网为准。</p>`}
const mtx=m=>m>=60?`约 ${Math.floor(m/60)} 小时${m%60?` ${m%60} 分`:""}`:`约 ${m} 分钟`;
function trainSights(n){if(!n.sights||!n.sights.length)return "";return `<div class="sec">沿途看点</div><ol class="tsights" style="--tc:${n.col||"var(--shu)"}">${n.sights.map(([nm,d,id])=>`<li><b>${id&&NODES[id]?`<button class="mylink" data-go="${id}">${esc(nm)} →</button>`:esc(nm)}</b><span>${esc(d)}</span></li>`).join("")}</ol>`}
function trainsHere(n){if(!n.trn||!n.trn.length)return "";return `<div class="sec">可以乘坐的观景列车</div><ul class="trhere">${n.trn.map(t=>`<li style="--tc:${t.col}"><button class="mylink" data-go="${t.id}">${esc(t.n)}</button><span class="trst">${esc(t.st)}站</span><span class="trgo">${t.go.map(([d,m])=>`→ ${esc(d)}，${mtx(m)}`).join("<br>")}</span></li>`).join("")}</ul><p class="scnote">时间按全程时长和距离估算，实际以时刻表为准；多数观景列车需要预订座位。</p>`}
function rightPage(n){
  const kindLabel=n.kind;
  let h=`<div class="kicker"><span class="kind">${kindLabel}</span><span>${n.parent?esc(n.parent.n):CFG.eyebrow}</span></div>
  <h1>${esc(n.n)}</h1><div class="ja">${esc(n.ja)}</div>`;
  if(n.t.length)h+=`<div class="chips">${n.t.map(t=>chip(t)).join("")}</div>`;
  h+=passBadge(n);
  if(n.depth>=1)h+=mineBlock(n);
  if(n.c.length&&((IMG[n.id]||[]).length||(n.ph&&CIMG[n.ph])))h+=photo(n,true);
  SEEN=new Set(Object.keys(TERMS_).filter(k=>TERMS_[k].n===n.n));
  h+=hotRef(n)+`<p class="intro">${lk(n.d)}</p>`+(n.id===CFG.passTableNode?passTable():"")+passBlock(n)+trainSights(n)+trainsHere(n)+multiBlock(n)+hotBlock(n)+viaBlock(n)+stayBlock(n);
  if(n.hl&&n.hl.length)h+=`<div class="sec">亮点</div><ol class="hl">${n.hl.map(x=>{const i=x.indexOf("：");return `<li>${i>0&&i<12?`<b>${esc(x.slice(0,i))}</b>${lk(x.slice(i+1))}`:lk(x)}</li>`}).join("")}</ol>`;
  if(n.i){h+=`<dl class="info">${Object.entries(INFO).filter(([k])=>n.i[k]).map(([k,l])=>`<dt>${l}</dt><dd>${esc(n.i[k])}</dd>`).join("")}</dl>`}
  if(n.depth>=2&&!n.term){const host=[n,n.parent].find(x=>x&&x.depth>=2&&x.u);
    h+=`<p class="official">${host?`<a href="${esc(host.u)}" target="_blank" rel="noopener">${host===n?"官方网站":"「"+esc(host.n)+"」官方网站"} ↗</a>`:`<a href="${esc(searchURL(n))}" target="_blank" rel="noopener">在网上搜索官方信息 ↗</a><label class="eng">用 <select data-eng aria-label="选择搜索引擎">${Object.entries(ENGINES).map(([k,v])=>`<option value="${k}"${k===ENGINE?" selected":""}>${v[0]}</option>`).join("")}</select> 搜索</label>`}<span>开放时间、门票、休息日等重要信息请以官方发布为准。</span></p>`}
  if(n.tip)h+=`<p class="tip"><b>小贴士</b>${lk(n.tip)}</p>`;
  if(n.archtx)h+=`<div class="sec">建筑看点</div><p class="archp">${lk(n.archtx)}</p>`;
  if(n.term&&TERMS_[n.term]&&TERMS_[n.term].k==="美食")h+=foodInfo(TERMS_[n.term]);
  if(n.term&&WILDK(TERMS_[n.term]))h+=wildInfo(TERMS_[n.term]);
  if(n.cards&&n.cards.length)h+=`<div class="sec">细节</div><div class="dcards">${n.cards.map(c=>`<div class="dcard${c.img&&CIMG[c.img]?" hasimg":""}">${c.svg?`<figure class="dsvg">${c.svg}</figure>`:""}${c.img&&CIMG[c.img]?`<figure${CIMG[c.img].ai?' class="ai"':""}><img src="${CIMG[c.img].src}" alt="${esc(c.h)}" loading="lazy"><figcaption>${CIMG[c.img].ai?`插画 · ${esc(CIMG[c.img].by)}`:`${esc(CIMG[c.img].by)} · <a href="${esc(CIMG[c.img].u)}" target="_blank" rel="noopener">${esc(CIMG[c.img].lic)}</a> · Wikimedia Commons`}</figcaption></figure>`:c.ext?extBox(c.ext,""):""}<span class="dk">${esc(c.k)}</span><b>${lk(c.h)}</b><p>${lk(c.p)}</p></div>`).join("")}</div>`;
  if(n.hist&&n.hist.length)h+=`<div class="sec">历史沿革</div><ol class="tl">${n.hist.map(([y,t])=>`<li><span class="yr">${esc(y)}</span><span>${lk(t)}</span></li>`).join("")}</ol>`;
  if(n.arch&&n.arch.length)h+=`<div class="sec">建筑档案</div><dl class="arch">${n.arch.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${lk(v)}</dd>`).join("")}</dl>`;
  SEEN=null;
  if(n.c.length){
    const label=n.depth===0?"章节":(n.c[0].kind||"下一层");
    if(FILTER&&UPPER(n)){const M=subtree(n).filter(x=>x.depth>=2&&!x.c.some(()=>false)&&matchTag(x,FILTER));
      h+=`<div class="sec">符合「${esc(tagLabel(FILTER))}」的景点 · ${M.length}</div><div class="kids">${M.map((c,i)=>`<button class="kid" data-go="${c.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(c.n)}</b><small>${esc(c.disp.slice(0,-1).slice(1).join(" › ")||c.parent.n)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`).join("")}</div>`;}
    h+=`<div class="sec">${label} · ${n.c.length}</div><div class="kids">${n.c.map((c,i)=>{const st=stateOf(n,c);if(st==="hide")return"";return `<button class="kid${st==="fade"?" fade":""}" data-go="${c.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${tiered(n)&&c.star?'<i class="star">★</i>':""}${esc(c.n)}</b>${passMini(c)}<small>${esc(c.d)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`}).join("")}</div>`;
  }
  const rel=n.depth>=2?related(n):[];
  if(rel.length)h+=`<div class="sec">同类推荐</div><div class="rel">${rel.map(m=>`<button class="relc" data-go="${m.id}"><b>${esc(m.n)}</b><small>${esc(m.parent.n)} · ${m.t.filter(t=>n.t.includes(t)).map(t=>TAGS[t]).join(" / ")}</small></button>`).join("")}</div>`;
  h+=localFood(n);h+=localWild(n);
  h+=srcBlock(n);
  if(n.depth>=1)h+=`<div class="folder mono">图片文件夹：${CFG.folder}\\${esc(n.folders.join("\\"))}</div>`;
  return h+`<span class="folio">${pg(n.page*2)} / ${pg(total*2)}</span>`;
}

const PREFJA=CFG.PREFJA||{},PREFZH=CFG.PREFZH||{};
function foodBlock(t){
  let h="";
  if(t.img&&CIMG[t.img]){const c=CIMG[t.img];h+=`<figure class="photo hero termimg${c.ai?" ai":""}"><img src="${c.src}" alt="${esc(t.n)}"><figcaption>${cap(c)}</figcaption></figure>`}
  else if(t.k==="美食")h+=`<div class="photo ext termimg">${extBox("https://www.google.com/search?tbm=isch&q="+encodeURIComponent(t.ja),"")}</div>`;
  return h}
function foodInfo(t){let h="";
  if(t.sm&&t.sm.length){const pct=x=>((x-1)/12*100).toFixed(2);
    h+=`<div class="scal"><div class="sec">时令</div><div class="scgrid"><div class="scrow"><span class="scl">最佳时期</span><div class="sctrack">${t.sm.map(([a,b,l])=>`<i class="sc-food" style="left:${pct(a)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%"${l?` title="${esc(l)}"`:""}></i>`).join("")}</div></div><div class="scrow scm"><span class="scl"></span><div class="sctrack">${[1,2,3,4,5,6,7,8,9,10,11,12].map(m=>`<span style="left:${((m-0.5)/12*100).toFixed(2)}%">${m}</span>`).join("")}</div></div></div>
    <ul class="evl">${[...new Set(t.sm.map(x=>x[2]).filter(Boolean))].map(l=>{const ss=t.sm.filter(x=>x[2]===l);let sg=ss.map(x=>[x[0],x[1]]);const wr=sg.find(x=>x[1]>=13),st=sg.find(x=>x[0]<=1.01);if(wr&&st&&wr!==st){sg=sg.filter(x=>x!==wr&&x!==st);sg.unshift([wr[0],st[1]+12])}
      return `<li><b>${esc(l)}</b><span>${sg.map(([a,b])=>{const B=b>13?b-12:b;const A=mlabel(a),Z=(b>13?"次年":"")+mlabel(B-0.01);return A+(Z!==A?"–"+Z:"")}).join("、")}</span></li>`}).join("")}</ul></div>`}
  const w=(t.w||[]).filter(x=>NODES[x]);
  if(w.length)h+=`<div class="sec">产地 · 在哪里吃</div><div class="cloud">${w.map(x=>`<button class="tag" data-go="${x}">${esc(NODES[x].n)}</button>`).join("")}</div>`;
  if(t.q){const kw=t.q,pj=CFG.food.pj!=null?CFG.food.pj:(PREFJA[t.pref]||"");
    h+=`<div class="sec">搜索热门餐厅</div><p class="foodlinks">${CFG.food.site==="tabelog"?`<a href="https://tabelog.com/${t.pref?t.pref+"/":""}rstLst/?sk=${encodeURIComponent(kw)}&SrtT=rt" target="_blank" rel="noopener">食べログ 评分排行 ↗</a>`:`<a href="https://www.tripadvisor.com/Search?q=${encodeURIComponent(kw+" "+CFG.food.en)}" target="_blank" rel="noopener">Tripadvisor ↗</a>`}<a href="https://www.google.com/maps/search/${encodeURIComponent(kw+" "+pj)}" target="_blank" rel="noopener">Google 地图 ↗</a><a href="https://www.dianping.com/ai-search?keyword=${encodeURIComponent((CFG.food.zh!=null?CFG.food.zh:(PREFZH[t.pref]||"")+" ")+t.n)}" data-dp="${esc((CFG.food.zh!=null?CFG.food.zh:(PREFZH[t.pref]||"")+" ")+t.n)}" data-dpk="${esc(t.n)}" target="_blank" rel="noopener">大众点评 ↗</a><span class="scnote" style="flex-basis:100%;margin:0">手机上点「大众点评」会在 App 里直接搜索这道菜，城市按 App 当前所选城市：${CFG.food.dpNote}</span><a href="https://www.google.com/search?q=${encodeURIComponent(kw+" "+pj+CFG.food.gq)}" target="_blank" rel="noopener">网页搜索 ↗</a></p><p class="scnote">本书不推荐具体店家。评分和营业信息以各网站为准。</p>`}
  return h;
}
function mlabel(x){const m=x>=13?12:Math.floor(x)>12?1:Math.floor(x);const d=x-Math.floor(x);return m+"月"+(d<0.34?"上旬":d<0.67?"中旬":"下旬")}
function localFood(n){const ids=new Set([n.id,...(n.depth<=1?[]:subtree(n).map(x=>x.id))]);if(n.depth===1)subtree(n).forEach(x=>ids.add(x.id));
  const fs=Object.entries(TERMS_).filter(([,t])=>t.k==="美食"&&(t.w||[]).some(x=>ids.has(x)));if(!fs.length)return "";
  return `<div class="sec">当地美食</div><div class="foods">${fs.map(([id,t])=>{const c=t.img&&CIMG[t.img];return `<button class="food" data-route="term-${id}">${c?`<img src="${c.src}" alt="" loading="lazy">`:`<span class="noimg">食</span>`}<b>${esc(t.n)}</b>${t.sm&&t.sm.length&&t.sm[0][2]&&t.sm[0][2]!==t.n?`<small>${esc(t.sm[0][2])}</small>`:""}</button>`}).join("")}</div>`}
function viaBlock(n){const V=(n.via||[]).filter(v=>NODES[v[0]]);if(!V.length)return "";return `<div class="sec">途经这里的徒步路线</div><div class="vias">${V.map(([id,l])=>`<button class="mylink" data-go="${id}">${esc(NODES[id].n)}${l?` <small>${esc(l)}</small>`:""} →</button>`).join("")}</div>`}
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
return `<div class="sec">行程地图</div><svg class="map planall" viewBox="0 0 600 440" data-fit="${fx.toFixed(1)} ${fy.toFixed(1)} ${Math.min(600,w).toFixed(1)}" role="img" aria-label="行程地图"><rect width="600" height="440" style="fill:var(--land)"/>${(typeof PLANBG!=="undefined"?PLANBG:BOOK.bg||"").replace("__HY__",HYPSO)}${lines}${mk}</svg><div class="pmlg">${ds.map((d,i)=>`<button data-planmap="${d}" title="只看这一天"><i style="background:${DAYC[i%DAYC.length]}"></i>第${i+1}天 · ${PLAN[d].length} 处</button>`).join("")}</div><p class="scnote">圆点颜色代表日期，数字是第几天，虚线按当天顺序连接；点圆点进入景点页，点下方的日期只看那一天。</p>`}
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
const BMLIST=CFG.basemaps||["osm"];let BMPREF=null;try{BMPREF=localStorage.getItem(CFG.id+"-bm");if(BMPREF!=="off"&&!BMLIST.includes(BMPREF))BMPREF=null}catch(_){}
function bmOf(svg){if(svg.__bm!==undefined)return svg.__bm;const p=svg.querySelector("g.geoP");if(!p)return "off";if(BMPREF==="off")return "off";const[cx,cy,cl,k]=p.dataset.p.split(" ").map(Number);return (BMPREF&&BMS[BMPREF]&&k*cl>900)?BMPREF:(k*cl>900?BMLIST[0]:"off")}
function bmCycle(svg){const o=["off",...BMLIST];const cur=bmOf(svg);const nx=o[(o.indexOf(cur)+1)%o.length];svg.__bm=nx;BMPREF=nx;try{localStorage.setItem(CFG.id+"-bm",nx)}catch(_){}
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
if(CFG.feat.zoom){new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1&&!(n.classList&&n.classList.contains("zw")))zScan(n)}))).observe(document.documentElement,{childList:true,subtree:true});
document.addEventListener("DOMContentLoaded",()=>zScan(document));setTimeout(()=>zScan(document),0);}
function passBlock(t){if(!t||(!t.buy&&!t.notes))return "";return `${t.buy&&t.buy.length?`<div class="sec">购票</div><div class="buy">${t.buy.map(([l,u])=>`<a class="buybtn" href="${esc(u)}" target="_blank" rel="noopener">${esc(l)} ↗</a>`).join("")}</div>`:""}${t.notes&&t.notes.length?`<div class="sec">注意事项</div><ol class="notes">${t.notes.map(x=>`<li>${lk(x)}</li>`).join("")}</ol><p class="scnote">票价与规则核对于 2026 年 11 月，每年可能调整，购买前请以官网为准。</p>`:""}`}
function termPages(id){
  const t=TERMS_[id];const back=(BACK[id]||[]);
  const L=`<span class="eyebrow">词条 · ${esc(t.k)}</span><div class="tagtitle termtitle">${esc(t.n)}</div><div class="ja mono">${esc(t.ja)}</div>
  <p class="intro" style="margin-top:14px">${esc(t.d)}</p>${passBlock(t)}${foodBlock(t)}${t.svg?`<figure class="termsvg">${t.svg}</figure>`:""}<p class="wiki">维基百科：<a href="https://zh.wikipedia.org/w/index.php?search=${encodeURIComponent(t.n.split("（")[0])}" target="_blank" rel="noopener">中文 ↗</a> · <a href="https://${CFG.wiki.lang}.wikipedia.org/w/index.php?search=${encodeURIComponent(t.ja.split("（")[0])}" target="_blank" rel="noopener">${CFG.wiki.label} ↗</a></p>${(t.rel||[]).filter(r=>TERMS_[r]).length?`<div class="sec">相关词条</div><div class="cloud">${t.rel.filter(r=>TERMS_[r]).map(r=>`<button class="tag" data-route="term-${r}">${esc(TERMS_[r].n)}</button>`).join("")}</div>`:""}
  <p style="margin-top:22px"><button class="btn" data-route="terms">← 词典总目</button></p><span class="folio">词</span>`;
  const R=`<div class="kicker"><span class="kind">词条</span><span>${t.k==="美食"?"时令 · 产地 · 餐厅搜索":t.k==="地质与地貌"?"地貌 · 在哪里能看到":WILDK(t)?"季节 · 常见地区":"在书中出现的位置"}</span></div><h1>${esc(t.n)}</h1>${WILDK(t)?wildInfo(t):foodInfo(t)}${back.length?`<div class="sec">出现在 · ${back.length}</div><div class="kids">${back.map((n,i)=>`<button class="kid" data-go="${n.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(n.n)}</b><small>${esc(n.disp.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small></span><em>P.${pg(n.page*2-1)}</em></button>`).join("")}</div>`:t.k==="美食"||WILDK(t)?"":`<p class="intro" style="margin-top:14px">目前书中还没有页面提到这个词条。</p>`}<span class="folio">词</span>`;
  return [L,R];
}
const TSEQ=()=>TCATS.flatMap(c=>Object.keys(TERMS_).filter(id=>TERMS_[id].k===c));
function termIndex(){
  const by=c=>Object.entries(TERMS_).filter(([,t])=>t.k===c);
  const L=`<span class="eyebrow">词典</span><div class="tagtitle">词典</div><p style="color:var(--ink-2)">${CFG.termIntro}点正文中的下划线会先弹出小卡片，再点「查看词条」进入这里。</p>
  <div class="cloud">${TCATS.map(c=>`<a class="tag" href="#tc-${encodeURIComponent(c)}" data-tjump="${esc(c)}">${esc(c)} <span class="mono" style="opacity:.6">${by(c).length}</span></a>`).join("")}</div><span class="folio">词</span>`;
  const R=`<div class="kicker"><span class="kind">索引</span><span>共 ${Object.keys(TERMS_).length} 条</span></div><h1>词典</h1>${TCATS.map(c=>`<div class="sec" id="tc-${esc(c)}">${esc(c)} · ${by(c).length}</div><div class="kids">${by(c).map(([id,t],i)=>`<button class="kid" data-route="term-${id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(t.n)}</b><small>${esc(t.d.slice(0,34))}…</small></span><em>${(BACK[id]||[]).length||""}</em></button>`).join("")}</div>`).join("")}<span class="folio">词</span>`;
  return [L,R];
}
function lca(ids){const ch=id=>{const a=[];let n=NODES[id];while(n){a.unshift(n);n=n.parent}return a};const cs=ids.map(ch);let i=0;while(cs.every(c=>c[i]&&c[i]===cs[0][i]))i++;let n=cs[0][Math.max(0,i-1)]||BOOK;if(!n.c.length&&n.parent)n=n.parent;if(ids.length===1&&NODES[ids[0]].parent)n=NODES[ids[0]].parent;return n}
function planPages(){
  const ds=planDates();
  const L=`<span class="eyebrow">个人</span><div class="tagtitle">旅行计划</div>${pvBar()}${CFG.feat.planMap&&planDates().length?planMapHtml(planDates()):""}
  <p style="color:var(--ink-2)">在任意景点页标题下的「旅行计划」里选一个日期并点「加入行程」，景点就会按日期排进这张行程单；也可以在每天下方的输入框直接搜索添加。用 ↑↓ 调整顺序，手机上向左滑可以删除（电脑上鼠标移上去点「删除」），时间会按顺序自动重算；点「在地图上看」会打开能涵盖当天所有景点的地图，并只显示当天的景点。地图上方的筛选里也可以直接选「第 N 天」。</p>
  ${ds.length?`<div class="plandays">${ds.map((d,i)=>`<div class="pday"><a href="#pd-${d}" data-pjump="${d}"><b>第${i+1}天</b><span>${fmtD(d,true)}</span><em>${PLAN[d].length} 处</em></a><button class="btn sm" data-planmap="${d}">在地图上看</button></div>`).join("")}</div>`:'<p style="color:var(--muted)">还没有安排任何日期。</p>'}
  <p style="margin-top:14px"><button class="btn" data-route="mytags">导出 / 导入（在「我的标签」页）</button> <button class="btn" data-planclear="1">${PLAN_CLEAR?"再点一次确认清空":"清空行程"}</button></p><span class="folio">PLAN</span>`;
  const R=`<div class="kicker"><span class="kind">行程单</span><span>${ds.length?fmtD(ds[0])+" – "+fmtD(ds[ds.length-1])+" · 共 "+ds.length+" 天":"空"}</span></div><h1>旅行计划</h1>${ds.length?ds.map((d,i)=>`<div class="sec" id="pd-${d}">第${i+1}天 · ${fmtD(d,true)} · ${PLAN[d].length} 处</div>${planDayHtml(d)}`).join(""):`<p class="intro" style="margin-top:14px">这里还是空的。翻到任何一个景点，在标题下方的「旅行计划」里选好日期，点「加入行程」。</p>`}<span class="folio">PLAN</span>`;
  return [L,R];
}
let PLAN_CLEAR=false;
function myPages(){
  const tags=myAll().filter(x=>Object.values(MY).some(a=>a.includes(x)));
  const L=`<span class="eyebrow">个人</span><div class="tagtitle">我的标签</div>
  <p style="color:var(--ink-2)">在任意景点页点「♡ 收藏」「想去」「已去过」，或添加自己的标签，就会汇总到这里。标签只保存在这台设备的浏览器里，换设备时可以用下面的导出和导入。</p>
  <div class="cloud">${tags.length?tags.map(x=>`<a class="tag" href="#mt-${encodeURIComponent(x)}" data-jump="${esc(x)}">${esc(x)} <span class="mono" style="opacity:.6">${Object.values(MY).filter(a=>a.includes(x)).length}</span></a>`).join(""):'<span style="color:var(--muted)">还没有保存任何景点。</span>'}</div>
  <div class="myio"><button class="btn" data-myexport="1">导出我的标签</button><button class="btn" data-myimport="1">导入</button><button class="btn" data-myclear="1">${CLEAR_ARMED?"再点一次确认清空":"清空全部"}</button></div>
  <textarea id="myio-text" class="myio-text" rows="4" placeholder="导出的内容会出现在这里；导入时把之前导出的内容粘贴到这里，再点「导入」。"></textarea><p class="status" id="myio-status"></p><span class="folio">MY</span>`;
  const R=`<div class="kicker"><span class="kind">清单</span><span>按标签分组</span></div><h1>我的标签</h1>${tags.length?tags.map(x=>{const L2=ORDER.filter(n=>(MY[n.id]||[]).includes(x));
    return `<div class="sec" id="mt-${esc(x)}">${esc(x)} · ${L2.length}</div><div class="kids">${L2.map((n,i)=>`<div class="kid myk"><span class="n">${String(i+1).padStart(2,"0")}</span><button class="mylink" data-go="${n.id}"><b>${esc(n.n)}</b><small>${esc(n.disp.slice(0,-1).join(" › ")||"总览")}</small></button><button class="myx" data-myremove="${n.id}|${esc(x)}" aria-label="从「${esc(x)}」移除">×</button></div>`).join("")}</div>`}).join(""):`<p class="intro" style="margin-top:14px">这里还是空的。翻到任何一个景点，在标题下方的「我的标签」里点一下，就能把它存进来。</p>`}<span class="folio">MY</span>`;
  return [L,R];
}
function guidePages(){
  const N=ORDER.filter(n=>n.depth>=2&&(!CFG.guide.leaves||!n.c.length)).length;
  const L=`<div class="gcover"><span class="eyebrow">${CFG.guide.eyebrow}</span><div class="cover-t">${CFG.title}</div><p class="cover-s">${CFG.guide.lead.replace("{N}",N)}</p>
  <div class="cover-img">${BOOK.img&&IMGS[BOOK.img]?`<img src="${IMGS[BOOK.img]}" alt="${esc(BOOK.n)}插画地图">`:mapSVG(BOOK)}</div><button class="btn pri" data-go="root">开始阅读 →</button></div>`;
  const S=CFG.guide.sections;
  const R=`<div class="kicker"><span class="kind">使用说明</span><span>第一次阅读请看这里</span></div><h1>怎样使用这本书</h1>${S.map(([h,p],i)=>`<div class="guide"><span class="gn">${String(i+1).padStart(2,"0")}</span><div><b>${h}</b><p>${p}</p></div></div>`).join("")}<span class="folio">ii</span>`;
  return [L,R];
}
let CLEAR_ARMED=false;

function seasonTagPages(t,list,T=t){
  const segOf=n=>(n.sm&&n.sm[t])||null;
  const rows=list.map(n=>({n,seg:segOf(n)||SC_DEF[t]||[],est:!segOf(n)})).filter(r=>r.seg.length);
  const nost=list.filter(n=>!rows.find(r=>r.n===n));
  const key=r=>{const a=r.seg.map(s=>s[0]);/* 跨年段：12 月底算在最前 */return Math.min(...a.map(x=>x>=12.5&&t!==CFG.SC_WRAP?x-12:x))};
  rows.sort((a,b)=>key(a)-key(b)||a.n.page-b.n.page);
  const pct=x=>((x-1)/12*100).toFixed(2);
  const fmt=x=>{const m=Math.floor(x)>12?1:Math.floor(x);const d=x-Math.floor(x);return m+"月"+(d<0.34?"上旬":d<0.67?"中旬":"下旬")};
  const span=seg=>{if(seg.some(x=>x[2]))return [...seg].sort((x,y)=>x[0]-y[0]).map(x=>`<b>${esc(x[2])}</b> ${esc(x[3]||"")}`).join("<br>");let sg=seg.map(x=>[...x]);const w=sg.find(x=>x[1]>=13),f=sg.find(x=>x[0]<=1.01);if(w&&f&&w!==f){sg=sg.filter(x=>x!==w&&x!==f);sg.unshift([w[0],f[1]+12])}
    const one=([a,b])=>{const A=fmt(a),B=fmt(Math.min(b-0.01,b>13?b-12:12.99)>12?Math.min(b-0.01,b>13?b-12:12.99)-12:Math.min(b-0.01,b>13?b-12:12.99));if(A===B)return A;return Math.floor(a)===Math.floor(b>13?b-12:Math.min(b-0.01,12.99))&&b<13?A+"–"+B.replace(/^\d+月/,""):A+"–"+B};
    return sg.map(one).join("、")};
  const plans=Object.keys(PLAN||{}).filter(d=>(PLAN[d]||[]).length).map(d=>{const x=new Date(d);return x.getMonth()+1+(x.getDate()-1)/31});
  const axis=`<div class="scrow scm"><span class="scl"></span><div class="sctrack">${[1,2,3,4,5,6,7,8,9,10,11,12].map(m=>`<span style="left:${((m-0.5)/12*100).toFixed(2)}%">${m}</span>`).join("")}</div></div>`;
  const others=SC_TAGS.filter(k=>TAGCOUNT[k]);
  const L=`<span class="eyebrow">时令</span><div class="tagtitle">${esc(tagLabel(T))}</div>${subBar(ORDER.filter(n=>hasTag(n,t)),T,"data-tag")}<p style="color:var(--ink-2)">共 ${list.length} 处，分布在 ${new Set(list.map(n=>(n.disp[0]||""))).size} 个地区。右侧按时间先后排列，色条是往年的大致最佳时期，点景点名可跳转。</p>
   <div class="cloud">${others.map(k=>`<button class="tag${k===t?" cur":""}" data-tag="${k}">${esc(TAGS[k])} <span class="mono" style="opacity:.6">${TAGCOUNT[k]}</span></button>`).join("")}</div>
   <div class="sec" style="margin-top:22px">时令总览</div><div class="scal"><div class="scgrid">${others.map(k=>{const ns=ORDER.filter(n=>hasTag(n,k));const segs=ns.flatMap(n=>(n.sm&&n.sm[k])||SC_DEF[k]||[]);return `<div class="scrow"><button class="scl scbtn" data-tag="${k}">${esc(TAGS[k])}</button><div class="sctrack">${segs.map(([a,b])=>`<i class="sc-${k}" style="left:${pct(a)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%;opacity:${k===t?.35:.18}"></i>`).join("")}</div></div>`}).join("")}${axis}</div></div>
   <p class="scnote">色条为往年大致时期，每年会有前后浮动，${CFG.SC_NOTE}${(CFG.SC_NOTE_T||{})[t]||""}</p><span class="folio">时令</span>`;
  const R=`<div class="kicker"><span class="kind">时令月历</span><span>按时间先后</span></div><h1>${esc(TAGS[t])}</h1>
   <div class="scal sclist" data-noswipe${t==="matsuri"?` style="--spw:170px"`:""}>${plans.length?`<div class="scplanlab">竖线 = 你的行程日期</div>`:""}<div class="scgrid">${axis}${rows.map(r=>`<div class="scrow scitem"><button class="scl scname" data-go="${r.n.id}" title="${esc(r.n.n)}"><b>${esc(r.n.n)}</b><small>${esc(r.n.disp.slice(1,-1).join("·")||r.n.disp[0]||"")}</small></button><div class="sctrack">${r.seg.map(([a,b,nm,dt])=>`<i class="sc-${t}${r.est?" est":""}" style="left:${pct(a)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%"${nm?` title="${esc(nm+" "+(dt||""))}"`:""}></i>`).join("")}${plans.map(m=>`<b class="scpl" style="left:${pct(m)}%"></b>`).join("")}</div><span class="scspan${t==="matsuri"?" wide":""}">${span(r.seg)}</span></div>`).join("")}${axis}</div></div>
   ${nost.length?`<p class="scnote">另有 ${nost.length} 处暂无时期资料：${nost.map(n=>`<button class="linkish" data-go="${n.id}">${esc(n.n)}</button>`).join("、")}</p>`:""}<span class="folio">时令</span>`;
  return [L,R];
}
function tagPages(T){
  const t=T.split("&")[0],list=ORDER.filter(n=>matchTag(n,T));
  const L=`<span class="eyebrow">标签</span><div class="tagtitle">${esc(TAGS[t])}</div>${TAG_PARENT[t]?`<p style="margin:0 0 6px"><span class="eyebrow">上级标签</span> <button class="tag" data-tag="${TAG_PARENT[t]}">${esc(TAGS[TAG_PARENT[t]])}</button></p>`:""}${TAG_KIDS[t]?`<p style="margin:0 0 6px"><span class="eyebrow">包含</span> ${TAG_KIDS[t].filter(k=>TAGCOUNT[k]).map(k=>`<button class="tag" data-tag="${k}">${esc(TAGS[k])} ${TAGCOUNT[k]}</button>`).join(" ")}</p>`:""}${subBar(ORDER.filter(n=>hasTag(n,t)),T,"data-tag")}<p style="color:var(--ink-2)">共 ${list.length} 处，分布在 ${new Set(list.map(n=>(n.disp[0]||"")) ).size} 个地区。点击右侧任意条目跳转。</p>
   <div class="cloud">${Object.keys(TAGS).filter(k=>TAGCOUNT[k]&&(!SUBHIDE.has(k)||k===t)).map(k=>`<button class="tag${k===t?" cur":""}" data-tag="${k}">${esc(TAGS[k])} <span class="mono" style="opacity:.6">${TAGCOUNT[k]}</span></button>`).join("")}</div><span class="folio">TAG</span>`;
  if(SC_TAGS.includes(t))return seasonTagPages(t,list,T);
  const R=`<div class="kicker"><span class="kind">索引</span><span>按书页顺序</span></div><h1>${esc(tagLabel(T))}</h1><div class="kids" style="margin-top:14px">${list.map((n,i)=>`<button class="kid" data-go="${n.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(n.n)}</b><small>${esc(n.disp.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small></span><em>P.${pg(n.page*2-1)}</em></button>`).join("")}</div><span class="folio">TAG</span>`;
  return [L,R];
}

/* ---------- navigation + page turn ---------- */
let cur="n-root";
const spread=$("#spread"),Lp=$("#L"),Rp=$("#R");
const wide=()=>matchMedia("(min-width:861px)").matches;
const reduced=()=>matchMedia("(prefers-reduced-motion:reduce)").matches;
function parseRoute(r){if(r==="guide")return{guide:true};if(r==="mytags")return{mytags:true};if(r==="plan")return{plan:true};if(r==="autoplan")return{auto:true};if(r.startsWith("trip-")&&r.length>6)return{trip:r.slice(5)};if(r==="terms")return{terms:true};if(r.startsWith("term-")&&TERMS_[r.slice(5)])return{term:r.slice(5)};if(r.startsWith("tag-")&&TAGS[r.slice(4).split("&")[0]])return{tag:r.slice(4)};const id=r.startsWith("n-")?r.slice(2):"root";return{node:NODES[id]||BOOK}}
function seqIndex(r){const p=parseRoute(r);return p.guide?0:p.node?p.node.page:-1}
function render(route,animate=true,dir){
  const prevRoute=cur;if(route!==prevRoute){FILTER=PENDING_FILTER;FBAR_OPEN=false}PENDING_FILTER=null;cur=route;const p=parseRoute(route);
  let L,R;if(p.guide)[L,R]=guidePages();else if(p.mytags)[L,R]=myPages();else if(p.plan)[L,R]=planPages();else if(p.auto)[L,R]=autoPages();else if(p.trip)[L,R]=tripPages(p.trip);else if(p.terms)[L,R]=termIndex();else if(p.term)[L,R]=termPages(p.term);else if(p.tag)[L,R]=tagPages(p.tag);else{L=leftPage(p.node);R=rightPage(p.node)}
  if(dir==null){const a=seqIndex(prevRoute),b=seqIndex(route);dir=(b<0||a<0)?1:(b>=a?1:-1)}
  const doFlip=animate&&wide()&&!reduced()&&prevRoute!==route;
  if(doFlip){
    const oldL=Lp.cloneNode(true),oldR=Rp.cloneNode(true);oldL.removeAttribute("id");oldR.removeAttribute("id");
    Lp.innerHTML=L;Rp.innerHTML=R;Lp.scrollTop=Rp.scrollTop=0;
    const newL=Lp.cloneNode(true),newR=Rp.cloneNode(true);newL.removeAttribute("id");newR.removeAttribute("id");
    spread.querySelectorAll(".cover,.leaf").forEach(e=>e.remove());
    const cover=document.createElement("div");cover.className="cover";const leaf=document.createElement("div");leaf.className="leaf";
    const front=document.createElement("div");front.className="face front";const back=document.createElement("div");back.className="face back";
    if(dir>0){cover.style.left="0";cover.appendChild(oldL);leaf.style.left="50%";leaf.style.transformOrigin="left center";front.appendChild(oldR);back.appendChild(newL)}
    else{cover.style.left="50%";cover.appendChild(oldR);leaf.style.left="0";leaf.style.transformOrigin="right center";front.appendChild(oldL);back.appendChild(newR)}
    leaf.append(front,back);spread.append(cover,leaf);
    requestAnimationFrame(()=>requestAnimationFrame(()=>{leaf.classList.add("turning");leaf.style.transform=`rotateY(${dir>0?-180:180}deg)`}));
    setTimeout(()=>{cover.remove()},380);
    setTimeout(()=>{leaf.remove()},800);
  } else {
    Lp.innerHTML=L;Rp.innerHTML=R;
    if(animate&&!wide()&&prevRoute!==route){spread.classList.remove("slide");void spread.offsetWidth;spread.classList.add("slide");window.scrollTo({top:0,behavior:reduced()?"auto":"smooth"})}
  }
  crumbs(p);edges(p);if(!$("#toc").hidden)buildTree();
}
function crumbs(p){
  const chain=[];let n=p.node;while(n){chain.unshift(n);n=n.parent}
  let h=p.guide?`<span class="cur">使用说明</span>`:p.auto?`<button data-go="root">${esc(BOOK.n)}</button> › <button data-route="plan">旅行计划</button> › <span class="cur">自动生成行程</span>`:p.trip?`<button data-go="root">${esc(BOOK.n)}</button> › <button data-route="plan">旅行计划</button> › <span class="cur">收到的行程</span>`:p.mytags?`<button data-go="root">${esc(BOOK.n)}</button> › <span class="cur">我的标签</span>`:p.plan?`<button data-go="root">${esc(BOOK.n)}</button> › <span class="cur">旅行计划</span>`:p.terms?`<button data-go="root">${esc(BOOK.n)}</button> › <span class="cur">词典</span>`:p.term?`<button data-go="root">${esc(BOOK.n)}</button> › <button data-route="terms">词典</button> › <span class="cur">${esc(TERMS_[p.term].n)}</span>`:p.tag?`<button data-go="root">${esc(BOOK.n)}</button> › <span class="cur">标签 · ${esc(tagLabel(p.tag))}</span>`:
    chain.map((c,i)=>i===chain.length-1?`<span class="cur">${esc(c.n)}</span>`:`<button data-go="${c.id}">${esc(c.n)}</button>`).join(" › ");
  $("#crumbs").innerHTML=h;
}
function edges(p){
  if(p.guide){$("#prevBtn").disabled=true;$("#nextBtn").disabled=false;syncTab();$("#prevBtn").title="";$("#nextBtn").title="下一页："+BOOK.n;return}
  if(CFG.feat.termPaging&&(p.terms||p.term)){const L=TSEQ(),j=p.term?L.indexOf(p.term):-1;$("#prevBtn").disabled=!p.term;$("#nextBtn").disabled=j>=L.length-1;syncTab();$("#prevBtn").title=j>0?"上一页："+TERMS_[L[j-1]].n:j===0?"上一页：词典索引":"";$("#nextBtn").title=j<L.length-1?"下一页："+TERMS_[L[j+1]].n:"";return}
  const i=p.node?p.node.page-1:-1;
  $("#prevBtn").disabled=i<0;$("#nextBtn").disabled=i<0||i>=total-1;
  syncTab();$("#prevBtn").title=i>0?"上一页："+ORDER[i-1].n:i===0?"上一页：使用说明":"";$("#nextBtn").title=i>=0&&i<total-1?"下一页："+ORDER[i+1].n:"";
}
let HIST=[],BACKNAV=false;
function go(route,dir){if(route===cur)return;if(!BACKNAV){HIST.push(cur);if(HIST.length>60)HIST.shift()}BACKNAV=false;try{history.replaceState(null,"","#"+route)}catch(e){}if(location.hash!=="#"+route){suppress=true;location.hash=route}render(route,true,dir)}
let suppress=false;
addEventListener("hashchange",()=>{if(suppress){suppress=false;return}render(location.hash.slice(1)||"guide")});
const goNode=id=>go("n-"+id);
$("#prevBtn").onclick=()=>{const p=parseRoute(cur);if(CFG.feat.termPaging&&(p.terms||p.term)){const L=TSEQ(),i=p.term?L.indexOf(p.term):-1;if(i>0)go("term-"+L[i-1],-1);else if(i===0)go("terms",-1);return}if(p.node&&p.node.page===1){go("guide",-1);return}if(p.node&&p.node.page>1)go("n-"+ORDER[p.node.page-2].id,-1)};
$("#nextBtn").onclick=()=>{const p=parseRoute(cur);if(CFG.feat.termPaging&&(p.terms||p.term)){const L=TSEQ(),i=p.term?L.indexOf(p.term):-1;if(i<L.length-1)go("term-"+L[i+1],1);return}if(p.guide){go("n-root",1);return}if(p.node&&p.node.page<total)go("n-"+ORDER[p.node.page].id,1)};
$("#home").onclick=()=>goNode("root");
addEventListener("keydown",e=>{if(e.target.matches("input"))return;
  if(e.key==="ArrowRight")$("#nextBtn").click();else if(e.key==="ArrowLeft")$("#prevBtn").click();
  else if(e.key==="Backspace"){const p=parseRoute(cur);if(p.node?.parent)go("n-"+p.node.parent.id,-1)}
  else if(e.key==="/"){e.preventDefault();$("#q").focus()}
  else if(e.key==="Escape"){closeAll();hidePop()}
  if(e.target.matches(".mk")&&e.key==="Enter")goNode(e.target.dataset.go)});

document.addEventListener("change",e=>{if(e.target.matches("[data-eng]")){ENGINE=e.target.value;try{localStorage.setItem((CFG.id+"-engine"),ENGINE)}catch(err){}render(cur,false)}});
document.addEventListener("keydown",e=>{if(e.target.id==="mytag-input"&&e.key==="Enter"){e.preventDefault();addMy()}},true);
function addMy(){const inp=document.getElementById("mytag-input");const p=parseRoute(cur);if(!inp||!p.node)return;const v=inp.value.trim().slice(0,12);if(!v)return;MY[p.node.id]=[...new Set([...(MY[p.node.id]||[]),v])];saveMy();refreshMine()}
const pop=document.createElement("div");pop.className="tpop";pop.hidden=true;pop.setAttribute("role","dialog");document.body.appendChild(pop);
function showPop(el){const id=el.dataset.term,t=TERMS_[id];if(!t)return;
  pop.innerHTML=`<div class="tp-h"><b>${esc(t.n)}</b><span class="mono">${esc(t.ja)}</span><em>${esc(t.k)}</em><button class="tp-x" data-popclose="1" aria-label="关闭">×</button></div>${t.img&&CIMG[t.img]?`<img class="tp-img" src="${CIMG[t.img].src}" alt="">`:""}<p>${esc(t.d)}</p>${t.svg?`<div class="tp-svg">${t.svg}</div>`:""}<button class="tp-go" data-route="term-${id}">查看词条${(BACK[id]||[]).length>1?` · 书中 ${(BACK[id]||[]).length} 处提到`:""} →</button>`;
  pop.hidden=false;const r=el.getBoundingClientRect(),W=Math.min(340,innerWidth-24);pop.style.width=W+"px";
  const left=Math.max(12,Math.min(innerWidth-W-12,r.left+r.width/2-W/2));pop.style.left=left+"px";
  const ph=pop.offsetHeight;const below=r.bottom+8+ph<innerHeight;pop.style.top=(below?r.bottom+8:Math.max(8,r.top-8-ph))+"px";}
const hidePop=()=>{pop.hidden=true};
addEventListener("scroll",e=>{if(e.target&&e.target.nodeType===1&&pop.contains(e.target))return;hidePop()},true);addEventListener("resize",hidePop);
document.addEventListener("click",e=>{
  if(e.target.closest("[data-planadd]")){const p=parseRoute(cur);const inp=document.getElementById("plan-date");const d=inp&&inp.value;if(!p.node||!d){inp&&inp.focus();return}LASTDATE=d;try{localStorage.setItem((CFG.id+"-plan-last"),d)}catch(err){}PLAN[d]=PLAN[d]||[];if(!PLAN[d].includes(p.node.id))PLAN[d].push(p.node.id);savePlan();refreshMine();return}
  const prm=e.target.closest("[data-planrm]");if(prm){const p=parseRoute(cur);const d=prm.dataset.planrm;PLAN[d]=(PLAN[d]||[]).filter(x=>x!==p.node.id);savePlan();refreshMine();return}
  const prm2=e.target.closest("[data-planrm2]");if(prm2){const [d,id]=prm2.dataset.planrm2.split("|");PLAN[d]=(PLAN[d]||[]).filter(x=>x!==id);savePlan();render(cur,false);return}
  const pmv=e.target.closest("[data-planmv]");if(pmv){const [d,id,dir]=pmv.dataset.planmv.split("|");const a=PLAN[d],i=a.indexOf(id),j=i+(+dir);if(j>=0&&j<a.length){[a[i],a[j]]=[a[j],a[i]];savePlan();render(cur,false)}return}
  const pmap=e.target.closest("[data-planmap]");if(pmap){const d=pmap.dataset.planmap;const n=lca(PLAN[d]);PENDING_FILTER="plan:"+d;closeAll();go("n-"+n.id);return}
  const pj=e.target.closest("[data-pjump]");if(pj){e.preventDefault();const el=document.getElementById("pd-"+pj.dataset.pjump);if(el)el.scrollIntoView({behavior:"smooth",block:"start"});return}
  if(e.target.closest("[data-planclear]")){if(!PLAN_CLEAR){PLAN_CLEAR=true;render(cur,false);setTimeout(()=>{PLAN_CLEAR=false},4000);return}PLAN={};savePlan();PLAN_CLEAR=false;render(cur,false);return}
  const tm=e.target.closest("[data-term]");if(tm){e.preventDefault();showPop(tm);return}
  if(e.target.closest("[data-popclose]")){hidePop();return}
  if(!e.target.closest(".tpop"))hidePop();
  const tc=e.target.closest("[data-tcat]");if(tc){const c=tc.dataset.tcat;closeAll();const jump=()=>{const el=document.getElementById("tc-"+c);if(el)el.scrollIntoView({behavior:"smooth",block:"start"})};if(cur==="terms")jump();else{go("terms");setTimeout(jump,500)}return}
  const tj=e.target.closest("[data-tjump]");if(tj){e.preventDefault();const el=document.getElementById("tc-"+tj.dataset.tjump);if(el)el.scrollIntoView({behavior:"smooth",block:"start"});return}
  const mt=e.target.closest("[data-mytoggle]");if(mt){const p=parseRoute(cur);if(!p.node)return;const v=mt.dataset.mytoggle;const a=MY[p.node.id]||[];MY[p.node.id]=a.includes(v)?a.filter(x=>x!==v):[...a,v];saveMy();refreshMine();return}
  if(e.target.closest("[data-myadd]")){addMy();return}
  const mr=e.target.closest("[data-myremove]");if(mr){const [id,v]=mr.dataset.myremove.split("|");MY[id]=(MY[id]||[]).filter(x=>x!==v);saveMy();render(cur,false);refreshMine();return}
  const rt=e.target.closest("[data-route]");if(rt){closeAll();hidePop();go(rt.dataset.route);return}
  const jp=e.target.closest("[data-jump]");if(jp){e.preventDefault();const el=document.getElementById("mt-"+jp.dataset.jump);if(el)el.scrollIntoView({behavior:"smooth",block:"start"});return}
  if(e.target.closest("[data-myexport]")){const s=JSON.stringify({mytags:MY,plan:PLAN});const ta=document.getElementById("myio-text");ta.value=s;ta.select();const st=document.getElementById("myio-status");
    (navigator.clipboard?navigator.clipboard.writeText(s):Promise.reject()).then(()=>st.textContent="已复制到剪贴板，也可以手动复制上面的内容。",()=>st.textContent="已选中上面的内容，请按 Ctrl+C 复制。");return}
  if(e.target.closest("[data-myimport]")){const ta=document.getElementById("myio-text");const st=document.getElementById("myio-status");try{let o=JSON.parse(ta.value);if(o&&o.plan){Object.entries(o.plan).forEach(([d,a])=>{if(Array.isArray(a)){PLAN[d]=[...new Set([...(PLAN[d]||[]),...a.filter(x=>NODES[x])])]}});savePlan()}if(o&&o.mytags)o=o.mytags;let n=0;Object.entries(o).forEach(([k,a])=>{if(NODES[k]&&Array.isArray(a)){MY[k]=[...new Set([...(MY[k]||[]),...a.map(String)])];n++}});saveMy();render(cur,false);refreshMine();document.getElementById("myio-status").textContent="已导入 "+n+" 个景点的标签。"}catch(err){st.textContent="内容格式不对，请粘贴之前导出的完整内容。"}return}
  if(e.target.closest("[data-myclear]")){if(!CLEAR_ARMED){CLEAR_ARMED=true;render(cur,false);setTimeout(()=>{CLEAR_ARMED=false},4000);return}MY={};saveMy();CLEAR_ARMED=false;render(cur,false);refreshMine();return}
  if(e.target.closest("[data-fmore]")){FBAR_OPEN=!FBAR_OPEN;render(cur,false);return}
  const fc=e.target.closest("[data-filter]");if(fc){FILTER=fc.dataset.filter||null;render(cur,false);return}
  if(e.target.closest("[data-edit]")){editing=!editing;render(cur,false);return}
  if(e.target.closest("[data-copypins]")){copyPins();return}
  const rp=e.target.closest("[data-resetpins]");if(rp){NODES[rp.dataset.resetpins].c.forEach(c=>{if(DEF[c.id])[c.px,c.py]=DEF[c.id]});savePins();render(cur,false);return}
  if(e.target.closest(".imgmap.editing"))return;
  const g=e.target.closest("[data-go]");const t=e.target.closest("[data-tag]");const pi=e.target.closest("[data-pi]");
  if(pi){const n=parseRoute(cur).node;if(n){n._pi=+pi.dataset.pi;render(cur,false)}return}
  if(t&&(!g||g.contains(t))){closeAll();go("tag-"+t.dataset.tag);return}
  if(g){closeAll();goNode(g.dataset.go);return}
});

/* ---------- search ---------- */
const q=$("#q"),res=$("#results");let hits=[],sel=0;
function norm(s){return String(s||"").toLowerCase().replace(/[·・\s]/g,"")}
function search(s){
  const k=norm(s);if(!k){res.hidden=true;return}
  const tagHits=Object.keys(TAGS).filter(t=>norm(TAGS[t]).includes(k)&&TAGCOUNT[t]);
  const nodeHits=ORDER.map(n=>{const nm=norm(n.n)+norm(n.ja);let sc=0;
    if(nm.includes(k))sc+=10+(norm(n.n)===k?10:0);if(n.t.some(t=>norm(TAGS[t]).includes(k)))sc+=4;if(norm(n.d).includes(k))sc+=2;return{n,sc}})
    .filter(x=>x.sc>0).sort((a,b)=>b.sc-a.sc||a.n.page-b.n.page).slice(0,12).map(x=>x.n);
  const top=nodeHits[0];
  const suggestTags=top&&norm(top.n).includes(k)?top.t:[];
  const termHits=Object.entries(TERMS_).filter(([,t])=>[t.n,t.ja,...t.a].some(x=>norm(x).includes(k))).slice(0,8);
  hits=[...tagHits.map(t=>({tag:t})),...nodeHits.map(n=>({n}))];sel=0;
  let h="";
  if(termHits.length)h+=`<div class="grp">词条</div><div class="tagrow">${termHits.map(([id,t])=>`<button class="tag termtag" data-route="term-${id}">${esc(t.n)} <small>${esc(t.k)}</small></button>`).join("")}</div>`;
  if(tagHits.length)h+=`<div class="grp">标签</div><div class="tagrow">${tagHits.map(t=>`<button class="tag" data-tag="${t}">${esc(TAGS[t])} · ${TAGCOUNT[t]}</button>`).join("")}</div>`;
  if(nodeHits.length)h+=`<div class="grp">页面</div>`+nodeHits.map((n,i)=>`<div class="res${i===0&&!tagHits.length?" on":""}" role="button" tabindex="0" data-go="${n.id}"><b>${esc(n.n)}</b> <span class="mono" style="font-size:11px;color:var(--muted)">P.${pg(n.page*2-1)}</span><small>${esc(n.disp.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small><span class="chips" style="margin:3px 0 0">${n.t.slice(0,5).map(t=>chip(t,1)).join("")}</span></div>`).join("");
  if(suggestTags.length)h+=`<div class="grp">「${esc(top.n)}」相关标签，点击看同类景点</div><div class="tagrow">${suggestTags.map(t=>chip(t)).join("")}</div>`;
  if(!h)h=`<div class="grp" style="padding:10px">没有找到「${esc(s)}」。试试 寺、神社、抹茶、雪景。</div>`;
  res.innerHTML=h;res.hidden=false;if(!wide())res.style.top=(q.getBoundingClientRect().bottom+6)+"px";else res.style.top="";
}
q.addEventListener("input",()=>search(q.value));
q.addEventListener("focus",()=>q.value&&search(q.value));
q.addEventListener("keydown",e=>{
  const items=[...res.querySelectorAll(".res")];
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();if(!items.length)return;sel=(sel+(e.key==="ArrowDown"?1:-1)+items.length)%items.length;items.forEach((b,i)=>b.classList.toggle("on",i===sel));items[sel].scrollIntoView({block:"nearest"})}
  else if(e.key==="Enter"){const b=items[sel]||res.querySelector("[data-tag]");if(b)b.click()}
  else if(e.key==="Escape"){res.hidden=true;q.blur()}
});
document.addEventListener("pointerdown",e=>{if(!e.target.closest(".search"))res.hidden=true});

/* ---------- toc + assets ---------- */
const open=new Set(CFG.tocOpen);
function buildTree(){
  const curId=parseRoute(cur).node?.id;
  let n=NODES[curId];while(n){open.add(n.id);n=n.parent}
  const li=n=>`<li><div class="row">${n.c.length?`<button class="tg" data-tg="${n.id}" aria-label="展开">${open.has(n.id)?"▼":"▶"}</button>`:`<span class="tg"></span>`}<button class="nm${n.id===curId?" cur":""}" data-go="${n.id}">${esc(n.n)}</button><span class="pg">${pg(n.page*2-1)}</span></div>${n.c.length&&open.has(n.id)?`<ul>${n.c.map(li).join("")}</ul>`:""}</li>`;
  $("#tree").innerHTML=`<button class="nm guide-link${cur==="guide"?" cur":""}" data-route="guide">使用说明</button><ul>${li(BOOK)}</ul>`;
  $("#mytoc").innerHTML=`<button class="ti l0" data-route="mytags"><b>我的标签</b><span class="n">${myCount()}</span></button><button class="ti l0" data-route="plan"><b>旅行计划</b><span class="n">${planDates().length?planDates().length+" 天":""}</span></button><button class="ti l0" data-route="autoplan"><b>✨ 自动生成行程</b><span class="n"></span></button>`;
  $("#termtoc").innerHTML=`<button class="ti l0" data-route="terms"><b>词典总目</b><span class="n">${Object.keys(TERMS_).length}</span></button>`+TCATS.map(c=>`<button class="ti l1" data-tcat="${esc(c)}"><b>${esc(c)}</b><span class="n">${Object.values(TERMS_).filter(t=>t.k===c).length}</span></button>`).join("");
  const G=CFG.tocGroups;
  const used=new Set(G.flatMap(g=>g[1].split(" ").flatMap(DESC)));const rest=Object.keys(TAGS).filter(k=>!used.has(k)&&TAGCOUNT[k]&&!TAG_PARENT[k]&&!SUBHIDE.has(k));if(rest.length)G.push(["其他",rest.join(" ")]);
  const row=(k,l)=>TAGCOUNT[k]?`<button class="ti l${l}${G[0][1].includes(k)?" season":""}" data-tag="${k}"><b>${esc(TAGS[k])}</b><span class="n">${TAGCOUNT[k]}</span></button>`+(TAG_KIDS[k]||[]).map(c=>row(c,l+1)).join(""):"";
  $("#tagidx").innerHTML=G.map(([g,ks])=>`<div class="grp">${g}</div>`+ks.split(" ").map(k=>row(k,0)).join("")).join("");
}
$("#tree").addEventListener("click",e=>{const t=e.target.closest("[data-tg]");if(t){e.stopPropagation();const id=t.dataset.tg;open.has(id)?open.delete(id):open.add(id);buildTree()}});
function closeAll(){$("#assets").hidden=true;res.hidden=true;$("#toc").hidden=true;$("#scrim").hidden=true}
$("#tocBtn").onclick=()=>{buildTree();$("#toc").hidden=false;$("#scrim").hidden=false};
$("#scrim").onclick=()=>{$("#toc").hidden=true;$("#assets").hidden=true;$("#scrim").hidden=true};
$("#assetBtn").onclick=()=>{$("#assets").hidden=false;$("#scrim").hidden=false};
$("#assetsX").onclick=()=>$("#scrim").click();
const ps=ORDER.filter(n=>n.depth>0).map(n=>`New-Item -ItemType Directory -Force -Path ".\\${n.folders.join("\\")}" | Out-Null`).join("\n");
$("#ps").textContent=ps;
$("#copyPs").onclick=async()=>{try{await navigator.clipboard.writeText(ps);$("#copyStatus").textContent="已复制"}catch(e){const r=document.createRange();r.selectNodeContents($("#ps"));const s=getSelection();s.removeAllRanges();s.addRange(r);$("#copyStatus").textContent="已选中，按 Ctrl+C 复制"}};

render(location.hash.slice(1)||"guide",false);refreshMine();
loadStored();

/* ===== 手机：底部导航 + 左右滑动翻页 ===== */
function syncTab(){syncBack();const tp=$("#tbPrev"),tn=$("#tbNext");if(!tp)return;tp.disabled=!HIST.some(r=>r!==cur);tn.disabled=$("#nextBtn").disabled;
  $("#tbPlan").classList.toggle("on",cur==="plan"||cur==="mytags");try{const c=myCount();$("#tbCnt").textContent=c?String(c):""}catch(e){}}
if(!wide())$("#q").placeholder="搜索景点、标签";
$("#tbPrev").onclick=()=>{while(HIST.length&&HIST[HIST.length-1]===cur)HIST.pop();if(!HIST.length)return;BACKNAV=true;go(HIST.pop(),-1);syncTab()};$("#tbNext").onclick=()=>$("#nextBtn").click();if($("#backBtn"))$("#backBtn").onclick=()=>$("#tbPrev").click();
$("#tbToc").onclick=()=>$("#tocBtn").click();
$("#tbSearch").onclick=()=>{window.scrollTo({top:0});setTimeout(()=>$("#q").focus(),50)};
$("#tbPlan").onclick=e=>{e.stopPropagation();go(cur==="plan"?"mytags":"plan")};
(function(){let x0=0,y0=0,t0=0,ok=false,dx=0;const hint=$("#swipehint");
  const noSwipe=el=>el.closest("input,select,textarea,.tpop,.drawer,.modal,.results,.termsvg,.scal,[data-noswipe]")||(()=>{let a=el;while(a&&a!==document.body){if(a.scrollWidth>a.clientWidth+4&&/auto|scroll/.test(getComputedStyle(a).overflowX))return true;a=a.parentElement}return false})();
  const book=$(".book");
  book.addEventListener("touchstart",e=>{if(wide()||e.touches.length!==1){ok=false;return}const t=e.touches[0];x0=t.clientX;y0=t.clientY;t0=Date.now();dx=0;ok=!noSwipe(e.target)&&x0>18&&x0<innerWidth-18},{passive:true});
  book.addEventListener("touchmove",e=>{if(!ok)return;const t=e.touches[0];dx=t.clientX-x0;const dy=t.clientY-y0;if(Math.abs(dy)>Math.abs(dx)*1.1&&Math.abs(dy)>12){ok=false;hint.style.opacity=0;return}
    if(Math.abs(dx)>30){const next=dx<0;const btn=next?$("#nextBtn"):$("#prevBtn");if(btn.disabled){hint.style.opacity=0;return}hint.textContent=next?"›":"‹";hint.style.left=next?"auto":"10px";hint.style.right=next?"10px":"auto";hint.style.opacity=Math.min(1,(Math.abs(dx)-30)/50)}},{passive:true});
  book.addEventListener("touchend",()=>{hint.style.opacity=0;if(!ok)return;ok=false;const fast=Date.now()-t0<450;if(Math.abs(dx)>(fast?60:110)){(dx<0?$("#nextBtn"):$("#prevBtn")).click()}},{passive:true});
})();


/* 大众点评：手机上用 App 搜索菜名（城市按 App 当前所选城市），约 2 秒内没跳走就改开网页版 */
document.addEventListener("click",e=>{const a=e.target.closest("a[data-dp]");if(!a)return;
  if(!matchMedia("(pointer:coarse)").matches)return;
  e.preventDefault();const web=a.href,kw=a.dataset.dpk||a.dataset.dp;let left=false;const onHide=()=>{if(document.hidden)left=true};
  document.addEventListener("visibilitychange",onHide);
  location.href="dianping://searchshoplist?keyword="+encodeURIComponent(kw);
  setTimeout(()=>{document.removeEventListener("visibilitychange",onHide);if(!left&&!document.hidden){const w=window.open(web,"_blank");if(!w)location.href=web}},2000)},true);

})();
<