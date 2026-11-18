import asyncio,re
from tiles import tile
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":1400,"height":900})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        async def h(r):
            m=re.search(r"/(\d+)/(\d+)/(\d+)\.(jpeg|png)$",r.request.url);await r.fulfill(status=200,content_type="image/png",body=tile(*map(int,m.groups()[:3])))
        await pg.route(re.compile(r"https://(wmts\.geo\.admin\.ch|tile\.openstreetmap\.org)/.*"),h)
        await pg.goto("file:///home/claude/swiss/site/index.html");await pg.wait_for_timeout(600)
        await pg.evaluate("location.hash='n-berncity'");await pg.wait_for_timeout(1200)
        q="(()=>{const s=document.querySelector('.zw svg.map');return [s.classList.contains('bmon'),[...s.querySelectorAll('g.tiles image')].map(i=>i.dataset.z).join(',').slice(0,40)]})()"
        print(await pg.evaluate(q))
        for _ in range(3): await pg.click(".zw .zc button[data-z=in]");await pg.wait_for_timeout(300)
        print(await pg.evaluate(q))
        await pg.click(".zw .zc .bmb");await pg.wait_for_timeout(400);print("osm",await pg.evaluate("document.querySelector('.zw g.tiles image').getAttribute('href')"))
        await pg.screenshot(path="tl-osm.png")
        await pg.click(".zw .zc .bmb");await pg.wait_for_timeout(400);print("off",await pg.evaluate(q))
        print(errs or "no errors");await b.close()
asyncio.run(main())
