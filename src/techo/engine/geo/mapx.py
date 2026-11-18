"""Extra map layers (railways, peaks, towns, scale bar) and topic maps (hiking routes, ski areas)."""
import json, math, sys
import os as _os
_SRC = _os.environ.get("TECHO_BOOK_SRC", "/home/claude/techo/books/swiss/src")
_GEO = _os.environ.get("TECHO_GEO", "/home/claude/geo")
sys.path.insert(0, _SRC + "/content")
from shapely.geometry import shape, LineString, MultiPoint, Point
from geo_extra import PEAKS, TOWNS, TOWN_ELEV, PASSES

W, H = 600, 440
RAILS = [shape(f["geometry"]) for f in json.load(open(_GEO + "/ne_10m_railroads_ch.geojson"))["features"]]
HIKE_C = "#3f7a34"; SKI_C = "#2f6db5"

def tw(s, size=12):
    return sum(size if ord(c) > 0x2E80 else size * 0.56 for c in s)

class Placer:
    def __init__(self): self.r = [(W - 150, H - 34, W, H)]
    def ok(self, b, margin=2):
        x0, y0, x1, y1 = b
        if x0 < 4 or y0 < 4 or x1 > W - 4 or y1 > H - 22: return False
        for a in self.r:
            if not (x1 + margin < a[0] or a[2] + margin < x0 or y1 + margin < a[1] or a[3] + margin < y0): return False
        return True
    def add(self, b): self.r.append(b)
    def place(self, x, y, w, h, gap=7, prefer=None):
        """Try positions around (x,y). Returns (tx, ty, anchor) for text baseline or None."""
        cands = [("r", x + gap, y - h / 2), ("l", x - gap - w, y - h / 2), ("t", x - w / 2, y - gap - h), ("b", x - w / 2, y + gap),
                 ("tr", x + gap - 2, y - gap - h + 2), ("br", x + gap - 2, y + gap - 2), ("tl", x - gap - w + 2, y - gap - h + 2), ("bl", x - gap - w + 2, y + gap - 2)]
        if prefer: cands.sort(key=lambda c: c[0] != prefer)
        for k, bx, by in cands:
            b = (bx, by, bx + w, by + h)
            if self.ok(b):
                self.add(b); return bx, by
        return None

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def rank_limit(k):
    return 1 if k < 220 else 2 if k < 900 else 3

def scalebar(P):
    pxkm = P.k / 111.32
    for L in (0.2, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200):
        if 45 <= L * pxkm <= 130: break
    w = L * pxkm; x1 = W - 18; x0 = x1 - w; y = H - 14
    lab = (f"{L:g} km")
    return (f'<g class="sbar"><path d="M{x0:.1f} {y-4}V{y}H{x1:.1f}V{y-4}" fill="none" style="stroke:var(--ink)" stroke-width="1.4"/>'
            f'<text x="{(x0+x1)/2:.1f}" y="{y-7}" text-anchor="middle">{lab}</text></g>')

def rail_svg(P, path_of):
    win = P.window(); out = []
    for g in RAILS:
        gi = g.intersection(win)
        if gi.is_empty: continue
        d = path_of(gi, P)
        out.append(d)
    if not out: return ""
    d = "".join(out)
    w, o, w2, da = (1.5, .32, .5, "3 3") if P.k < 220 else (2.2, .45, .8, "4 4") if P.k < 900 else (2.6, .55, 1.1, "4 4")
    return (f'<path d="{d}" fill="none" style="stroke:var(--ink-2)" stroke-width="{w}" opacity="{o}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" style="stroke:var(--land)" stroke-width="{w2}" stroke-dasharray="{da}" opacity=".9"/>')

PEAK_PATH = lambda x, y, s=6: f'M{x:.1f} {y-s:.1f}L{x+s*0.95:.1f} {y+s*0.7:.1f}H{x-s*0.95:.1f}Z'

