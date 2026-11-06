# 接入日更

这个仓库里没有产品榜的日更生成器。`tiers.py` 只处理分层数据，`xhs/` 是另一块页面。GitHub Actions 目录不存在。下面的脚本没有被任何站外任务调用。

## 命令

在仓库根目录执行。

```bash
python3 product-opportunities/apply_opportunities.py
```

脚本会重写 `product-opportunities/reports/` 下的 10 个页面，并只修改同时满足两点的 HTML。

- 正文含有 `更新于 2026-11-06 06:18（北京时间）`
- 指定面板里，显示序和原链接同时对上

对不上的卡片不会被写上别人的分析。没有这句时间的页面会原样跳过，包括下一天的新榜。再跑一次不会叠第二段分析。

默认文件是 `index.html` 和 `2026-11-06.html`。站外生成器如果写出别的路径，把路径接在命令后面。不要对 `xhs/` 运行。

## 生成器里可以加的一步

日更在写完当天 HTML 之后加这一行。路径按生成器的工作目录改。

```bash
python3 product-opportunities/apply_opportunities.py path/to/2026-11-06.html
```

只有页面仍是 2026-11-06 06:18 这一份快照时，分析才会留下。新的一天需要新的快照数据，不能复用这个文件。
