# CHANGELOG

## 0.1.0 — 初版（concurrency-design）

- 结构复刻 general-programming / ui-design / database-management：创建路径 12 节点 + 修改路径。
- 机制约束沿用：垃圾回收 / 上下文压缩 / 逻辑链 / 过程链存取 / 惩罚 / 沙盒。
- 新增领域约束三条：
  `resistance/共享可变状态约束/`（状态归属、同步机制唯一、可见性显式、复合操作原子化、安全发布）、
  `resistance/锁粒度约束/`（全局锁序无环、临界区最小、持锁时长有界、锁内禁止阻塞 IO）、
  `resistance/取消安全约束/`（四条终止路径、超时显式、取消沿树传播、收尾幂等）。
- 新增薄技能依赖声明：file_ops / code-guidelines / pavedpath-code / python / git（见 `dependence/`）。
- 新增知识库 7 域 19 条目：理论基础、经典书目、执行模型、数据结构、并发控制、实践模式、工具与检测。
  本次构建环境外网不可达（urlopen 10060），条目如实标注 `[本地]`，未伪造 URL。
- 新增脚本：`race_probe.py`（共享态与 check-then-act 剖面）、`deadlock_check.py`（锁序环与顺序不一致）、
  `thread_safety_lint.py`（锁内阻塞/吞取消/无超时等待）、`stress_test_runner.py`（多线程多轮压测，默认 dry-run）。
- 新增 `tests/test_domain_scripts.py`：四脚本冒烟测试（含真并发压测与锁序验环）。
- 违规后果：共享态无同步 → 数据竞争与不可复现脏值；锁序有环 → 死锁挂起吞吐归零；
  取消被吞 → 上层以为已停而工作仍在跑。
- 兜底：无网络 → `[本地]` 标注并说明缺口；无 TSan/Helgrind → 降级静态剖面 + 多轮压测并声明
  「未经检测器确证」。
