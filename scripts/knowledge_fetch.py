"""knowledge_fetch.py — 开放文献抓取：白名单主机，原始页与出处落 tmp（禁写 skill 目录）。"""
import hashlib, json, os, re, sys, time
from urllib.request import Request, urlopen
ALLOWED = re.compile(r"(wikipedia\.org|arxiv\.org|doi\.org|stackoverflow\.com|"
                     r"github\.com|gitlab\.com|[^/]*\.org)$")
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    url, out = g("--url"), g("--out", "tmp/downloads")
    if not url:
        print("用法: --url <白名单页> [--out dir]"); sys.exit(2)
    host = re.sub(r"^https?://", "", url).split("/")[0]
    if not ALLOWED.search(host):
        print("[拒绝] 非白名单来源:", host); sys.exit(1)
    os.makedirs(out, exist_ok=True)
    rid = hashlib.sha1(url.encode()).hexdigest()[:12]
    try:
        body = urlopen(Request(url, headers={"User-Agent": "concurrency-design/1.0"}),
                       timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        print("[失败] 网络不可用：降级本地资料并报告缺口:", e); sys.exit(1)
    html = os.path.join(out, rid + ".html")
    open(html, "w", encoding="utf-8").write(body)
    prov = os.path.join(out, rid + ".provenance.json")
    json.dump({"url": url, "host": host, "ts": time.strftime("%F %T"),
               "license": "引用页各自许可·仅存摘要与出处", "bytes": len(body)},
              open(prov, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[已抓取]", html, "|", prov)
main()
