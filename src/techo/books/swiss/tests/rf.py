import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        pg.on("requestfailed", lambda r: print("FAIL", r.url[:150]))
        for r in ["n-tmb","n-chamonix","n-root"]:
            await pg.goto("file:///home/claude/swiss/site/index.html#"+r); await pg.wait_for_timeout(1500)
        await b.close()
asyncio.run(main())
