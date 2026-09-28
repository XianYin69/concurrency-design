"""process_chain.py — 过程链存取：save/load/interrupt/resume，状态落用户缓存目录（不入 skill 目录）。"""
import json, os, sys, time
def home():
    b = os.environ.get("SMS_HOME")
    b = b or os.path.join(os.path.expanduser("~"), "AppData", "Local", "SMS")
    d = os.path.join(b, "cache", "concurrency-design")
    os.makedirs(d, exist_ok=True)
    return d
def fpath():
    return os.path.join(home(), "process_chain.json")
def load_doc():
    if os.path.exists(fpath()):
        return json.load(open(fpath(), encoding="utf-8"))
    return {"steps": [], "interrupts": []}
def dump(d):
    json.dump(d, open(fpath(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def parse(raw):
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}
def save(step, data):
    d = load_doc()
    d["steps"].append({"step": step, "data": parse(data), "ts": time.strftime("%F %T")})
    dump(d); print("[过程链] 存档", step)
def interrupt(step, reason):
    d = load_doc()
    d["interrupts"].append({"step": step, "reason": reason, "ts": time.strftime("%F %T")})
    dump(d); print("[过程链] 中断", step, "|", reason)
def resume(step):
    d = load_doc()
    d["interrupts"] = [i for i in d["interrupts"] if i["step"] != step]
    dump(d); print("[过程链] 恢复", step, "| 剩余未解 =", len(d["interrupts"]))
a = sys.argv[1:]
g = lambda k, d="": a[a.index(k) + 1] if k in a else d
if not a:
    print("用法: save --step S --data JSON | load | interrupt --step S --reason R | resume --step S")
elif a[0] == "save":
    save(g("--step"), g("--data", "{}"))
elif a[0] == "load":
    print(json.dumps(load_doc(), ensure_ascii=False, indent=1))
elif a[0] == "interrupt":
    interrupt(g("--step"), g("--reason"))
elif a[0] == "resume":
    resume(g("--step"))
else:
    print("未知子命令", a[0])
