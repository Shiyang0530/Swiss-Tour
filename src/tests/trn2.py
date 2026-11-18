import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        for h,sel in [("n-berninaexpress",".tsights"),("n-luzerncity",".trhere"),("tag-train","#R")]:
            await pg.goto("file:///home/claude/swiss/site/index.html#"+h);await pg.wait_for_timeout(1200)
            el=await pg.query_selector(sel)
            if el: await el.scroll_into_view_if_needed()
            await pg.wait_for_timeout(200);await pg.screenshot(path=f"trn2-{h}.png")
        print(await pg.evaluate("document.getElementById('R').innerText.slice(0,400)"))
        print(errs);await b.close()
asyncio.run(main())
