"""t248：日常 #newsmall 选题区结构化的行为测试（数据 new-small-v2.json + 站点首页渲染）。"""
import html, json, re, subprocess, sys, unittest
from pathlib import Path
S = Path(__file__).resolve().parent; X = S.parents[1]; R = X.parent
D = json.loads((S / 'new-small-v2.json').read_text())
HUB = (X / 'index.html').read_text()
B = re.search(r'<h2 id="newsmall">.*?</div>', HUB, re.S).group(0)

class NewSmall(unittest.TestCase):
    def test_v2_in_sync_with_sources(s):
        before = (S / 'new-small-v2.json').read_text()
        subprocess.run([sys.executable, str(S / 'build_new_small.py')], check=True, capture_output=True)
        s.assertEqual((S / 'new-small-v2.json').read_text(), before)
    def test_counts_dynamic_and_honest(s):
        kws = [k for g in D['keywords_coverage']['groups'] for k in g['keywords']]
        c = D['counts']
        done = sum(any(r['status'] != 'partial' for r in k['searches']) for k in kws)
        s.assertEqual((c['planned'], c['this_round'], c['searched']), (len(kws), sum(k['this_round'] for k in kws), done))
        s.assertIn(f'关键词计划 {c["planned"]} 个 · 本轮优先 {c["this_round"]} 个 · 已完成扫描 {c["searched"]} 个', B)
        s.assertEqual(B.count('本轮待搜') + B.count('后备，待搜'), sum(not k['searches'] for k in kws))
        s.assertNotIn('无合格新帖', B)
    def test_legacy_kept_not_new_search(s):
        leg = D['keywords_coverage']['legacy'][0]
        s.assertEqual(leg['query'], 'AI工具'); s.assertIn('不算本轮新搜', leg['note'])
        s.assertNotIn('AI工具', [k['query'] for g in D['keywords_coverage']['groups'] for k in g['keywords']])
        old = [x for x in D['samples'] if x['batch'].startswith('旧池')]
        s.assertEqual(len(old), 4)
        for x in old: s.assertEqual(x['date_status'], 'relative')  # 无年份、无绝对时间证据，不升级
    def test_reading_order_evidence_reasons_then_advice(s):
        # t249：能确认什么 → 帖子与数据 → 原因 → 建议 → 关键词覆盖 → 旧样本池
        idx = [B.index(f'id="{x}"') for x in ('ns-confirm', 'ns-posts', 'ns-advice', 'ns-coverage', 'ns-history')]
        s.assertEqual(idx, sorted(idx))
        ids = set(re.findall(r'id="([^"]+)"', B))
        for h in re.findall(r'href="#(ns-[^"]+)"', B): s.assertIn(h, ids)
        for x in [y for y in D['samples'] if not y['batch'].startswith('旧池')]:
            art = re.search(rf'<article id="ns-s-{x["id"]}"[^>]*>.*?</article>', B, re.S).group(0)
            s.assertLess(B.index(f'id="ns-s-{x["id"]}"'), B.index('id="ns-advice"'))
            head = art.split('<details>')[0]  # 发布时间、数据、原因与结论都在折叠之前
            for v in (x['date'], x['counts'], x['appeal']['fact'], x['appeal']['hypothesis'], x['appeal']['missing']): s.assertIn(html.escape(v), head)
            s.assertLess(head.index('发布时间'), head.index('可能受欢迎的原因'))
        for x in [y for y in D['samples'] if y['batch'].startswith('旧池')]:
            s.assertGreater(B.index(f'id="ns-s-{x["id"]}"'), B.index('id="ns-history"'))
        for p in D['proposals']:
            for t in p['titles']: s.assertLessEqual(len(t), 20)
            art = re.search(rf'<article id="ns-{p["id"]}">.*?<details>', B, re.S).group(0)
            for f in ('audience_problem', 'angle', 'takeaway', 'evidence_gap'): s.assertIn(html.escape(p[f]), art)
            for i in p['support_ids']: s.assertIn(f'href="#ns-s-{i}"', art)
    def test_honest_heat_summary(s):
        conf = re.search(r'<section id="ns-confirm">.*?</section>', B, re.S).group(0)
        if not D['confirm']['hot_confirmed']: s.assertIn('暂未确认热帖', conf)
        s.assertIn('粉丝少不等于火', conf)
        for bad in ('热门帖', '爆了', '已火', '赞粉比为'): s.assertNotIn(bad, B)
    def test_tier_order_and_rules(s):
        L = list(D['tiers'].values())
        s.assertLess(B.index(L[0]), B.index(L[1])); s.assertLess(B.index(L[1]), B.index(L[2]))
        for r in D['rules']: s.assertIn(html.escape(r), B)
    def test_samples_keep_real_titles_and_unproven_status(s):
        src = {x['source_id']: x['title'] for x in json.loads((X / 'seven/src/seven.json').read_text())['step2']['latest']}
        for x in D['samples']:  # 对全部已提交样本检查
            if x['id'] in src: s.assertEqual(x['title'], src[x['id']])  # 原标题完整保留，≤20 字只约束建议标题
            if x['date_status'] != 'absolute_verified': s.assertIsNone(x['date_evidence'])
            if x['classification'] == 'unproven':
                blk = re.search(rf'<article id="ns-s-{x["id"]}"[^>]*>.*?</article>', B, re.S).group(0).split('<details>')[0]
                s.assertRegex(blk, '未证实：')
        # 补搜样本标题与仓库外原始记录逐字相同（原始记录只在采集机上；别处 checkout 只跑上面的检查）
        for raw in Path('/workspace/xhs-small-structured-20261109').glob('search-batch*/samples/*/sample.json'):
            r = json.loads(raw.read_text()); s.assertEqual(next(y for y in D['samples'] if y['url'] == r['note_url_clean'])['title'], r['title'])
    def test_links_clean_and_private(s):
        for t in re.findall(r'<a\b[^>]*href="https[^"]*"[^>]*>', B):
            s.assertIn('target="_blank"', t); s.assertRegex(t, r'href="https://www\.xiaohongshu\.com/explore/[0-9a-f]{24}"')
        blob = B + json.dumps(D, ensure_ascii=False)
        for bad in ('xsec', '5098143774', '/workspace', '听记知识库'): s.assertNotIn(bad, blob)
        pf = Path('/workspace/money/xhs-real/topic-keyword-watch/topics.json')
        if pf.exists():
            for t in json.loads(pf.read_text())['topics']:
                tj = (t.get('tingji') or {}).get('title')
                if tj: s.assertNotIn(tj, blob)

    def test_generator_fallback(s):
        import importlib.util, os, shutil, tempfile
        tmp = Path(tempfile.mkdtemp())
        for f in Path('/workspace/digests').glob('*.py'):
            if f.name != 'xhs_library.py': os.symlink(f, tmp / f.name)
        shutil.copy(R / 'review/xhs-seven-20261108/xhs_library.py', tmp / 'nsgen.py'); sys.path.insert(0, str(tmp))
        sp = importlib.util.spec_from_file_location('nsgen', tmp / 'nsgen.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        site = Path(tempfile.mkdtemp()); (site / 'topics/src').mkdir(parents=True); m.SITE = site
        shutil.copy(S / 'new-small.json', site / 'topics/src/new-small.json')
        old = m._daily_new_small(); s.assertIn('<ul><li><a href=', old); s.assertNotIn('ns-P', old)   # 无 v2：旧写法
        (site / 'topics/src/new-small-v2.json').write_text('{"samples": null}')
        s.assertEqual(m._daily_new_small(), old)                                                  # v2 坏：退回旧写法
        shutil.copy(S / 'new-small-v2.json', site / 'topics/src/new-small-v2.json')
        s.assertIn('id="ns-P1"', m._daily_new_small())
        # 搜索状态：空 sample_ids 不等于没有合格帖；每种状态按真实含义显示
        v = json.loads((S / 'new-small-v2.json').read_text()); kw = v['keywords_coverage']['groups'][0]['keywords']
        base = dict(captured='2026-11-09', sort='最新', sort_evidence='筛选面板截图', scanned_count=12, opened_count=0, sample_ids=[], limits='x')
        kw[0]['searches'] = [dict(base, status='scanned_pending', pending_candidates=3)]
        kw[1]['searches'] = [dict(base, status='partial', pending_candidates=0)]
        kw[2]['searches'] = [dict(base, status='checked_none', opened_count=4, pending_candidates=0, no_qualified_basis='4 篇均为旧帖编辑')]
        (site / 'topics/src/new-small-v2.json').write_text(json.dumps(v, ensure_ascii=False)); h = m._daily_new_small()
        s.assertIn('已扫描，候选待核</b>（2026-11-09，最新排序；扫 12 张、开 0 篇、待核候选 3 条）', h)
        s.assertIn('未完成（部分搜索或中断）', h)
        s.assertIn('依据：4 篇均为旧帖编辑', h)
        s.assertNotIn('无合格', h)

if __name__ == '__main__':
    unittest.main()
