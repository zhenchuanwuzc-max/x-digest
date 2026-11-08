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
        s.assertEqual((c['planned'], c['this_round'], c['searched']), (len(kws), sum(k['this_round'] for k in kws), sum(bool(k['searches']) for k in kws)))
        s.assertIn(f'关键词计划 {c["planned"]} 个 · 本轮优先 {c["this_round"]} 个 · 已实际搜完 {c["searched"]} 个', B)
        unsearched = [k for k in kws if not k['searches']]
        s.assertEqual(B.count('本轮待搜') + B.count('后备，待搜'), len(unsearched))
        s.assertNotIn('0 条', B)
    def test_legacy_kept_not_new_search(s):
        leg = D['keywords_coverage']['legacy'][0]
        s.assertEqual(leg['query'], 'AI工具'); s.assertIn('不算本轮新搜', leg['note'])
        s.assertNotIn('AI工具', [k['query'] for g in D['keywords_coverage']['groups'] for k in g['keywords']])
        old = [x for x in D['samples'] if x['batch'].startswith('旧池')]
        s.assertEqual(len(old), 4)
        for x in old: s.assertIn('不称新帖已核', x['date'])
    def test_proposals_first_then_evidence(s):
        s.assertLess(B.index('<h3>建议选题'), B.index('<h3>关键词覆盖')); s.assertLess(B.index('<h3>关键词覆盖'), B.index('<h3>真实样本'))
        ids = set(re.findall(r'id="([^"]+)"', B))
        for h in re.findall(r'href="#(ns-[^"]+)"', B): s.assertIn(h, ids)
        for p in D['proposals']:
            for t in p['titles']: s.assertLessEqual(len(t), 20)
            s.assertTrue(p['ocean_case'] and p['evidence_gap'] and p['next'])
            for f in ('audience_problem', 'angle', 'takeaway'): s.assertIn(html.escape(p[f]), B)
        s.assertEqual(B.count('<details'), len(D['proposals']) + len(D['samples']))
    def test_tier_order_and_rules(s):
        L = list(D['tiers'].values())
        s.assertLess(B.index(L[0]), B.index(L[1])); s.assertLess(B.index(L[1]), B.index(L[2]))
        for r in D['rules']: s.assertIn(html.escape(r), B)
    def test_no_hype_claims(s):
        s.assertNotIn('全平台最热', B)
        for m in re.finditer('爆款', B):  # 每处“爆款”前 12 字内必须有否定或未证实
            s.assertRegex(B[max(0, m.start() - 12):m.end() + 4], '不|未|非', B[m.start() - 12:m.end()])
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

if __name__ == '__main__':
    unittest.main()
