# t223 + t224 计划（2026-11-08 19:2x UTC+8）
- 定位依据：小红书创作中心「定位」段（xhs/index.html#pos）：大厂产品经理，讲进门后如何把活干好；三支柱 AI实操 · Lenny产品方法 · 大厂日常；不求职、不编数字、第一人称只用 Ocean 原话。账号名「AI具身牛马」见张咋啦页。记忆库检索（home-macpro）超时未返回，未据记忆补充。
- 数据：X 关注者 2026-11-08 19:14 UTC+8 公共读取 14 人；收入/小红书/公众号只取各人物页已核来源 + 本轮 X 检索（近一月窗口，结果见 search-*.txt 摘录）；无可核写「未找到公开数值」。
- 元数据单源 people.json 扩展：does/users/x/xhs/wx/income（各带 src+date+kind）+ brief（面向谁/痛点/本人怎么解/Ocean 可做）+ actions（首页结论表）。
- 生成：build_index 首页（结论表+行动顺序 / 14 卡统一字段 / 专题）；xhs/growth/src/page_kit.py 统一 brief 注入与跨页链接新标签；split_creators 与 8 个人物页生成器都调用它；播客页（静态）原地处理；xhs_library 副本里入口链接新标签。
- 测试：14 卡字段齐全、未知状态、来源链接；14 页摘要存在且位于正文前；跨页 blank + noreferrer、页内锚点不 blank；原文保留（去导航/摘要/target-rel 后与基线一致）；生成一致；旧回归；390/1440。
