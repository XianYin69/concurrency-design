# scripts（脚本库）

本目录存放可执行辅助脚本：校验、生成、检索、机制兜底。工具本身不限行数（50 行红线只约束 markdown），
文件名英文、小写、下划线分隔。

## 通用机制

- [`check_links.py`](check_links.py)：悬空链接校验（红线：悬空 = 0）。
- [`lint_check.py`](lint_check.py)：体量与坏味道自查（.md ≤50 行；脚本不计行数，查裸 except、print 残留、长行）。
- [`logic_chain.py`](logic_chain.py)：逻辑链 add/verify/debate（正反双链）。
- [`process_chain.py`](process_chain.py)：过程链 save/load/interrupt/resume。
- [`penalty.py`](penalty.py)：惩罚计数，达 10 次熔断。
- [`garbage_collect.py`](garbage_collect.py)：tmp 过期产物回收（默认预览）。
- [`context_compress.py`](context_compress.py)：按关键词压缩上下文。
- [`sandbox.py`](sandbox.py)：固定路径沙盒 create/list/deliver/clean。
- [`deps_check.py`](deps_check.py)：dependence/ 声明项可达性自检。
- [`browser_learn.py`](browser_learn.py)：派 file_ops 联网取证（须 :grant network）。
- [`knowledge_fetch.py`](knowledge_fetch.py)：白名单文献抓取（落 tmp）。
- [`knowledge_convert.py`](knowledge_convert.py)：HTML→md 摘要与出处。
- [`scaffold_project.py`](scaffold_project.py)：工程脚手架（本技能出 src/tests/bench 结构）。
- [`run_tests.py`](run_tests.py)：构建与测试执行 + 报告。
- [`flowchart_helper.py`](flowchart_helper.py)：需求模糊时出流程草稿。
- [`self_update.py`](self_update.py)：report/compare 版本比对。

## 领域脚本

- [`race_probe.py`](race_probe.py)：共享可变状态与 check-then-act 竞态剖面（静态启发式，出清单）。
- [`deadlock_check.py`](deadlock_check.py)：由加锁顺序日志建「锁序图」并检测环与不一致顺序。
- [`thread_safety_lint.py`](thread_safety_lint.py)：线程安全体检（无同步写、锁内阻塞、无界队列、缺超时）。
- [`stress_test_runner.py`](stress_test_runner.py)：多线程/多轮重复执行目标，出失败与超时剖面（默认 dry-run）。

## 运行约定

1. 用项目默认 Python：`python -B scripts/<name>.py`。
2. 任何写盘脚本默认预览，落盘须显式 `--yes`；压测脚本另需 [取消安全约束](../resistance/取消安全约束/取消安全约束.md) 的超时上限。
3. 运行前先读 [resistance](../resistance/resistance.md) 确认权限与回滚策略。
4. 缓存与临时产物一律落 tmp 或用户缓存目录，禁止写入 skill 目录。
