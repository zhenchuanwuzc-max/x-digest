# 合并后共享文件同步（按顺序；任一 sha 不符即停止并报告冲突，不覆盖）
预期现值（2026-11-08 19:00 UTC+8 核对）：
- /workspace/money/ai-creators-growth.html  9815ddab4e43de6cc7fa028b82446675eb5dfcec4d6639d1c988077ac12ebf7d —— 本次不改
- /workspace/digests/xhs_library.py  a593ae153a89bf8321229970cb6a9fc391b8dee776dcf04705928b8d814dea23 —— 备份 growth-nav/xhs_library.backup-a593ae15.py
- /workspace/digests/monitors/xhs_library.json  547edc0fbab9aea2c360a2d674090c6556215b630303e2d2d412dd415665daa5（会被日常 append 改动；若变了只要 profile_url 仍为旧值脚本仍可用，先另存备份）
- /workspace/xhs-ui-20261108/build_zhangzala.py  a22246273257f5c3486c3bc26ea7c6b3d507770695445ca00f5dd918912f993b —— 备份 growth-nav/build_zhangzala.external.backup-a2224627.py

1. 确认无日常构建在跑；/workspace/digests/site-repo 干净后 `git merge --ff-only origin/main` 到合并 SHA（需要 xhs/growth/src/split_creators.py、people.json）。
2. 核 sha 后：`cp review/xhs-growth-ia-20261108/xhs_library.py /workspace/digests/xhs_library.py`，cmp 一致。
3. `python3 review/xhs-growth-ia-20261108/fix_profile_urls.py`（自动唯一名备份、原子写、幂等；输出 changed 12 left []）。
4. 核 sha 后：`cp review/xhs-growth-ia-20261108/build_zhangzala.external.py /workspace/xhs-ui-20261108/build_zhangzala.py`（该脚本已过时、直接写 site-repo，不要运行；只为防止将来重跑恢复旧导航）。
5. 用真实日常路径验收：在 site-repo 运行 `python3 /workspace/digests/xhs_library.py --sync-creators` 后 `git -C /workspace/digests/site-repo status --short` 应为空（输出与合并产物逐字节一致）；再跑 `check_generator.py growth-nav/xhs_library.backup-a593ae15.py`。
6. 线上防缓存抓 xhs/growth/、xhs/、xhs/creators.html、6 个新人物页、2 个专题页、xhs/plan.html、xhs/growth/hector.html、8 个人物页，逐字节对比合并产物。
