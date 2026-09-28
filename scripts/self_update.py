"""self_update.py — 自更新接口：report 汇总版本与变更，compare 与目标目录比对差异。"""
import os, sys, time, hashlib
def digest(root):
    h = hashlib.sha1()
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in (".git", "__pycache__", "tmp"))
        for f in sorted(fn):
            if f.endswith((".md", ".py")):
                p = os.path.join(dp, f)
                h.update(f.encode()); h.update(open(p, "rb").read())
    return h.hexdigest()[:12]
def main():
    a = sys.argv[1:]
    op = a[0] if a else "report"
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    root = g("--root", ".")
    if op == "report":
        print("[报告] root =", os.path.abspath(root))
        print("[报告] digest =", digest(root), "| ts =", time.strftime("%F %T"))
        ch = os.path.join(root, "CHANGELOG.md")
        print("[报告] CHANGELOG 存在 =", os.path.exists(ch))
    elif op == "compare":
        tgt = g("--target")
        if not tgt: print("用法: compare --root <tmp> --target <已装目录>"); sys.exit(2)
        x, y = digest(root), digest(tgt)
        print("[比对]", x, "vs", y, "|", "一致" if x == y else "有差异（需释放/合并）")
        sys.exit(0 if x == y else 4)
    else:
        print("用法: report [--root dir] | compare --root <tmp> --target <dir>")
main()
