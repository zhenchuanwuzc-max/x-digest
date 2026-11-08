# 部署七步工作台（父级执行；子代理不合并不部署）
1. 合并 PR 后，在部署 checkout 里同步 xhs/seven/、xhs/index.html、xhs/growth/。
2. 共享生成器替换（入口才会在日更里保留）：
   - 核对 live 指纹：`sha256sum /workspace/digests/xhs_library.py` 前 16 位必须是 7749396a3c41be76，不对就停。
   - 确认没有别的进程在写这个文件（日更不在运行）。
   - 备份已存在：/workspace/creator-growth-20261108/growth-nav/xhs_library.pre-seven-7749396a.py
   - 预检：`PYTHONDONTWRITEBYTECODE=1 python3 review/xhs-seven-20261108/check_generator.py /workspace/digests/xhs_library.py` 输出 OK。
   - 复制 review/xhs-seven-20261108/xhs_library.py → /workspace/digests/xhs_library.py。
3. 差异只有：「今天写啥」后新增「选题热帖：新帖、小号优先」块（读 xhs/topics/src/new-small.json，导航「选题」组首项，组由仓库内 xhs/apply_xhs_shell.py 定）；长驻工具多一条「七步工作台」+ 7 步摘要；hit() 加 seven/ 新标签。两份数据缺失或损坏时对应块不出现，日更不中断；routine 与运行时间不变。
4. 旧的 review/xhs-growth-practical-20261108/check_generator.py 比较 live 与旧镜像，替换后以本目录脚本为准。
