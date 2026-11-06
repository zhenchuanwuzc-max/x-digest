# 2026-11-06 产品机会

读者要在现有产品榜上看到每个前五名的国内机会，并能点进一份独立报告。最小改动是给这一天的十张卡片加一段分析，并生成十个静态页。

## 核对

GitHub 热榜默认打开的是「本周涨星」`#jm-ghw`。前五名与任务列出的仓库一致。

AI 产品榜单默认选中的是「周」。日榜在 `#jm-phd`。周榜显示序前五是 beacon.sh、Wanaka Studio、Floot Payments、Glasshand、Pushary for Teams。日榜前五仍是 Glasshand、Pushary for Teams、Maritime、Clocknext、Rerun。重叠的两份报告同时给出周榜和日榜入口。月榜不写。默认选中的周榜没有改。

## 形状

一份快照数据。脚本只在页面含有「更新于 2026-11-06 06:18（北京时间）」时写入。卡片还要同时对上显示序和原链接。对不上就失败，不把这段话安到别的产品上。再跑一次得到同一结果。

仓库里没有日更生成器。`INTEGRATION.md` 是给站外生成器接上的命令，目前没有任务在调用它。

## 不做

不改 `xhs/`。不改周榜和月榜。不把星数或票数写成用户数。不执行 dsh-purge，报告里不引用提示词。

## 环境

仓库没有 `AGENTS.md`。没有 `pstack-dev-rules`、`dev-collab-efficiency`，也没有 `/workspace/pstack-enforce/pstack-check`。这些检查没有跑。`deslop` 技能不在本环境。
