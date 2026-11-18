import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);pg=await b.new_page()
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("http://localhost:8765/index.html")
        for i in range(12):
            await pg.wait_for_timeout(2500)
            print(i, await pg.evaluate("(()=>{const t=document.getElementById('offst');return t?(t.hidden?'hidden':'')+' '+t.textContent:'none'})()"))
        print(errs);await b.close()
asyncio.run(main())
