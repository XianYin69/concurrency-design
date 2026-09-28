"""test_domain_scripts.py — 领域脚本冒烟（race_probe/deadlock_check/lint/stress）。"""
import os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(os.path.dirname(HERE), "scripts")
BAD = ("import threading, time\nclass C:\n def __init__(self):\n  self.lock = threading.Lock()"
       "\n  self.n = 0\n def bump(self):\n  self.n += 1\n def slow(self):\n"
       "  with self.lock:\n   time.sleep(1)\n")
GOOD = ("import threading\nclass C:\n def __init__(self):\n  self._lock = threading.Lock()"
        "\n  self._n = 0\n def add(self, k):\n  with self._lock:\n   self._n += k\n")
TGT = "import threading\nL = threading.Lock()\nN = [0]\ndef bump():\n with L:\n  N[0] += 1\n"

def run(name, *args):
    return subprocess.run([sys.executable, "-B", os.path.join(S, name), *args],
                          capture_output=True, text=True)

class Domain(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def w(self, n, t):
        with open(os.path.join(self.tmp, n), "w", encoding="utf-8") as f:
            f.write(t)
        return f.name

    def test_race_probe(self):
        self.assertEqual(run("race_probe.py", self.w("bad.py", BAD)).returncode, 1)
        self.assertEqual(run("race_probe.py", self.w("good.py", GOOD)).returncode, 0)

    def test_deadlock_check(self):
        r = run("deadlock_check.py", self.w("locks.log", "t1: A > B\nt2: B > A\n"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("锁序环", r.stdout)
        o = self.w("ok.log", "t1: A > B\nt2: A > B > C\n")
        self.assertEqual(run("deadlock_check.py", o).returncode, 0)

    def test_thread_safety_lint(self):
        r = run("thread_safety_lint.py", self.w("bad.py", BAD))
        self.assertEqual(r.returncode, 1)
        self.assertIn("锁内阻塞IO", r.stdout)

    def test_stress_runner(self):
        t = self.w("tgt.py", TGT)
        self.assertIn("dry-run", run("stress_test_runner.py", "--target", t, "--fn", "bump").stdout)
        e = run("stress_test_runner.py", "--target", t, "--fn", "bump", "--yes",
                "--threads", "4", "--rounds", "25", "--timeout", "10")
        self.assertEqual(e.returncode, 0)
        self.assertIn("失败=0", e.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
