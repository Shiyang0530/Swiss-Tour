import re
def _hours(s):
    if not s: return None
    best = None
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s*(?:[–\-至到]\s*(\d+(?:\.\d+)?)\s*)?(个)?\s*小时(?:\s*(\d+)\s*分钟)?', s):
        a = float(m.group(2) or m.group(1)) + (int(m.group(4)) / 60 if m.group(4) else 0)
        best = a if best is None else max(best, a)
    if best is None:
        m = re.search(r'(\d+)\s*分钟', s)
        if m: best = int(m.group(1)) / 60
    m = re.search(r'(\d+)\s*(?:[–\-至到]\s*(\d+)\s*)?天', s)
    if m: best = max(best or 0, 24 * int(m.group(2) or m.group(1)))
    return best
def dur_tag(n):
    """d4h / d1 / dmulti for a hike node"""
    if n.get("kd") == "多日路线" or n.get("multi") and n.get("kd") != "分段": return "dmulti"
    tm = n.get("tm")
    s1 = tm.get("s") if isinstance(tm, dict) else None
    l = (n.get("i") or {}).get("l")
    # first clause of the hike line is the main walk; topic stats are preferred
    h = _hours(s1)
    if h is None and l: h = _hours(re.split(r'[；;]', l)[0])
    if h is None: h = _hours(n.get("d", "")[:400])
    if h is None: return None
    return "d4h" if h <= 4 else ("d1" if h <= 14 else "dmulti")