def poi_layers(P, placer, avoid_pts=(), lim=None, skip_names=()):
    """Peaks and towns with collision-free labels. avoid_pts: [(x,y)] where a marker sits (skip duplicates)."""
    lim = lim or rank_limit(P.k)
    win = P.window(-14)
    s = []; keys = set()
    def near(x, y):
        return any((x - a) ** 2 + (y - b) ** 2 < 15 ** 2 for a, b in avoid_pts)
    seen = set()
    items = ([("pk",) + p for p in PEAKS if 0 < p[5] <= lim] + [("tn", t[0], t[1], TOWN_ELEV.get(t[0]), t[2], t[3], t[4]) for t in TOWNS if t[4] <= lim]
             + [("ps",) + p for p in PASSES if p[5] <= lim])
    items.sort(key=lambda it: (it[6], {"pk": 0, "tn": 1, "ps": 2}[it[0]]))
    for kind, zh, orig, elev, lat, lon, rank in items:
        if zh in seen or zh in skip_names: continue
        if not win.contains(Point(lon, lat)): continue
        x, y = P.xy(lat, lon)
        if near(x, y): continue
        w = tw(zh, 11.5) + (tw(f" {elev}", 10) if elev else 0)
        b = (x - 6, y - 6, x + 6, y + 6)
        if not placer.ok(b, 0): continue
        pos = placer.place(x, y, w, 13, gap=6 if kind == "tn" else 8)
        if pos is None:
            continue
        placer.add(b); seen.add(zh)
        tx, ty = pos
        if kind == "pk":
            s.append(f'<path class="pkm" d="{PEAK_PATH(x, y + 1)}"/><text class="pk" x="{tx:.1f}" y="{ty+10.5:.1f}">{esc(zh)}<tspan class="el"> {elev}</tspan></text>')
            keys.add("peak")
        elif kind == "ps":
            s.append(f'<path class="psm" d="M{x-5:.1f} {y-5:.1f}Q{x-1:.1f} {y:.1f} {x-5:.1f} {y+5:.1f}M{x+5:.1f} {y-5:.1f}Q{x+1:.1f} {y:.1f} {x+5:.1f} {y+5:.1f}"/><text class="tn" x="{tx:.1f}" y="{ty+10.5:.1f}">{esc(zh)}<tspan class="el"> {elev}</tspan></text>')
            keys.add("pass")
        else:
            el = f'<tspan class="el"> {elev}</tspan>' if elev else ""
            s.append(f'<circle class="tnm" cx="{x:.1f}" cy="{y:.1f}" r="3.4"/><text class="tn" x="{tx:.1f}" y="{ty+10.5:.1f}">{esc(zh)}{el}</text>')
            keys.add("town")
    return "".join(s), keys

def marker_boxes(placer, kids, lw):
    for c in kids:
        x, y = c["x"], c["y"]
        placer.add((x - 16, y - 16, x + 16, y + 16))
        w = lw[c["id"]]
        if x < 440: placer.add((x + 20, y - 10, x + 24 + w, y + 10))
        else: placer.add((x - 24 - w, y - 10, x - 20, y + 10))

def mk_kind(c):
    t = [x for x in c.get("t", []) if x not in ("hot", "alps", "arch", "town")]
    if c["id"] in SKI_NODES or (t and t[0] == "ski"): return "ski"
    if c["id"] in HIKE_NODES or (t and t[0] == "hike"): return "hike"
    if t and t[0] in ("cog", "funi", "cable", "train"): return "mtn"
    return ""

SKI_NODES = set(); HIKE_NODES = set()

# ---------------- topic maps ----------------
def haversine(a, b):
    R = 6371.0; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def circled(i):
    return str(i)

