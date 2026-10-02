"""lint_check.py — 体量与坏味道自查：.md ≤50 行（50 行红线只约束 markdown 文本）；
脚本 .py/.ps1/.sh/.cmd 不计行数，只查裸 except、print 调试残留、>100 字符长行、超长函数。"""
import os, re, sys
LIMIT = 50
FUNC_MAX = 60
MD = (".md",)
SCRIPT = (".py", ".ps1", ".sh", ".cmd")

def _lines(p):
    try:
        return open(p, encoding="utf-8").read().splitlines()
    except Exception:
        return None

def _long_funcs(src):
    """粗略计超长函数：以 def 行为起点，到下一个同级 def/class 或文件尾。"""
    marks = [m.start() for m in re.finditer(r"^(?:def |class |async def )", src, re.M)]
    bad = 0
    for i, s in enumerate(marks):
        e = marks[i + 1] if i + 1 < len(marks) else len(src)
        if src[s:e].count("\n") > FUNC_MAX:
            bad += 1
    return bad

def check(root):
    bad = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", ".kilo", "__pycache__", "node_modules", "tmp")]
        for f in fn:
            p = os.path.join(dp, f)
            ls = _lines(p) if f.endswith(MD + SCRIPT) else None
            if ls is None:
                continue
            if f.endswith(MD) and len(ls) > LIMIT:
                bad.append((p, f"md {len(ls)} 行 > {LIMIT}"))
            if f.endswith(SCRIPT):
                src = "\n".join(ls)
                if re.search(r"except\s*:", src):
                    bad.append((p, "裸 except"))
                if "scripts" not in dp and re.search(r"^\s*print\(", src, re.M):
                    bad.append((p, "print 残留"))
                if any(len(l) > 100 for l in ls):
                    bad.append((p, "存在 >100 字符长行"))
                if f.endswith(".py") and _long_funcs(src):
                    bad.append((p, f"超长函数 >{FUNC_MAX} 行"))
    return bad

def main():
    a = sys.argv[1:]
    root = a[a.index("--path") + 1] if "--path" in a else "."
    bad = check(root)
    for p, w in bad:
        print("问题:", os.path.relpath(p, root), "|", w)
    print("问题数 =", len(bad))
    sys.exit(1 if bad else 0)

main()
