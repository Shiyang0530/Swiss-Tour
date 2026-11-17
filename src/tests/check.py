import asyncio, sys, json
from playwright.async_api import async_playwright
routes = sys.argv[1].split(",") if len(sys.argv)>1 else ["guide","n-root","n-berner","n-grindelwald","n-bachalpsee","n-trains","n-food","n-fondue","tag-ski","autoplan","terms","term-cograil"]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]
        pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type in ("error","warning") else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        await pg.goto("file:///home/claude/swiss/site/index.html")
        await pg.wait_for_timeout(800)
        for r in routes:
            await pg.evaluate(f"location.hash='{r}'")
            await pg.wait_for_timeout(1300)
            await pg.screenshot(path=f"/home/claude/swiss/tests/{r}.png")
        print("\n".join(errs[:30]) or "no errors")
        await b.close()
asyncio.run(main())
