import asyncio, json
from playwright.async_api import async_playwright
U="file:///home/claude/swiss/site/index.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(U+"#n-root"); await pg.wait_for_timeout(800)
        plan={"2027-07-01":["kapellbruecke","altstadt","rigibahn"],"2027-07-02":["jungfraubahn","sphinx","first","bachalpsee"],"2027-07-03":["oeschinensee","viaalpina-s13"],"2027-07-04":["matterhorn","gornergrat","sunnegga"]}
        for d,ids in plan.items():
            for i in ids:
                await pg.goto(U+"#n-"+i); await pg.wait_for_timeout(500)
                await pg.fill("#plan-date", d); await pg.click('[data-planadd="1"]'); await pg.wait_for_timeout(150)
        for h in ["n-root","n-berner","plan"]:
            await pg.goto(U+"#"+h); await pg.wait_for_timeout(1300)
            el=await pg.query_selector("#L"); await el.screenshot(path=f"tests/pm-{h}.png")
        print(errs or "ok"); await b.close()
asyncio.run(main())
