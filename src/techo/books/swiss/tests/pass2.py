import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":1400,"height":900})
        await pg.goto("file:///home/claude/swiss/site/index.html#n-transport");await pg.wait_for_timeout(1200)
        el=await pg.query_selector(".ptab");await el.scroll_into_view_if_needed();await pg.wait_for_timeout(300)
        await pg.screenshot(path="pass-tab.png");await b.close()
asyncio.run(main())
