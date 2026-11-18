import asyncio
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);pg=await b.new_page()
    await pg.goto('file:///home/claude/swiss/site/index.html');await pg.wait_for_timeout(800);await pg.click('text=目录');await pg.wait_for_timeout(600)
    print(await pg.evaluate("document.getElementById('tagidx').textContent"));await b.close()
asyncio.run(m())
