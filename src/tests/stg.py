import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html#n-tmb"); await pg.wait_for_timeout(1500)
        await pg.click('.stgrow[data-mk="tmb"][data-s="4"]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path="/home/claude/swiss/tests/stg-tmb.png")
        print(await pg.evaluate('document.querySelectorAll(".stg.on,.pstg.on,.stgrow.on").length'))
        await pg.goto("file:///home/claude/swiss/site/index.html#n-viaalpina"); await pg.wait_for_timeout(1500)
        await pg.evaluate('document.querySelector("details.multi").open=true')
        await pg.click('.stgrow[data-mk="viaalpina"][data-s="5"]'); await pg.wait_for_timeout(800)
        el=await pg.query_selector('.mmap[data-mk="viaalpina"]'); await el.screenshot(path="/home/claude/swiss/tests/stg-va.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
