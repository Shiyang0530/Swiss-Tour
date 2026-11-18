/* ===== 自动生成行程 ===== */
const AP_BASES=CFG.ap.AP_BASES;
const AP_PACE={light:{n:"轻松",start:570,budget:330,max:3,night:0},mid:{n:"适中",start:540,budget:450,max:5,night:1},dense:{n:"密集",start:510,budget:570,max:7,night:1}};
const AP_TAG_G=CFG.ap.AP_TAG_G;
const AP_TAGS=AP_TAG_G.flatMap(g=>g[1].split(" "));const AP_SEASON=CFG.ap.AP_SEASON;
const AP_REG_TOP=CFG.ap.AP_REG_TOP;
const AP_REG_SUB=CFG.ap.AP_REG_SUB;
const AP_REGIONS={...AP_REG_TOP,...AP_REG_SUB};
const apRegion=id=>{let n=NODES[id];while(n){if(AP.regions[n.id])return n.id;n=n.parent}return ""};
let AP={start:"",end:"",base:"auto",pace:"mid",mode:"public",tags:[],must:[],regions:{}};
try{Object.assign(AP,JSON.parse(localStorage.getItem((CFG.id+"-autoplan"))||"{}"))}catch(e){}
if(!AP.regions||typeof AP.regions!=="object")AP.regions={};
const apSave=()=>{try{localStorage.setItem((CFG.id+"-autoplan"),JSON.stringify(AP))}catch(e){}};
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
    const ordered0=apOrder(list,B);const ordered=ordered0.slice();{let g=0;const NO=new Set(["pontocho","takasegawa","dotonbori",(CFG.id+"-station")]);if(ordered.length>1&&NO.has(ordered[0].id))ordered.reverse();while(ordered.length>1&&NO.has(ordered[0].id)&&g++<5)ordered.push(ordered.shift())}
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
const AP_PLACES=CFG.ap.AP_PLACES;
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
  const NO=new Set(["pontocho","takasegawa","dotonbori",(CFG.id+"-station")]);if(ordered.length>1&&NO.has(ordered[0].id))ordered.reverse();
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
