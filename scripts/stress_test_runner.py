"""stress_test_runner.py — 目标函数多线程/多轮重复执行，出失败与超时剖面。
用法：python -B scripts/stress_test_runner.py --target <file.py> --fn <name>
      [--threads 8] [--rounds 20] [--timeout 5] [--yes]
默认 dry-run 只出计划；--yes 才起线程。退出码 0=全通过 1=有失败/超时 2=用法错。"""
import argparse, importlib.util, sys, threading, time
def load(path, name):
    spec = importlib.util.spec_from_file_location("t", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, name)
def run(a):
    fn, res, lk = load(a.target, a.fn), [], threading.Lock()
    def work():
        for _ in range(a.rounds):
            try:
                fn()
                r = ("ok", "")
            except Exception as e:
                r = ("fail", f"{type(e).__name__}: {e}"[:80])
            with lk:
                res.append(r)
            if r[0] == "fail":
                return
    ts = [threading.Thread(target=work, daemon=True) for _ in range(a.threads)]
    t0 = time.time()
    [x.start() for x in ts]
    [x.join(a.timeout) for x in ts]
    return res, sum(x.is_alive() for x in ts), round(time.time() - t0, 3)
def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--target"), ap.add_argument("--fn")
    for k, ty, d in (("threads", int, 8), ("rounds", int, 20), ("timeout", float, 5)):
        ap.add_argument("--" + k, type=ty, default=d)
    ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    if not a.target or not a.fn or not a.target.endswith(".py"):
        print(__doc__.strip())
        return 2
    if not a.yes:
        print(f"[dry-run] {a.threads} 线程 x {a.rounds} 轮 = {a.threads * a.rounds} 次调用，"
              f"硬超时 {a.timeout}s（加 --yes 执行）")
        return 0
    res, hung, el = run(a)
    bad = [r for r in res if r[0] != "ok"]
    for x in bad[:8]:
        print("失败:", x[1])
    print(f"完成={len(res)}/{a.threads * a.rounds} 失败={len(bad)} 挂起线程={hung} 用时={el}s")
    return 1 if (bad or hung or len(res) < a.threads * a.rounds) else 0
if __name__ == "__main__":
    sys.exit(main())
