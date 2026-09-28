# POSIX 线程（pthreads）与内核同步

来源：[本地]（IEEE 1003.1 / Linux 语义常识，未联网确证）· 用途：低层线程语义与 C 侧实现。

## 核心对象

| 对象 | 语义要点 |
|---|---|
| `pthread_t` | 线程；创建失败返回错误码而非异常 |
| `pthread_mutex_t` | normal / errorcheck / recursive 属性；递归锁掩盖设计问题 |
| `pthread_cond_t` | 必须与互斥锁 + `while` 谓词循环搭配（虚假唤醒） |
| `pthread_rwlock_t` | 写优先/读优先策略影响饥饿 |
| `sem_t` | 计数信号量，跨进程可用 |
| `pthread_key_t` | 线程局部存储（TLS），析构顺序易漏资源 |

## 高频结论

1. `pthread_cancel` 是异步/延迟取消，默认清理路径脆弱 → 优先**协作式标志 + 条件变量**取消。
2. 信号处理函数内只能调 async-signal-safe 函数；在 handler 里加锁/`malloc` 是事故源。
3. `join` 前线程资源未回收即泄漏；分离线程（detach）须自行保证生命周期。
4. 内存屏障：`__sync_*` 已淘汰，用 `stdatomic.h`（C11）`atomic_*` 与显式 memory_order。
5. futex 是用户态/内核态混合等待的原语（mutex/semaphore 底层），争用分析时须知道其唤醒代价。

## 适用边界

- 具体选项（如 `PTHREAD_MUTEX_ADAPTIVE_NP`、glibc 版本行为）属须确证项，须查对应实现文档。

- 返回 [references](../references.md) · [死锁四条件与破坏](../理论基础/死锁四条件与破坏.md)
