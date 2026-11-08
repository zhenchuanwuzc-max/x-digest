# 检查点（feature playbook，t227–t229）
| 步骤 | 状态 | 说明 |
|---|---|---|
| 0 技能 | 做了 | 重新加载最新 creator-growth-analysis（“不为所有人硬凑相同作品数”“证据是否覆盖核心结论”）；未改技能 |
| 1 how | 做了 | 导出 14 人全部作品卡池（t227/works-pool.txt，仓库外） |
| 2 architect | 跳过：单 owner | Codex 只读复核 |
| 3 throughput | 做了 | 数据 → page_kit/build_index → 全量重建 → 测试 |
| 5 验证 | 做了 | test_growth 21、旧回归 4 套、check_generator、layout 8 页×390/1280/1440（含对比表行高不留大空白）并人工看截图 |
| 5b Codex | 见 review.md | |
| 6 提交 | 做了 | |

| 原则 | 读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 一件事 = 一张作品卡 {id,title,step,edge,src}，首页只引用 id，不另写一份；对比表以字段为列 | 做了 |
