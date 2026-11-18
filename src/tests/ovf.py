import asyncio,sys
from playwright.async_api import async_playwright
JS="""()=>{const W=innerWidth,out=[];const R=document.getElementById('R')||document.body;
 document.querySelectorAll('body *').forEach(e=>{if(!e.offsetParent&&getComputedStyle(e).position!=='fixed')return;const cs=getComputedStyle(e);
  if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&e.scrollWidth>e.clientWidth+4&&e.clientWidth>0&&!e.closest('.zw')&&!e.matches('.fbar,.fbar *'))out.push('SCROLL '+e.tagName+'.'+e.className+' '+e.scrollWidth+'>'+e.clientWidth);
 });
 if(document.documentElement.scrollWidth>W+1)out.push('PAGE '+document.documentElement.scrollWidth);
 document.querySelectorAll('#L *, #R *, .page *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+2&&!e.closest('[style*=overflow],.mtab,.zw,.fbar,svg')){const cs=getComputedStyle(e);out.push('WIDE '+e.tagName+'.'+String(e.className).slice(0,30)+' '+Math.round(r.right))}});
 return [...new Set(out)].slice(0,6)}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
        await pg.goto("file:///home/claude/swiss/site/index.html");await pg.wait_for_timeout(800)
        routes=await pg.evaluate("['cover','toc','terms','autoplan','plan','tags','guide'].concat(ORDER_IDS())") if False else None
        routes=await pg.evaluate("""(()=>{const r=['','terms','autoplan','plan'];document.querySelectorAll('[data-go]').forEach(e=>{});return r})()""")
        ids=await pg.evaluate("""(()=>{try{return Object.keys(NODES)}catch(e){return null}})()""")
        hs_t=[]
        if True:
            import json,re
            s=open('/home/claude/swiss/out/data.js').read();i=s.find('const BOOK=');j=s.find(chr(10),i);B=json.loads(s[i+11:j].rstrip(';'))
            ids=[]
            def w(n): ids.append(n['id']);[w(c) for c in n.get('c',[])]
            w(B)
            T=re.findall(r'"([a-z0-9]+)":\{"n"',s[s.find('const TERMS'):s.find(chr(10),s.find('const TERMS'))]); hs_t=['term-'+t for t in T]
        hs=hs_t+["n-"+i for i in ids]+["terms","autoplan","plan","tag-hike","tag-train","tag-transport","tag-ski","guide"]
        bad=0
        for h in hs:
            await pg.evaluate(f"location.hash='{h}'");await pg.wait_for_timeout(250)
            r=await pg.evaluate(JS)
            if r: bad+=1;print(h,r)
        print("checked",len(hs),"bad",bad);await b.close()
asyncio.run(main())
