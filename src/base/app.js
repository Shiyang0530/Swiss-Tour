<script>
(()=>{
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
(function merge(n){if(typeof DEEP!=="undefined"&&DEEP[n.id])Object.assign(n,DEEP[n.id]);(n.c||[]).forEach(merge)})(BOOK);
const NODES={},ORDER=[],PATH={};
(function walk(n,p,depth,folders,underKyoto){
  n.parent=p;n.depth=depth;n.c=n.c||[];n.t=n.t||[];
  const fs=depth===0?[]:[...folders,n.f||n.n];n.folders=fs;n.key=fs.join("/");PATH[n.key]=n;
  const uk=underKyoto||n.id==="kyoto";
  n.kind=depth===0?"总览":depth===1?"地区":(uk?["","","区域","景点","看点"][depth]:["","","景点","看点"][depth]);
  NODES[n.id]=n;n.page=ORDER.push(n);
  n.c.forEach(c=>walk(c,n,depth+1,fs,uk));
})(BOOK,null,0,[],false);
const total=ORDER.length;
const TAG_PARENT={sengoku:"history",meiji:"history",myth:"history",literature:"history",unesco:"history",genji:"literature"};
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
function lk(s){const e=esc(s);if(!SEEN||!TRE)return e;return e.replace(TRE,m=>{const id=TMAP[m];if(SEEN.has(id))return m;SEEN.add(id);return `<button class="term" data-term="${id}">${m}</button>`})}
const nodeText=n=>[n.d,n.tip,...(n.hl||[]),...(n.hist||[]).map(x=>x[1]),...(n.arch||[]).map(x=>x[1]),...(n.cards||[]).flatMap(c=>[c.h,c.p])].filter(Boolean).join("\n");
const BACK={};if(TRE)ORDER.forEach(n=>{new Set(nodeText(n).match(TRE)||[]).forEach(m=>{const id=TMAP[m];(BACK[id]=BACK[id]||[]);if(!BACK[id].includes(n))BACK[id].push(n)})});
const srcOf=n=>n.src?n.src:(n.parent&&n.parent.src&&!n.c.length?n.parent.src:null);
function srcBlock(n){const s=srcOf(n);if(!s)return"";return `<div class="srcs"><span class="eyebrow">资料来源</span><ol>${s.map(k=>{const v=SRCS[k];return v?`<li><a href="${esc(v[1])}" target="_blank" rel="noopener">${esc(v[0])}</a></li>`:""}).join("")}</ol><p>内容依据以上资料整理；开放时间、票价和公开日期以官方发布为准。</p></div>`}

/* ---------- images (IndexedDB, per browser) ---------- */
const IMG={};
function dbOpen(){return new Promise((res,rej)=>{try{const r=indexedDB.open("kyoto-book",1);r.onupgradeneeded=()=>r.result.createObjectStore("img");r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)}catch(e){rej(e)}})}
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
const ENGINES={google:["Google","https://www.google.com/search?q="],bing:["Bing","https://www.bing.com/search?q="],baidu:["百度","https://www.baidu.com/s?wd="],yahoojp:["Yahoo! JAPAN","https://search.yahoo.co.jp/search?p="],duck:["DuckDuckGo","https://duckduckgo.com/?q="]};
let ENGINE="google";try{const e=localStorage.getItem("kyoto-engine");if(e&&ENGINES[e])ENGINE=e}catch(err){}
const searchURL=n=>ENGINES[ENGINE][1]+encodeURIComponent(ENGINE==="baidu"?n.n:(n.ja||n.n).split("（")[0]);
const PRESET=["收藏","想去","已去过"];
let PLAN={};try{PLAN=JSON.parse(localStorage.getItem("kyoto-plan")||"{}")||{}}catch(e){PLAN={}}
const savePlan=()=>{Object.keys(PLAN).forEach(d=>{PLAN[d]=(PLAN[d]||[]).filter(id=>NODES[id]);if(!PLAN[d].length)delete PLAN[d]});try{localStorage.setItem("kyoto-plan",JSON.stringify(PLAN))}catch(e){};try{pvSync()}catch(e){}};
const planDates=()=>Object.keys(PLAN).sort();
const datesOf=id=>planDates().filter(d=>PLAN[d].includes(id));
const WK="日一二三四五六";
const fmtD=(d,long)=>{const t=new Date(d+"T00:00:00");if(isNaN(t))return d;const s=(t.getMonth()+1)+"月"+t.getDate()+"日";return long?t.getFullYear()+"年"+s+" 周"+WK[t.getDay()]:s};
const dayNo=d=>planDates().indexOf(d)+1;
let LASTDATE="";try{LASTDATE=localStorage.getItem("kyoto-plan-last")||""}catch(e){}
/* ===== 旅行计划多版本 ===== */
let PV={cur:"",v:{}};
try{PV=JSON.parse(localStorage.getItem("kyoto-plans")||"null")||PV}catch(e){}
if(!PV.v)PV={cur:"",v:{}};
const pvSave=()=>{try{localStorage.setItem("kyoto-plans",JSON.stringify(PV))}catch(e){}};
const pvNew=(name,plan,meta,opt)=>{const id="v"+Date.now().toString(36);PV.v[id]={name,ts:Date.now(),plan:JSON.parse(JSON.stringify(plan||{})),meta:meta||{},opt:opt||null};PV.cur=id;pvSave();return id};
if(!PV.cur||!PV.v[PV.cur]){const ks=Object.keys(PV.v);if(ks.length)PV.cur=ks[0];else pvNew("我的行程",PLAN);}
function pvSync(){if(PV.v[PV.cur]){PV.v[PV.cur].plan=JSON.parse(JSON.stringify(PLAN));pvSave()}}
function pvSwitch(id){if(!PV.v[id])return;PV.cur=id;PLAN=JSON.parse(JSON.stringify(PV.v[id].plan||{}));savePlan();pvSave()}
const pvMeta=()=>(PV.v[PV.cur]&&PV.v[PV.cur].meta)||{};

/* ===== 自动生成行程 ===== */
const AP_BASES={auto:{n:"帮我推荐"},kyotost:{n:"京都站周边",g:[34.9858,135.7588]},kawara:{n:"京都市中心（四条河原町）",g:[35.0037,135.7686]},arashi:{n:"岚山",g:[35.0150,135.6780]},umeda:{n:"大阪（梅田）",g:[34.7025,135.4959]},namba:{n:"大阪（难波）",g:[34.6662,135.5013]},nara:{n:"奈良站周边",g:[34.6810,135.8196]}};
const AP_PACE={light:{n:"轻松",start:570,budget:330,max:3,night:0},mid:{n:"适中",start:540,budget:450,max:5,night:1},dense:{n:"密集",start:510,budget:570,max:7,night:1}};
const AP_TAG_G=[["时令","sakura momiji snow matsuri newyear"],["适合人群","elderly couple family"],["历史文化","history sengoku meiji genji literature myth unesco"],["寺社与建筑","temple shrine zen castle garden museum"],["自然风景","nature view hike lake beach onsen"],["吃喝玩乐","hot food tea street night shopping deer"],["实用","free"]];
const AP_TAGS=AP_TAG_G.flatMap(g=>g[1].split(" "));const AP_SEASON=["sakura","momiji","snow","matsuri","newyear"];
const AP_REG_TOP={kyoto:"京都",nara:"奈良",osaka:"大阪",shiga:"滋贺",uminokyoto:"海之京都",morinokyoto:"森之京都"};
const AP_REG_SUB={higashiyama:"东山",central:"京都市中心",arashiyama:"岚山·嵯峨野",rakuhoku:"洛北",north:"贵船·鞍马·大原",fushimi:"伏见·山科",uji:"宇治"};
const AP_REGIONS={...AP_REG_TOP,...AP_REG_SUB};
const apRegion=id=>{let n=NODES[id];while(n){if(AP.regions[n.id])return n.id;n=n.parent}return ""};
let AP={start:"",end:"",base:"auto",pace:"mid",mode:"public",tags:[],must:[],regions:{}};
try{Object.assign(AP,JSON.parse(localStorage.getItem("kyoto-autoplan")||"{}"))}catch(e){}
if(!AP.regions||typeof AP.regions!=="object")AP.regions={};
const apSave=()=>{try{localStorage.setItem("kyoto-autoplan",JSON.stringify(AP))}catch(e){}};
let AP_RES=null,AP_SEED=1;
const km=(a,b)=>{const R=6371,t=Math.PI/180,dl=(b[0]-a[0])*t,dn=(b[1]-a[1])*t,x=Math.sin(dl/2)**2+Math.cos(a[0]*t)*Math.cos(b[0]*t)*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(x))};
function apTravel(a,b,mode,remote){const d=km(a,b)*1.25;if(d<1.1)return Math.round(d*14+4);
  let t=mode==="car"?(d<15?14+d*2.4:18+d*1.15)+8:(d<12?18+d*2.7:28+d*1.3);if(remote&&mode!=="car")t+=40;return Math.round(t/5)*5}
const apMonth=d=>{const t=new Date(d+"T00:00:00");return t.getMonth()+1+(t.getDate()-1)/31};
function apDays(s,e){const a=[];if(!s)return a;let t=new Date(s+"T00:00:00");const end=new Date((e||s)+"T00:00:00");while(t<=end&&a.length<21){a.push(t.toISOString().slice(0,10).replace(/^(\d+)-(\d+)-(\d+)$/,(m,y,mo,da)=>`${y}-${mo}-${da}`));t=new Date(t.getTime()+86400000)}
  return a.map(x=>{const t2=new Date(x+"T12:00:00Z");return x})}
