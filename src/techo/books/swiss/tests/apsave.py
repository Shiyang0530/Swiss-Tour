import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html#autoplan"); await pg.wait_for_timeout(800)
        await pg.fill("#ap-start","2027-07-10"); await pg.fill("#ap-end","2027-07-13")
        await pg.click("[data-apgo]"); await pg.wait_for_timeout(800)
        await pg.click("[data-apre]"); await pg.wait_for_timeout(500); await pg.goto("file:///home/claude/swiss/site/index.html#plan"); await pg.wait_for_timeout(800)
        print(await pg.evaluate("location.hash"))
        print((await pg.inner_text("#R"))[:600])
        print(await pg.evaluate("JSON.stringify(Object.keys(localStorage).map(k=>[k,localStorage[k].slice(0,300)]))"))
        print(errs or "ok"); await b.close()
asyncio.run(main())
