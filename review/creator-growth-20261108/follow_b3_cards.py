"""关注第三批的图卡覆盖度——唯一来源；函数沿用第二批（视频写“未主动播放、未观看”）。证据在仓库外 following-batch3/*/ledger.md（2026-11-08 只读）。"""
from follow_b2_cards import VIDEO, pages, complete, text, full
COV = {
 "keruiji": {"w1": VIDEO, "w2": VIDEO},
 "will": {"w1": full(8), "w2": full(6)},
 "huguagua": {"w1": full(4), "w2": full(5)},
 "claire": {"w1": full(7), "w2": full(7)},
 "fufujie": {"w1": VIDEO, "w2": full(9)},  # 视频只看标题描述评论；图文 9/9 全读  # 图文全读，无空白页、无重试  # 图文全读，无空白页、无重试  # 图文全读；空白页经重试补齐（部分只等约 6 秒，台账已注）
}
def gaps(slug): return {w: text(c) for w, c in COV[slug].items() if not complete(c)}
