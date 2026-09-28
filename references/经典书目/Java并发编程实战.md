# Java 并发编程实战（Goetz 等，2006）

来源：[本地]（书目与主题常识，未联网确证页码）· 用途：线程安全性与发布实践基线。

## 主线结构

- **并发基础**：线程安全定义、原子性与 `volatile`、不变式（invariant）、加锁三动机
  （原子性/可见性/有序性）。
- **结构化并发任务**：任务与执行、`Executor`/线程池、取消与关闭、池大小估算、异常处理
  （`Future` 吞异常的坑）。
- **活性、性能与测试**：死锁/饥饿/活锁、可扩展性（Amdahl/Gustafson）、并发测试方法
  （确定性、时序植入、压力与比较测试）。
- **高级主题**：显式锁与条件队列、自定义同步器（AQS 思路）、原子变量与非阻塞算法、
  锁分段（striping）、`Fork/Join` 与工作窃取。

## 高频结论（可用于裁决）

1. 安全发布四法：初始化后不改的静态字段、`final` 字段、`volatile` 引用、锁保护字段/引用。
2. 复合操作不因单条字节码而原子；`i++` 需 `AtomicInteger` 或锁。
3. 取消用 `interrupt` 协作式传播；`Thread.stop` 禁用（见 [取消与超时模式](../实践模式/取消与超时模式.md)）。
4. 优先现有并发容器（`ConcurrentHashMap`、`BlockingQueue`）而非自加锁。
5. 池大小按 CPU/IO 比与目标利用率估算，须以压测数据修正。

## 适用边界

- 成书早于 Java 8/17/21：`CompletableFuture`、`Flow`（Reactive Streams）、虚拟线程（Loom）、
  `StructuredTaskScope` 不在其内，用到时须经浏览器学习确证版本与语义。

- 返回 [references](../references.md) · [内存模型与happens-before](../理论基础/内存模型与happens-before.md)