def context_pts(pts, n=2, km=14):
    """Nearest big peaks (rank<=2) within km of the route, so the map shows the landmark mountains."""
    best = []
    diag = max(haversine(a, b) for a in pts for b in pts) if len(pts) > 1 else 0
    km = min(km, max(3.0, diag * 0.9))
    for zh, orig, elev, lat, lon, rank in PEAKS:
        if not (0 < rank <= 2): continue
        d = min(haversine((lat, lon), p) for p in pts)
        if d <= km: best.append((d, (lat, lon)))
    best.sort()
    return [p for _, p in best[:n]]

def overlay(P, path_of, HIKE, SKI):
    """Trails and lifts drawn on regular area maps."""
    s = []; keys = []
    win = P.window()
    if P.k >= 300:
        for k, spec in HIKE.items():
            ln = LineString([(b, a) for a, b, *_ in spec[2]])
            if not ln.intersects(win): continue
            ski = len(spec) > 3 and spec[3] == "ski"
            col = SKI_C if ski else HIKE_C
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (P.xy(a, b) for a, b, *_ in spec[2]))
            wd = 2.4 if P.k >= 900 else 1.6
            s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd}" stroke-dasharray="5 3" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')
            kk = "trail_ski" if ski else "trail"
            if kk not in keys: keys.append(kk)
    if P.k >= 900:
        for k, (title, lifts, st) in SKI.items():
            for nm, l, typ in lifts:
                ln = LineString([(b, a) for a, b in l])
                if not ln.intersects(win): continue
                xy = [P.xy(a, b) for a, b in l]
                d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
                s.append(f'<path d="{d}" fill="none" style="stroke:var(--ink)" stroke-width="1.5" opacity=".7"/>')
                for x, y in (xy[0], xy[-1]):
                    s.append(f'<rect class="stn" x="{x-2.5:.1f}" y="{y-2.5:.1f}" width="5" height="5" style="fill:var(--page);stroke:var(--ink)" stroke-width="1.2" opacity=".85"/>')
                if "lift" not in keys: keys.append("lift")
    return "".join(s), keys

def edge_pointers(P, placer, pts, maxkm=22, n=2):
    """Arrows at the map edge pointing to big peaks just outside the frame."""
    win = P.window(-20)
    cands = []
    for zh, orig, elev, lat, lon, rank in PEAKS:
        if not (0 < rank <= 2) or win.contains(Point(lon, lat)): continue
        d = min(haversine((lat, lon), p) for p in pts)
        if d <= maxkm: cands.append((d, zh, elev, lat, lon))
    cands.sort(); out = []; used = set()
    cx, cy = W / 2, H / 2
    for d, zh, elev, lat, lon in cands:
        if zh in used or len(out) >= n: continue
        tx, ty = P.xy(lat, lon); dx, dy = tx - cx, ty - cy
        x0, x1, y0, y1 = 26, W - 26, 26, H - 40
        t = min([v for v in ((x1 - cx) / dx if dx > 0 else None, (x0 - cx) / dx if dx < 0 else None,
                             (y1 - cy) / dy if dy > 0 else None, (y0 - cy) / dy if dy < 0 else None) if v is not None])
        ex, ey = cx + dx * t, cy + dy * t
        ang = math.degrees(math.atan2(dy, dx))
        lab = f"{zh} {elev} · 约 {d:.0f} km"
        w = tw(zh, 11.5) + tw(f" {elev} · 约 {d:.0f} km", 10)
        pos = placer.place(ex, ey, w, 13, gap=12)
        if not pos: continue
        used.add(zh)
        out.append(f'<g class="edgep"><path d="M-7 -5L5 0L-7 5Z" transform="translate({ex:.1f} {ey:.1f}) rotate({ang:.0f})" fill="#7b6a55"/>'
                   f'<text class="pk" x="{pos[0]:.1f}" y="{pos[1]+10.5:.1f}">{esc(zh)}<tspan class="el"> {elev} · 约 {d:.0f} km</tspan></text></g>')
    return "".join(out)

