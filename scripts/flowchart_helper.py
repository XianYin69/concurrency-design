"""flowchart_helper.py — 需求模糊时输出 mermaid 流程草稿，辅助与用户对齐（默认预览）。"""
import os, sys
def build(steps):
    lines = ["```mermaid", "flowchart TD"]
    prev = None
    for i, s in enumerate(steps):
        cur = f"N{i}[{s}]"
        lines.append("  " + cur)
        if prev:
            lines.append(f"  {prev} --> {cur}")
        prev = cur
    lines.append("```")
    return "\n".join(lines)
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    steps = [s for s in g("--steps").split(",") if s]
    dst = g("--out", "tmp/outline.md")
    if not steps:
        print("用法: --steps A,B,C [--out tmp/outline.md] [--yes]"); sys.exit(2)
    md = "# 流程草稿\n\n" + build(steps) + "\n\n> 请用户确认节点与顺序后再进入分支分析。\n"
    if "--yes" not in a:
        print(md); print("[预览] 未写盘，执行须 --yes"); return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(md)
    print("[已写出]", dst)
main()
