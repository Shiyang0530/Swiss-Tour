import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for h in ["n-root","n-wallis","n-leman","n-berner","n-viaalpina","n-term-stp"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1200)
            el=await pg.query_selector("#L"); await el.screenshot(path=f"tests/il-{h}.png")
        await pg.goto(U+"#n-root"); await pg.wait_for_timeout(800)
        await pg.click('.zc button[data-z="in"]'); await pg.click('.zc button[data-z="in"]'); await pg.wait_for_timeout(300)
        el=await pg.query_selector("#L .zw"); await el.screenshot(path="tests/il-zoom.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
