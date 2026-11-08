| 步骤 | 状态 | 说明 |
|---|---|---|
| pstack 初始化 | 做了 | 仓库根 pstack-models.toml |
| playbook | 做了 | feature |
| 同 worktree 写手 | 做了 | 无 build/codex 进程；wt 干净，新分支自 6f5239c |
| 草稿整合为正式内容 | 做了 | 仓库外 analysis/FINAL.md；三份追加稿保留作过程记录 |
| 数据+生成器+页面 | 做了 | follow_b1_cards.py（覆盖度唯一来源）、add_follow_b1.py、build_{lulu,laoa,karl}.py、export_follow_b1_ledgers.py（脱敏台账副本） |
| 测试/布局/Codex | 做了 | 全部测试过（growth 29）；重建幂等、其它 builder 无 diff；390/1280/1440 无溢出；Codex 5 条：4 改 1 交父级 |
| 最后 6 卡并入 → 冻结 | 做了 | final-gap-ledger 6 张截图逐张核对后并入；老A 29/29、Karl 32/32 |

| 原则 | 已读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 图卡覆盖度用 {total,read,partial,missing} 数据结构生成文字与状态，测试按数据断言不得称完整；人数动态 | 做了 |

## 复盘
- 做了：覆盖度做成数据后，补卡只改一处，“待补”文字自动消失、测试按数据断言。
- 下次改：首轮把 {1–3,7,9–14} 手算成 9 张——之后页数一律由集合计算；台账 ledger 描述与截图不符两处，以截图为准，核对要逐张。