function apRng(seed){let s=seed%2147483647;if(s<=0)s+=2147483646;return()=>(s=s*16807%2147483647)/2147483647}
const segHit=(segs,m)=>(segs||[]).some(([a,b])=>m>=a-0.02&&m<=b+0.02);
function apGenerate(){
  const days=[];{let t=new Date(AP.start+"T00:00:00");const end=new Date((AP.end||AP.start)+"T00:00:00");while(t<=end&&days.length<21){const y=t.getFullYear(),mo=String(t.getMonth()+1).padStart(2,"0"),da=String(t.getDate()).padStart(2,"0");days.push(`${y}-${mo}-${da}`);t.setDate(t.getDate()+1)}}
  if(!days.length)return {err:"请先选择出发和结束日期。"};
  const pace=AP_PACE[AP.pace]||AP_PACE.mid,mode=AP.mode,T=AP.tags,rnd=apRng(AP_SEED*7919+days.length);
  const ms=days.map(apMonth);
  const ids=Object.keys(PLANDATA).filter(id=>NODES[id]);
  const fixed={};const notes={};
  const S={};
  for(const id of ids){const n=NODES[id],[la,lo,dur,f]=PLANDATA[id];const has=k=>(n.t||[]).includes(k);
    if(T.includes("elderly")&&!f.includes("e")&&!AP.must.includes(id))continue;
    let s=10+(has("hot")?8:0)+(n.star?(!T.filter(k=>k!=="elderly").length||T.includes("hot")?15:5):0);
    const ev=(n.sm&&n.sm.matsuri)||[];
    const inSeason=k=>k==="matsuri"?days.some((d,i)=>ev.some(([a,b])=>ms[i]>=a-0.005&&ms[i]<=b+0.005)):k==="newyear"?days.some(d=>/-(12-31|01-0[1-3])$/.test(d)):ms.some(m=>segHit((n.sm&&n.sm[k])||SC_DEF[k],m));
    let hit=0;T.forEach(k=>{if(k==="elderly"||!has(k))return;if(AP_SEASON.includes(k)&&!inSeason(k))return;s+=AP_SEASON.includes(k)?20:12;hit++});if(T.filter(k=>k!=="elderly").length&&!hit)s-=4;
    for(const k of ["sakura","momiji","snow"]){if(has(k)&&inSeason(k))s+=10}
    days.forEach((d,i)=>{const m=ms[i];ev.forEach(([a,b,nm])=>{if(m>=a-0.005&&m<=b+0.005){if(b-a<0.2){(fixed[d]=fixed[d]||[]).push({id,nm});}else s+=6}})});
    if(f.includes("s")&&!["sakura","momiji"].some(k=>has(k)&&inSeason(k))&&!AP.must.includes(id))continue;
    if(f.includes("x")&&!Object.values(fixed).some(a=>a.some(x=>x.id===id)))continue;
    if(f.includes("r")&&mode!=="car")s-=8;
    if(AP.must.includes(id))s+=1000;
    s+=rnd()*3;
    S[id]={id,g:[la,lo],dur,f,s,remote:f.includes("r")};}
  if(T.includes("onsen")&&!AP.must.some(id=>(NODES[id].t||[]).includes("onsen"))){const far=x=>{const tt=apTravel([34.9858,135.7588],x.g,mode,x.remote);return tt>100&&(mode!=="car"||days.length<4)?120+tt*0.2:tt*0.1};const o=Object.values(S).filter(x=>(NODES[x.id].t||[]).includes("onsen")).sort((a,b)=>(b.s-far(b))-(a.s-far(a)))[0];if(o)o.s+=400}
  if(T.includes("food")){Object.values(S).forEach(x=>{if((NODES[x.id].t||[]).includes("food"))x.s+=4})}
  // 跨年
  days.forEach((d,i)=>{if(d.endsWith("-12-31")){const c=["chionin","yasaka"].find(x=>S[x]);if(c)(fixed[d]=fixed[d]||[]).push({id:c,nm:c==="chionin"?"除夜之钟":"白朮诣（跨年参拜）",eve:1})}
    if(d.endsWith("-01-01")){const c=["inari","yasaka","heian","shimogamo"].find(x=>S[x]);if(c)(fixed[d]=fixed[d]||[]).push({id:c,nm:"初诣"})}});
  // 住宿
  let base=AP.base,baseWhy="";
  if(base==="auto"){const top=Object.values(S).sort((a,b)=>b.s-a.s).slice(0,Math.max(6,days.length*pace.max));let best=null;
    for(const k in AP_BASES){if(k==="auto")continue;const g=AP_BASES[k].g;const avg=top.reduce((a,x)=>a+apTravel(g,x.g,mode,x.remote),0)/top.length;if(!best||avg<best[1])best=[k,avg]}
    base=best[0];baseWhy=`按你选的景点计算，从这里出发平均交通时间最短（约 ${Math.round(best[1])} 分钟）`}
  const B=AP_BASES[base].g;
  const used=new Set();const plan={},meta={};const warn=[];
  AP.tags.filter(k=>AP_SEASON.includes(k)).forEach(k=>{if(!Object.keys(S).some(id=>{const n=NODES[id];return (n.t||[]).includes(k)&&(k==="matsuri"?days.some((d,i)=>((n.sm&&n.sm.matsuri)||[]).some(([a,b])=>ms[i]>=a-0.005&&ms[i]<=b+0.005)):k==="newyear"?days.some(d=>/-(12-31|01-0[1-3])$/.test(d)):ms.some(m=>segHit((n.sm&&n.sm[k])||SC_DEF[k],m)))}))warn.push(`出行日期不在「${TAGS[k]}」的时节内，这个偏好没有生效`)});
  const reserved=new Set();Object.values(fixed).forEach(a=>a.forEach(x=>reserved.add(x.id)));
  const regDay={};{const free=days.map((d,i)=>[d,i]).filter(([d])=>!fixed[d]);const pref=[...free.slice(1,-1),...free.slice(-1),...free.slice(0,1)].map(x=>x[0]);let pi=0;
    const want=[];const fixedIn=r=>days.filter(d=>fixed[d]&&fixed[d].some(x=>apRegion(x.id)===r||(r==="kyoto"&&NODES[x.id]&&(()=>{let n=NODES[x.id];while(n){if(n.id==="kyoto")return 1;n=n.parent}})()))).length;
    Object.entries(AP.regions||{}).sort((a,b)=>(a[0]==="kyoto"||AP_REG_SUB[a[0]]?1:0)-(b[0]==="kyoto"||AP_REG_SUB[b[0]]?1:0)).forEach(([r,k])=>{const kk=r==="kyoto"?Math.max(0,k-fixedIn("kyoto")):k;for(let j=0;j<kk;j++)want.push(r)});
    const order=[];for(let j=0;j<want.length;j++){if(pi>=pref.length){warn.push(`日期不够，「${AP_REGIONS[want[j]]}」少排了 1 天`);continue}order.push([pref[pi++],want[j]])}
    order.sort((a,b)=>a[0]<b[0]?-1:1);const seen={};order.forEach(([d,r])=>{regDay[d]=r});}
  const KY=new Set(["kyoto",...Object.keys(AP_REG_SUB)]);const regSet=new Set(Object.values(regDay).filter(r=>!KY.has(r)));
  const pace0=pace;
  days.forEach((d,di)=>{
    const cx=apDayCtx(d,days,AP,B,pace0);const pace={...pace0,start:cx.start,budget:cx.budget,max:cx.max,night:cx.night};
    const list=[];let eve=null;
    (fixed[d]||[]).forEach(x=>{if(!S[x.id]||used.has(x.id))return;const night=x.eve||PLANDATA[x.id][3].includes("n");if(night&&!eve)eve={...S[x.id],ev:x.nm};else list.push({...S[x.id],ev:x.nm});used.add(x.id)});
    const rg=regDay[d]||"";
    const pool=()=>Object.values(S).filter(x=>!used.has(x.id)&&!reserved.has(x.id)&&!(PLANDATA[x.id][3].includes("x"))&&(rg?apRegion(x.id)===rg:!regSet.has(apRegion(x.id))||x.s>=1000&&!Object.values(regDay).includes(apRegion(x.id))));
    const tripCost=arr=>{if(!arr.length)return 0;let t=0,p=B;const o=apOrder(arr,B);o.forEach(x=>{t+=apTravel(p,x.g,mode,x.remote)+x.dur;p=x.g});return t+apTravel(p,B,mode,false)};
    if(!list.length&&pace.max){let best=null;const P=pool();for(const x of P){if(x.dur<40&&x.s<1000)continue;const rt=apTravel(B,x.g,mode,x.remote)*2+x.dur;if(rt>pace.budget+(x.s>=400||(rg&&!KY.has(rg))?300:60))continue;const nb=P.filter(y=>y!==x&&!y.f.includes("v")&&!y.f.includes("n")&&apTravel(x.g,y.g,mode,y.remote)<=(mode==="car"?35:30)).map(y=>y.s).sort((a,b)=>b-a).slice(0,pace.max-1).reduce((a,b)=>a+b,0);const v=x.s+nb*0.6-rt*0.06-(x.f.includes("n")?6:0);if(!best||v>best[0])best=[v,x]}
      if(best){list.push(best[1]);used.add(best[1].id)}}
    const BD=pace.budget+(list.length&&!cx.short?Math.max(0,Math.min(150,2*apTravel(B,list[0].g,mode,list[0].remote)-50)):0);
    let guard=0;while(list.length<pace.max&&guard++<40){const last=apOrder(list,B).slice(-1)[0]||{g:B};let best=null;
      for(const x of pool()){if(PLANDATA[x.id][3].includes("v")&&list.length&&!rg)continue;const c=tripCost([...list,x]);if(c>BD)continue;const near=Math.min(...list.map(y=>apTravel(y.g,x.g,mode,x.remote)));const fromA=apTravel(list[0].g,x.g,mode,x.remote);if(fromA>(mode==="car"?35:30))continue;const v=x.s-near*0.7-(x.f.includes("n")?6:0);if(!best||v>best[0])best=[v,x]}
      if(!best)break;list.push(best[1]);used.add(best[1].id)}
    if(list.length&&list.length<pace.max&&tripCost(list)<BD*0.65){let guard2=0;while(list.length<pace.max&&guard2++<20){let best=null;const ord=apOrder(list,B),last=ord[ord.length-1];
      for(const x of pool()){if(x.f.includes("v"))continue;const c=tripCost([...list,x]);if(c>BD)continue;const tt=apTravel(last.g,x.g,mode,x.remote);if(tt>30)continue;const v=x.s-tt*0.5-(x.f.includes("n")?6:0);if(!best||v>best[0])best=[v,x]}
      if(!best)break;list.push(best[1]);used.add(best[1].id)}}
    const ordered0=apOrder(list,B);const ordered=ordered0.slice();{let g=0;const NO=new Set(["pontocho","takasegawa","dotonbori","kyoto-station"]);if(ordered.length>1&&NO.has(ordered[0].id))ordered.reverse();while(ordered.length>1&&NO.has(ordered[0].id)&&g++<5)ordered.push(ordered.shift())}
    if(!eve&&(pace.night||T.includes("night")&&!cx.dep)&&ordered.length){const last=ordered[ordered.length-1];let best=null;
      for(const x of pool()){if(!PLANDATA[x.id][3].includes("n"))continue;const tt=apTravel(last.g,x.g,mode,false);if(tt>35)continue;const v=x.s-tt*0.3;if(!best||v>best[0])best=[v,x]}
      if(best){eve=best[1];used.add(eve.id)}}
    if(!eve&&!ordered.length&&cx.pre.length&&pace0.night&&cx.start<=19*60+30&&!cx.dep){let best=null;
      for(const x of pool()){if(!PLANDATA[x.id][3].includes("n"))continue;const tt=apTravel(B,x.g,mode,false);if(tt>25)continue;const v=x.s-tt*0.5;if(!best||v>best[0])best=[v,x]}
      if(best){eve=best[1];used.add(eve.id)}}
    const all=[...ordered,...(eve?[eve]:[])];
    plan[d]=all.map(x=>x.id);
    const {rows,back,food,note,dep}=apDayCalc(ordered,eve,B,pace,mode,rg,cx);
    meta[d]={rows,back,food,note,rg,dep};
  });
  // 少换宿：同一大区的日子排在一起
  const top1=d=>{const c={};(plan[d]||[]).forEach(id=>{let n=NODES[id];while(n&&n.depth>1)n=n.parent;if(n)c[n.id]=(c[n.id]||0)+1});const k=Object.keys(c).sort((a,b)=>c[b]-c[a])[0];return k||""};
  if(AP.few!==false){const free=days.filter((d,i)=>!fixed[d]&&!(i===0&&toMin(AP.arrT)!=null)&&!(i===days.length-1&&toMin(AP.depT)!=null));const fixIdx=days.map((d,i)=>fixed[d]?i:-1).filter(i=>i>=0);
    const kyLast=fixIdx.length&&fixIdx.reduce((a,b)=>a+b,0)/fixIdx.length>=(days.length-1)/2;
    const grp={},order=[];free.forEach(d=>{const k=top1(d);if(!grp[k]){grp[k]=[];order.push(k)}grp[k].push(d)});
    let seq=order.filter(k=>k&&k!=="kyoto");if(grp.kyoto)seq=kyLast?[...seq,"kyoto"]:["kyoto",...seq];if(grp[""])seq.push("");
    const src=seq.flatMap(k=>grp[k]).map(d=>[plan[d],meta[d]]);free.forEach((d,i)=>{plan[d]=src[i][0];meta[d]=src[i][1]});
    const lbl={kyoto:"京都",nara:"奈良",osaka:"大阪",shiga:"滋贺",uminokyoto:"海之京都",morinokyoto:"森之京都"};
    let i=0;while(i<days.length){const k=top1(days[i]);let j=i;while(j+1<days.length&&top1(days[j+1])===k)j++;
      if(k&&k!=="kyoto"&&j>i&&meta[days[i]])meta[days[i]].note=[`第${i+1}–${j+1}天都在${lbl[k]}，如果想少坐车，也可以这几晚住在${lbl[k]}`,...(meta[days[i]].note||[])];
      i=j+1}}
  days.forEach((d,i)=>{if(!(plan[d]||[]).length&&!(i===0&&toMin(AP.arrT)!=null)&&!(i===days.length-1&&toMin(AP.depT)!=null))warn.push(`${fmtD(d)} 没有找到合适的景点，可以减少偏好标签或改成「密集」`)});
  const missMust=AP.must.filter(id=>!Object.values(plan).some(a=>a.includes(id)));
  missMust.forEach(id=>warn.push(`必去景点「${NODES[id].n}」没能排进去（交通时间过长），可以把节奏改成「密集」或手动加入`));
  return {days,plan,meta,base,baseWhy,warn,opt:JSON.parse(JSON.stringify(AP))};
}
function apDayCalc(ordered,eve,B,pace,mode,rg,cx){
    cx=cx||{pre:[],post:[]};let t=cx.start!=null?cx.start:pace.start,p=B,lunch=t>=14*60;const rows=[...(cx.pre||[])];
    ordered.forEach(x=>{const tr=apTravel(p,x.g,mode,x.remote);t+=tr;if(!lunch&&t>=12*60){rows.push({lunch:1,at:t});t+=60;lunch=true}t=Math.ceil(t/5)*5;rows.push({id:x.id,at:t,dur:x.dur,tr,ev:x.ev||""});t+=x.dur;p=x.g;
      if(!lunch&&t>=12*60+30){rows.push({lunch:1,at:t});t+=60;lunch=true}});
    if(eve){const tr=apTravel(p,eve.g,mode,false);t=Math.ceil(Math.max(t+tr,18*60)/5)*5;rows.push({id:eve.id,at:t,dur:eve.dur,tr,ev:eve.ev||"",eve:1});p=eve.g}
    const back=apTravel(p,B,mode,false);
    const all=[...ordered,...(eve?[eve]:[])];const tight=cx.post&&cx.post.length&&t+back>cx.post[0].at;
    rows.push(...(cx.post||[]));
    const idset=new Set();all.forEach(x=>{idset.add(x.id);let n=NODES[x.id];while(n&&n.depth>1){idset.add(n.id);n=n.parent}});
    const food=Object.entries(TERMS_).filter(([,tm])=>tm.k==="美食"&&(tm.w||[]).some(w=>idset.has(w))).map(([k])=>k).slice(0,3);
    const far=all.find(x=>(x.f||"").includes("v")&&km(B,x.g)>40);
    const note=[];if(far)note.push(`${NODES[far.id].n}离住处较远，建议当晚在当地过夜，次日再回来`);
    all.forEach(x=>{if(x.remote&&mode!=="car")note.push(`${NODES[x.id].n}公共交通班次较少，请提前查好时刻表`)});
    if(rg)note.unshift(`这一天专门安排「${AP_REGIONS[rg]}」`);
    if(tight)note.unshift("离开日时间偏紧，建议删掉一两个景点");
    if(cx.pre&&cx.pre.length&&!ordered.length)note.unshift(eve?"到达日：入住后晚上在附近走走":"到达日：抵达后先入住休息");
    return {rows,back,food,note,dep:cx.dep?1:0}}
