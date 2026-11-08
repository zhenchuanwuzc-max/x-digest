# xhs/growth 按人名单入口 · 检查点表（refactoring playbook）

> 真实状态记录：首个提交 840a306 之前**没有**加载原则、没有写本表、没有跑 pstack-check、没有 Codex 审查（漏做，不补称开工前通过）。以下为 2026-11-08 18:41（UTC+8）起补做后的状态。

| 步骤 | 状态 | 说明 |
|---|---|---|
| pstack 初始化 | 做了 | 仓库根有 pstack-models.toml |
| 1 Pin 行为契约（how） | 做了（补） | 未单独加载 how 技能；直接读了旧 index.html 全文与引用它的 nav_merge/xhs_library/apply_xhs_shell；契约=14 人可达、旧链接可解析、#people 锚点、Hector 播客与 Lenny 素材可达，写入 src/test_index.py；旧页备份在仓库外 growth-index-before.html |
| 2 领域结构 | 做了 | 人物名单 = 一份 people.json（数据），页面由生成器渲染 |
| 3 目标形状（architect） | 不适用 | 单文件生成器，不跨模块边界，未开 architect |
| 4 先减后加 | 做了 | 删掉旧四类抬头和重复 Hector 卡、废弃 a.card hover CSS |
| 5 小步迁移 | 做了 | 调用方：xhs/index.html 入口说明 + 共享生成器同一行同步；nav_merge 的 xhs/growth/ 链接不变 |
| 6 真实产物证明 | 做了 | test_index.py 8 项、check_generator.py、test_xhs_shell、test_creator_pages、390/1440 截图 |
| 7 读者负担 | 做了 | 左栏 14 个名字、无混杂；名单一处维护 |
| 8 提交/Opening a PR | 做了（不开 PR，由父 bot 合并） | |
| Codex 只读审查 | 做了（补） | 见 codex-review.md |

| 原则 | 读 | 落实动作 | 结果 |
|---|---|---|---|
| principle-model-the-domain | 已读 | 名单只在 people.json，页面无手写人物分支；测试比对 nav/卡片顺序=名单顺序 | 做了 |
| principle-foundational-thinking | 已读 | 先定 people.json 字段（id/name/href/go/extra）再写渲染 | 做了 |
| principle-redesign-from-first-principles | 已读 | 按“按人名唯一入口”重做整页，同步 xhs 入口说明与共享生成器，不在旧分类上加一栏 | 做了 |
| principle-subtract-before-you-add | 已读 | 删旧分类抬头、重复 Hector 卡、无用 a.card hover 规则 | 做了 |
| principle-laziness-protocol | 已读 | 人数从 people.json 取，共享生成器只改一行+一个小函数；check_generator 证明只差一行 | 做了 |
| principle-migrate-callers-then-delete-legacy-apis | 已读 | 测试改为断言新契约（每人一个主链接、旧 URL 可解析），删“旧 href 必须出现在页上”的旧断言 | 做了 |
| principle-prove-it-works | 已读 | 可重跑脚本 test_index.py / check_generator.py + 浏览器截图 | 做了 |
| principle-minimize-reader-load | 已读 | 左栏只剩人名；README 式页脚指明名单源与生成器 | 做了 |
| principle-sequence-verifiable-units | 已读 | 每次改动后先重跑 test_index 再进下一步；提交顺序：首版 → 审查修订 | 做了 |
