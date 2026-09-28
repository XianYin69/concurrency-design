"""sandbox.py — 沙盒机制：未指定目标目录时在固定路径作业；交付/删除默认预览，--yes 执行。"""
import json, os, shutil, sys, time
def root():
    b = os.environ.get("SMS_HOME")
    b = b or os.path.join(os.path.expanduser("~"), "AppData", "Local", "SMS")
    d = os.path.join(b, "sandbox"); os.makedirs(d, exist_ok=True); return d
def idx(): return os.path.join(root(), "index.json")
def load():
    return json.load(open(idx(), encoding="utf-8")) if os.path.exists(idx()) else {}
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    op = a[0] if a else ""
    if op == "create":
        name = g("--name", "skill")
        p = os.path.join(root(), time.strftime(name + "-%Y%m%d-%H%M%S"))
        os.makedirs(p, exist_ok=True)
        d = load(); d[p] = {"name": name, "ts": time.strftime("%F %T")}
        json.dump(d, open(idx(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("[沙盒]", p)
    elif op == "list":
        for k, v in load().items(): print(k, "|", v.get("name"), v.get("ts"))
    elif op == "deliver":
        src, dst = g("--id"), g("--to")
        if not (src and dst): print("用法: deliver --id <沙盒> --to <目标> [--yes]"); sys.exit(2)
        if "--yes" not in a: print("[预览] 复制", src, "->", dst); return
        shutil.copytree(src, dst, dirs_exist_ok=True); print("[已交付]", dst)
    elif op == "clean":
        p = g("--id")
        if "--yes" not in a: print("[预览] 删除沙盒", p); return
        shutil.rmtree(p, ignore_errors=True)
        d = load(); d.pop(p, None)
        json.dump(d, open(idx(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("[已清理]", p)
    else:
        print("用法: create --name N | list | deliver --id P --to T [--yes] | clean --id P [--yes]")
main()
