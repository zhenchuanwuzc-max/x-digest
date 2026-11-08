# 成长人物全量清单与分批（2026-11-08 UTC+8）
父 bot 说的“20 人”和实际盘点对不上。实际情况：
- 成长入口（xhs/growth/index.html）直接链接 9 人：卡兹克、张咋啦、歸藏、花叔、范凯说 AI、宝玉、向阳乔木、Hector Serrano，以及档案里的 Lenny。
- 对标档案（xhs/creators.html）另有深描 5 人：Shreyas Doshi、Ali Abdaal、swyx、Pieter Levels（levelsio）、Justin Welsh。
- 档案分类表里还有大约 30 个只列名字或一行简介的账号，不算在本次范围内。
本次范围：除张咋啦外 13 人（入口 8 人 + 档案深描 5 人）。要不要把分类表里的账号也算进来，请 Ocean 确认。

| 批次 | 人物 | 页面 | 本地已有资料 | 一手资料可行性 | 状态 |
|---|---|---|---|---|---|
| 1 | 卡兹克 | xhs/kazike.html | 旧深拆页，链接多 | X（API）+ 公众号原文可读 | 本批完成（初步深化：小红书待补） |
| 2 | 宝玉 | xhs/baoyu.html | 薄页 | X @dotey、博客 baoyu.io 可读 | 下一批 |
| 2 | 歸藏 | xhs/guizang.html | 薄页 | X @op7418、周刊站可读 | 下一批 |
| 2 | 向阳乔木 | xhs/qiaomu.html | 薄页 | X @vista8、qiaomu.ai 可读 | 下一批 |
| 3 | 花叔 | xhs/huashu.html | 薄页 | X @AlchainHust、huasheng.ai | 待做 |
| 3 | 范凯说 AI | xhs/fankai.html | 薄页 | X @fankaishuoai；小红书是主平台，受限 | 待做（小红书缺口大） |
| 3 | Hector Serrano | xhs/growth/hector.html | 播客全文对照，内容很多 | 播客原文已有；X 账号待确认 | 待做 |
| 4 | Lenny | creators.html#lenny | 档案专节 | X、Newsletter 可读 | 待做；页面在生成器管理的档案里，需先定放在哪 |
| 4 | Shreyas / Ali / swyx / levelsio / Justin Welsh | creators.html 各专节 | 档案深描 | X 和各自网站可读；多数没有小红书账号（待确认） | 待做；同上 |

## 生成源检查
- xhs/creators.html 由 /workspace/digests/xhs_library.py --sync-creators 从 /workspace/money/ai-creators-growth.html 生成，直接改会被覆盖。第 4 批要先决定是改生成源，还是给这些人建独立页（需要 Ocean 同意）。
- kazike.html、baoyu.html 等独立页和 growth/index.html 没有生成器引用（用 rg 查过 xhs_library.py 和 xhs_day_build.py），可以直接编辑。本批没改任何生成器或 routine。
