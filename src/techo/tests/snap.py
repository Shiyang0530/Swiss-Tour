"""逐页快照：打开电子书，把每一页（全部节点、词条、标签、使用说明、计划、自动行程）渲染后的 HTML 存下来，
用来比较“合并引擎前后”是否完全一致。  python3 snap.py <网址> <书编号> <输出.json>"""
import asyncio, json, sys
from playwright.async_api import async_playwright
URL, BOOK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
AP = {"kyoto": [{"start": "2027-04-01", "end": "2027-04-04", "base": "auto", "pace": "mid", "mode": "public", "tags": [], "must": [], "regions": {}},
                {"start": "2027-11-20", "end": "2027-11-26", "base": "auto", "pace": "dense", "mode": "public", "tags": ["temple"], "must": ["kinkakuji"], "regions": {}}],
      "swiss": [{"start": "2027-07-10", "end": "2027-07-16", "base": "auto", "pace": "mid", "mode": "public", "tags": [], "must": [], "regions": {}, "hike": True, "hikeDur": ["d4h", "d1"]},
                {"start": "2027-01-10", "end": "2027-01-14", "base": "auto", "pace": "mid", "mode": "public", "tags": [], "must": [], "regions": {}, "ski": True}]}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 1200, "height": 900})
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.route("**/*", lambda r: r.abort() if not r.request.url.startswith(URL.rsplit("/", 1)[0]) else r.continue_())
        await pg.goto(URL); await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(1200)
        routes = await pg.evaluate("""()=>{const o=[];(function w(n){o.push('n-'+n.id);(n.c||[]).forEach(w)})(BOOK);
          return [...o,...Object.keys(TERMS).map(k=>'term-'+k),...Object.keys(TAGS).map(k=>'tag-'+k),'terms','guide','plan','mytags','autoplan']}""")
        snap = {"_toc": await pg.evaluate("['tree','tagidx','termtoc','mytoc'].map(i=>{const e=document.getElementById(i);return e?e.innerHTML:null})")}
        get = "()=>[document.getElementById('L').innerHTML,document.getElementById('R').innerHTML,(document.getElementById('crumbs')||{}).innerHTML]"
        for r in routes:
            await pg.evaluate(f"location.hash={json.dumps('#'+r)}"); await pg.wait_for_timeout(25)
            snap[r] = await pg.evaluate(get)
        for i, o in enumerate(AP[BOOK]):
            await pg.evaluate(f"localStorage.setItem({json.dumps(BOOK+'-autoplan')},{json.dumps(json.dumps(o))});localStorage.removeItem({json.dumps(BOOK+'-plans')})")
            await pg.goto(URL + "#guide"); await pg.reload(); await pg.wait_for_timeout(800)
            await pg.evaluate("location.hash='#autoplan'"); await pg.wait_for_timeout(200)
            await pg.click("[data-apgo]"); await pg.wait_for_timeout(300)
            snap[f"_ap{i}"] = await pg.evaluate(get)
            snap[f"_ap{i}_ls"] = await pg.evaluate("JSON.stringify(Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage[k].replace(/\\d{13}/g,'T').replace(/\"v[a-z0-9]{8}\"/g,'ID')])))")
        snap["_errors"] = errs
        json.dump(snap, open(OUT, "w"), ensure_ascii=False)
        print(BOOK, len(snap), "pages, errors:", errs[:3])
        await b.close()
asyncio.run(main())