def topic_hike(spec, Proj, bg_svg, path_of, ends=None, mk=None, labels=None):
    title, stats, pts = spec[0], spec[1], spec[2]
    kind = spec[3] if len(spec) > 3 else "hike"
    col = SKI_C if kind == "ski" else HIKE_C
    line = [(p[0], p[1]) for p in pts]
    stops = [p for p in pts if len(p) >= 6]
    P = Proj(line + context_pts(line), 0.018, pad=(95, 70))
    bg, _ = bg_svg(P, labels=False)
    s = [bg]
    xy = [P.xy(a, b) for a, b in line]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    s.append(f'<path d="{d}" fill="none" style="stroke:var(--page)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    # direction chevrons along the line
    tot = sum(math.dist(xy[i], xy[i + 1]) for i in range(len(xy) - 1))
    step = max(60, tot / 9); acc = step / 2
    for i in range(len(xy) - 1):
        (x0, y0), (x1, y1) = xy[i], xy[i + 1]; L = math.dist(xy[i], xy[i + 1])
        while acc < L:
            t = acc / L; cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
            s.append(f'<path d="M-3.5 -3.5L1.5 0L-3.5 3.5" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" transform="translate({cx:.1f} {cy:.1f}) rotate({ang:.0f})"/>')
            acc += step
        acc -= L
    placer = Placer()
    for x, y in xy: placer.add((x - 3, y - 3, x + 3, y + 3))
    loop = math.dist(P.xy(*stops[0][:2]), P.xy(*stops[-1][:2])) < 10
    marks = []; labs = []; lst = []
    num = 0
    for j, p in enumerate(stops):
        lat, lon, zh, orig, elev, role = p[:6]
        x, y = P.xy(lat, lon)
        if role == "e" and loop:
            continue
        num += 1
        if role in ("s", "e"):
            txt = "起" if role == "s" else "终"
            if role == "s" and loop: txt = "起"
            marks.append(f'<g class="tst"><circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{col}" stroke="#fff" stroke-width="2.5"/><text x="{x:.1f}" y="{y:.1f}">{txt}</text></g>')
            placer.add((x - 12, y - 12, x + 12, y + 12))
        else:
            marks.append(f'<g class="twp"><circle cx="{x:.1f}" cy="{y:.1f}" r="8.5" fill="#fff" stroke="{col}" stroke-width="2.4"/><text x="{x:.1f}" y="{y:.1f}" style="fill:{col}">{num}</text></g>')
            placer.add((x - 9, y - 9, x + 9, y + 9))
        lst.append([num, zh, orig, elev, role if not (role == "s" and loop) else "loop"])
    for j, p in enumerate(stops):
        lat, lon, zh, orig, elev, role = p[:6]
        if role == "e" and loop: continue
        x, y = P.xy(lat, lon)
        w = max(tw(zh, 13), tw(f"{elev} m", 10.5)); h = 28
        pos = placer.place(x, y, w, h, gap=16 if role in ("s", "e") else 12)
        if pos:
            tx, ty = pos
            labs.append(f'<text class="tsl" x="{tx:.1f}" y="{ty+12:.1f}">{esc(zh)}</text><text class="tse" x="{tx:.1f}" y="{ty+25:.1f}">{elev} m</text>')
    poi, keys = poi_layers(P, placer, avoid_pts=[P.xy(p[0], p[1]) for p in stops], lim=3, skip_names={p[2] for p in stops})
    s += [poi, edge_pointers(P, placer, line), "".join(marks), "".join(labs), scalebar(P)]
    lg = ["route_ski" if kind == "ski" else "route_hike", "start", "via"] + sorted(keys, key=["peak", "pass", "town"].index) + ["rail", "water"]
    prof = profile(stops, line, col)
    out = dict(k=kind, t=title, s=stats, svg="".join(s), list=lst, lg=lg, prof=prof)
    if ends:
        # stage segments: index ranges along the polyline
        cum = [0.0]
        for i in range(len(line) - 1): cum.append(cum[-1] + haversine(line[i], line[i + 1]))
        D = cum[-1] or 1
        names = [p[2] if len(p) >= 6 else None for p in pts]
        prev = 0; segs = []; bands = []
        for si, nm in enumerate(ends):
            if si == len(ends) - 1: j = len(line) - 1
            else:
                j = next(k for k in range(prev + 1, len(line)) if names[k] == nm)
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy[prev:j + 1])
            segs.append(f'<path class="stg" data-s="{si + 1}" d="{d}"/>')
            x0 = 40 + cum[prev] / D * 540; x1 = 40 + cum[j] / D * 540
            bands.append(f'<rect class="pstg" data-s="{si + 1}" x="{x0:.1f}" y="14" width="{max(2, x1 - x0):.1f}" height="72"/><text class="pstl" data-s="{si + 1}" x="{(x0 + x1) / 2:.1f}" y="24" text-anchor="middle">第 {labels[si] if labels else si + 1} 段</text>')
            prev = j
        # insert stage overlay before the markers so stop circles stay on top
        out["svg"] = out["svg"].replace('<g class="tst">', '<g class="stgs">' + "".join(segs) + '</g><g class="tst">', 1)
        out["prof"] = prof.replace('<path d="M', "".join(bands) + '<path d="M', 1) if prof else prof
        out["mk"] = mk
    return out

