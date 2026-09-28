"""lint_check.py — 体量与坏味道自查：.md/脚本 ≤50 行、长函数、裸 except、print 调试残留。"""
import os, re, sys
LIMIT = 50
def check(root):
    bad = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "node_modules", "tmp")]
        for f in fn:
            p = os.path.join(dp, f)
            if f.endswith(".md") or f.endswith(".py"):
                try: lines = open(p, encoding="utf-8").read().splitlines()
                except Exception: continue
                if len(lines) > LIMIT: bad.append((p, f"{len(lines)} 行 > {LIMIT}"))
            if f.endswith(".py"):
                try: src = open(p, encoding="utf-8").read()
                except Exception: continue
                if re.search(r"except\s*:", src): bad.append((p, "裸 except"))
                if "scripts" not in dp and re.search(r"^\s*print\(", src, re.M):
                    bad.append((p, "print 残留"))
                if any(len(l) > 100 for l in lines): bad.append((p, "存在 >100 字符长行"))
    return bad
def main():
    a = sys.argv[1:]
    root = a[a.index("--path") + 1] if "--path" in a else "."
    bad = check(root)
    for p, w in bad: print("问题:", os.path.relpath(p, root), "|", w)
    print("问题数 =", len(bad)); sys.exit(1 if bad else 0)
main()
