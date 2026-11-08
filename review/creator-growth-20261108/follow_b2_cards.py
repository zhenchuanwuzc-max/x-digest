"""关注第二批（老A的AI研究所 / 杰森的效率工坊 / Accio Work / 知危）的图卡覆盖度——唯一来源；函数沿用 follow_b1_cards。
证据在仓库外 following-batch2/*/（ledger.md、supplement-ledger.md、third-post-ledger.md、n2_hook/ledger.md、n3_reach/ledger.md），2026-11-08 只读采集，空白页经等待重试补齐。"""
import follow_b1_cards as _b1
from follow_b1_cards import VIDEO, pages, complete, text as _text
def text(c):
    # 第二批：页面打开时有自动播放，所以不写“未播放”，只写未主动播放、未观看
    return "视频笔记：按 Ocean 要求只看标题和描述，未主动播放、未观看或分析视频内容" if c == VIDEO else _text(c)
full = lambda n: dict(total=n, read=list(range(1, n + 1)), partial=[], pending={})
COV = {
 "laoa-yanjiusuo": {"w1": full(11), "w2": full(15), "w3": full(11)},
 "jason-effi": {"w1": full(10), "w2": VIDEO, "w3": full(7)},
 "accio-work": {"w1": full(8), "w2": VIDEO, "w3": full(1)},
 "zhiwei": {"w1": VIDEO, "w2": VIDEO},
}
def gaps(slug): return {w: text(c) for w, c in COV[slug].items() if not complete(c)}
