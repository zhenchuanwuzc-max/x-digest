# 张咋啦页：作品拆解独立成章（t206，方案 B，Ocean 已确认，2026-11-08 UTC+8）
设计确认：Ocean 回答确认卡 t206s832，原话「时间线后单独放作品拆解，再接对照表和语气节奏。」
基线：main 9c711ed；分支 xhs-zhangzala-works-20261108；单一写手（box 上没有 codex 或其他 git 写进程，只有一个 worktree）。
范围：只改 xhs/zhangzala.html 和本目录。Lenny、其他人物页、每日 routine、生成器都不碰。

## 页面顺序
overview → timeline(s1–s5) → #works（6 张卡 w1–w6）→ #compare → #voice → #limits → #for-ocean → #sources
删掉：#archive 及其下全部内容（old-milestones、old-breakout、pieces、x-top、viral、appendix）。

## 数据形状（principle-model-the-domain）
每张卡是一条记录：{id, 标题, 链接[], 时间线位置, 事实, 自述?, 观察, 假设, 边界, 可借鉴}，在 build.py 里用一张 WORKS 表表达，由一个渲染函数统一输出。证据层级只有 5 种标签（事实 / 自述 / 观察 / 假设 / 边界），不散写在各段文字里。

## 步骤（每步验证后再进下一步）
1. 写 test_zhangzala.py：钉住新结构（顺序、id、锚点、删除项、禁用数字、6 卡有链接和层级）。在旧页上跑，应该红。
2. build.py 从 9c711ed 页面生成新页。跑测试，应该绿；再跑 xhs/test_xhs_shell.py 全量。
3. 用 Playwright 在 390 / 1440 宽度做本地 file:// 布局检查：页面无横向滚动，对照表在小屏转成卡片。
4. 提交：先提交 review 文件（测试和计划），再提交页面。
5. 本地 Codex（gpt-6.1-sol，只读）做一次静态内容和布局审查 → 修复 → 复测。
6. 推分支，导出预览目录，准备 PR 文案（由父 bot 开 PR）。

## 第 2 轮（t207/t208，Ocean 授权补充，不上线）
在 #works 和 #compare 之间加 #audience「谁在看，为什么愿意看」。顺序测试、目录（桌面和手机）、390 宽度小屏卡片检查同步更新。
