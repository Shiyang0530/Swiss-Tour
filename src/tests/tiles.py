import asyncio, sys, io, math, re
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright
# fake tile: grey grid, plus red cross at each target lat/lon
T=[(46.9480,7.4474),(46.5967,7.9076),(47.0517,8.3077)]  # Zytglogge, Muerren approx, Kapellbruecke
def tile(z,x,y):
    im=Image.new("RGB",(256,256),(235,235,225)); d=ImageDraw.Draw(im); d.rectangle([0,0,255,255],outline=(150,150,150))
    for la,lo in T:
        n=2**z; px=((lo+180)/360*n-x)*256; t=math.radians(la); py=((1-math.log(math.tan(t)+1/math.cos(t))/math.pi)/2*n-y)*256
        if -20<px<276 and -20<py<276: d.line([px-15,py,px+15,py],fill=(255,0,0),width=3); d.line([px,py-15,px,py+15],fill=(255,0,0),width=3)
    b=io.BytesIO(); im.save(b,"PNG"); return b.getvalue()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":900})
        errs=[]; reqs=[]
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        async def h(route):
            m=re.search(r"/(\d+)/(\d+)/(\d+)\.(jpeg|png)$",route.request.url); reqs.append(route.request.url)
            await route.fulfill(status=200,content_type="image/png",body=tile(*map(int,m.groups()[:3])))
        await pg.route(re.compile(r"https://(wmts\.geo\.admin\.ch|tile\.openstreetmap\.org)/.*"),h)
        await pg.goto("file:///home/claude/swiss/site/index.html"); await pg.wait_for_timeout(800)
        for r in sys.argv[1].split(","):
            await pg.evaluate(f"location.hash='{r}'"); await pg.wait_for_timeout(1500)
            el=await pg.query_selector("svg.map:not(.cover-img svg)")
            await pg.screenshot(path=f"tl-{r}.png")
        print(len(reqs), reqs[:2]); print("\n".join(errs) or "no errors")
        await b.close()
if __name__=="__main__": asyncio.run(main())
