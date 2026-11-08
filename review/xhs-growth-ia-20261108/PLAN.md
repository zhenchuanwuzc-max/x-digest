# 人物成长研究 · 信息架构与迁移清单（t222，2026-11-08 UTC+8）

## 盘点（真实生成路径）
| 产物 | 生成方式 | 旧问题 |
|---|---|---|
| xhs/growth/index.html | 仓库内 xhs/growth/src/build_index.py ← people.json | 卡片墙+长描述，偏“一堆” |
| xhs/creators.html | 共享 /workspace/digests/xhs_library.py::sync_creators ← /workspace/money/ai-creators-growth.html，日常 build() 每天重写 | 所有人+分类+结论的大合集，第二个首页 |
| xhs/{kazike,zhangzala,baoyu,guizang,qiaomu,huashu,fankai,hector}.html | 静态产物；review/creator-growth-20261108/build_*.py（creator_page_lib / build_kazike；zhangzala 生成器在仓库外 /workspace/xhs-ui-20261108） | 侧栏顶部带“小红书全入口 + 对标档案（合集锚点）” |
| xhs/growth/hector.html | 静态（播客全文对照） | 已是独立内容，顶部返回链接 |
| xhs/index.html 内 #profiles/#growth | 共享 xhs_library.py（小红书创作中心，非本模块） | 指向 creators.html 合集 |
| research/ai-depth-levels-2026-10-28.html | 研究站，非本模块 | 只引用，不改 |

## 目标架构
- 首页（唯一）xhs/growth/：①跨人物结论（短，观察/建议标清，出自原 creators #verdict 与 #takeaways）②14 人导航 ③专题导航。
- 人物页（14）：8 个原页 + 6 个新页 xhs/{lenny,shreyas,ali,swyx,levelsio,justinwelsh}.html（从共享源对应 h2 段切出，原 id 不变）。侧栏只有本页目录 + “← 人物成长研究”。
- 专题页（4）：xhs/topic-types.html（按类型对标 + 小红书可抄 5 条 + 来源与局限）、xhs/topic-lip-growth.html（learn-in-public 怎么涨与变现）、xhs/growth/hector.html（播客全文对照，原样）、research/ai-depth-levels（引用）。
- xhs/creators.html → 最小兼容页：每个旧 id 一行静态链接到新位置（同名锚点），不含正文。
- 单一元数据源：xhs/growth/src/people.json（total/people/topics）；切分规则 xhs/growth/src/split_creators.py（仓库内版本化），共享 sync_creators 只调用它。

## 迁移清单（旧 → 新）
| 旧 | 新 |
|---|---|
| creators.html#verdict | growth/#total（提炼） |
| #takeaways #pm #career #tools #lip #bigco #ai #sources | topic-types.html#同名 |
| #lip-growth | topic-lip-growth.html#lip-growth |
| #lenny… #justinwelsh 及其子锚点 | {id}.html#同名 |
| #kazike #guizang #huashu #baoyu #qiaomu #fankai（含子锚点） | 对应 {slug}.html（已按一手资料重写的独立页） |
| #zara（含子锚点） | zhangzala.html |
| #overseas | growth/#people |
| Lenny 素材池（xhs/#lenny，小红书创作中心资产） | 不列为成长研究专题；Lenny 人物页内给明确外链 |

## 有意不迁移
- creators 源里 7 位中文作者的旧版深描段：已被 2026-11-05~08 一手资料重写页取代，不再对外渲染；原文仍在共享源与 git 历史，兼容页锚点指向新页。
- 原 h1/引言：属于旧合集首页框架，删除。
