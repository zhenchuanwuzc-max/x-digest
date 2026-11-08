# 成长人物全量清单与分批（2026-11-08 UTC+8）
父 bot 说的“20 人”和实际盘点对不上。实际情况：
- 成长入口（xhs/growth/index.html）直接链接 9 人：卡兹克、张咋啦、歸藏、花叔、范凯说 AI、宝玉、向阳乔木、Hector Serrano，以及档案里的 Lenny。
- 对标档案（xhs/creators.html）另有深描 5 人：Shreyas Doshi、Ali Abdaal、swyx、Pieter Levels（levelsio）、Justin Welsh。
- 档案分类表里还有大约 30 个只列名字或一行简介的账号，不算在本次范围内。
本次范围：除张咋啦外 13 人（入口 8 人 + 档案深描 5 人）。要不要把分类表里的账号也算进来，请 Ocean 确认。

| 批次 | 人物 | 页面 | 本地已有资料 | 一手资料可行性 | 状态 |
|---|---|---|---|---|---|
| 1 | 卡兹克 | xhs/kazike.html | 旧深拆页，链接多 | X（API）+ 公众号原文可读 | 完成（X 一手资料深化；小红书未核） |
| 2 | 宝玉 | xhs/baoyu.html | 薄页 | X @dotey、博客 baoyu.io 可读 | 完成（X 一手资料深化；小红书未核） |
| 2 | 歸藏 | xhs/guizang.html | 薄页 | X @op7418、周刊站可读 | 完成（X 一手资料深化；小红书未核） |
| 2 | 向阳乔木 | xhs/qiaomu.html | 薄页 | X @vista8、qiaomu.ai 可读 | 完成（X 一手资料深化；小红书未核） |
| 3 | 花叔 | xhs/huashu.html | 薄页 | X @AlchainHust、huasheng.ai | 待做 |
| 3 | 范凯说 AI | xhs/fankai.html | 薄页 | X @fankaishuoai；小红书是主平台，受限 | 待做（小红书缺口大） |
| 3 | Hector Serrano | xhs/growth/hector.html | 播客全文对照，内容很多 | 播客原文已有；X 账号待确认 | 待做 |
| 4 | Lenny | creators.html#lenny | 档案专节 | X、Newsletter 可读 | 待做；页面在生成器管理的档案里，需先定放在哪 |
| 4 | Shreyas / Ali / swyx / levelsio / Justin Welsh | creators.html 各专节 | 档案深描 | X 和各自网站可读；多数没有小红书账号（待确认） | 待做；同上 |

## 生成源检查
- xhs/creators.html 由 /workspace/digests/xhs_library.py --sync-creators 从 /workspace/money/ai-creators-growth.html 生成，直接改会被覆盖。第 4 批要先决定是改生成源，还是给这些人建独立页（需要 Ocean 同意）。
- kazike.html、baoyu.html 等独立页和 growth/index.html 没有生成器引用（用 rg 查过 xhs_library.py 和 xhs_day_build.py），可以直接编辑。本批没改任何生成器或 routine。

## 验收口径调整（2026-11-08 17:32 UTC+8，Ocean t219）
“大部分人都是一份双发的，所以X有就够了。”X 本人原帖 + 作品一手资料足够；缺小红书不再算未完成，但每页都写“小红书未核”，不据此判断小红书效果，只有确证才标双发。

## 剩余 9 人下一批顺序
1. 第 3 批：花叔 → 范凯说 AI（X 为主，小红书未核即可）→ Hector Serrano（先确认 X 账号；播客原文已有）。三页都是独立页，可直接改。
2. 第 4 批：Lenny → Shreyas Doshi → swyx → levelsio → Justin Welsh → Ali Abdaal。都在生成器管理的 creators.html 里，开工前要 Ocean 定：改生成源 /workspace/money/ai-creators-growth.html，还是给每人建独立页。


## 第三批状态（2026-11-08 UTC+8）
- 花叔 xhs/huashu.html、范凯 xhs/fankai.html、Hector xhs/hector.html（新深拆页；播客对照保留 xhs/growth/hector.html）：完成，X 一手资料深化，小红书未核。
- Codex 只读审查 14 条（高 3、中 11）全部已改，摘要见 codex-review-batch3.md。

## 第四批（下一批，等父 bot 合并部署后再开工）
Lenny、Shreyas、Ali Abdaal、swyx、levelsio、Justin Welsh：改生成源 /workspace/money/ai-creators-growth.html 对应段落，再重建 xhs/creators.html，保持锚点。

## batch4 (2026-11-08)
Lenny / Shreyas Doshi / Ali Abdaal / swyx / levelsio / Justin Welsh：review/creator-growth-20261108/batch4/（源副本、构建脚本、6 份台账、网页摘录、测试、布局检查、Codex 摘要）。
