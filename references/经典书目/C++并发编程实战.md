# C++ 并发编程实战（Anthony Williams）

来源：[本地]（书目与主题常识，未联网确证版次细节）· 用途：C++11 及以后并发设施选型。

## 主线结构

- **C++11 基础**：`std::thread`、`std::mutex`/`lock_guard`/`unique_lock`/`scoped_lock`、
  `std::condition_variable`、`std::future`/`promise`/`async`、`std::atomic` 与内存序。
- **线程管理**：传递参数、detach、线程标识、异常跨线程传播、`jthread`/`stop_token`（C++20）。
- **共享数据与保护**：保护数据、避免竞态、`shared_ptr` 的原子性边界、无锁栈/队列设计。
- **高级**：`atomic` 的等待/通知（C++20 `wait`）、并行算法（`execution policy`）、
  协程（C++20）、内存序与硬件映射。

## 高频结论

1. 未指定内存序的 `atomic` 默认 `seq_cst`；降级为 `release/acquire/relaxed` 须有基准与注释。
2. `std::mutex` 加锁失败即未定义；用 RAII 包装，禁止手写 `lock/unlock` 配对。
3. 数据竞争 = 未定义行为（比 Java 更严苛），必须用 TSan 验证（见检测工具条目）。
4. `shared_ptr` 控制块原子但所指对象不原子；引用本身跨线程读写需额外同步。
5. 条件变量必须与谓词循环搭配（`wait(lk, pred)`），否则丢通知/虚假唤醒。

## 适用边界

- 版次差异大（C++11/14/17/20/23）：用到 `jthread`、`latch`、`barrier`、`semaphore`、协程时
  须先确证编译器与标准库支持度。

- 返回 [references](../references.md) · [内存模型与happens-before](../理论基础/内存模型与happens-before.md)
