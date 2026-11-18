// 从京都 index.html 抽出数据常量（BOOK/TAGS/TERMS/DEEP/PLANDATA/CARDIMG/IMGS/SRC/TAG_PARENT）
const fs=require("fs");const s=fs.readFileSync(process.argv[2],"utf8");
const scripts=[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const main=scripts.find(x=>x.includes("const BOOK="));
const i=main.indexOf("const TAGS="),j=main.indexOf("const NODES=");
const pre=main.slice(i,j);
// TAG_PARENT 在 NODES 之后，单独取一行
const tp=s.match(/TAG_PARENT=(\{[^;]*\});/);
const code=pre+"\n;module.exports={TAGS,BOOK,DEEP:typeof DEEP!=='undefined'?DEEP:{},TERMS:typeof TERMS!=='undefined'?TERMS:{},SRC:typeof SRC!=='undefined'?SRC:{},PLANDATA:typeof PLANDATA!=='undefined'?PLANDATA:{},CARDIMG:typeof CARDIMG!=='undefined'?CARDIMG:{},IMGS:typeof IMGS!=='undefined'?IMGS:{},DIAG_NUKI:typeof DIAG_NUKI!=='undefined'?DIAG_NUKI:'',TAG_PARENT:"+(tp?tp[1]:"{}")+"};";
fs.writeFileSync("/tmp/kx.js",code);
const D=require("/tmp/kx.js");
const out={};for(const k in D){try{out[k]=JSON.parse(JSON.stringify(D[k]))}catch(e){out[k]=null;console.error("skip",k,e.message)}}
fs.writeFileSync(process.argv[3],JSON.stringify(out));
console.log(Object.keys(out).map(k=>k+":"+(out[k]?JSON.stringify(out[k]).length:0)).join(" "));
