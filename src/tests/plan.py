import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
        await pg.goto("file:///home/claude/swiss/site/index.html#autoplan")
        await pg.wait_for_timeout(800)
        await pg.fill("#ap-start","2027-07-10"); await pg.fill("#ap-end","2027-07-17")
        await pg.fill("#ap-arrt","09:30"); await pg.fill("#ap-dept","18:00")
        await pg.click("[data-apgo]")
        await pg.wait_for_timeout(1000)
        txt = await pg.inner_text("#R")
        print(txt[:3000])
        await pg.screenshot(path="/home/claude/swiss/tests/plan.png", full_page=False)
        # winter test
        await pg.fill("#ap-start","2027-01-20"); await pg.fill("#ap-end","2027-01-24")
        await pg.click("[data-aptag='ski']")
        await pg.click("[data-apgo]")
        await pg.wait_for_timeout(1000)
        txt = await pg.inner_text("#R")
        print("=====WINTER\n"+txt[:2000])
        print("\n".join(errs) or "no errors")
        await b.close()
asyncio.run(main())
