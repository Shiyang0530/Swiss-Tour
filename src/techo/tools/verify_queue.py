"""滚动核实（规范第六部分）：每周挑核实日期最旧的一批条目，列出要核对的内容。

  python3 verify_queue.py [--n 20] [--book kyoto|swiss] [--json]
      列出待核实清单（从没核实过的优先，其次核实日期最旧的；一级必去优先），写到 reports/verify-年-周.md
  python3 verify_queue.py --mark 1000001 2000003 … [--date 2026-11-25]
      人工或 Claude 确认无误后，把这些条目的核实日期改成今天（或指定日期）
"""
import datetime, json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tdb import ROOT, DB, BOOKS, jload, jdump

KINDS = ("spot", "subspot", "line", "area", "event", "food")
LBL = {"h": "开放 / 运营时间", "p": "门票", "a": "交通", "s": "通票", "e": "海拔", "l": "路线"}

def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def queue(E, n, book=None):
    cand = []
    for i, e in E.items():
        if e["type"] not in KINDS or (book and book not in e["books"]): continue
        p = e.get("practical") or {}
        if not (p.get("url") or p.get("info") or e.get("season")): continue
        cand.append((e.get("verified") or "0000-00-00", e.get("tier", 2), i))
    cand.sort()
    return [i for _, _, i in cand[:n]]

def item(i, e):
    p = e.get("practical") or {}
    b = next(iter(e["books"]))
    q = e["name"].get("local") or e["name"].get("zh")
    lines = [f"### {i} {e['name'].get('zh')}（{e['name'].get('local', '')}）",
             f"- 书：{', '.join(e['books'])} · 级别 {e.get('tier')} · 上次核实：{e.get('verified') or '从未'}"]
    if p.get("url"): lines.append(f"- 官网：{p['url']}")
    lines.append(f"- 搜索：https://www.google.com/search?q={urllib.parse.quote(q + ' 営業時間 料金' if b == 'kyoto' else q + ' Öffnungszeiten Preise')}")
    for k, v in (p.get("info") or {}).items():
        lines.append(f"- {LBL.get(k, k)}：{v}")
    if p.get("pass"): lines.append(f"- 通票 / 半价卡：{p['pass']}")
    if e.get("season"): lines.append(f"- 时令：{json.dumps(e['season'], ensure_ascii=False)}")
    lines.append("- 要核对：开放时间、票价、是否停运或改名、官网链接是否还有效")
    return "\n".join(lines)

def main():
    E = jload(os.path.join(DB, "entries.json"))
    if "--mark" in sys.argv:
        day = arg("--date", datetime.date.today().isoformat())
        ids = [x for x in sys.argv[sys.argv.index("--mark") + 1:] if not x.startswith("--") and x != day]
        for i in ids:
            if i not in E: print("没有这个编号：", i); continue
            E[i]["verified"] = day
        jdump(os.path.join(DB, "entries.json"), E)
        print(f"已把 {len(ids)} 个条目的核实日期设为 {day}")
        return
    n = int(arg("--n", 20)); book = arg("--book")
    Q = queue(E, n, book)
    if "--json" in sys.argv:
        print(json.dumps([dict(id=i, name=E[i]["name"], url=(E[i].get("practical") or {}).get("url"), info=(E[i].get("practical") or {}).get("info"), verified=E[i].get("verified")) for i in Q], ensure_ascii=False, indent=1))
        return
    y, w, _ = datetime.date.today().isocalendar()
    out = os.path.join(ROOT, "reports", f"verify-{y}-W{w:02d}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    never = sum(1 for e in E.values() if e["type"] in KINDS and not e.get("verified"))
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# 本周核实清单（{y} 年第 {w} 周）\n\n共 {len(Q)} 条；资料库里还有 {never} 条从未核实。确认无误后运行：\n\n"
                f"    python3 tools/verify_queue.py --mark {' '.join(Q)}\n\n只把「可能变了」的条目改资料库，改完再标记核实日期。\n\n")
        f.write("\n\n".join(item(i, E[i]) for i in Q) + "\n")
    print(f"待核实 {len(Q)} 条 → {out}")

if __name__ == "__main__":
    main()
