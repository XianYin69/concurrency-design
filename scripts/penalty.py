"""penalty.py — 惩罚熔断：hit 计一次失败，达 10 次熔断要求回退或求助；reset 清零。"""
import json, os, sys, time
LIMIT = 10
def home():
    b = os.environ.get("SMS_HOME")
    b = b or os.path.join(os.path.expanduser("~"), "AppData", "Local", "SMS")
    d = os.path.join(b, "cache", "concurrency-design"); os.makedirs(d, exist_ok=True); return d
def fpath(): return os.path.join(home(), "penalty.json")
def load():
    return json.load(open(fpath(), encoding="utf-8")) if os.path.exists(fpath()) else {}
def main():
    a = sys.argv[1:]
    if not a: print("用法: hit <step> [原因] | reset <step> | status"); return
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    doc = load()
    if a[0] == "hit":
        step = a[1]; doc[step] = doc.get(step, 0) + 1
        doc[step + ":last"] = time.strftime("%F %T")
        json.dump(doc, open(fpath(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if doc[step] >= LIMIT:
            print(f"[熔断] {step} 失败 {doc[step]} 次 >= {LIMIT}：强制回退本步或求助用户，禁止继续重试")
            sys.exit(3)
        print(f"[惩罚] {step} 第 {doc[step]}/{LIMIT} 次")
    elif a[0] == "reset":
        step = a[1]; doc.pop(step, None); doc.pop(step + ":last", None)
        json.dump(doc, open(fpath(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("[清零]", step)
    else:
        keep = {k: v for k, v in doc.items() if not k.endswith(":last")}
        print(json.dumps(keep, ensure_ascii=False))
main()
