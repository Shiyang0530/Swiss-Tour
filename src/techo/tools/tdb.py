"""techo 通用资料库：读写与编号工具"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db")
BOOKS = os.path.join(ROOT, "books")
TYPE_DIGIT = {"spot": "1", "subspot": "1", "line": "2", "region": "3", "area": "3",
              "dict": "4", "decor": "4", "food": "5", "event": "6", "chapter": "7"}
# 号段：大区 3000101–3000999，其余面 3001001 起；装饰图标 4000101–4000999（预留），词典 4001001 起
START = {"spot": 1000001, "line": 2000001, "region": 3000101, "area": 3001001, "decor": 4000101,
         "dict": 4001001, "food": 5000001, "event": 6000001, "chapter": 7000001}
POOL = {"subspot": "spot"}

def jload(p, default=None):
    if not os.path.exists(p): return default
    with open(p, encoding="utf-8") as f: return json.load(f)

def jdump(p, obj, compact=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        if compact: json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        else: json.dump(obj, f, ensure_ascii=False, indent=1)

class Ids:
    """7 位编号：唯一、永不更改、永不复用。ids.json 记录 书:类别:旧键 → 编号，以及已用过的最大号。"""
    def __init__(self):
        self.p = os.path.join(DB, "ids.json")
        d = jload(self.p, {"map": {}, "next": {}})
        self.map, self.next = d["map"], d["next"]
    def get(self, book, ns, key, typ, want=None):
        k = f"{book}:{ns}:{key}"
        if k in self.map: return self.map[k]
        pool = POOL.get(typ, typ)
        used = set(self.map.values())
        if want and want not in used:
            i = want
        else:
            n = self.next.get(pool, START[pool])
            while str(n) in used: n += 1
            i = str(n); self.next[pool] = n + 1
        self.map[k] = i
        return i
    def rev(self, book):
        out = {}
        for k, v in self.map.items():
            b, ns, key = k.split(":", 2)
            if b == book: out[v] = (ns, key)
        return out
    def save(self): jdump(self.p, {"map": self.map, "next": self.next})

def js_consts(text):
    """读取 build 输出的 data.js：每行 const X=<json>;"""
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*const ([A-Z_][A-Z_0-9]*)=(.*);\s*$", line)
        if not m: continue
        try: out[m.group(1)] = json.loads(m.group(2))
        except Exception: pass
    return out
