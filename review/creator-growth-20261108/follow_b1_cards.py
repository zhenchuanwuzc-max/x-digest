"""首批关注研究（Lulu / 老A进阶实操 / Karl）的图卡覆盖度——唯一来源。
页面上“读了几页、缺哪页”和“是否读完”都从这里生成；证据见仓库外 following-batch1/*/ledger.md、supplement-ledger.md、final-gap-ledger.md（2026-11-08 补齐，含空白页等待重试）。
video: 视频笔记，按 Ocean 要求只看标题和描述（不是缺口）。
图文: total 轮播页数；read 有内容可读；partial 只部分可读；pending 未读到（空白待重试 / 无截图待补）。"""
VIDEO = "video"
COV = {
 "lulu-ai": {"w1": VIDEO, "w2": VIDEO, "w3": VIDEO},
 "laoa-jinjie": {"w1": dict(total=10, read=list(range(1, 11)), partial=[], pending=[]),
          "w2": dict(total=10, read=list(range(1, 11)), partial=[], pending={}),
          "w3": dict(total=9, read=list(range(1, 10)), partial=[], pending={})},
 "karl-aigc": {"w1": dict(total=9, read=list(range(1, 10)), partial=[], pending={}),
          "w2": dict(total=9, read=list(range(1, 10)), partial=[], pending={}),
          "w3": dict(total=14, read=list(range(1, 15)), partial=[], pending={})},
}
def pages(ns):
    ns = sorted(ns); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1: j += 1
        out.append(str(ns[i]) if i == j else f"{ns[i]}–{ns[j]}"); i = j + 1
    return "、".join(out)
def complete(c): return c == VIDEO or (not c["partial"] and not c["pending"] and len(c["read"]) == c["total"])
def text(c):
    if c == VIDEO: return "视频笔记：按 Ocean 要求只看标题和描述，视频未播放"
    s = f"图文 {c['total']} 页，已读 {len(c['read'])}/{c['total']}（第 {pages(c['read'])} 页）"
    if c["partial"]: s += f"；第 {pages(c['partial'])} 页只部分可读"
    if c["pending"]: s += "；待补：" + "，".join(f"第 {k} 页（{v}）" for k, v in sorted(c["pending"].items()))
    return s
def gaps(slug): return {w: text(c) for w, c in COV[slug].items() if not complete(c)}
