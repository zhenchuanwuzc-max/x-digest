# t225 对标优先（分支 xhs-growth-bench-20261108，基于 main 6c48ca0，单写者）
目标：首页总判断每个方向先显示“对标谁（人名链接）→ 他做了什么（代表作品锚点 + 一手来源）→ 学这一步 / 别照搬”，再显示面向谁、痛点、Ocean 借鉴、怎么验证；人物页顶部摘要“他咋做”加代表作品锚点与动作。
数据只取已有人物页代表作品拆解；不新研究、不排名、不造因果。生成源：people.json（practice[].bench、people[].brief.work）+ build_index + page_kit。
共享生成器、money 源不动；旧外部 builder 4eb58311 不运行（zhangzala 走仓库内 build.py，输入 git 9c711ed）。
