# ABA 问题、内存回收与 RCU

来源：[本地]（未联网确证）· 用途：无锁结构的进展保证与回收协议设计。

## ABA

- 定义：CAS 比较「值」而非「历史」——线程读到 A，别线程改 B 再改回 A（甚至同址复用节点），
  CAS 仍成功，但结构不变量已被破坏（链表指针复活、size 与 head 不一致）。
- 常见解法：
  1. **带版本指针**（tagged pointer / DCAS 思路）：值 + 单调版本一起比较。
  2. **节点不重用**（epoch/hazard 回收）：旧节点永不复用则 ABA 退化为无害。
  3. **锁保护关键路径**：只在 CAS 失败重试处加锁，成本可控。
- 语言现实：Java `AtomicStampedReference`；C++ 无 DCAS 保证（`double_compare_exchange` 非普遍）；
  Go 无 CAS 泛型原语，通常用 mutex/channel 替代。

## 回收协议（无锁的难点在「何时能 free」）

| 协议 | 思路 | 代价 |
|---|---|---|
| Hazard Pointer | 发布「我正在用 X」，回收前检查 | 读侧写内存，扩展性有限 |
| Epoch-Based (EBR) | 全局纪元 + 延迟批量回收 | 需线程活跃性保证，慢线程阻塞回收 |
| RCU | 写侧复制并发布新指针，宽限期后回收旧数据 | 写放大；读侧几乎零成本 |

- RCU 三要素：**发布**（写指针用 `rcu_assign_pointer`/release）、**订阅**（`rcu_read_lock` +
  `rcu_dereference`/acquire）、**宽限期**（`synchronize_rcu`/call_rcu）。
- 内核 RCU 与用户态（liburcu、`std::atomic` 手写、Java 无原生 RCU）语义不同，须分别确证。

## 用法

1. 写无锁结构前先回答：谁负责回收？没有答案就不要上无锁。
2. 任何「CAS 成功即正确」的断言须能说明为何不构成 ABA。

- 返回 [references](../references.md) · [多处理器编程艺术](../经典书目/多处理器编程艺术.md)
