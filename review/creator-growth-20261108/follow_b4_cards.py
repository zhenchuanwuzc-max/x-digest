"""关注第四批的图卡覆盖度——唯一来源；函数沿用第二批（视频写“未主动播放、未观看”）。证据在仓库外 following-batch4/*/ledger.md（2026-11-08 只读）。"""
from follow_b2_cards import VIDEO, pages, complete, text, full
COV = {
 "heideng": {"w1": full(1), "w2": full(7)},  # 图文全读；n2 第 4 页首截空白，等待后同页重截成功
 "menqiang": {"w1": VIDEO, "w2": full(16)},
 "lidan": {"w1": VIDEO, "w2": full(5)},
 "pupu-wanzi": {"w1": VIDEO, "w2": full(12)},  # 视频只看标题、描述、评论；照片图文 12/12 静态画面（LIVE 动态未看）  # 视频只看标题、描述、评论；纯文字图卡 5/5  # 视频只看标题、完整描述、评论；图文 16/16（第 9 页首截空白后重截成功）
}
def gaps(slug): return {w: text(c) for w, c in COV[slug].items() if not complete(c)}
