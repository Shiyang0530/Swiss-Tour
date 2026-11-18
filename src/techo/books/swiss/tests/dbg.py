import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":1400,"height":900})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html#tag-hike");await pg.wait_for_timeout(1500)
        print(await pg.evaluate("location.hash"), await pg.evaluate("(document.querySelector('.fsub')||{}).outerHTML||'none'"))
        print(errs)
        await b.close()
asyncio.run(main())