def profile(stops, line, col):
    # cumulative distance of each stop along the polyline
    cum = [0.0]
    for i in range(len(line) - 1): cum.append(cum[-1] + haversine(line[i], line[i + 1]))
    idx = {}
    k = 0
    for i, p in enumerate(line):
        pass
    # map stops to positions on line (stops are a subsequence of line points)
    pos = []; li = 0
    full = [(p[0], p[1]) for p in line]
    for st in stops:
        while li < len(full) and (abs(full[li][0] - st[0]) > 1e-9 or abs(full[li][1] - st[1]) > 1e-9): li += 1
        if li >= len(full): break
        pos.append((cum[li], st[4], st)); li += 1
    if len(pos) < 2: return ""
    D = pos[-1][0] or 1; es = [e for _, e, _ in pos]; e0, e1 = min(es), max(es)
    if e1 - e0 < 60: e0 -= 60; e1 += 60
    pad = (e1 - e0) * 0.15; e0 -= pad; e1 += pad
    X = lambda d: 40 + d / D * 540; Y = lambda e: 86 - (e - e0) / (e1 - e0) * 70
    pts = [(X(d), Y(e)) for d, e, _ in pos]
    area = f"M{pts[0][0]:.1f} 86 " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in pts) + f" L{pts[-1][0]:.1f} 86Z"
    s = [f'<rect width="600" height="100" style="fill:var(--land)"/>',
         f'<path d="{area}" fill="{col}" opacity=".16"/>',
         f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>']
    for (x, y), (_, e, st) in zip(pts, pos):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#fff" stroke="{col}" stroke-width="1.6"/>')
    s.append(f'<text class="pf" x="6" y="{Y(max(es))+4:.1f}">{max(es)}</text><text class="pf" x="6" y="{Y(min(es))+4:.1f}">{min(es)}</text>')
    s.append(f'<text class="pf" x="40" y="98">起点</text><text class="pf" x="580" y="98" text-anchor="end">终点</text>')
    s.append(f'<text class="pf" x="300" y="12" text-anchor="middle">海拔剖面（示意，按站点海拔连线）</text>')
    return "".join(s)

def topic_ski(spec, Proj, bg_svg, path_of):
    title, lifts, stations = spec
    allp = [p for _, l, _ in lifts for p in l] + [(s[0], s[1]) for s in stations]
    P = Proj(allp + context_pts(allp, 1), 0.02, pad=(90, 65))
    bg, _ = bg_svg(P, labels=False)
    s = [bg]
    hull = MultiPoint([(b, a) for a, b in allp]).convex_hull.buffer(0.006, join_style=1)
    s.append(f'<path d="{path_of(hull, P)}" fill="{SKI_C}" fill-opacity=".1" stroke="{SKI_C}" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="6 4"/>')
    placer = Placer(); lst = []; nums = []
    for i, (nm, l, typ) in enumerate(lifts):
        xy = [P.xy(a, b) for a, b in l]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
        if typ == "f":
            s.append(f'<path d="{d}" fill="none" style="stroke:var(--ink)" stroke-width="4" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="5 5"/>')
        elif typ == "c":
            s.append(f'<path d="{d}" fill="none" style="stroke:var(--ink)" stroke-width="2" stroke-dasharray="7 4"/>')
        else:
            s.append(f'<path d="{d}" fill="none" style="stroke:var(--ink)" stroke-width="2.2"/>')
        for x, y in xy:
            s.append(f'<rect class="stn" x="{x-3.2:.1f}" y="{y-3.2:.1f}" width="6.4" height="6.4" style="fill:var(--page);stroke:var(--ink)" stroke-width="1.6"/>')
            placer.add((x - 4, y - 4, x + 4, y + 4))
        for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
            for t in (0.25, 0.5, 0.75): placer.add(((x0 + (x1 - x0) * t) - 2, (y0 + (y1 - y0) * t) - 2, (x0 + (x1 - x0) * t) + 2, (y0 + (y1 - y0) * t) + 2))
        # number badge at the middle of the longest segment
        seg = max(range(len(xy) - 1), key=lambda j: math.dist(xy[j], xy[j + 1]))
        (x0, y0), (x1, y1) = xy[seg], xy[seg + 1]
        nums.append((i + 1, (x0 + x1) / 2, (y0 + y1) / 2))
        lst.append([i + 1, nm, {"g": "吊厢 / 空中缆车", "c": "吊椅", "f": "缆索铁路 / 登山铁路"}[typ]])
    nb = []
    for i, x, y in nums:
        nb.append(f'<g class="lfn"><circle cx="{x:.1f}" cy="{y:.1f}" r="8"/><text x="{x:.1f}" y="{y:.1f}">{i}</text></g>')
        placer.add((x - 9, y - 9, x + 9, y + 9))
    labs = []
    for lat, lon, zh, orig, elev in stations:
        x, y = P.xy(lat, lon)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{SKI_C}" stroke="#fff" stroke-width="1.8"/>')
        placer.add((x - 5, y - 5, x + 5, y + 5))
    for lat, lon, zh, orig, elev in stations:
        x, y = P.xy(lat, lon)
        w = max(tw(zh, 13), tw(f"{elev} m", 10.5))
        pos = placer.place(x, y, w, 28, gap=8)
        if pos:
            tx, ty = pos
            labs.append(f'<text class="tsl" x="{tx:.1f}" y="{ty+12:.1f}">{esc(zh)}</text><text class="tse" x="{tx:.1f}" y="{ty+25:.1f}">{elev} m</text>')
    poi, keys = poi_layers(P, placer, avoid_pts=[P.xy(a, b) for a, b, *_ in stations], lim=3, skip_names={x[2] for x in stations})
    s += nb + [poi, edge_pointers(P, placer, allp)] + labs + [scalebar(P)]
    els = [x[4] for x in stations]
    stats = f"海拔约 {min(els)}–{max(els)} m · 图中标出 {len(lifts)} 条主要缆车 / 登山铁路"
    st_list = [[zh, orig, elev] for _, _, zh, orig, elev in stations]
    lg = ["skiarea", "lift_g", "lift_c", "lift_f", "station"] + sorted(keys, key=["peak", "pass", "town"].index) + ["rail", "water"]
    used = {t for _, _, t in lifts}
    lg = [k for k in lg if not (k.startswith("lift_") and k[-1] not in used)]
    return dict(k="ski", t=title, s=stats, svg="".join(s), list=lst, st=st_list, lg=lg)
