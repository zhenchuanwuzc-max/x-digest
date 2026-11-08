# 检查点（feature playbook）· 成长人物第 1 批
| 步骤 | 状态 | 说明 |
|---|---|---|
| 1 how | 做了 | 通读 zhangzala.html 全部结构、CSS、旧留档；确认没有生成器写这个页面（rg 生成器无引用） |
| 2 architect | 做了 | t206 已比较两个方案；Ocean 选了 B（独立成章），不再重复探索 |
| 3a 阻塞前置 | 做了 | fetch 后 main=origin/main=9c711ed，工作区干净，单写手；先写钉住测试 |
| 3b 独立工作流 | 不适用：单文件页面，没有可并行的不相交文件 |
| 3c 共享可变状态 | 做了 | 只有一个写手写 zhangzala.html；Codex 审查用 read-only，不写文件 |
| 3d 最小分解 | 做了 | 一个写手最合适：单文件内容重排，拆开反而要合并冲突 |
| 4 委派实现 | 做了 | 本 executor 子代理自己负责 diff，Codex sol 只读审查，审查和实现分开（playbook 允许子代理自己负责 diff） |
| 5 在对应界面验证 | 做了 | 本地 file:// 用 Playwright 量 390/1440 宽度，加结构测试 |
| 6 小提交有序 | 做了 | 测试和计划一个提交，页面一个提交，审查修复一个提交 |
| 7 interrogate | 不适用：设计已由 Ocean 明确确认，没有争议 |
| 8 Opening a PR | 做了 | 推分支，PR 文案交父 bot 用 GitHub 工具创建；不推 main，不自动合并 |

| 原则 | 是否已读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 6 张卡用一张 WORKS 表加一个渲染函数；证据层级固定 5 种标签 | 做了：build.py 里的 WORKS 表 |
| principle-sequence-verifiable-units | 已读 | 先在旧页上跑测试看到红，再改页面看到绿；每个提交单独验证 | 做了：见 verify.out |
| principle-separate-before-serializing-shared-state | 已读 | 单写手；审查只读；预览导出到仓库外目录 | 做了 |
| 第2批 | 宝玉/歸藏/乔木 页面+台账+测试+布局+Codex 审查 | 完成 2026-11-08 |

## 关注第二批（2026-11-08 23:10 UTC+8，分支 xhs-growth-follow-b2-20261108 自 main f58a3e2）
- [x] 4 人：老A的AI研究所（3 图文 37 页）、杰森的效率工坊（图文 10/10、7/7 + 视频标题描述）、Accio Work（图文 8/8、1/1 + 视频标题描述；品牌号）、知危（2 视频，标题描述层）。
- [x] 覆盖度唯一来源 follow_b2_cards.py；人物数据 add_follow_b2.py；公开台账 export_follow_b2_ledgers.py（去 token、采集账号、关注关系行）。
- [x] 首页每方向最多 3 位重点对标人已满，第二批只进人物名单，不挤进方向。共享生成器不改（0ecd4a60 已数据驱动），入口人数 22。
- [x] Codex：“视频未播放”与自动播放不符 → 改“未主动播放、未观看”；可见评论误放“假设”格 → 移到事实格；“至少 3 位读者”→“至少 3 处”。均已修并加回归。
- [x] 全量重建幂等；7 套测试过；首批页、七步、日常选题无 diff；390/1280/1440 无溢出。
