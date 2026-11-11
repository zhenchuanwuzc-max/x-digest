# xhs 热帖互动门槛 · feature 检查点表
日期: 2026-11-10 (Asia/Irkutsk)
playbook: feature
目标: 日报/入口只把达标互动帖当热帖；去掉「新帖、小号优先」；修入口昨日未确认块压今天；合并 PR47 上线

## Throughput checkpoint
| 维度 | 状态 | 说明 |
|---|---|---|
| Blocking first steps | 做了 | 先读生成器/日数据/PR47；写门槛单源；再改渲染与日页 |
| Independent workstreams | 不适用：原因 | 共享生成器与日 HTML 同源，不宜并行双写 |
| Shared mutable state | 做了 | 单一门槛模块；日 JSON / hub 生成串行；site-repo 单分支写 |
| Smallest safe decomposition | 做了 | 一人改完：门槛模块 → 生成器 → 日数据重建 → 测试 → PR |

## 原则（playbook 点名）
| 原则 | 已读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-separate-before-serializing-shared-state | 已读 | 门槛规则独立成 xhs_hot_gate.py；site-repo 单 worktree 写 HTML，不双开写手 | 做了 |
| principle-model-the-domain | 已读 | 用 age_band + likes/collects 判定函数编码门槛，避免散落 if；日页 hot/watch 分区 | 做了 |
| principle-sequence-verifiable-units | 已读 | 先单测门槛 → 再改渲染 → 再改日 JSON → 重建 → 全量相关测试 → PR → 线上核对 | 做了 |
| principle-laziness-protocol | 已读 | 不重写整套 new-small 流水线；入口去掉注入；日页 hot_first 加规则句与观察中折叠 | 做了 |

## 步骤
| 步骤 | 状态 | 证据 |
|---|---|---|
| 1 how 子系统 | 做了 | 已读 xhs_library._daily_new_small / _new_small_v2 / render 注入；xhs_day_build.build_hot_first_body；日 JSON |
| 2 architect | 跳过 | 方案单一：门槛单源 + 去注入 + 日页分区；无多形态需 arena |
| 3 实现 | 待做 | |
| 4 验证 | 待做 | |
| 5 Opening a PR | 待做 | |
| 6 合并上线与线上核对 | 待做 | Ocean 已授权网站改动直接上线 |

## 收口
| 步骤 | 状态 | 证据 |
|---|---|---|
| 实现 | 做了 | PR #48 squash b811ebf |
| 验证 | 做了 | 单测全绿；线上 hub/day/11-09/11-10 已核 |
| Opening a PR | 做了 | https://github.com/zhenchuanwuzc-max/x-digest/pull/48 |
| 合并上线与线上核对 | 做了 | 2026-11-10 09:20 UTC+8 拉线上通过；#47 已关 |
