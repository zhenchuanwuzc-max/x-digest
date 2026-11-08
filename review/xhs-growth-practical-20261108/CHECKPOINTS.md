# 检查点（feature playbook，t223 + t224 合并批）
| 步骤 | 状态 | 说明 |
|---|---|---|
| pstack 初始化 | 做了 | pstack-models.toml |
| 1 how | 做了 | 读 build_index/split_creators/creator_page_lib/build_kazike/zhangzala build、各人物页数字段落 |
| 2 architect | 跳过：单 owner 无并行设计 | Codex 只读审查作复核 |
| 3 throughput | 做了 | 阻塞：数据台账→people.json；独立：page_kit（摘要注入 / 新标签）；共享写只在合并后 |
| 4 委派 | 不适用：子代理不可再派 | 自持 diff + Codex 审查 |
| 5 验证 | 做了 | test_growth 21 项、test_xhs_shell、test_creator_pages、test_zhangzala、test_batch4 全过；check_generator OK；layout_check 8 页×390/1440 OK |
| 5b Codex 只读审查 | 做了 | 3 条 P2 全修：乔木证据拆开并标第三方稿；卡片显示全部口径；行动顺序标「建议」。日志在仓库外 growth-nav/codex-t223.log |
| 6 提交 | 做了 | 本分支 xhs-growth-practical-20261108 |
| 8 PR / 合并 / 部署 | 父 bot | 见 DEPLOY-STEPS.md |

| 原则 | 读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 指标统一 {text,kind,src,date,note}，kind 枚举 事实/自述/未找到；未找到文字固定「未找到公开数值」；测试按枚举校验 JSON 和页面可见标注 | 做了 |
