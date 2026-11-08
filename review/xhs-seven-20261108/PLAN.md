# 七步工作台（t242/t243）
- 内容源（仓库外，私有）：latest-topic-library/seven-step-pack.json + article-analysis.md。import_seven.py 把它转成仓库内唯一公开源 xhs/seven/src/seven.json（私有相对路径映射为公开人物页；最新池按实际条数，不补）。
- build_seven.py → xhs/seven/index.html（独立工作台页：左目录、无 JS、7 节每节“产物 / 状态 / 缺口”）。
- 入口：xhs/index.html 长驻工具加「七步工作台」+ 7 步可扫摘要，数据读 SITE/seven/src/seven.json（与日更同源，日更不覆盖）。改动做在新镜像 review/xhs-seven-20261108/xhs_library.py（基于 7749396a），共享源由父级部署时核指纹后替换。
- 等待：最新排序真实样本（scout-ai-tools）到齐后并入 latest_pool 再 freeze。