const AP_PLACES={kix:{n:"关西机场",air:1,t:{ky:90,os:55,na:90}},itm:{n:"伊丹机场",air:1,t:{ky:60,os:30,na:75}},kyotost:{n:"京都站（新干线）",t:{ky:20,os:45,na:50}},shinosaka:{n:"新大阪站（新干线）",t:{ky:35,os:20,na:60}}};
const apZone=g=>km(g,[34.68,135.82])<12?"na":km(g,[34.69,135.50])<15?"os":"ky";
const toMin=s=>{const m=/^(\d{1,2}):(\d{2})/.exec(s||"");return m?+m[1]*60+ +m[2]:null};
function apDayCtx(d,days,o,B,pace){const c={start:pace.start,budget:pace.budget,max:pace.max,night:pace.night,pre:[],post:[],dep:0,short:0};
  const z=apZone(B),arr=d===days[0]?toMin(o.arrT):null,dep=d===days[days.length-1]?toMin(o.depT):null;
  if(arr!=null){const P=AP_PLACES[o.arrP]||AP_PLACES.kix,ex=P.air?60:10,tr=P.t[z];c.pre.push({mv:1,at:arr,txt:`抵达${P.n}${P.air?"（入境、取行李约 1 小时）":""}`});c.pre.push({mv:1,at:arr+ex,txt:`前往住处，约 ${tr} 分钟，寄存行李`});
    const s=Math.ceil((arr+ex+tr+30)/5)*5;c.budget=Math.max(0,pace.start+pace.budget-Math.max(s,pace.start));c.start=Math.max(s,pace.start);c.short=1;if(arr+ex+tr>=19*60){c.budget=0}}
  if(dep!=null){const P=AP_PLACES[o.depP]||AP_PLACES.kix,buf=P.air?120:20,tr=P.t[z];const L=Math.floor((dep-buf-tr)/5)*5,back=L-20;
    c.post.push({mv:1,at:back,txt:"回住处取行李"});c.post.push({mv:1,at:L,txt:`出发前往${P.n}，约 ${tr} 分钟`});c.post.push({mv:1,at:dep,txt:`${P.air?"航班起飞（提前 2 小时到机场）":"列车出发"}`});
    c.budget=Math.max(0,Math.min(c.budget,back-c.start));c.dep=1;c.short=1;c.night=back>=21*60?c.night:0;c.end=back}
  if(c.budget<75){c.budget=0;c.max=0}else if(c.short)c.max=Math.max(1,Math.min(pace.max,Math.round(pace.max*c.budget/pace.budget+0.4)));
  return c}
const apMk=(id,ex)=>{const [la,lo,dur,f]=PLANDATA[id];return Object.assign({id,g:[la,lo],dur,f,remote:f.includes("r")},ex||{})};
function apResched(d){const r=AP_RES;if(!r||!r.plan[d])return;const old=r.meta[d]||{rows:[]};const ex={};old.rows.forEach(x=>{if(x.id)ex[x.id]={ev:x.ev||"",eve:x.eve}});
  const pace=AP_PACE[r.opt.pace]||AP_PACE.mid,mode=r.opt.mode,B=AP_BASES[r.base].g;
  const ids=r.plan[d].filter(id=>PLANDATA[id]);const eveId=ids.find(id=>ex[id]&&ex[id].eve);
  const ordered=apOrder(ids.filter(id=>id!==eveId).map(id=>apMk(id,{ev:(ex[id]||{}).ev})),B);
  const NO=new Set(["pontocho","takasegawa","dotonbori","kyoto-station"]);if(ordered.length>1&&NO.has(ordered[0].id))ordered.reverse();
  const eve=eveId?apMk(eveId,{ev:ex[eveId].ev}):null;
  r.plan[d]=[...ordered,...(eve?[eve]:[])].map(x=>x.id);
  r.meta[d]=Object.assign(apDayCalc(ordered,eve,B,pace,mode,old.rg),{rg:old.rg})}
function apSugg(q,all){q=(q||"").trim().toLowerCase();if(!q)return [];const out=[];
  for(const id of (all?Object.keys(NODES).filter(k=>NODES[k].depth>=2):Object.keys(PLANDATA))){const n=NODES[id];if(!n)continue;const hay=[n.n,n.ja||"",id].join(" ").toLowerCase();if(hay.includes(q))out.push(id);if(out.length>=8)break}
  return out}
function planCalc(d){const v=PV.v[PV.cur]||{},o=v.opt||{},pace=AP_PACE[o.pace]||AP_PACE.mid,mode=o.mode||"public",B=((AP_BASES[o.baseRes]||AP_BASES[o.base]||{}).g)||AP_BASES.kawara.g;
  const M=(v.meta||{})[d]||{};const eveIds=new Set((M.rows||[]).filter(r=>r.eve).map(r=>r.id));const evs={};(M.rows||[]).forEach(r=>{if(r.id&&r.ev)evs[r.id]=r.ev});
  const pts=(PLAN[d]||[]).map(id=>{let n=NODES[id],pd=null;while(n&&!(pd=PLANDATA[n.id]))n=n.parent;if(!pd)return null;const own=PLANDATA[id];return {id,g:[pd[0],pd[1]],dur:own?own[2]:30,f:own?own[3]:"",remote:pd[3].includes("r"),ev:evs[id]||""}}).filter(Boolean);
  let eve=null;if(pts.length>1&&eveIds.has(pts[pts.length-1].id))eve=pts.pop();
  const cx=apDayCtx(d,planDates(),o,B,pace);
  return Object.assign(apDayCalc(pts,eve,B,pace,mode,M.rg,cx),{rg:M.rg})}
const liveMeta=()=>{const o={};planDates().forEach(d=>o[d]=planCalc(d));return o};
const durTx=m=>m>=60?(m/60).toFixed(m%60?1:0)+" 小时":m+" 分钟";
function planDayHtml(d){const M=planCalc(d),ids=PLAN[d],seen=new Set();const n=ids.length;
  const row=(id,r)=>{const k=ids.indexOf(id),N=NODES[id];seen.add(id);return `<li class="apsw${r&&r.eve?" eve":""}" data-apid="${id}" data-apd="${d}"><time>${r?hm(r.at):"—"}</time><span><button class="mylink" data-go="${id}"><b>${esc(N.n)}</b></button>${r&&r.ev?`<em class="apev">${esc(r.ev)}</em>`:""}<small>${r?`游览约 ${durTx(r.dur)} · 前往约 ${r.tr} 分钟${r.eve?" · 晚间":""}`:esc(N.folders.slice(0,-1).join(" › "))}</small></span><span class="pmv"><button data-planmv="${d}|${id}|-1" aria-label="上移"${k?"":" disabled"}>↑</button><button data-planmv="${d}|${id}|1" aria-label="下移"${k<n-1?"":" disabled"}>↓</button></span><button class="apx" data-planrm2="${d}|${id}" aria-label="删除">删除</button></li>`};
  let h=`<ol class="apday pl">${M.rows.map(r=>r.mv?`<li class="lunch mv"><time>${hm(r.at)}</time><span>${esc(r.txt)}</span></li>`:r.lunch?`<li class="lunch"><time>${hm(r.at)}</time><span>午餐 · 约 1 小时</span></li>`:row(r.id,r)).join("")}${ids.filter(id=>!seen.has(id)).map(id=>row(id,null)).join("")}</ol>`;
  h+=`<div class="apadd"><input data-plaaddin="${d}" placeholder="＋ 添加景点，输入名称…" autocomplete="off"><div class="apsug" data-apsug="p${d}"></div></div>`;
  if(M.food&&M.food.length)h+=`<div class="apfood">当地美食：${M.food.map(k=>`<button class="tag" data-route="term-${k}">${esc(TERMS_[k].n)}</button>`).join("")}</div>`;
  if(M.note&&M.note.length)h+=`<p class="scnote">${M.note.map(esc).join("；")}</p>`;
  const last=M.rows.filter(r=>!r.mv).slice(-1)[0];if(last&&!M.dep)h+=`<p class="scnote">约 ${hm(last.at+(last.dur||60)+M.back)} 回到住处</p>`;
  return h}
function apOrder(arr,B){const rest=[...arr],o=[];let p=B;while(rest.length){let bi=0,bd=1e9;rest.forEach((x,i)=>{const d=km(p,x.g);if(d<bd){bd=d;bi=i}});const x=rest.splice(bi,1)[0];o.push(x);p=x.g}
  const L=a=>{let s=0,q=B;a.forEach(x=>{s+=km(q,x.g);q=x.g});return s+km(q,B)};let best=L(o),imp=true,g=0;
  while(imp&&g++<30){imp=false;for(let i=0;i<o.length-1;i++)for(let j=i+1;j<o.length;j++){const c=[...o.slice(0,i),...o.slice(i,j+1).reverse(),...o.slice(j+1)];const l=L(c);if(l<best-1e-6){best=l;o.splice(0,o.length,...c);imp=true}}}
  return o}
const hm=m=>String(Math.floor(m/60)).padStart(2,"0")+":"+String(Math.round(m%60)).padStart(2,"0");
function apSchedule(d,meta,plan,edit){const M=meta&&meta[d];if(!M)return "";
  return `<ol class="apday">${M.rows.map(r=>r.mv?`<li class="lunch mv"><time>${hm(r.at)}</time><span>${esc(r.txt)}</span></li>`:r.lunch?`<li class="lunch"><time>${hm(r.at)}</time><span>午餐 · 约 1 小时</span></li>`:`<li class="${r.eve?"eve ":""}${edit?"apsw":""}"${edit?` data-apid="${r.id}" data-apd="${d}"`:""}><time>${hm(r.at)}</time><span><button class="mylink" data-go="${r.id}"><b>${esc(NODES[r.id].n)}</b></button>${r.ev?`<em class="apev">${esc(r.ev)}</em>`:""}<small>游览约 ${r.dur>=60?(r.dur/60).toFixed(r.dur%60?1:0)+" 小时":r.dur+" 分钟"} · 前往约 ${r.tr} 分钟${r.eve?" · 晚间":""}</small></span>${edit?`<button class="apx" data-aprm="${d}|${r.id}" aria-label="删除">删除</button>`:""}</li>`).join("")}</ol>
  ${edit?`<div class="apadd"><input data-apaddin="${d}" placeholder="＋ 添加景点，输入名称…" autocomplete="off"><div class="apsug" data-apsug="${d}"></div></div>`:""}
  ${M.food&&M.food.length?`<div class="apfood">当地美食：${M.food.map(k=>`<button class="tag" data-route="term-${k}">${esc(TERMS_[k].n)}</button>`).join("")}</div>`:""}
  ${M.note&&M.note.length?`<p class="scnote">${M.note.map(esc).join("；")}</p>`:""}`}
