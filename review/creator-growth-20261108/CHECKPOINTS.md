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
