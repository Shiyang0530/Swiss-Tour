import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for h in ["n-leman","n-lausanne","n-chamonix","n-oeschinensee","term-edelweiss","n-grindelwald"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f"tests/ph-{h}.png", full_page=False)
        await pg.goto(U+"#n-oeschinensee"); await pg.wait_for_timeout(800)
        await pg.evaluate('document.querySelector("#L").scrollTop=99999; document.querySelector("#R").scrollTop=99999; window.scrollTo(0,99999)')
        await pg.wait_for_timeout(400); await pg.screenshot(path="tests/ph-oesch2.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
