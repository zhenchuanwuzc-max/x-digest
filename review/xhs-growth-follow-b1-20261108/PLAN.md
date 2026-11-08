# 人物 16–18：小红书关注首批（Lulu的AI野路子 / 老A的AI进阶实操 / Karl的AIGC产品丨光之年）
依据：Ocean t232（关注里粉丝>1万都纳入）、t233（视频只看标题和描述，图文看全）、t235（空白要重试）、t237（完整的都做完）。
证据（repo 外）：/workspace/creator-growth-20261108/following-batch1/{lulu,lao-a-jin-jie,karlaigc}/ledger.md + supplement-ledger.md + 截图；私有草稿 analysis/。
## 设计
- 覆盖度建模为数据：每篇作品 cards={total, read, partial, missing, blank}，页面“已读几页/缺哪页”由此生成，测试断言未读完的作品不出现“全读/完成”。
- 每人一个 builder（creator_page_lib，与 zhixin 同链），add_follow_b1.py 统一往 people.json 增 3 人（可重复运行）。首页对比表加 3 行、X/公众号/收入 未找到+未核。
- 公开页不写：Ocean 关注关系/账号、研究名单、带 xsec_token 的 URL。
- 两个老A分开；Karl 与老A课程大纲相似只写观察。课程/offer 是自述，不当收入或交付。
## 冻结条件
最后 6 卡（老A Skills p2；Karl 课程 p4；Karl Agent p4 下半/p5/p6/p8）证据到达并并入后才 commit/push 冻结；未到则报告状态。
