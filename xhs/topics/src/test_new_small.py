"""t248/t270：#newsmall 数据层测试；2026-11-10 起入口不再注入该板块。"""
import html, json, re, subprocess, sys, unittest
from pathlib import Path
S = Path(__file__).resolve().parent; X = S.parents[1]; R = X.parent
D = json.loads((S / 'new-small-v2.json').read_text())
HUB = (X / 'index.html').read_text()

class NewSmall(unittest.TestCase):
    def test_v2_in_sync_with_sources(s):
        before = (S / 'new-small-v2.json').read_text()
        subprocess.run([sys.executable, str(S / 'build_new_small.py')], check=True, capture_output=True)
        s.assertEqual((S / 'new-small-v2.json').read_text(), before)

    def test_hub_no_longer_injects_newsmall_block(s):
        s.assertNotIn('id="newsmall"', HUB)
        s.assertNotIn('选题热帖：新帖、小号优先', HUB)
        s.assertIn('热帖门槛', HUB)

    def test_counts_dynamic(s):
        kws = [k for g in D['keywords_coverage']['groups'] for k in g['keywords']]
        c = D['counts']
        done = sum(any(r['status'] != 'partial' for r in k['searches']) for k in kws)
        s.assertEqual((c['planned'], c['this_round'], c['searched']), (len(kws), sum(k['this_round'] for k in kws), done))

    def test_legacy_kept_not_new_search(s):
        leg = D['keywords_coverage']['legacy'][0]
        s.assertEqual(leg['query'], 'AI工具'); s.assertIn('不算本轮新搜', leg['note'])
        old = [x for x in D['samples'] if x['batch'].startswith('旧池')]
        s.assertEqual(len(old), 4)

    def test_samples_keep_real_titles_and_links_clean(s):
        src = {x['source_id']: x['title'] for x in json.loads((X / 'seven/src/seven.json').read_text())['step2']['latest']}
        for x in D['samples']:
            if x['id'] in src: s.assertEqual(x['title'], src[x['id']])
            if x['date_status'] != 'absolute_verified': s.assertIsNone(x['date_evidence'])
        blob = json.dumps(D, ensure_ascii=False)
        for bad in ('xsec', '5098143774', '/workspace', '听记知识库'): s.assertNotIn(bad, blob)
        for x in D['samples']:
            s.assertRegex(x['url'], r'^https://www\.xiaohongshu\.com/explore/[0-9a-f]{24}$')

    def test_proposals_title_len(s):
        for p in D['proposals']:
            for t in p['titles']: s.assertLessEqual(len(t), 20)

    def test_generator_helper_still_renders_offline(s):
        import importlib.util, os, shutil, tempfile
        tmp = Path(tempfile.mkdtemp())
        for f in Path('/workspace/digests').glob('*.py'):
            if f.name.endswith('.py'):
                try: os.symlink(f, tmp / f.name)
                except FileExistsError: pass
        sys.path.insert(0, str(tmp))
        sp = importlib.util.spec_from_file_location('nsgen', '/workspace/digests/xhs_library.py')
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        site = Path(tempfile.mkdtemp()); (site / 'topics/src').mkdir(parents=True); m.SITE = site
        shutil.copy(S / 'new-small.json', site / 'topics/src/new-small.json')
        old = m._daily_new_small(); s.assertIn('新帖、小号优先', old)  # helper itself still can render legacy
        shutil.copy(S / 'new-small-v2.json', site / 'topics/src/new-small-v2.json')
        s.assertIn('id="ns-confirm"', m._daily_new_small())

if __name__ == '__main__':
    unittest.main()
