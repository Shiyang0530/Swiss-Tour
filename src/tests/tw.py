import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for h in ["tag-town","n-baselaltstadt","n-berncity","n-kapellbruecke"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1200); await pg.screenshot(path=f"tests/tw-{h}.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
