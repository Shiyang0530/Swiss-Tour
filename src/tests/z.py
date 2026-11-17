import asyncio
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(U+"#n-oeschinensee"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path="tests/z-oesch.png")
        print("hike tagged", await pg.evaluate('(()=>{const A=[];(function w(n){A.push(n);(n.c||[]).forEach(w)})(BOOK);return A.filter(n=>(n.t||[]).includes("hike")).length})()'),
              "ballenberg", await pg.evaluate('JSON.stringify((()=>{const A=[];(function w(n){A.push(n);(n.c||[]).forEach(w)})(BOOK);return A.filter(n=>/Ballenberg|巴伦贝格/i.test(JSON.stringify([n.n,n.ja]))).map(n=>[n.id,n.n,n.t])})())'))
        print("tag label", await pg.evaluate('TAGS.hike'))
        await pg.goto(U+"#n-root"); await pg.wait_for_timeout(1500)
        print("zw", await pg.evaluate('document.querySelectorAll(".zw").length'))
        await pg.click('.zc button[data-z="in"]'); await pg.click('.zc button[data-z="in"]'); await pg.wait_for_timeout(200)
        box=await (await pg.query_selector(".zw svg.map")).bounding_box()
        await pg.mouse.move(box["x"]+300,box["y"]+200); await pg.mouse.down(); await pg.mouse.move(box["x"]+150,box["y"]+120,steps=8); await pg.mouse.up()
        print("vb", await pg.evaluate('document.querySelector(".zw svg.map").getAttribute("viewBox")'), "hash", await pg.evaluate("location.hash"))
        await pg.screenshot(path="tests/z-root.png")
        await pg.goto(U+"#n-berner"); await pg.wait_for_timeout(1500)
        await pg.evaluate('document.querySelectorAll("details.multi").forEach(d=>d.open=true)')
        await pg.click('.stgrow[data-mk="viaalpina"][data-s="12"]'); await pg.wait_for_timeout(800)
        el=await pg.query_selector('.mmap[data-mk="viaalpina"]'); await el.screenshot(path="tests/z-va.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
async def va():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        await pg.goto(U+"#n-berner"); await pg.wait_for_timeout(1500)
        await pg.evaluate('document.querySelectorAll("details.multi").forEach(d=>d.open=true)')
        el=await pg.query_selector('.mmap[data-mk="viaalpina"] svg.map'); await el.scroll_into_view_if_needed()
        bx=await el.bounding_box()
        for _ in range(2): await pg.mouse.dblclick(bx["x"]+bx["width"]*0.45,bx["y"]+bx["height"]*0.55)
        await pg.wait_for_timeout(300)
        await (await pg.query_selector('.mmap[data-mk="viaalpina"]')).screenshot(path="tests/z-va2.png")
        await b.close()
asyncio.run(va())
