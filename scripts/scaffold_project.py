"""scaffold_project.py — 工程脚手架：建 src/tests 布局与最小可运行入口，默认预览。"""
import os, sys
README = "# 项目\n\n- 入口: src/main.py\n- 测试: tests/test_main.py\n- 运行: python -B src/main.py\n"
MAIN = ('"""入口模块：只做编排，业务逻辑在各自模块内。"""\n'
        "import sys\n\n\ndef run(data):\n"
        '    """主逻辑：输入 data 返回结果；异常向上抛，不静默吞。"""\n'
        "    return data\n\n\ndef main(argv=None):\n"
        "    a = list(sys.argv[1:] if argv is None else argv)\n"
        '    print(run(" ".join(a)))\n    return 0\n\n\n'
        'if __name__ == "__main__":\n    raise SystemExit(main())\n')
TEST = ("import os, sys, unittest\n"
        "sys.path.insert(0, os.path.join(os.path.dirname(__file__), \"..\", \"src\"))\n"
        "import main as m\n\n\nclass TestRun(unittest.TestCase):\n"
        "    def test_passthrough(self):\n"
        "        self.assertEqual(m.run(\"x\"), \"x\")\n\n"
        "    def test_empty(self):\n"
        "        self.assertEqual(m.run(\"\"), \"\")\n\n\n"
        "if __name__ == \"__main__\":\n    unittest.main()\n")
TPL = {"README.md": README, "src/main.py": MAIN, "tests/test_main.py": TEST,
       "tests/__init__.py": ""}
def main():
    a = sys.argv[1:]
    g = lambda k, d="": a[a.index(k) + 1] if k in a else d
    tgt = g("--target")
    yes = "--yes" in a
    if not tgt:
        print("用法: --target <dir> [--yes]（默认预览）"); sys.exit(2)
    for rel, body in TPL.items():
        p = os.path.join(tgt, rel)
        if not yes:
            print("[预览]", p); continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p):
            print("[跳过] 已存在", p); continue
        open(p, "w", encoding="utf-8").write(body)
        print("[写入]", p)
    print("[脚手架]", tgt, "| 下一步：按大纲替换占位实现并补测试")
main()
