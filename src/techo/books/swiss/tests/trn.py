import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":390,"height":844})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        for h in ["n-gotthardpanorama","n-glacierexpress","n-transport"]:
            await pg.goto("file:///home/claude/swiss/site/index.html#"+h);await pg.wait_for_timeout(1300)
            ms=await pg.query_selector_all("svg.map")
            print(h,len(ms),await pg.evaluate("[...document.querySelectorAll('svg.map')].map(s=>s.classList.contains('rtf')+':'+s.querySelectorAll('.rt.on').length)"))
            for i,m in enumerate(ms[:2]): await m.screenshot(path=f"trn-{h}-{i}.png")
        print(errs);await b.close()
asyncio.run(main())
