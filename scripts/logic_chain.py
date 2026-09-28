"""logic_chain.py — 逻辑链：add 记决策（frm→to→why），debate 铺正反双链，verify 查断链。"""
import json, os, sys, time
def _p(a):
    return a[0] if a and not a[0].startswith("--") else "logic_chain.jsonl"
def add(path, frm, to, why):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": f"l{int(time.time()*1000)%100000}", "from": frm,
                            "to": to, "why": why, "ts": time.strftime("%F %T")},
                           ensure_ascii=False) + "\n")
    print("[逻辑链]", frm, "->", to)
def debate(pro, con):
    print("[正方]", pro); print("[反方]", con)
    print("[裁决] 需人工/上游确认：两条论据链已并列，取证据更实一侧并记入逻辑链。")
def verify(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")] if os.path.exists(path) else []
    miss = [r for r in rows if not (r.get("from") and r.get("to") and r.get("why"))]
    print("逻辑链条数 =", len(rows), "| 缺字段 =", len(miss))
    sys.exit(1 if miss else 0)
def flag(a, k):
    return a[a.index(k) + 1] if k in a else ""
a = sys.argv[1:]
if not a: print("用法: add <file> --from X --to Y --why Z | debate --pro P --con C | verify <file>")
elif a[0] == "add": add(_p(a[1:]), flag(a, "--from"), flag(a, "--to"), flag(a, "--why"))
elif a[0] == "debate": debate(flag(a, "--pro"), flag(a, "--con"))
elif a[0] == "verify": verify(_p(a[1:]))
else: print("未知子命令", a[0])
