"""race_probe.py — 共享可变状态与 check-then-act 竞态剖面（静态启发式，非证明）。
用法：python -B scripts/race_probe.py <文件或目录> [--json]；0=无 1=有 2=用法错。"""
import json, os, re, sys
CONC = r"(threading|Thread|asyncio|concurrent|Lock|Mutex|synchronized|atomic|tokio)"
GUARD = r"(with\s+\w*\.?\w*lock|synchronized|\.acquire\(\)|\.lock\(\))"
INIT = r"def\s+__init__|__new__"
BLK = r"(requests\.|urlopen|\.read\(\)|\.recv\(|sleep\(|input\()"
SRC = (".py", ".java", ".go", ".cpp", ".js", ".rs")
R = [("check-then-act", r"^\s*if[^\n]*(contains|exists|is_?not_?None| in self)", "", 1),
     ("非原子读改写", r"self\.\w+\s*(\+=|-=|\*=|/=|%=)", "U", 1),
     ("裸共享字段写", r"^\s*self\.(?!_?[a-z]*lock)\w+\s*=\s*\w", "U", 1),
     ("无界队列", r"(Queue\(\s*\)|deque\(\s*\)|LinkedBlockingQueue\(\s*\))", "", 0),
     ("sleep掩盖竞态", r"(Thread\.sleep|time\.sleep)\s*\(", "", 0),
     ("锁内可疑阻塞", r"(with\s+self\.\w*lock|synchronized\s*\()", "B", 0)]

def scan(p):
    txt = open(p, encoding="utf-8", errors="replace").read()
    ls, sh, out = txt.splitlines(), re.search(CONC, txt), []
    for i, ln in enumerate(ls, 1):
        pre, post = "\n".join(ls[max(0, i - 3):i - 1]), "\n".join(ls[i:i + 4])
        for name, rx, need, want in R:
            if not re.search(rx, ln) or (want and not sh):
                continue
            if need == "U" and (re.search(GUARD, pre) or re.search(INIT, pre)):
                continue
            if need == "B" and not re.search(BLK, post):
                continue
            out.append({"file": p, "line": i, "kind": name, "text": ln.strip()[:52]})
            break
    return out

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a or not os.path.exists(a[0]):
        print(__doc__.strip()); return 2
    fs = []
    for dp, dn, fn in os.walk(a[0]):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "tmp", "node_modules")]
        fs += [os.path.join(dp, f) for f in fn if f.endswith(SRC)]
    hits = [h for f in sorted(fs or [a[0]]) for h in scan(f)]
    if "--json" in sys.argv:
        print(json.dumps(hits, ensure_ascii=False))
    else:
        for h in hits:
            print(f"{h['file']}:{h['line']} [{h['kind']}] {h['text']}")
        print(f"竞态风险点 = {len(hits)}（启发式，须压测/TSan 复核）")
    return 1 if hits else 0

if __name__ == "__main__":
    sys.exit(main())
