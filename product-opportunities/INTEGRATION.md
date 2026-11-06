# 接入日更

研究数据是按日期分开的 JSON。渲染脚本按产品原链接把分析挂到当天 HTML 上。研究流程只新增或修改 `product-opportunities/research/YYYY-MM-DD.json`。它不改 Python，也不改页面结构。公开的 JSON 仍然走 PR，合并之后发布脚本才能读到。

`jm-ghw` 是 GitHub 热榜的本周涨星。`jm-ph` 是 AI 产品周榜。`jm-phd` 是 AI 产品日榜。月榜不在这三栏里。

## 研究文件

字段说明在 `research-schema.json`。2026-11-06 的真实样例是 `research/2026-11-06.json`。

每一条用 `match_href` 对齐卡片标题上的链接。显示序可以变，链接不变就挂在同一张卡片上。链接不在指定栏里就跳过这一条，不会写到别的卡片上。

`ready` 是当天核验过的产品，要有 2 到 4 句摘要、`verified_on`、报告文件名和 https 来源。`reuse` 沿用旧报告，`verified_on` 必须是原来的核验日，页面上会写出这个日期。`pending` 表示还没研究，不能填写报告文件名，页面只显示待研究，没有链接。

声明过的栏里，显示序 01 到 05 如果没有任何一条对上链接，脚本补一句待研究，仍然不给链接。

报告文件不在 `product-opportunities/reports/` 里时，脚本不写这个链接。

## 命令

先检查某一天的 JSON。

```bash
python3 product-opportunities/apply_opportunities.py --check-research 2026-11-06
```

发布程序写完当天 HTML 之后，在站点仓库根目录执行。

```bash
python3 product-opportunities/apply_opportunities.py index.html "$DAY.html"
```

`$DAY.html` 的文件名就是日期，例如 `2026-11-07.html`。`index.html` 没有日期文件名时，脚本读正文里的 `更新于 YYYY-MM-DD`。两个日期不一致就报错，不写入。没有 `research/YYYY-MM-DD.json` 时，这一页保持原样，不会改用另一天的文件。再跑一次得到同一结果。

不要对 `xhs/` 运行。

## 现有发布脚本

发布脚本里如果已经有上面这一行，就不用改命令。不要把日期写死成 2026-11-06，也不要在缺少当天 JSON 时复制前一天的文件。

研究任务并进现有的每天选题流水线。当天榜单出来之后，只为 GitHub 周榜、AI 周榜、AI 日榜的新进入产品，或有实质变化的旧产品，写新的摘要和报告。没变的产品在当天 JSON 里用 `reuse` 指向已有报告，并保留原 `verified_on`。没有研究的新产品用 `pending`。内容 PR 合并后，下一次发布才会挂上。