function apTime(d,id){const M=pvMeta()[d];if(!M)return "";const r=M.rows.find(x=>x.id===id);return r?`<time class="apt">${hm(r.at)}</time>`:""}
function apDayExtra(d){const M=pvMeta()[d];if(!M)return "";return `${M.food&&M.food.length?`<div class="apfood">当地美食：${M.food.map(k=>`<button class="tag" data-route="term-${k}">${esc(TERMS_[k].n)}</button>`).join("")}</div>`:""}${M.note&&M.note.length?`<p class="scnote">${M.note.map(esc).join("；")}</p>`:""}`}
function autoPages(){
  const tagChip=k=>TAGS[k]?`<button class="fchip${AP.tags.includes(k)?" on":""}" data-aptag="${k}">${esc(TAGS[k])}</button>`:"";
  const opt=(o,k,v)=>Object.entries(o).map(([key,x])=>`<button class="fchip${AP[k]===key?" on":""}" data-apset="${k}|${key}">${esc(x.n||x)}</button>`).join("");
  const spots=Object.keys(PLANDATA).filter(id=>NODES[id]);
  const L=`<span class="eyebrow">个人</span><div class="tagtitle">自动生成行程</div>
  <p style="color:var(--ink-2)">填好日期和偏好，自动按区域排出每天的路线和大致时间，生成后可以保存成一个行程版本，再在「旅行计划」里手动调整。</p>
  <div class="apform">
   <label>旅行日期</label><div class="aprow"><input type="date" id="ap-start" value="${esc(AP.start)}"><span>至</span><input type="date" id="ap-end" value="${esc(AP.end)}"></div>
   <label>到达 / 离开时间（可选，不填按整天安排）</label>
   <div class="aprow wrap apio"><span>到达</span><input type="time" id="ap-arrt" value="${esc(AP.arrT||"")}"><select id="ap-arrp">${Object.entries(AP_PLACES).map(([k,x])=>`<option value="${k}"${(AP.arrP||"kix")===k?" selected":""}>${esc(x.n)}</option>`).join("")}</select></div>
   <div class="aprow wrap apio"><span>离开</span><input type="time" id="ap-dept" value="${esc(AP.depT||"")}"><select id="ap-depp">${Object.entries(AP_PLACES).map(([k,x])=>`<option value="${k}"${(AP.depP||"kix")===k?" selected":""}>${esc(x.n)}</option>`).join("")}</select></div>
   <label>住宿</label><div class="aprow"><select id="ap-base">${Object.entries(AP_BASES).map(([k,x])=>`<option value="${k}"${AP.base===k?" selected":""}>${esc(x.n)}</option>`).join("")}</select></div>
   <label>节奏</label><div class="aprow">${opt({light:{n:"轻松 · 3 处"},mid:{n:"适中 · 4–5 处"},dense:{n:"密集 · 6–7 处"}},"pace")}</div>
   <label>交通方式</label><div class="aprow">${opt({public:{n:"公共交通"},car:{n:"自驾"}},"mode")}</div>
   <label>换宿</label><div class="aprow wrap"><button class="fchip${AP.few!==false?" on":""}" data-apfew="1" aria-pressed="${AP.few!==false}">${AP.few!==false?"✓ ":""}少换宿</button><span class="scnote" style="margin:0">选中后，京都、奈良、大阪等同一大区的日子会尽量排在一起</span></div>
   <label>想去的区域（可选 · 每点一次多排一天，点到上限后归零；没指定的日子自动安排）</label>${[["一级区域",AP_REG_TOP],["京都细分",AP_REG_SUB]].map(([g,o])=>`<div class="aptg"><span>${g}</span><div class="aprow wrap">${Object.entries(o).map(([k,n])=>{const c=AP.regions[k]||0;return `<button class="fchip${c?" on":""}" data-apreg="${k}">${esc(n)}${c?` · ${c} 天`:""}</button>`}).join("")}</div></div>`).join("")}
   <label>偏好（可多选，不选则以热门景点为主；时令类只在出行日期对得上时生效）</label>${AP_TAG_G.map(([g,ks])=>`<div class="aptg"><span>${g}</span><div class="aprow wrap">${ks.split(" ").map(tagChip).join("")}</div></div>`).join("")}
   <label>必去景点（可选）</label><div class="aprow"><input id="ap-must" list="ap-spots" placeholder="输入景点名…"><datalist id="ap-spots">${spots.map(id=>`<option value="${esc(NODES[id].n)}">`).join("")}</datalist><button class="mt plus" data-apmust="1">添加</button></div>
   <div class="aprow wrap">${AP.must.map(id=>`<span class="mt on pd">${esc(NODES[id].n)}<button class="px" data-apmustrm="${id}">×</button></span>`).join("")}</div>
   <div class="aprow" style="margin-top:10px"><button class="btn pri" data-apgo="1">✨ 生成行程</button>${AP_RES&&!AP_RES.err?`<button class="btn" data-apre="1">换一种排法</button>`:""}</div>
  </div><span class="folio">AUTO</span>`;
  let R=`<div class="kicker"><span class="kind">行程预览</span><span>${AP_RES&&AP_RES.days?fmtD(AP_RES.days[0])+" – "+fmtD(AP_RES.days[AP_RES.days.length-1])+" · 共 "+AP_RES.days.length+" 天":""}</span></div><h1>行程预览</h1>`;
  if(!AP_RES)R+=`<p class="intro" style="margin-top:14px">在左边填好条件，点「生成行程」。</p>`;
  else if(AP_RES.err)R+=`<p class="intro" style="margin-top:14px">${esc(AP_RES.err)}</p>`;
  else{const r=AP_RES;
    R+=`<p class="apbase">住宿：<b>${esc(AP_BASES[r.base].n)}</b>${r.baseWhy?`<br><small>${esc(r.baseWhy)}</small>`:""}</p>`;
    if(r.warn.length)R+=`<p class="scnote apwarn">${r.warn.map(esc).join("<br>")}</p>`;
    R+=r.days.map((d,i)=>`<div class="sec">第${i+1}天 · ${fmtD(d,true)}</div>${r.plan[d].length||r.meta[d].rows.length?apSchedule(d,r.meta,r.plan,true):'<p class="scnote">自由活动 / 休息日</p>'+apSchedule(d,{[d]:{rows:[],back:0,food:[],note:[]}},r.plan,true)}${(()=>{const M=r.meta[d],L=M.rows.filter(x=>!x.mv).slice(-1)[0];return L&&!M.dep?`<p class="scnote">约 ${hm(L.at+(L.dur||60)+M.back)} 回到住处</p>`:""})()}`).join("");
    const nm=`自动行程 ${fmtD(r.days[0])}–${fmtD(r.days[r.days.length-1])} · ${AP_PACE[r.opt.pace].n}`;
    R+=`<div class="apsave"><input id="ap-name" value="${esc(nm)}" maxlength="40" aria-label="版本名称"><button class="btn pri" data-apsave="1">保存为新版本并设为当前行程</button></div>
    <p class="scnote">时间为大致估算（按直线距离和交通方式推算），开放时间、预约和交通以官方信息为准。</p>`}
  R+=`<span class="folio">AUTO</span>`;
  return [L,R];
}
function pvBar(){const ks=Object.keys(PV.v);return `<div class="pvbar"><label>行程版本</label><select id="pv-sel">${ks.map(k=>`<option value="${k}"${k===PV.cur?" selected":""}>${esc(PV.v[k].name)}</option>`).join("")}</select>
  <div class="aprow wrap"><button class="btn sm pri" data-route="autoplan">✨ 自动生成行程</button><button class="btn sm" data-pvdup="1">复制为新版本</button><button class="btn sm" data-pvnew="1">新建空白版本</button><button class="btn sm" data-pvren="1">重命名</button><button class="btn sm${SH_OPEN?" on":""}" data-shopen="1">📤 分享行程</button>${ks.length>1?`<button class="btn sm" data-pvdel="1">${PV_DEL?"再点一次确认删除":"删除此版本"}</button>`:""}</div>
  ${shareBox()}${PV_REN?`<div class="aprow"><input id="pv-name" value="${esc(PV.v[PV.cur].name)}" maxlength="40"><button class="btn sm pri" data-pvrenok="1">确定</button></div>`:""}</div>`}
let PV_DEL=false,PV_REN=false;
document.addEventListener("focusin",e=>{const el=e.target;if(el.dataset&&(el.dataset.apaddin||el.dataset.plaaddin))setTimeout(()=>{try{el.scrollIntoView({block:"start",behavior:"smooth"})}catch(_){}},300)});
document.addEventListener("input",e=>{const el=e.target;if(el.dataset&&el.dataset.plaaddin){const d=el.dataset.plaaddin,box=document.querySelector(`[data-apsug="p${d}"]`);if(!box)return;
  box.innerHTML=apSugg(el.value,true).map(id=>{const N=NODES[id],has=PLAN[d].includes(id),other=planDates().filter(k=>k!==d&&PLAN[k].includes(id)).map(k=>"第"+dayNo(k)+"天");return `<button data-plaaddid="${d}|${id}"${has?" disabled":""}><b>${esc(N.n)}</b><small>${esc(N.folders.slice(0,-1).join(" › "))}${has?" · 已在这一天":other.length?" · 也在"+other.join("、"):""}</small></button>`}).join("")||(el.value.trim()?'<p class="scnote">没有找到匹配的景点</p>':"");return}
  if(!el.dataset||!el.dataset.apaddin)return;const d=el.dataset.apaddin;const box=document.querySelector(`[data-apsug="${d}"]`);if(!box)return;
  const used=new Set(Object.values(AP_RES?AP_RES.plan:{}).flat());
  box.innerHTML=apSugg(el.value).map(id=>{const where=Object.keys(AP_RES.plan).find(k=>AP_RES.plan[k].includes(id));return `<button data-apaddid="${d}|${id}"><b>${esc(NODES[id].n)}</b><small>${esc(NODES[id].ja||"")}${where?` · 已在第${AP_RES.days.indexOf(where)+1}天，点选会移到这天`:""}</small></button>`}).join("")||(el.value.trim()?'<p class="scnote">没有找到匹配的景点</p>':"")});
(function(){let sx=0,sy=0,li=null,dx=0;
  document.addEventListener("touchstart",e=>{const l=e.target.closest(".apsw");document.querySelectorAll(".apsw.open").forEach(x=>{if(x!==l)x.classList.remove("open")});if(!l)return;li=l;sx=e.touches[0].clientX;sy=e.touches[0].clientY;dx=0},{passive:true});
  document.addEventListener("touchmove",e=>{if(!li)return;dx=e.touches[0].clientX-sx;const dy=e.touches[0].clientY-sy;if(Math.abs(dy)>Math.abs(dx)){return}if(dx<-10)li.style.transform=`translateX(${Math.max(dx,-84)}px)`;else if(dx>10&&li.classList.contains("open"))li.style.transform=`translateX(${Math.min(-84+dx,0)}px)`},{passive:true});
  document.addEventListener("touchend",()=>{if(!li)return;li.style.transform="";if(dx<-40)li.classList.add("open");else if(dx>30)li.classList.remove("open");li=null},{passive:true});})();
