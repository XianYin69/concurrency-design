# 事件循环与 async/await

来源：[本地]（未联网确证）· 用途：判断 IO 密集场景是否用异步模型。

## 模型要点

- **单线程事件循环 + 非阻塞 IO**（libuv/epoll/kqueue/IOCP）：并发靠「等待时让出」而非多线程。
- `async/await` = 状态机糖：挂起点必须显式；未 `await` 的 promise/task 是**静默失败**主因。
- 并发原语：`gather`/`when_all`/`Task.WhenAll`、`wait_for`/`any`、信号量限并发、超时与取消。
- Python 特有：GIL 使 CPU 并行无效；`asyncio` 中调用阻塞函数会卡住整个循环 →
  须 `to_thread`/专用执行器隔离。

## 高频结论

1. **不要在事件循环线程里做阻塞操作**（磁盘、DNS、同步 HTTP、`time.sleep`）—— 一处阻塞，全体停摆。
2. 取消语义：`CancelledError`（Python）/`stop_token`/`CancellationToken` 必须向上传播，
   `except Exception` 会误吞取消（Python 3.8+ `CancelledError` 继承 `BaseException`）。
3. 背压：异步管道须有界队列；无界 = 内存换延迟。
4. 混合模型（async + 线程池）时，跨边界传递取消与异常最容易漏，须显式桥接。
5. 观测：循环延迟（lag）、待处理回调数、连接数、队列深度。

## 适用判据

- 连接多、每连接计算少 → 事件循环；计算重 → 线程/进程池或工作窃取；两者皆有 → 分层（异步接入 + 计算池）。

- 返回 [references](../references.md) · [取消与超时模式](../实践模式/取消与超时模式.md)
