"""check_links.py — 悬空链接校验：扫描 .md 相对链接，目标不存在即报悬空（红线：悬空=0）。"""
import os, re, sys
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
def scan(root):
    bad = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("tmp", ".git", "__pycache__")]
        for f in fn:
            if not f.endswith(".md"): continue
            p = os.path.join(dp, f)
            for m in LINK.finditer(open(p, encoding="utf-8").read()):
                t = m.group(1).split("#")[0].strip()
                if not t or t.startswith(("http:", "https:", "mailto:")): continue
                tgt = os.path.normpath(os.path.join(dp, t))
                if not os.path.exists(tgt): bad.append((p, t))
    return bad
def main():
    a = sys.argv[1:]
    root = a[a.index("--root") + 1] if "--root" in a else "."
    bad = scan(root)
    for p, t in bad: print("悬空:", os.path.relpath(p, root), "->", t)
    print("悬空链接数 =", len(bad))
    sys.exit(1 if bad else 0)
main()
