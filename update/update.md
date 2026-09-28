# update（自更新审批流）

技能本体与约束的修改须经此接口审批，防止自我改写失控。

## 审批范围

- `resistance/` 任意约束的新增/修订；
- `SKILL.md` 红线与流程节点增删；
- `dependence/` 依赖项变更；
- `scripts/` 机制脚本行为变更。

## 流程

1. 提案：在 tmp 写 `update-proposal.md`（改什么、为什么、影响面、回滚方案）。
2. 辩论：`python -B scripts/logic_chain.py debate --pro <支持> --con <反对>`。
3. 审批：结论记逻辑链；涉及删除既有约束 → 必须用户当轮确认 + grant danger。
4. 实施：功能分支提交，走 [git工作流约束](../resistance/git工作流约束/git工作流约束.md)。
5. 登记：`CHANGELOG.md` 记版本、日期、变更条目与违规后果。
6. 比对：`python -B scripts/self_update.py report` 与 `compare` 确认释放一致。

## 禁止

- 未经审批直接改 resistance/（红线：不得删除约束）。
- 一次提案夹带多项无关变更（无法回滚）。

## 相关

- [约束编写节点](../branch/流程/约束编写/约束编写.md) ·
  [收尾节点](../branch/流程/收尾/收尾.md) · [resistance](../resistance/resistance.md)
