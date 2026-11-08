# 检查点（feature playbook，t225）
| 步骤 | 状态 | 说明 |
|---|---|---|
| 1 how | 做了 | 读 14 人代表作品卡 id、标题、一手链接 |
| 2 architect | 跳过：单 owner | Codex 只读审查复核 |
| 3 throughput | 做了 | 数据 → 生成器 → 重建 → 测试 |
| 5 验证 | 做了 | test_growth 21、旧回归 4 套、check_generator、layout 16 视图 |
| 5b Codex | 做了 | 4 条 P2 全修，见 review.md |
| 6 提交 | 做了 | |

| 原则 | 读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 对标条目统一 {pid, work(锚点), title, did, src, learn, skip}；人物摘要 work 与首页对标同一 id，测试断言锚点真实存在、来源出现在人物页 | 做了 |
