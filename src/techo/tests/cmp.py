"""比较两份逐页快照。python3 cmp.py 旧.json 新.json"""
import json, re, sys, difflib
def norm(s):
    if s is None: return s
    s = re.sub(r'<div class="zc">.*?</div>', '', s)
    s = re.sub(r'<div class="zw">', '', s)
    s = re.sub(r' (bmon|zoomed)(?=[" ])', '', s)
    s = re.sub(r'<g class="tiles"[^>]*>.*?</g>', '', s)
    s = re.sub(r'v[a-z0-9]{8}', 'VID', s)
    s = re.sub(r'<text class="bmattr"[^>]*>[^<]*</text>', '', s)
    return s
def n(v): return [norm(x) for x in v] if isinstance(v, list) else norm(v)
A, B = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
bad = [k for k in A if n(A[k]) != n(B.get(k))]
extra = [k for k in B if k not in A]
print(f"{len(A)} 页，不同 {len(bad)}，新增 {len(extra)}")
for k in bad[:int(sys.argv[3]) if len(sys.argv) > 3 else 8]:
    x, y = n(A[k]), n(B.get(k))
    if isinstance(x, list):
        for i, (p, q) in enumerate(zip(x, y or [None] * len(x))):
            if p != q:
                p, q = p or "", q or ""
                sm = difflib.SequenceMatcher(None, p, q, autojunk=False)
                o = next(o for o in sm.get_opcodes() if o[0] != "equal")
                print(f"  {k}[{i}] {o[0]}: …{p[max(0,o[1]-60):o[2]+30][:220]!r}\n      → …{q[max(0,o[3]-60):o[4]+30][:220]!r}")
                break
    else: print(" ", k, str(x)[:200], "→", str(y)[:200])
