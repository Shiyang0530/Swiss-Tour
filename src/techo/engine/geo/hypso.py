"""示意海拔分层：用书中已知海拔的点（山峰、城镇、湖面、山口、站点）插值，生成一张覆盖全区的半透明分层图。"""
import sys, json, numpy as np
import os as _os
_SRC = _os.environ.get("TECHO_BOOK_SRC", "/home/claude/techo/books/swiss/src")
_GEO = _os.environ.get("TECHO_GEO", "/home/claude/geo")
sys.path.insert(0, _SRC + "/content")
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from PIL import Image
from shapely.geometry import shape, box
from geo_extra import PEAKS, TOWNS, TOWN_ELEV, PASSES, HYPSO_EXTRA, LAKE_ELEV
from topo import HIKE, SKI

LON0, LON1, LAT0, LAT1 = 4.5, 11.8, 44.8, 48.5
RES = 360  # px per degree
BANDS = [(1000, (192, 172, 116, 110)), (2000, (150, 120, 78, 160)), (3000, (236, 238, 242, 235))]

def points():
    pts = []
    for zh, orig, e, lat, lon, r in PEAKS: pts.append((lat, lon, e))
    for zh, orig, lat, lon, r in TOWNS: pts.append((lat, lon, TOWN_ELEV[zh]))
    for zh, orig, e, lat, lon, r in PASSES: pts.append((lat, lon, e))
    for spec in HIKE.values():
        for p in spec[2]:
            if len(p) >= 6: pts.append((p[0], p[1], p[4]))
    for title, lifts, st in SKI.values():
        for s in st: pts.append((s[0], s[1], s[4]))
    pts += HYPSO_EXTRA
    # lake shores at lake level
    lakes = []
    names = {"Lake Geneva": "日内瓦湖", "Bodensee": "博登湖", "Lago di Como": "科莫湖", "Walensee": "瓦伦湖", "Zugersee": "楚格湖", "Bielersee": "比尔湖",
             "Zürichsee": "苏黎世湖", "Neuchâtel": "纳沙泰尔湖", "MURTENSEE": "穆尔滕湖", "Vierwaldstättersee": "琉森湖", "Lago di Lugano - Ceresio": "卢加诺湖",
             "Brienzersee": "布里恩茨湖", "Thunersee": "图恩湖", "Lac d' Annecy": "安纳西湖", None: "马焦雷湖"}
    REG = box(LON0, LAT0, LON1, LAT1)
    for f in ("ne_10m_lakes.geojson", "ne_10m_lakes_europe.geojson"):
        for ft in json.load(open(_GEO + "/" + f))["features"]:
            g = shape(ft["geometry"])
            if not g.intersects(REG): continue
            zh = names.get(ft["properties"].get("name"))
            if zh not in LAKE_ELEV: continue
            e = LAKE_ELEV[zh]; lakes.append((g, e))
            polys = g.geoms if g.geom_type == "MultiPolygon" else [g]
            for pg in polys:
                cs = list(pg.exterior.coords)
                for x, y in cs[::max(1, len(cs) // 40)]: pts.append((y, x, e))
    return pts, lakes

def build(out="/home/claude/techo/build/swiss/hypso.webp"):
    pts, lakes = points()
    P = np.array([(p[1], p[0]) for p in pts]); V = np.array([p[2] for p in pts], float)
    nx, ny = int((LON1 - LON0) * RES), int((LAT1 - LAT0) * RES)
    gx = LON0 + (np.arange(nx) + .5) / RES; gy = LAT1 - (np.arange(ny) + .5) / RES
    GX, GY = np.meshgrid(gx, gy)
    Z = griddata(P, V, (GX, GY), method="linear")
    Zn = griddata(P, V, (GX, GY), method="nearest")
    Z = np.where(np.isnan(Z), Zn, Z)
    Z = gaussian_filter(Z, 9)
    img = np.zeros((ny, nx, 4), np.uint8)
    for thr, col in BANDS:
        img[Z >= thr] = col
    Image.fromarray(img, "RGBA").save(out, "WEBP", lossless=True, quality=100, method=6)
    print("hypso", nx, ny, len(pts), "points", round(float(Z.max())), "max")
    return out

if __name__ == "__main__":
    build()
