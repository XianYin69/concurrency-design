"""context_compress.py — 上下文压缩：按关键词与比例抽取相关行，输出精简摘要（默认预览）。"""
import os, sys
def score(line, kws):
    low = line.lower()
    return sum(1 for k in kws if k.lower() in low)
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    ratio = float(g("--ratio", "0.3")) or 0.3
    kws = [k for k in g("--kw").split(",") if k]
    path = g("--path", "SKILL.md")
    if not os.path.exists(path): print("无文件:", path); return
    lines = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    keep = max(1, int(len(lines) * ratio))
    ranked = sorted(range(len(lines)), key=lambda i: (-score(lines[i], kws), i))[:keep]
    out = "\n".join(lines[i] for i in sorted(ranked))
    if "--yes" not in a:
        print("[预览] 原", len(lines), "行 -> 压缩", keep, "行\n" + out); return
    dst = g("--out", path + ".compressed")
    open(dst, "w", encoding="utf-8").write(out + "\n")
    print("[已压缩]", dst, keep, "行")
main()
