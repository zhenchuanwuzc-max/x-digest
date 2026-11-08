# 检查点（feature playbook；开工前写，2026-11-08 18:5x UTC+8）
| 步骤 | 状态 | 说明 |
|---|---|---|
| pstack 初始化 | 做了 | pstack-models.toml 存在 |
| 1 how | 做了（手工） | 读 sync_creators、build_index、creator_page_lib、8 页侧栏、creators 段结构，见 PLAN.md 盘点 |
| 2 architect | 跳过：未开并行设计探索 | 本机单 owner，方案见 PLAN.md；以 Codex 只读审查作设计复核 |
| 3 throughput | 做了 | 阻塞：先写 split+兼容页；独立：8 页侧栏修正；共享写：共享源/生成器只由父 bot 合并后同步；最小分解：单 owner（耦合同一元数据） |
| 4 委派实现 | 不适用：本身是子代理不可再派 | 自己持有 diff，Codex gpt-6.1-sol read-only 做审查分离 |
| 5 真实表面验证 | 做了 | test_growth 12 项、check_generator、旧回归（test_xhs_shell、test_creator_pages、迁移后 test_batch4）、7 页×390/1440 无横溢 |
| 6 有序提交 | 做了 | 470bd27 架构迁移 → 审查修订提交 |
| 7 interrogate | 不适用：无争议方案 | |
| 8 Opening a PR | 父 bot 开/合并 | |

| 原则 | 读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 人物/专题/结论只在 people.json；旧锚点迁移规则是一张表（split_creators.ROUTES），不散落 if | 做了（已验证） |
| principle-separate-before-serializing-shared-state | 已读 | 不在开发中写共享源/共享生成器；只写分支副本，合并后由单一步骤同步 | 做了（已验证） |
| principle-sequence-verifiable-units | 已读 | 每步后跑 test_index/test_split 再进下一步 | 做了（已验证） |

## Codex 只读审查（gpt-6.1-sol）
高/中 0；低 1：首页结论来源说明称 verdict 现存于专题，不准确 → 已改为“原文在共享源与 git 历史”。原始日志仓库外 growth-nav/codex-ia-review.log。

## 复盘
- 本轮开工前写 PLAN/检查点并跑 pstack-check（通过，见 pstack-check-start.txt）；architect/委派按实际情况标跳过/不适用。
- 下次：8 个人物页生成器里有一个在仓库外（zhangzala），应纳入仓库。
