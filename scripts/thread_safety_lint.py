"""thread_safety_lint.py — 线程安全静态体检（锁内阻塞、吞取消、无超时等待等）。
用法：python -B scripts/thread_safety_lint.py <文件或目录>
退出码 0=净 1=有问题 2=用法错误。启发式清单，须配合 race_probe 与压测。"""
import os, re, sys
E = (".py", ".java", ".go", ".cpp", ".js", ".rs")
CONC = r"(threading|Thread|asyncio|concurrent|Lock|Mutex|synchronized|atomic|tokio)"
IO = r"(requests\.|urlopen|\.read\(\)|\.recv\(|sleep\(|input\()"
RULES = [("锁内阻塞IO", r"(with\s+self\.\w*lock|synchronized\s*\()", IO),
         ("吞掉中断取消", r"except\s*\((InterruptedError|CancelledError)", r"pass\b"),
         ("无超时等待", r"(join\(\s*\)|\.get\(\s*\)|wait\(\s*\)|\.acquire\(\s*\))", None),
         ("裸共享计数器", r"^\s*(global\s+\w+|\w*count\w*\s*(\+=|-=))", None),
         ("无界线程池队列", r"(ThreadPoolExecutor\(\s*\)|CachedThreadPool)", None)]

def scan(p):
    txt = open(p, encoding="utf-8", errors="replace").read()
    if not re.search(CONC, txt):
        return []
    ls, out = txt.splitlines(), []
    for i, ln in enumerate(ls, 1):
        for name, rx, ctx in RULES:
            if not re.search(rx, ln):
                continue
            if ctx and not re.search(ctx, "\n".join(ls[i - 1:i + 5])):
                continue
            out.append((p, i, name, ln.strip()[:52]))
            break
    return out

def files_of(a):
    if os.path.isfile(a):
        return [a]
    fs = []
    for dp, dn, fn in os.walk(a):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "tmp")]
        fs += [os.path.join(dp, f) for f in fn if f.endswith(E)]
    return fs

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    if not a or not os.path.exists(a[0]):
        print(__doc__.strip())
        return 2
    hits = [h for f in files_of(a[0]) for h in scan(f)]
    for f, i, name, t in hits:
        print(f"{f}:{i} [{name}] {t}")
    print("线程安全问题 =", len(hits))
    return 1 if hits else 0

if __name__ == "__main__":
    sys.exit(main())