/* ===== 分享行程 ===== */
const SHARE_BASE="https://shiyang0530.github.io/kyoto-techo/";
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
  if(url)s+=`\n在《京都旅行手帖》里打开（可一键导入行程）：\n${url}\n`;return s}
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
  el.innerHTML=`<header><div class="ps-brand">京都旅行手帖</div><h1>${esc(name)}</h1><p>${fmtD(ds[0],true)} – ${fmtD(ds[ds.length-1],true)} · 共 ${ds.length} 天</p></header>`+
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
  if(b=q("[data-apreg]")){const k=b.dataset.apreg,c=AP.regions[k]||0,mx=Math.min(k==="kyoto"?10:4,Math.max(1,apDays(AP.start,AP.end).length));if(c>=mx)delete AP.regions[k];else AP.regions[k]=c+1;apSave();render(cur,false);return}
  if(b=q("[data-apset]")){const [k,v]=b.dataset.apset.split("|");AP[k]=v;apSave();render(cur,false);return}
  if(q("[data-apmust]")){const v=($("#ap-must").value||"").trim();const id=Object.keys(PLANDATA).find(k=>NODES[k]&&NODES[k].n===v);if(id&&!AP.must.includes(id)){AP.must.push(id);apSave();render(cur,false)}return}
  if(b=q("[data-apmustrm]")){AP.must=AP.must.filter(x=>x!==b.dataset.apmustrm);apSave();render(cur,false);return}
  if(q("[data-apgo]")){AP_SEED=1;AP_RES=apGenerate();render(cur,false);if(!wide()){const r=document.getElementById("R");r&&r.scrollIntoView({behavior:"smooth"})}return}
  if(q("[data-apre]")){AP_SEED++;AP_RES=apGenerate();render(cur,false);return}
  if(q("[data-apsave]")&&AP_RES&&!AP_RES.err){const nm=($("#ap-name").value||"自动行程").trim();PLAN=JSON.parse(JSON.stringify(AP_RES.plan));pvNew(nm,PLAN,AP_RES.meta,Object.assign({},AP_RES.opt,{baseRes:AP_RES.base}));savePlan();go("plan");return}
  if(q("[data-pvdup]")){const c=PV.v[PV.cur];pvNew((c?c.name:"行程")+"（副本）",PLAN,c?c.meta:{},c?c.opt:null);render(cur,false);return}
  if(q("[data-pvnew]")){PLAN={};pvNew("新行程 "+(Object.keys(PV.v).length+1),{});savePlan();render(cur,false);return}
  if(q("[data-pvren]")){PV_REN=!PV_REN;render(cur,false);return}
  if(q("[data-pvrenok]")){const v=($("#pv-name").value||"").trim();if(v){PV.v[PV.cur].name=v;pvSave()}PV_REN=false;render(cur,false);return}
  if(q("[data-pvdel]")){if(!PV_DEL){PV_DEL=true;render(cur,false);setTimeout(()=>{PV_DEL=false},4000);return}delete PV.v[PV.cur];PV_DEL=false;pvSwitch(Object.keys(PV.v)[0]);render(cur,false);return}
},true);

let PENDING_FILTER=null;
let MY={};try{MY=JSON.parse(localStorage.getItem("kyoto-mytags")||"{}")||{}}catch(e){MY={}}
function saveMy(){Object.keys(MY).forEach(k=>{if(!MY[k]||!MY[k].length)delete MY[k]});try{localStorage.setItem("kyoto-mytags",JSON.stringify(MY))}catch(e){}}
const myAll=()=>{const s=new Set(PRESET);Object.values(MY).forEach(a=>a.forEach(x=>s.add(x)));return [...s]};
const myCount=()=>Object.keys(MY).filter(k=>NODES[k]).length;
function mineBlock(n){const cur=MY[n.id]||[];
  return `<div class="mine" id="mine"><span class="eyebrow">我的标签</span><div class="mrow">${myAll().map(x=>`<button class="mt${cur.includes(x)?" on":""}" data-mytoggle="${esc(x)}" aria-pressed="${cur.includes(x)}">${x==="收藏"?(cur.includes(x)?"♥ ":"♡ "):""}${esc(x)}</button>`).join("")}<span class="madd"><input id="mytag-input" maxlength="12" placeholder="新标签…" aria-label="添加自己的标签"><button class="mt plus" data-myadd="1">添加</button></span></div>${n.depth>=2?`<div class="mrow prow"><span class="eyebrow">旅行计划</span>${datesOf(n.id).map(d=>`<span class="mt on pd">第${dayNo(d)}天 · ${fmtD(d)}<button class="px" data-planrm="${d}" aria-label="从${fmtD(d)}移除">×</button></span>`).join("")}<span class="madd"><input type="date" id="plan-date" value="${esc(LASTDATE)}" aria-label="选择日期"><button class="mt plus" data-planadd="1">加入行程</button></span><button class="mt" data-route="plan">查看行程单 →</button></div>`:""}</div>`}
