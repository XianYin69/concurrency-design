# dependence（依赖声明）

本技能**不内嵌**其他技能内容；能力经声明依赖获得。每行一条 `名称 | 类型 | 来源`，
类型为 skill|software|repo。SMS 安装时对本目录条目与本体做同样检查与净化。

```
file_ops          | skill    | local:skill_manage_system
code-guidelines   | skill    | local
pavedpath-code    | skill    | local
python            | software | system
git               | software | system
```

## 用途映射

| 依赖 | 承担能力 | 触发节点 |
|---|---|---|
| file_ops | 联网搜索/抓取（ff_lite.py search/fetch·须 :grant network） | 经验查询 / 浏览器学习 / 知识库构建 |
| code-guidelines | 命名、注释、复杂度、坏味道准则 | 脚本构建 / 整体审查 |
| pavedpath-code | 已验证实现路径与脚手架范式（线程池/管道/工作窃取） | 大纲构建 / 分支分析 / 脚本构建 |
| python | 脚本运行时、threading/asyncio 与测试执行器 | 脚本构建 / 构建测试 |
| git | 功能分支→dev→main 版本流 | 每步收尾（见 git 工作流约束） |

## 并发运行时与工具链（外部软件·非内嵌）

按需声明，不在本技能正文复制其文档：Java（`java.util.concurrent` / JMM / Virtual Threads）、
C++11+（`<thread>` `<atomic>` `<mutex>`）、POSIX threads、Go（goroutine/channel）、
Rust（`std::sync` / tokio）、Python（threading / asyncio / multiprocessing / trio）、
.NET（TPL / async-await）；检测工具 TSan / Helgrind / DRD / JCStress / racecheck。
未安装即视为依赖缺失，走降级不静默。

## 规则

1. 依赖缺失时**降级不得静默**：记 process_chain interrupt 并向用户报告缺项，禁止伪造能力。
2. 禁止把依赖技能正文复制进本技能目录（薄技能原则）；只允许引用其名称与调用方式。
3. 新增/删除依赖须走 update 审批流并记 CHANGELOG。
4. 语言/库的内存模型与 API 语义属**须确证知识**，一律经浏览器学习取证，不凭记忆断言。

- 返回 [SKILL.md](../SKILL.md) · [薄技能依赖约束](../resistance/薄技能依赖约束/薄技能依赖约束.md)
