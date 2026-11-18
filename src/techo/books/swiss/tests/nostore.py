import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":390,"height":844}, is_mobile=True)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script("""Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}});Object.defineProperty(window,'indexedDB',{get(){throw new Error('denied')}});""")
        await pg.goto("file:///home/claude/swiss/site/index.html#n-chillon"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path="nostore.png"); print(errs or "ok"); await b.close()
asyncio.run(main())
