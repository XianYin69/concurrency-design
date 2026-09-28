"""run_tests.py — 构建与测试执行器：pytest 优先，缺失降级 unittest，默认 --dry-run 预览。"""
import os, subprocess, sys, time
def has(mod):
    return subprocess.run([sys.executable, "-c", "import " + mod],
                          capture_output=True).returncode == 0
def plan(path):
    cmds = []
    if os.path.isdir(os.path.join(path, "tests")):
        if has("pytest"):
            cmds.append([sys.executable, "-m", "pytest", "-q", path])
        else:
            cmds.append([sys.executable, "-m", "unittest", "discover",
                         "-s", path, "-t", path, "-p", "test_*.py", "-v"])
    cmds.append([sys.executable, "-m", "compileall", "-q", path])
    if os.path.exists(os.path.join(path, "package.json")):
        cmds.append(["npm", "test", "--prefix", path])
    return cmds
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    path = g("--path", ".")
    cmds = plan(path)
    if "--dry-run" in a:
        for c in cmds:
            print("[预览]", " ".join(c))
        return
    t0, fails = time.time(), 0
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True, timeout=600)
        print("$", os.path.basename(c[0]) if len(c[0]) < 40 else "py", " ".join(c[1:]),
              "-> rc", r.returncode)
        print(((r.stdout or "") + (r.stderr or ""))[-600:])
        fails += (r.returncode != 0)
    rep = os.path.join(path, "test-report.md")
    open(rep, "w", encoding="utf-8").write(
        "# 测试报告\n\n- 时间: " + time.strftime("%F %T") + "\n- 命令数: " + str(len(cmds)) +
        "\n- 失败: " + str(fails) + "\n- 用时: %.1fs\n" % (time.time() - t0))
    print("[报告]", rep, "| 失败 =", fails)
    sys.exit(1 if fails else 0)
main()
