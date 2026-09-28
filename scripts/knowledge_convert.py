"""knowledge_convert.py — HTML→md 摘要：只留要点与出处，不存版权正文。"""
import json, os, re, sys
def paras(html):
    h = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", html)
    h = re.sub(r"(?is)<[^>]+>", " ", h)
    out = []
    for p in re.split(r"(?is)</p>|<br\s*/?>", h):
        s = re.sub(r"\s+", " ", p).strip()
        if len(s) > 80:
            out.append(s[:200])
        if len(out) >= 5:
            break
    return out
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    src, dst = g("--src"), g("--dst")
    if not src:
        print("用法: --src tmp/downloads/x.html [--dst references/领域/主题.md]"); sys.exit(2)
    html = open(src, encoding="utf-8", errors="ignore").read()
    pp = src.replace(".html", ".provenance.json")
    m = json.load(open(pp, encoding="utf-8")) if os.path.exists(pp) else {}
    body = "\n".join("- " + p for p in paras(html)) or "- （无可摘正文）"
    md = ("# " + os.path.basename(dst or src).rsplit(".", 1)[0] + "\n\n"
          "- 来源: " + str(m.get("url", "未知")) + "\n- 抓取: " + str(m.get("ts", "")) + "\n\n"
          "## 要点\n\n" + body + "\n\n> 仅存摘要与出处，正文版权归原作者。\n")
    if not dst:
        print(md); return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        print("[跳过] 已存在", dst); return
    open(dst, "w", encoding="utf-8").write(md[:1800])
    print("[已转换]", dst)
main()
