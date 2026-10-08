"""browser_learn.py — 浏览器学习入口：派 file_ops（ff_lite.py search/fetch）取证，结论落 tmp 供蒸馏。"""
import os, subprocess, sys, time
def ff_lite():
    r = os.path.join(os.environ.get("SMS_SKILLS") or os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "SMS", "skills"),
                     "skill_manage_system", "skill", "sub_skills", "file_ops")
    for n in ("ff_lite.py", "ff_lite"):
        p = os.path.join(r, n)
        if os.path.exists(p): return p
    return None
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    q, out, dry = g("--query"), g("--out", "tmp/learn"), "--dry-run" in a
    tool = ff_lite()
    if not q or not tool:
        print("[拒绝] 缺 --query 或 file_ops/ff_lite.py 不可达：依赖缺失须报告，禁止臆造 API"); sys.exit(1)
    mode, arg = ("fetch", g("--fetch")) if "--fetch" in a else ("search", q)
    cmd = [sys.executable, "-B", tool, mode, arg]
    if dry: print("[预览]", " ".join(cmd)); return
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    os.makedirs(out, exist_ok=True)
    f = os.path.join(out, time.strftime("learn-%Y%m%d-%H%M%S.md"))
    open(f, "w", encoding="utf-8").write(
        f"# 取证 {q}\n\n- 工具: {os.path.basename(tool)} {mode}\n"
        f"- 时间: {time.strftime('%F %T')}\n\n"
        + (r.stdout or "") + (r.stderr or ""))
    print("[已取证]", f, "| 下一步：蒸馏入知识链与 references/"); sys.exit(r.returncode)
main()
