import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for h in ["term-marmot","n-oeschinensee","n-chamonix","n-root","n-wild","tag-hike"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f"tests/w-{h}.png")
        await pg.goto(U+"#n-root"); await pg.wait_for_timeout(800)
        await pg.evaluate('document.querySelector("#L [data-filter=hike]").click()'); await pg.wait_for_timeout(600)
        el=await pg.query_selector("#L"); await el.screenshot(path="tests/w-root-hike.png")
        print(await pg.evaluate('[...document.querySelectorAll("#L g.mk text.num")].map(t=>t.textContent).join(",")'))
        print(errs or "ok"); await b.close()
asyncio.run(main())
