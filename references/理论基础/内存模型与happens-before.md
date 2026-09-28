# 内存模型与 happens-before（JMM / C++11 atomics / x86-TSO）

来源：[本地]（未联网确证）· 用途：判定可见性与有序性风险。

## 是什么

- 内存模型 = 语言/硬件对「哪条读能看到哪条写、以什么顺序可见」的契约，分**语言级**（JMM、C++11）
  与**硬件级**（x86-TSO、ARM/POWER 弱序）两层；语言级给出 happens-before 保证，硬件级决定代价。
- happens-before：若 A hb B，则 A 的写对 B 的读可见且有序。它是**传递闭包**，不是时间先后。
- 无 hb 关系的两访问（至少一个是写）= 数据竞争 → 语言级未定义行为（C/C++）或
  不可预期值（Java 允许读到任意已写入值）。

## 关键要点

- **释放-获取**：`release 写` + `对应 acquire 读` 建立 hb，把之前的所有普通写一并发布（安全发布）。
- **x86-TSO**：仅 StoreLoad 会重排；故 x86 上「不加锁的 volatile 读」看似安全，
  **不可**类推到 ARM/POWER，也不可类推到语言级重排（编译器同样重排）。
- C++11 `memory_order` 六档：relaxed / consume(不推荐) / acquire / release / acq_rel / seq_cst；
  默认 seq_cst，降级须有基准证据。
- Java `final` 字段在构造函数正确逸出前有冻结语义；`volatile` 提供 hb 但不提供复合原子性。

## 用法

1. 先问「有没有 happens-before 边」，没有就是 bug，与是否复现无关。
2. 需要顺序+可见性用 release/acquire 配对；只需单变量原子性用 relaxed，须注释理由。
3. 任何跨语言/跨架构类推须经浏览器学习确证（查官方内存模型文档）。

- 返回 [references](../references.md) · [竞态条件与数据竞争](竞态条件与数据竞争.md)