function refreshMine(){const el=document.querySelector("#R .mine");const p=parseRoute(cur);if(el&&p.node)el.outerHTML=mineBlock(p.node);const c=document.getElementById("myCnt");if(c)c.textContent=myCount();try{syncTab()}catch(e){}}
let FILTER=null,FBAR_OPEN=false;
const UPPER=n=>n.id==="root"||n.id==="kyoto";
const tiered=n=>!UPPER(n)&&n.c.length>5;
function subtree(n){const a=[];(function w(x){x.c.forEach(c=>{a.push(c);w(c)})})(n);return a}
const isMy=k=>k&&k.startsWith("my:");
const isPlan=k=>k&&k.startsWith("plan:");
const matchTag=(n,k)=>isPlan(k)?(k==="plan:*"?datesOf(n.id).length>0:(PLAN[k.slice(5)]||[]).includes(n.id)):isMy(k)?(k==="my:*"?!!(MY[n.id]&&MY[n.id].length):(MY[n.id]||[]).includes(k.slice(3))):hasTag(n,k);
const tagLabel=k=>isPlan(k)?(k==="plan:*"?"旅行计划":"行程 "+fmtD(k.slice(5))):isMy(k)?(k==="my:*"?"我的标签":k.slice(3)):TAGS[k];
const cntIn=(c,k)=>subtree(c).filter(x=>matchTag(x,k)).length+(matchTag(c,k)?1:0);
function stateOf(n,c){if(!FILTER)return"show";if(UPPER(n))return cntIn(c,FILTER)?"show":"hide";if(matchTag(c,FILTER))return"show";return tiered(n)&&c.star?"fade":(tiered(n)?"hide":"hide")}
function badge(n,c){return FILTER&&UPPER(n)?cntIn(c,FILTER):0}
function filterBar(n){
  const pool=UPPER(n)?subtree(n):n.c;
  const cnt={};pool.forEach(x=>Object.keys(TAGS).forEach(k=>{if(hasTag(x,k))cnt[k]=(cnt[k]||0)+1}));
  const myc={};pool.forEach(x=>{const a=MY[x.id]||[];if(a.length)myc["my:*"]=(myc["my:*"]||0)+1;a.forEach(v=>myc["my:"+v]=(myc["my:"+v]||0)+1)});
  const pc={};pool.forEach(x=>{const a=datesOf(x.id);if(a.length)pc["plan:*"]=(pc["plan:*"]||0)+1;a.forEach(d=>pc["plan:"+d]=(pc["plan:"+d]||0)+1)});
  const pks=Object.keys(pc).sort((a,b)=>(b==="plan:*")-(a==="plan:*")||a.localeCompare(b));
  const pchip=k=>`<button class="fchip plan${FILTER===k?" on":""}" data-filter="${esc(k)}">${k==="plan:*"?"📅 旅行计划":"第"+dayNo(k.slice(5))+"天 "+fmtD(k.slice(5))}<small>${pc[k]}</small></button>`;
  const mks=Object.keys(myc).sort((a,b)=>(b==="my:*")-(a==="my:*")||((PRESET.indexOf(a.slice(3))+1)||99)-((PRESET.indexOf(b.slice(3))+1)||99)||myc[b]-myc[a]);
  const ks=Object.keys(cnt).sort((a,b)=>(b==="hot")-(a==="hot")||cnt[b]-cnt[a]);if(!ks.length&&!mks.length&&!pks.length)return"";
  const LIM=8,more=ks.length>LIM;
  const chip=(k,i)=>`<button class="fchip${FILTER===k?" on":""}${i>=LIM&&FILTER!==k?" extra":""}" data-filter="${k}">${esc(TAGS[k])}<small>${cnt[k]}</small></button>`;
  const mchip=k=>`<button class="fchip my${FILTER===k?" on":""}" data-filter="${esc(k)}">${k==="my:*"?"♥ 我的标签":esc(k.slice(3))}<small>${myc[k]}</small></button>`;
  return `<div class="fbar${FBAR_OPEN?" open":""}" role="toolbar" aria-label="按标签筛选"><button class="fchip${FILTER?"":" on"}" data-filter="">全部</button>${pks.map(pchip).join("")}${mks.map(mchip).join("")}${ks.map(chip).join("")}${more?`<button class="fmore" data-fmore="1">${FBAR_OPEN?"收起 ▴":`更多 ${ks.length-LIM} ▾`}</button>`:""}</div>`;
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
  const marks=kids.map(c=>{const i=n.c.indexOf(c);const st=focus?(c.id===focus?"show":"fade"):stateOf(n,c);if(st==="hide")return"";const minor=tiered(n)&&!c.star;const r=minor?10:14;const right=c.x<440;const tx=right?c.x+r+8:c.x-r-8;const b=badge(n,c);
    return `<g class="mk${minor?" minor":""}${st==="fade"?" fade":""}" data-go="${c.id}" tabindex="0" role="link" aria-label="${esc(c.n)}"><circle cx="${c.x}" cy="${c.y}" r="${r}"/><text class="num" x="${c.x}" y="${c.y}">${i+1}</text><text class="lab" x="${tx}" y="${c.y+5}" text-anchor="${right?"start":"end"}">${esc(c.n)}${b?` · ${b}`:""}</text></g>`}).join("");
  return `<svg class="map${P?" plan":""}" viewBox="0 0 600 440" role="img" aria-label="${esc(n.n)}${P?"境内":""}示意地图"><rect width="600" height="440" style="fill:var(--land)"/><g stroke-width=".5">${grid}</g>${P?planSVG(P):hills+water+rivers+geo}${route}${marks}
  <g transform="translate(560 40)"><path d="M0 -18 L7 6 L0 1 L-7 6Z" style="fill:var(--ink)"/><text y="22" text-anchor="middle" style="fill:var(--ink);font:600 11px var(--f-mono)">N</text></g>
  <text x="14" y="428" style="fill:var(--muted);font:10px var(--f-mono)">${P?esc(P.note||"境内示意图 · 非实际比例"):"示意图 · 非实际比例"+(n.route?" · 虚线为推荐步行顺序":"")}</text></svg>`;
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
const SC_TAGS=["sakura","momiji","snow","matsuri","newyear"];
const SC_DEF={sakura:[[3.7,4.2]],momiji:[[11.4,12.1]],snow:[[1.1,2.7]],newyear:[[12.97,13],[1,1.15]],matsuri:[]};
function seasonCal(n){const tags=(n.t||[]).filter(t=>SC_TAGS.includes(t));if(!tags.length)return "";
  const rows=tags.map(t=>{const seg=(n.sm&&n.sm[t])||SC_DEF[t];if(!seg||!seg.length)return "";
    return `<div class="scrow"><span class="scl">${esc((TAGS[t]||t))}</span><div class="sctrack">${seg.map(([a,b,nm,dt])=>`<i class="sc-${t}" style="left:${((a-1)/12*100).toFixed(2)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%"${nm?` title="${esc(nm+" "+(dt||""))}"`:""}></i>`).join("")}</div></div>${seg.some(x=>x[2])?`<ul class="evl">${[...seg].sort((x,y)=>x[0]-y[0]).filter(x=>x[2]).map(x=>`<li><b>${esc(x[2])}</b><span>${esc(x[3]||"")}</span></li>`).join("")}</ul>`:""}`}).join("");
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
  if(!a.length)return `<div class="photo${small?" small":""}"><div class="ph">在这个文件夹放入照片<span class="mono">京都旅游${n.key?"\\"+n.folders.join("\\"):""}</span></div></div>`;
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
try{const o=JSON.parse(localStorage.getItem("kyoto-pins")||"{}");for(const k in o)if(NODES[k]){NODES[k].px=o[k][0];NODES[k].py=o[k][1]}}catch(e){}
function savePins(){const o={};ORDER.forEach(n=>{if(n.px!=null&&(n.px!==DEF[n.id][0]||n.py!==DEF[n.id][1]))o[n.id]=[n.px,n.py]});try{localStorage.setItem("kyoto-pins",JSON.stringify(o))}catch(e){}return o}
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
const INFO={p:"门票",h:"时间",a:"交通"};
function related(n){
  const fam=new Set([n.id,n.parent?.id,...n.c.map(c=>c.id)]);
  return ORDER.filter(m=>!fam.has(m.id)&&m.depth>=2).map(m=>({m,s:m.t.filter(t=>n.t.includes(t)&&t!=="hot").length+(m.t.includes("hot")?.3:0)}))
    .filter(x=>x.s>=1).sort((a,b)=>b.s-a.s).slice(0,4).map(x=>x.m);
}
function leftPage(n){
  const pp=!n.c.length&&n.parent&&(n.parent.air||n.parent.plan);
  let h=`<div class="maphead"><span class="eyebrow">${n.c.length?(n.air?"境内图 · 航空照片":n.img?"插画地图":n.plan?"境内图":"地图"):pp?"境内图 · 位置":"图片"}</span><span class="eyebrow mono">${esc(n.ja||"")}</span></div>`;
  if(n.c.length){
    h+=filterBar(n);
    h+=n.img?imgMap(n):mapSVG(n);
    h+=`<div class="legend">${n.c.map((c,i)=>{const st=stateOf(n,c);if(st==="hide")return"";return `<button data-go="${c.id}" class="${st==="fade"?"fade":""}${tiered(n)&&c.star?" star":""}"><span class="n">${n.img?"·":String(i+1).padStart(2,"0")}</span><b>${esc(c.n)}${badge(n,c)?` <small>${badge(n,c)}</small>`:""}</b></button>`}).join("")}</div>`;
  } else if(pp){h+=(n.parent.air?imgMap(n.parent,n.id):mapSVG(n.parent,n.id))+`<div class="legend">${n.parent.c.map((c,i)=>`<button data-go="${c.id}" class="${c.id===n.id?"star":"fade"}"><span class="n">${String(i+1).padStart(2,"0")}</span><b>${esc(c.n)}</b></button>`).join("")}</div>`+photo(n,true)}
  else h+=photo(n,false);
  return h+`<span class="folio">${pg(n.page*2-1)}</span>`;
}
function rightPage(n){
  const kindLabel={总览:"总览",地区:"地区",区域:"区域",景点:"景点",看点:"看点"}[n.kind];
  let h=`<div class="kicker"><span class="kind">${kindLabel}</span><span>${n.parent?esc(n.parent.n):"关西 · 冬日"}</span></div>
  <h1>${esc(n.n)}</h1><div class="ja">${esc(n.ja)}</div>`;
  if(n.t.length)h+=`<div class="chips">${n.t.map(t=>chip(t)).join("")}</div>`;
  if(n.depth>=1)h+=mineBlock(n);
  if(n.c.length&&((IMG[n.id]||[]).length||(n.ph&&CIMG[n.ph])))h+=photo(n,true);
  SEEN=new Set(Object.keys(TERMS_).filter(k=>TERMS_[k].n===n.n));
  h+=`<p class="intro">${lk(n.d)}</p>`;
  if(n.hl&&n.hl.length)h+=`<div class="sec">亮点</div><ol class="hl">${n.hl.map(x=>{const i=x.indexOf("：");return `<li>${i>0&&i<12?`<b>${esc(x.slice(0,i))}</b>${lk(x.slice(i+1))}`:lk(x)}</li>`}).join("")}</ol>`;
  if(n.i){h+=`<dl class="info">${Object.entries(INFO).filter(([k])=>n.i[k]).map(([k,l])=>`<dt>${l}</dt><dd>${esc(n.i[k])}</dd>`).join("")}</dl>`}
  if(n.depth>=2){const host=[n,n.parent].find(x=>x&&x.depth>=2&&x.u);
    h+=`<p class="official">${host?`<a href="${esc(host.u)}" target="_blank" rel="noopener">${host===n?"官方网站":"「"+esc(host.n)+"」官方网站"} ↗</a>`:`<a href="${esc(searchURL(n))}" target="_blank" rel="noopener">在网上搜索官方信息 ↗</a><label class="eng">用 <select data-eng aria-label="选择搜索引擎">${Object.entries(ENGINES).map(([k,v])=>`<option value="${k}"${k===ENGINE?" selected":""}>${v[0]}</option>`).join("")}</select> 搜索</label>`}<span>开放时间、门票、休息日等重要信息请以官方发布为准。</span></p>`}
  if(n.tip)h+=`<p class="tip"><b>小贴士</b>${lk(n.tip)}</p>`;
  if(n.cards&&n.cards.length)h+=`<div class="sec">细节</div><div class="dcards">${n.cards.map(c=>`<div class="dcard${c.img&&CIMG[c.img]?" hasimg":""}">${c.svg?`<figure class="dsvg">${c.svg}</figure>`:""}${c.img&&CIMG[c.img]?`<figure${CIMG[c.img].ai?' class="ai"':""}><img src="${CIMG[c.img].src}" alt="${esc(c.h)}" loading="lazy"><figcaption>${CIMG[c.img].ai?`插画 · ${esc(CIMG[c.img].by)}`:`${esc(CIMG[c.img].by)} · <a href="${esc(CIMG[c.img].u)}" target="_blank" rel="noopener">${esc(CIMG[c.img].lic)}</a> · Wikimedia Commons`}</figcaption></figure>`:c.ext?extBox(c.ext,""):""}<span class="dk">${esc(c.k)}</span><b>${lk(c.h)}</b><p>${lk(c.p)}</p></div>`).join("")}</div>`;
  if(n.hist&&n.hist.length)h+=`<div class="sec">历史沿革</div><ol class="tl">${n.hist.map(([y,t])=>`<li><span class="yr">${esc(y)}</span><span>${lk(t)}</span></li>`).join("")}</ol>`;
  if(n.arch&&n.arch.length)h+=`<div class="sec">建筑档案</div><dl class="arch">${n.arch.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${lk(v)}</dd>`).join("")}</dl>`;
  SEEN=null;
  if(n.c.length){
    const label=n.depth===0?"章节":(n.c[0].kind||"下一层");
    if(FILTER&&UPPER(n)){const M=subtree(n).filter(x=>x.depth>=2&&!x.c.some(()=>false)&&matchTag(x,FILTER));
      h+=`<div class="sec">符合「${esc(tagLabel(FILTER))}」的景点 · ${M.length}</div><div class="kids">${M.map((c,i)=>`<button class="kid" data-go="${c.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(c.n)}</b><small>${esc(c.folders.slice(0,-1).slice(1).join(" › ")||c.parent.n)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`).join("")}</div>`;}
    h+=`<div class="sec">${label} · ${n.c.length}</div><div class="kids">${n.c.map((c,i)=>{const st=stateOf(n,c);if(st==="hide")return"";return `<button class="kid${st==="fade"?" fade":""}" data-go="${c.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${tiered(n)&&c.star?'<i class="star">★</i>':""}${esc(c.n)}</b><small>${esc(c.d)}</small></span><em>P.${pg(c.page*2-1)}</em></button>`}).join("")}</div>`;
  }
  const rel=n.depth>=2?related(n):[];
  if(rel.length)h+=`<div class="sec">同类推荐</div><div class="rel">${rel.map(m=>`<button class="relc" data-go="${m.id}"><b>${esc(m.n)}</b><small>${esc(m.parent.n)} · ${m.t.filter(t=>n.t.includes(t)).map(t=>TAGS[t]).join(" / ")}</small></button>`).join("")}</div>`;
  h+=localFood(n);
  h+=srcBlock(n);
  if(n.depth>=1)h+=`<div class="folder mono">图片文件夹：京都旅游\\${esc(n.folders.join("\\"))}</div>`;
  return h+`<span class="folio">${pg(n.page*2)} / ${pg(total*2)}</span>`;
}

const PREFJA={kyoto:"京都",nara:"奈良",shiga:"滋賀",osaka:"大阪",hyogo:"兵庫"},PREFZH={kyoto:"京都",nara:"奈良",shiga:"滋贺",osaka:"大阪",hyogo:"兵库"};
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
  if(t.q){const kw=t.q,pj=PREFJA[t.pref]||"";
    h+=`<div class="sec">搜索热门餐厅</div><p class="foodlinks"><a href="https://tabelog.com/${t.pref?t.pref+"/":""}rstLst/?sk=${encodeURIComponent(kw)}&SrtT=rt" target="_blank" rel="noopener">食べログ 评分排行 ↗</a><a href="https://www.google.com/maps/search/${encodeURIComponent(kw+" "+pj)}" target="_blank" rel="noopener">Google 地图 ↗</a><a href="https://www.dianping.com/ai-search?keyword=${encodeURIComponent((PREFZH[t.pref]||"")+" "+t.n)}" data-dp="${esc((PREFZH[t.pref]||"")+" "+t.n)}" data-dpk="${esc(t.n)}" target="_blank" rel="noopener">大众点评 ↗</a><span class="scnote" style="flex-basis:100%;margin:0">手机上点「大众点评」会在 App 里直接搜索这道菜，城市按 App 当前所选城市：出发前请先在 App 里把城市切换到京都或大阪，到了日本会自动定位。</span><a href="https://www.google.com/search?q=${encodeURIComponent(kw+" "+pj+" 人気店")}" target="_blank" rel="noopener">网页搜索 ↗</a></p><p class="scnote">本书不推荐具体店家。评分和营业信息以各网站为准。</p>`}
  return h;
}
function mlabel(x){const m=x>=13?12:Math.floor(x)>12?1:Math.floor(x);const d=x-Math.floor(x);return m+"月"+(d<0.34?"上旬":d<0.67?"中旬":"下旬")}
function localFood(n){const ids=new Set([n.id,...(n.depth<=1?[]:subtree(n).map(x=>x.id))]);if(n.depth===1)subtree(n).forEach(x=>ids.add(x.id));
  const fs=Object.entries(TERMS_).filter(([,t])=>t.k==="美食"&&(t.w||[]).some(x=>ids.has(x)));if(!fs.length)return "";
  return `<div class="sec">当地美食</div><div class="foods">${fs.map(([id,t])=>{const c=t.img&&CIMG[t.img];return `<button class="food" data-route="term-${id}">${c?`<img src="${c.src}" alt="" loading="lazy">`:`<span class="noimg">食</span>`}<b>${esc(t.n)}</b>${t.sm&&t.sm.length&&t.sm[0][2]&&t.sm[0][2]!==t.n?`<small>${esc(t.sm[0][2])}</small>`:""}</button>`}).join("")}</div>`}
function termPages(id){
  const t=TERMS_[id];const back=(BACK[id]||[]);
  const L=`<span class="eyebrow">词条 · ${esc(t.k)}</span><div class="tagtitle termtitle">${esc(t.n)}</div><div class="ja mono">${esc(t.ja)}</div>
  <p class="intro" style="margin-top:14px">${esc(t.d)}</p>${foodBlock(t)}${t.svg?`<figure class="termsvg">${t.svg}</figure>`:""}<p class="wiki">维基百科：<a href="https://zh.wikipedia.org/w/index.php?search=${encodeURIComponent(t.n.split("（")[0])}" target="_blank" rel="noopener">中文 ↗</a> · <a href="https://ja.wikipedia.org/w/index.php?search=${encodeURIComponent(t.ja.split("（")[0])}" target="_blank" rel="noopener">日文 ↗</a></p>${(t.rel||[]).filter(r=>TERMS_[r]).length?`<div class="sec">相关词条</div><div class="cloud">${t.rel.filter(r=>TERMS_[r]).map(r=>`<button class="tag" data-route="term-${r}">${esc(TERMS_[r].n)}</button>`).join("")}</div>`:""}
  <p style="margin-top:22px"><button class="btn" data-route="terms">← 词典总目</button></p><span class="folio">词</span>`;
  const R=`<div class="kicker"><span class="kind">词条</span><span>${t.k==="美食"?"时令 · 产地 · 餐厅搜索":"在书中出现的位置"}</span></div><h1>${esc(t.n)}</h1>${foodInfo(t)}${back.length?`<div class="sec">出现在 · ${back.length}</div><div class="kids">${back.map((n,i)=>`<button class="kid" data-go="${n.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(n.n)}</b><small>${esc(n.folders.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small></span><em>P.${pg(n.page*2-1)}</em></button>`).join("")}</div>`:t.k==="美食"?"":`<p class="intro" style="margin-top:14px">目前书中还没有页面提到这个词条。</p>`}<span class="folio">词</span>`;
  return [L,R];
}
function termIndex(){
  const by=c=>Object.entries(TERMS_).filter(([,t])=>t.k===c);
  const L=`<span class="eyebrow">词典</span><div class="tagtitle">词典</div><p style="color:var(--ink-2)">正文里带下划线的词都收录在这里：宗派、建筑样式、佛像、祭典，以及相关的人物和历史事件。点正文中的下划线会先弹出小卡片，再点「查看词条」进入这里。</p>
  <div class="cloud">${TCATS.map(c=>`<a class="tag" href="#tc-${encodeURIComponent(c)}" data-tjump="${esc(c)}">${esc(c)} <span class="mono" style="opacity:.6">${by(c).length}</span></a>`).join("")}</div><span class="folio">词</span>`;
  const R=`<div class="kicker"><span class="kind">索引</span><span>共 ${Object.keys(TERMS_).length} 条</span></div><h1>词典</h1>${TCATS.map(c=>`<div class="sec" id="tc-${esc(c)}">${esc(c)} · ${by(c).length}</div><div class="kids">${by(c).map(([id,t],i)=>`<button class="kid" data-route="term-${id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(t.n)}</b><small>${esc(t.d.slice(0,34))}…</small></span><em>${(BACK[id]||[]).length||""}</em></button>`).join("")}</div>`).join("")}<span class="folio">词</span>`;
  return [L,R];
}
function lca(ids){const ch=id=>{const a=[];let n=NODES[id];while(n){a.unshift(n);n=n.parent}return a};const cs=ids.map(ch);let i=0;while(cs.every(c=>c[i]&&c[i]===cs[0][i]))i++;let n=cs[0][Math.max(0,i-1)]||BOOK;if(!n.c.length&&n.parent)n=n.parent;if(ids.length===1&&NODES[ids[0]].parent)n=NODES[ids[0]].parent;return n}
function planPages(){
  const ds=planDates();
  const L=`<span class="eyebrow">个人</span><div class="tagtitle">旅行计划</div>${pvBar()}
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
    return `<div class="sec" id="mt-${esc(x)}">${esc(x)} · ${L2.length}</div><div class="kids">${L2.map((n,i)=>`<div class="kid myk"><span class="n">${String(i+1).padStart(2,"0")}</span><button class="mylink" data-go="${n.id}"><b>${esc(n.n)}</b><small>${esc(n.folders.slice(0,-1).join(" › ")||"总览")}</small></button><button class="myx" data-myremove="${n.id}|${esc(x)}" aria-label="从「${esc(x)}」移除">×</button></div>`).join("")}</div>`}).join(""):`<p class="intro" style="margin-top:14px">这里还是空的。翻到任何一个景点，在标题下方的「我的标签」里点一下，就能把它存进来。</p>`}<span class="folio">MY</span>`;
  return [L,R];
}
function guidePages(){
  const L=`<div class="gcover"><span class="eyebrow">关西 · 京都及周边</span><div class="cover-t">京都旅行手帖</div><p class="cover-s">一本可以翻页、搜索、按兴趣筛选的旅行电子书。六个章节，从京都城中到日本海边，${ORDER.filter(n=>n.depth>=2).length} 个景点与看点。</p>
  <div class="cover-img"><img src="${IMGS.ROOT}" alt="京都及周边插画地图"></div><button class="btn pri" data-go="root">开始阅读 →</button></div>`;
  const S=[["翻页与层级","书按「总览 → 章节 → 区域 → 景点 → 看点」一层层展开，每一层左边是地图，右边是介绍。点地图上的地名或右侧列表就能进入下一层。用两侧的 ‹ › 按钮或键盘 ← → 按书页顺序翻页，Backspace 回到上一层，顶部的路径可以随时跳回任何一层。手机上底部的「‹ 返回」回到上一个看过的页面，左右滑动或「下一页」按书页顺序翻页。"],
  ["读懂地图","插画地图上的大号书法字是该区域的主推景点，小字是其他景点；地图边缘的罗盘箭头指向图外的景点，点击即可前往。示意地图上的编号与下方图例对应。"],
  ["按兴趣筛选","地图上方有一排标签，例如「赏枫」「日本战国」「免门票」。选一个标签，地图和列表只保留符合的景点，主推景点不符合时会变淡。在总览和京都页选标签，会显示每个区域有几处符合。翻页后筛选自动清除。"],
  ["搜索与标签索引","右上角搜索框可以搜景点名，也可以搜标签，按 / 键快速聚焦。打开「目录」，下方的「标签索引」按时令、历史文化、寺社、自然、吃喝玩乐分组，「历史」包含日本战国、明治维新、文学等子标签，点任意一行进入该标签的全部景点。"],
  ["我的标签","每个景点标题下都有「我的标签」：点「♡ 收藏」「想去」「已去过」，或输入自己的标签（例如「第二天」「带父母」）。所有保存的景点汇总在目录最后的「我的标签」页，可以导出后在别的设备导入。标签只保存在你自己的浏览器里。"],
  ["旅行计划","景点页的「我的标签」下方有「旅行计划」：选一个日期，点「加入行程」即可把景点排进那一天，一个景点也可以排进多天。顶部的「旅行计划」按钮打开行程单，按日期列出每天的景点并可调整顺序；点「在地图上看」或在地图上方选「第 N 天」，地图只显示当天的景点。行程和我的标签一起导出、导入。"],
  ["自动生成行程","在「旅行计划」页或目录里点「✨ 自动生成行程」：填出发和结束日期（可以再填到达、离开的时间和机场／车站，到达日和离开日会自动扣掉入境、交通和提前到机场的时间）、住宿地点（不填会推荐住宿区域）、节奏（轻松／适中／密集）、交通方式（公共交通／自驾），再选几个偏好标签，例如「适合老人」「适合情侣」「美食」「温泉」，也可以指定必去景点。想专门去奈良、大阪、宇治等地玩一天，就在「想去的区域」里点一下（每点一次多排一天）；时令类偏好（赏樱、赏枫、赏雪、祭典、跨年）只在出行日期对得上时生效。系统会按区域把景点排成每天的路线，给出大致时间、午餐和当地美食，并自动考虑出行期间的赏樱、红叶、祭典和跨年活动。不满意可以点「换一种排法」，也可以直接改预览：手机上把某个景点向左滑出「删除」，电脑上鼠标移上去点「删除」；每天下方的输入框打字即可搜索并添加景点，时间会自动重算；满意就保存为一个版本，之后在旅行计划里照常手动调整。"],
  ["多版本行程","旅行计划顶部的「行程版本」可以保存多套方案：切换、复制为新版本、新建空白版本、重命名或删除。每个版本单独保存，互不影响。"],
  ["分享行程","在旅行计划页点「📤 分享行程」：复制链接发给朋友，对方打开就是这本手帖，并能一键把行程导入成自己的新版本；「复制文字版」适合直接贴进微信；「打印 / 存为 PDF」会生成一份干净的行程单，打印时选「存储为 PDF」即可。"],
  ["词典与深度内容","正文中带虚下划线的词（宗派、建筑样式、佛像、人物、历史事件等）可以点击，先弹出一张小卡片，再点「查看词条」进入词典页，看它在书中哪些地方出现。重点古迹还有「亮点」「历史沿革」「建筑档案」，看点页里有结构、佛像等细节卡和境内图。每页底部列出资料来源。目录里的「词典」可以浏览全部词条。"],
  ["门票与官网","景点页列出门票、时间和交通的参考信息。开放时间和票价经常调整，请以官方发布为准：有官网的景点可以直接打开，其他景点可以用你选择的搜索引擎（Google、Bing、百度、Yahoo! JAPAN、DuckDuckGo）搜索。"],
  ["离线使用","整本书是一个 HTML 文件，地图、字体和文字都已内置。把文件保存到电脑或手机，用浏览器打开即可离线阅读；只有官网和搜索链接需要联网。在 iPhone 上请用 Safari 打开，而不是在「文件」里预览。"]];
  const R=`<div class="kicker"><span class="kind">使用说明</span><span>第一次阅读请看这里</span></div><h1>怎样使用这本书</h1>${S.map(([h,p],i)=>`<div class="guide"><span class="gn">${String(i+1).padStart(2,"0")}</span><div><b>${h}</b><p>${p}</p></div></div>`).join("")}<span class="folio">ii</span>`;
  return [L,R];
}
let CLEAR_ARMED=false;

function seasonTagPages(t,list){
  const segOf=n=>(n.sm&&n.sm[t])||null;
  const rows=list.map(n=>({n,seg:segOf(n)||SC_DEF[t]||[],est:!segOf(n)})).filter(r=>r.seg.length);
  const nost=list.filter(n=>!rows.find(r=>r.n===n));
  const key=r=>{const a=r.seg.map(s=>s[0]);/* 跨年段：12 月底算在最前 */return Math.min(...a.map(x=>x>=12.5&&t!=="momiji"?x-12:x))};
  rows.sort((a,b)=>key(a)-key(b)||a.n.page-b.n.page);
  const pct=x=>((x-1)/12*100).toFixed(2);
  const fmt=x=>{const m=Math.floor(x)>12?1:Math.floor(x);const d=x-Math.floor(x);return m+"月"+(d<0.34?"上旬":d<0.67?"中旬":"下旬")};
  const span=seg=>{if(seg.some(x=>x[2]))return [...seg].sort((x,y)=>x[0]-y[0]).map(x=>`<b>${esc(x[2])}</b> ${esc(x[3]||"")}`).join("<br>");let sg=seg.map(x=>[...x]);const w=sg.find(x=>x[1]>=13),f=sg.find(x=>x[0]<=1.01);if(w&&f&&w!==f){sg=sg.filter(x=>x!==w&&x!==f);sg.unshift([w[0],f[1]+12])}
    const one=([a,b])=>{const A=fmt(a),B=fmt(Math.min(b-0.01,b>13?b-12:12.99)>12?Math.min(b-0.01,b>13?b-12:12.99)-12:Math.min(b-0.01,b>13?b-12:12.99));if(A===B)return A;return Math.floor(a)===Math.floor(b>13?b-12:Math.min(b-0.01,12.99))&&b<13?A+"–"+B.replace(/^\d+月/,""):A+"–"+B};
    return sg.map(one).join("、")};
  const plans=Object.keys(PLAN||{}).filter(d=>(PLAN[d]||[]).length).map(d=>{const x=new Date(d);return x.getMonth()+1+(x.getDate()-1)/31});
  const axis=`<div class="scrow scm"><span class="scl"></span><div class="sctrack">${[1,2,3,4,5,6,7,8,9,10,11,12].map(m=>`<span style="left:${((m-0.5)/12*100).toFixed(2)}%">${m}</span>`).join("")}</div></div>`;
  const others=SC_TAGS.filter(k=>TAGCOUNT[k]);
  const L=`<span class="eyebrow">时令</span><div class="tagtitle">${esc(TAGS[t])}</div><p style="color:var(--ink-2)">共 ${list.length} 处，分布在 ${new Set(list.map(n=>(n.folders[0]||""))).size} 个地区。右侧按时间先后排列，色条是往年的大致最佳时期，点景点名可跳转。</p>
   <div class="cloud">${others.map(k=>`<button class="tag${k===t?" cur":""}" data-tag="${k}">${esc(TAGS[k])} <span class="mono" style="opacity:.6">${TAGCOUNT[k]}</span></button>`).join("")}</div>
   <div class="sec" style="margin-top:22px">时令总览</div><div class="scal"><div class="scgrid">${others.map(k=>{const ns=ORDER.filter(n=>hasTag(n,k));const segs=ns.flatMap(n=>(n.sm&&n.sm[k])||SC_DEF[k]||[]);return `<div class="scrow"><button class="scl scbtn" data-tag="${k}">${esc(TAGS[k])}</button><div class="sctrack">${segs.map(([a,b])=>`<i class="sc-${k}" style="left:${pct(a)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%;opacity:${k===t?.35:.18}"></i>`).join("")}</div></div>`}).join("")}${axis}</div></div>
   <p class="scnote">色条为往年大致时期，每年会有前后浮动，出发前请查当年的开花、红叶或活动公告。<b>浅色</b>表示该地点没有单独资料，按京都市区平均估计。${t==="snow"?"京都市区一个冬天通常只积雪几次、每次一两天，色条表示可能遇到的时段。":""}</p><span class="folio">时令</span>`;
  const R=`<div class="kicker"><span class="kind">时令月历</span><span>按时间先后</span></div><h1>${esc(TAGS[t])}</h1>
   <div class="scal sclist" data-noswipe${t==="matsuri"?` style="--spw:170px"`:""}>${plans.length?`<div class="scplanlab">竖线 = 你的行程日期</div>`:""}<div class="scgrid">${axis}${rows.map(r=>`<div class="scrow scitem"><button class="scl scname" data-go="${r.n.id}" title="${esc(r.n.n)}"><b>${esc(r.n.n)}</b><small>${esc(r.n.folders.slice(1,-1).join("·")||r.n.folders[0]||"")}</small></button><div class="sctrack">${r.seg.map(([a,b,nm,dt])=>`<i class="sc-${t}${r.est?" est":""}" style="left:${pct(a)}%;width:${Math.max(1.2,(b-a)/12*100).toFixed(2)}%"${nm?` title="${esc(nm+" "+(dt||""))}"`:""}></i>`).join("")}${plans.map(m=>`<b class="scpl" style="left:${pct(m)}%"></b>`).join("")}</div><span class="scspan${t==="matsuri"?" wide":""}">${span(r.seg)}</span></div>`).join("")}${axis}</div></div>
   ${nost.length?`<p class="scnote">另有 ${nost.length} 处暂无时期资料：${nost.map(n=>`<button class="linkish" data-go="${n.id}">${esc(n.n)}</button>`).join("、")}</p>`:""}<span class="folio">时令</span>`;
  return [L,R];
}
function tagPages(t){
  const list=ORDER.filter(n=>hasTag(n,t));
  const L=`<span class="eyebrow">标签</span><div class="tagtitle">${esc(TAGS[t])}</div>${TAG_PARENT[t]?`<p style="margin:0 0 6px"><span class="eyebrow">上级标签</span> <button class="tag" data-tag="${TAG_PARENT[t]}">${esc(TAGS[TAG_PARENT[t]])}</button></p>`:""}${TAG_KIDS[t]?`<p style="margin:0 0 6px"><span class="eyebrow">包含</span> ${TAG_KIDS[t].filter(k=>TAGCOUNT[k]).map(k=>`<button class="tag" data-tag="${k}">${esc(TAGS[k])} ${TAGCOUNT[k]}</button>`).join(" ")}</p>`:""}<p style="color:var(--ink-2)">共 ${list.length} 处，分布在 ${new Set(list.map(n=>(n.folders[0]||"")) ).size} 个地区。点击右侧任意条目跳转。</p>
   <div class="cloud">${Object.keys(TAGS).filter(k=>TAGCOUNT[k]).map(k=>`<button class="tag${k===t?" cur":""}" data-tag="${k}">${esc(TAGS[k])} <span class="mono" style="opacity:.6">${TAGCOUNT[k]}</span></button>`).join("")}</div><span class="folio">TAG</span>`;
  if(SC_TAGS.includes(t))return seasonTagPages(t,list);
  const R=`<div class="kicker"><span class="kind">索引</span><span>按书页顺序</span></div><h1>${esc(TAGS[t])}</h1><div class="kids" style="margin-top:14px">${list.map((n,i)=>`<button class="kid" data-go="${n.id}"><span class="n">${String(i+1).padStart(2,"0")}</span><span><b>${esc(n.n)}</b><small>${esc(n.folders.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small></span><em>P.${pg(n.page*2-1)}</em></button>`).join("")}</div><span class="folio">TAG</span>`;
  return [L,R];
}

/* ---------- navigation + page turn ---------- */
let cur="n-root";
const spread=$("#spread"),Lp=$("#L"),Rp=$("#R");
const wide=()=>matchMedia("(min-width:861px)").matches;
const reduced=()=>matchMedia("(prefers-reduced-motion:reduce)").matches;
function parseRoute(r){if(r==="guide")return{guide:true};if(r==="mytags")return{mytags:true};if(r==="plan")return{plan:true};if(r==="autoplan")return{auto:true};if(r.startsWith("trip-")&&r.length>6)return{trip:r.slice(5)};if(r==="terms")return{terms:true};if(r.startsWith("term-")&&TERMS_[r.slice(5)])return{term:r.slice(5)};if(r.startsWith("tag-")&&TAGS[r.slice(4)])return{tag:r.slice(4)};const id=r.startsWith("n-")?r.slice(2):"root";return{node:NODES[id]||BOOK}}
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
  let h=p.guide?`<span class="cur">使用说明</span>`:p.auto?`<button data-go="root">京都及周边</button> › <button data-route="plan">旅行计划</button> › <span class="cur">自动生成行程</span>`:p.trip?`<button data-go="root">京都及周边</button> › <button data-route="plan">旅行计划</button> › <span class="cur">收到的行程</span>`:p.mytags?`<button data-go="root">京都及周边</button> › <span class="cur">我的标签</span>`:p.plan?`<button data-go="root">京都及周边</button> › <span class="cur">旅行计划</span>`:p.terms?`<button data-go="root">京都及周边</button> › <span class="cur">词典</span>`:p.term?`<button data-go="root">京都及周边</button> › <button data-route="terms">词典</button> › <span class="cur">${esc(TERMS_[p.term].n)}</span>`:p.tag?`<button data-go="root">京都及周边</button> › <span class="cur">标签 · ${esc(TAGS[p.tag])}</span>`:
    chain.map((c,i)=>i===chain.length-1?`<span class="cur">${esc(c.n)}</span>`:`<button data-go="${c.id}">${esc(c.n)}</button>`).join(" › ");
  $("#crumbs").innerHTML=h;
}
function edges(p){
  if(p.guide){$("#prevBtn").disabled=true;$("#nextBtn").disabled=false;syncTab();$("#prevBtn").title="";$("#nextBtn").title="下一页："+BOOK.n;return}
  const i=p.node?p.node.page-1:-1;
  $("#prevBtn").disabled=i<0;$("#nextBtn").disabled=i<0||i>=total-1;
  syncTab();$("#prevBtn").title=i>0?"上一页："+ORDER[i-1].n:i===0?"上一页：使用说明":"";$("#nextBtn").title=i>=0&&i<total-1?"下一页："+ORDER[i+1].n:"";
}
let HIST=[],BACKNAV=false;
function go(route,dir){if(route===cur)return;if(!BACKNAV){HIST.push(cur);if(HIST.length>60)HIST.shift()}BACKNAV=false;try{history.replaceState(null,"","#"+route)}catch(e){}if(location.hash!=="#"+route){suppress=true;location.hash=route}render(route,true,dir)}
let suppress=false;
addEventListener("hashchange",()=>{if(suppress){suppress=false;return}render(location.hash.slice(1)||"guide")});
const goNode=id=>go("n-"+id);
$("#prevBtn").onclick=()=>{const p=parseRoute(cur);if(p.node&&p.node.page===1){go("guide",-1);return}if(p.node&&p.node.page>1)go("n-"+ORDER[p.node.page-2].id,-1)};
$("#nextBtn").onclick=()=>{const p=parseRoute(cur);if(p.guide){go("n-root",1);return}if(p.node&&p.node.page<total)go("n-"+ORDER[p.node.page].id,1)};
$("#home").onclick=()=>goNode("root");
addEventListener("keydown",e=>{if(e.target.matches("input"))return;
  if(e.key==="ArrowRight")$("#nextBtn").click();else if(e.key==="ArrowLeft")$("#prevBtn").click();
  else if(e.key==="Backspace"){const p=parseRoute(cur);if(p.node?.parent)go("n-"+p.node.parent.id,-1)}
  else if(e.key==="/"){e.preventDefault();$("#q").focus()}
  else if(e.key==="Escape"){closeAll();hidePop()}
  if(e.target.matches(".mk")&&e.key==="Enter")goNode(e.target.dataset.go)});

document.addEventListener("change",e=>{if(e.target.matches("[data-eng]")){ENGINE=e.target.value;try{localStorage.setItem("kyoto-engine",ENGINE)}catch(err){}render(cur,false)}});
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
  if(e.target.closest("[data-planadd]")){const p=parseRoute(cur);const inp=document.getElementById("plan-date");const d=inp&&inp.value;if(!p.node||!d){inp&&inp.focus();return}LASTDATE=d;try{localStorage.setItem("kyoto-plan-last",d)}catch(err){}PLAN[d]=PLAN[d]||[];if(!PLAN[d].includes(p.node.id))PLAN[d].push(p.node.id);savePlan();refreshMine();return}
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
  if(nodeHits.length)h+=`<div class="grp">页面</div>`+nodeHits.map((n,i)=>`<div class="res${i===0&&!tagHits.length?" on":""}" role="button" tabindex="0" data-go="${n.id}"><b>${esc(n.n)}</b> <span class="mono" style="font-size:11px;color:var(--muted)">P.${pg(n.page*2-1)}</span><small>${esc(n.folders.slice(0,-1).join(" › ")||"总览")} · ${n.kind}</small><span class="chips" style="margin:3px 0 0">${n.t.slice(0,5).map(t=>chip(t,1)).join("")}</span></div>`).join("");
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
const open=new Set(["root","kyoto"]);
function buildTree(){
  const curId=parseRoute(cur).node?.id;
  let n=NODES[curId];while(n){open.add(n.id);n=n.parent}
  const li=n=>`<li><div class="row">${n.c.length?`<button class="tg" data-tg="${n.id}" aria-label="展开">${open.has(n.id)?"▼":"▶"}</button>`:`<span class="tg"></span>`}<button class="nm${n.id===curId?" cur":""}" data-go="${n.id}">${esc(n.n)}</button><span class="pg">${pg(n.page*2-1)}</span></div>${n.c.length&&open.has(n.id)?`<ul>${n.c.map(li).join("")}</ul>`:""}</li>`;
  $("#tree").innerHTML=`<button class="nm guide-link${cur==="guide"?" cur":""}" data-route="guide">使用说明</button><ul>${li(BOOK)}</ul>`;
  $("#mytoc").innerHTML=`<button class="ti l0" data-route="mytags"><b>我的标签</b><span class="n">${myCount()}</span></button><button class="ti l0" data-route="plan"><b>旅行计划</b><span class="n">${planDates().length?planDates().length+" 天":""}</span></button><button class="ti l0" data-route="autoplan"><b>✨ 自动生成行程</b><span class="n"></span></button>`;
  $("#termtoc").innerHTML=`<button class="ti l0" data-route="terms"><b>词典总目</b><span class="n">${Object.keys(TERMS_).length}</span></button>`+TCATS.map(c=>`<button class="ti l1" data-tcat="${esc(c)}"><b>${esc(c)}</b><span class="n">${Object.values(TERMS_).filter(t=>t.k===c).length}</span></button>`).join("");
  const G=[["时令","sakura momiji snow matsuri newyear"],["历史文化","history"],["寺社与建筑","temple shrine zen castle garden museum"],["自然风景","nature view hike lake beach onsen"],["适合人群","elderly couple family"],["吃喝玩乐","hot food tea street night shopping deer"],["实用信息","free allday"]];
  const used=new Set(G.flatMap(g=>g[1].split(" ").flatMap(DESC)));const rest=Object.keys(TAGS).filter(k=>!used.has(k)&&TAGCOUNT[k]&&!TAG_PARENT[k]);if(rest.length)G.push(["其他",rest.join(" ")]);
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
function syncTab(){const tp=$("#tbPrev"),tn=$("#tbNext");if(!tp)return;tp.disabled=!HIST.some(r=>r!==cur);tn.disabled=$("#nextBtn").disabled;
  $("#tbPlan").classList.toggle("on",cur==="plan"||cur==="mytags");try{const c=myCount();$("#tbCnt").textContent=c?String(c):""}catch(e){}}
if(!wide())$("#q").placeholder="搜索景点、标签";
$("#tbPrev").onclick=()=>{while(HIST.length&&HIST[HIST.length-1]===cur)HIST.pop();if(!HIST.length)return;BACKNAV=true;go(HIST.pop(),-1);syncTab()};$("#tbNext").onclick=()=>$("#nextBtn").click();
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