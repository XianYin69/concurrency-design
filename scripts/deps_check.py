"""deps_check.py — 依赖自检：读 dependence/ 声明，逐项验证本地可达（薄技能红线）。"""
import os, re, shutil, sys
ROW = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*\|\s*(skill|software|repo)\s*\|\s*(\S+)")
def declared(path):
    if not os.path.exists(path):
        return []
    return [(m.group(1), m.group(2), m.group(3))
            for m in (ROW.match(l) for l in open(path, encoding="utf-8")) if m]
def sroot():
    return (os.environ.get("SMS_SKILLS") or os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "SMS", "skills"))
def ok_software(name):
    if name == "python":
        return bool(shutil.which("python") or shutil.which("python3"))
    return bool(shutil.which(name))
def ok_skill(name, src):
    cand = [os.path.join(sroot(), name)]
    if src.startswith("local:"):
        base = os.path.join(sroot(), src.split(":", 1)[1])
        cand += [os.path.join(base, name),
                 os.path.join(base, "skill", "sub_skills", name),
                 os.path.join(base, "sub_skills", name)]
    return any(os.path.exists(os.path.join(c, "SKILL.md")) for c in cand)
def main():
    a = sys.argv[1:]
    dep = a[a.index("--dependence") + 1] if "--dependence" in a else "dependence/dependence.md"
    miss = []
    for n, k, s in declared(dep):
        ok = ok_software(n) if k == "software" else ok_skill(n, s)
        print(("  OK   " if ok else "  缺失 ") + f"{n} | {k} | {s}")
        if not ok:
            miss.append(n)
    print("缺失 =", len(miss), miss, "| 缺失即记 interrupt 并报告，禁止伪造能力")
    sys.exit(1 if miss else 0)
main()
