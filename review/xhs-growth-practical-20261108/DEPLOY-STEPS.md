# 合并后部署（父 bot 执行；不要手改线上）
1. 校验共享生成器未被他人改动：`sha256sum /workspace/digests/xhs_library.py` 必须 = 811cdc61480eb94a382329b9a8fe8f494c787a9b11ab84677a21a73e529decb9；不等则报冲突、停。
2. 备份：`cp -p /workspace/digests/xhs_library.py /workspace/creator-growth-20261108/growth-nav/xhs_library.pre-t223-811cdc61.py`
3. 覆盖：`cp review/xhs-growth-practical-20261108/xhs_library.py /workspace/digests/xhs_library.py`（唯一改动：入口页指向人物成长研究模块的链接加 target=_blank rel="noopener noreferrer"，人物页文件名读 xhs/growth/src/people.json）。
4. 部署仓库 /workspace/digests/site-repo 拉到合并后的 main；`python3 xhs/growth/src/build_index.py` 结果应与仓库一致（无 diff）。
5. 每日 build() 会调 sync_creators（用合并后的 split_creators + page_kit），产物应与仓库同名文件逐字节一致；跑 `python3 review/xhs-growth-practical-20261108/check_generator.py <备份文件>` 应 OK。
6. 共享 money 源 /workspace/money/ai-creators-growth.html 不动（9815ddab…）。
7. 线上缓存穿透 curl 抽查 growth/、kazike.html、lenny.html、xhs/index.html 与 main 逐字节一致。
