"""deadlock_check.py — 加锁顺序日志的锁序环与顺序不一致检测（死锁风险）。
用法：python -B scripts/deadlock_check.py <log>   每行形如： t1: A > B > C
退出码 0=无环且一致 1=有环或不一致 2=用法错误。"""
import os, re, sys
from collections import defaultdict
LINE = re.compile(r"^\s*[^:\s]+\s*:\s*(.+)$")
def pairs(path):
    P = set()
    for raw in open(path, encoding="utf-8", errors="replace"):
        m = LINE.match(raw.strip()) if not raw.startswith("#") else None
        if not m:
            continue
        lk = [x.strip() for x in re.split(r">|,|\|", m.group(1)) if x.strip()]
        P |= {(a, b) for a, b in zip(lk, lk[1:]) if a != b}
    return P

def cycles(P):
    adj = defaultdict(set)
    for a, b in P:
        adj[a].add(b)
    st, out = {}, []
    def dfs(u, path):
        st[u] = 1
        for v in sorted(adj[u]):
            if st.get(v) == 1:
                out.append(" -> ".join(path[path.index(v):] + [v]))
            elif not st.get(v):
                dfs(v, path + [v])
        st[u] = 2
    for u in sorted(adj):
        if not st.get(u):
            dfs(u, [u])
    return out

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print(__doc__.strip())
        return 2
    P = pairs(sys.argv[1])
    bad = sorted({f"{a}>{b} 与 {b}>{a} 并存" for a, b in P if (b, a) in P and a < b})
    cyc = cycles(P)
    for x in bad:
        print("顺序不一致：", x)
    for c in cyc:
        print("锁序环：", c)
    print(f"加锁对={len(P)} 不一致={len(bad)} 环={len(cyc)}")
    return 1 if (bad or cyc) else 0
if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    sys.exit(main())
