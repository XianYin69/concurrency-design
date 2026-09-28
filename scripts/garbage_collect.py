"""garbage_collect.py — 垃圾回收：列出/清理 tmp 过期产物，默认预览，--yes 执行。"""
import os, sys, time
SKIP = (".git", "__pycache__", "node_modules")
def items(path, age):
    now = time.time(); out = []
    for dp, dn, fn in os.walk(path):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            p = os.path.join(dp, f)
            try: d = now - os.path.getmtime(p)
            except OSError: continue
            if d > age * 86400: out.append((p, int(d / 86400)))
    return out
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    path = g("--path", "tmp"); age = float(g("--age", "7")); dry = "--yes" not in a
    if not os.path.isdir(path):
        print("无 tmp 目录:", path); return
    rows = items(path, age)
    for p, d in rows:
        print(("[预览] " if dry else "[删除] ") + str(d) + "天前 " + p)
    if dry:
        print("待回收 =", len(rows), "| 执行须 --yes"); return
    n = 0
    for p, _ in rows:
        try:
            os.remove(p); n += 1
        except OSError as e:
            print("失败:", p, e)
    for dp, dn, fn in os.walk(path, topdown=False):
        if dp != path and os.path.isdir(dp) and not os.listdir(dp):
            os.rmdir(dp)
    print("已回收 =", n)
main()
