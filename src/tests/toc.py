import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":1400,"height":900})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html");await pg.wait_for_timeout(800)
        await pg.click("#tocBtn") if await pg.query_selector("#tocBtn") else None
        await pg.wait_for_timeout(800)
        txt=await pg.evaluate("document.body.innerText")
        print("4 小时内" in txt, "交通" in txt, errs)
        await pg.screenshot(path="toc.png");await b.close()
asyncio.run(main())
