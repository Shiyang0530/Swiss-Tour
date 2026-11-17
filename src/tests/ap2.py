import asyncio,json
from playwright.async_api import async_playwright
CASES=[
 ("auto 7d Jul zrh", dict(start="2027-07-05",end="2027-07-11",arrP="zrh",depP="zrh",regions={},hike=False,ski=False)),
 ("auto 7d Jul zrh hike", dict(start="2027-07-05",end="2027-07-11",arrP="zrh",depP="zrh",regions={},hike=True,ski=False)),
 ("manual zermatt2 jungfrau2 luzern1", dict(start="2027-07-05",end="2027-07-10",arrP="zrh",depP="zrh",regions={"zermatt":2,"jungfrauregion":2,"luzern":1},hike=False)),
 ("Jan hike+ski", dict(start="2027-01-10",end="2027-01-14",arrP="zrh",depP="zrh",regions={},hike=True,ski=True)),
 ("scenic zermatt->graub", dict(start="2027-07-05",end="2027-07-10",arrP="zrh",depP="zrh",regions={"zermatt":2,"graubuenden":2},hike=False)),
]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page(viewport={"width":1400,"height":900})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html");await pg.wait_for_timeout(500)
        for name,o in CASES:
            base=dict(base='auto',pace='mid',mode='public',tags=[],must=[],few=True,scenic=True,hikeDur=['d4h','d1'],arrT='',depT='');base.update(o)
            await pg.evaluate("o=>localStorage.setItem('swiss-autoplan',JSON.stringify(o))",base)
            await pg.goto("file:///home/claude/swiss/site/index.html#autoplan");await pg.reload();await pg.wait_for_timeout(900)
            await pg.click("[data-apgo]");await pg.wait_for_timeout(900)
            t=await pg.evaluate("document.getElementById('R').innerText")
            print("=====",name);print(t[:1800])
        await pg.screenshot(path="ap2.png")
        print(errs);await b.close()
asyncio.run(main())
