import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":420,"height":900}, device_scale_factor=1.5, is_mobile=True, has_touch=True)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for r in sys.argv[1].split(","):
            await pg.goto("file:///home/claude/swiss/site/index.html#"+r); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f"/home/claude/swiss/tests/f-{r}.png", full_page=True)
        print(errs or "ok"); await b.close()
asyncio.run(main())
