"""把日常 #newsmall 选题区整理成结构化数据 new-small-v2.json（2026-11-09 t248）。
来源：newsmall-keywords.json（关键词计划与真实搜索记录）、newsmall-proposals.json（建议选题）、
../../seven/src/seven.json step2.latest（既有 4 条样本的原始字段，只读）、new-small.json（旧数据，规则与分层沿用，保持兼容）。"""
import json, re
from pathlib import Path
S = Path(__file__).resolve().parent; X = S.parents[1]
KW = json.loads((S / 'newsmall-keywords.json').read_text())
PR = json.loads((S / 'newsmall-proposals.json').read_text())
OLD = json.loads((S / 'new-small.json').read_text())
LATEST = json.loads((X / 'seven/src/seven.json').read_text())['step2']['latest']
EXTRA = [json.loads(p.read_text()) for p in sorted(S.glob('newsmall-samples-*.json'))]  # 补搜样本（父级交来后按日期一份）
CLEAN = re.compile(r'^https://www\.xiaohongshu\.com/explore/[0-9a-f]{24}$')

def legacy(x):
    v = x['followers_verified']
    return dict(id=x['source_id'], url=x['url'], title=x['title'], author=x['author'], tier=x['tier'], format=x['format'],
        followers=(f"{v}（2026-11-08 主页核过）" if v else "未核"),
        entry=f"关键词「{x['search']['keyword']}」· {x['search']['sort_actually_used']}排序 · 前 12 张卡轻扫，排序位置未记",
        date=x['published_raw'] + "；只有相对时间、无年份，不称新帖已核",
        counts=f"赞 {x['counts_2026_11_08']['likes']} / 藏 {x['counts_2026_11_08']['collects']} / 评 {x['counts_2026_11_08']['comments']}（2026-11-08 读取）",
        same_period=("同类 1 天内样本，但同期基线不足，不比高低、不称爆款" if x['comparable_same_period'] else (x['why_not'] or "不同期") + "，不做同期比较"),
        coverage=x['coverage'], structure=x['skeleton'], borrow=x['borrowable_action'],
        claims=x['author_claims'], limits=x['limits'], batch="旧池（AI工具，2026-11-08），不算本轮新搜")

samples = [legacy(x) for x in LATEST]
for f in EXTRA: samples += f['samples']
ids = {s['id'] for s in samples}
for s in samples:
    assert CLEAN.match(s['url']) and 'xsec' not in json.dumps(s, ensure_ascii=False), s['url']
    assert s['tier'] in OLD['tiers'], s['tier']
groups = KW['groups']
allkw = [k for g in groups for k in g['keywords']]
searched = [k for k in allkw if k['searches']]
for k in allkw:
    for r in k['searches']:
        assert set(r.get('sample_ids', [])) <= ids, k['query']
for p in PR['proposals']:
    assert all(len(t) <= 20 for t in p['titles']), p['id']
    assert set(p['sample_ids']) <= ids and p['group'] in {g['id'] for g in groups}, p['id']
out = dict(asof=max([KW['plan_date']] + [f['captured'] for f in EXTRA]), rules=OLD['rules'], tiers=OLD['tiers'], gaps=OLD['gaps'],
    counts=dict(planned=len(allkw), this_round=sum(k['this_round'] for k in allkw), searched=len(searched)),
    keywords_coverage=dict(groups=groups, legacy=KW['legacy']), samples=samples, proposals=PR['proposals'])
(S / 'new-small-v2.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print('ok', out['counts'], len(samples), 'samples', len(PR['proposals']), 'proposals')
