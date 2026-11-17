import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for h in ["n-viaalpina","n-viaalpina-s12","n-tmb","n-hauteroute-s5","n-kandersteg"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1300)
            await pg.screenshot(path=f"tests/rt-{h}.png")
        await pg.goto(U+"#n-viaalpina"); await pg.wait_for_timeout(1000)
        await pg.click('.zw svg.map g.mk >> nth=3'); await pg.wait_for_timeout(800)
        h1=await pg.evaluate("location.hash"); t=await pg.get_attribute("#backBtn","title")
        await pg.click("#backBtn"); await pg.wait_for_timeout(800)
        print(h1,t,await pg.evaluate("location.hash"))
        print(errs or "ok"); await b.close()
asyncio.run(main())
