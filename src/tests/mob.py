import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True)
        await pg.goto("file:///home/claude/swiss/site/index.html#n-transport");await pg.wait_for_timeout(1300)
        el=await pg.query_selector(".ptab");await el.scroll_into_view_if_needed()
        print(await pg.evaluate("""(()=>{const t=document.querySelector('.ptab');const w=t.closest('.mtab');const cs=getComputedStyle(t);const b=t.querySelector('tbody td button');const bc=getComputedStyle(b);
          return {tw:t.offsetWidth,ww:w.offsetWidth,minw:cs.minWidth,tl:cs.tableLayout,btn:[b.offsetWidth,b.offsetHeight,bc.color,bc.display,bc.fontSize,bc.visibility,bc.opacity],mt:getComputedStyle(w).overflowX}})()"""))
        await pg.screenshot(path="mob-ptab.png");await b.close()
asyncio.run(main())
