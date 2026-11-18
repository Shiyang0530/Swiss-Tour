import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":375,"height":812},is_mobile=True,has_touch=True)
        for h,sel in [("n-transport",".ptab"),("n-tmb",".mtab table"),("n-tmb-s3",".crumbs")]:
            await pg.goto("file:///home/claude/swiss/site/index.html#"+h);await pg.wait_for_timeout(1200)
            el=await pg.query_selector(sel);await el.scroll_into_view_if_needed();await pg.wait_for_timeout(200)
            await pg.screenshot(path=f"mob2-{h}.png")
        print(await pg.evaluate("[...document.querySelectorAll('.fbar')].map(f=>getComputedStyle(f).overflowX+' '+f.scrollWidth+'/'+f.clientWidth)"))
        await b.close()
asyncio.run(main())
