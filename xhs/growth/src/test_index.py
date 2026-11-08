import json, re, sys, unittest
from pathlib import Path
D = Path(__file__).resolve().parent; G = D.parent; X = G.parent
sys.path.insert(0, str(D)); import build_index
H = (G/'index.html').read_text(); P = json.loads((D/'people.json').read_text())['people']
BEFORE_HREFS = ['../kazike.html','../zhangzala.html','../guizang.html','../huashu.html','../fankai.html','../baoyu.html','../qiaomu.html','../hector.html','../creators.html','../creators.html#lenny','../','https://zhenchuanwuzc-max.github.io/x-digest/']
class T(unittest.TestCase):
    def test_generated(s): s.assertEqual(H, build_index.render())
    def test_14_unique(s):
        s.assertEqual(len(P), 14); s.assertEqual(len({p['id'] for p in P}), 14); s.assertEqual(len({p['href'] for p in P}), 14)
    def test_nav_people_only(s):
        nav = H[H.index('<aside'):H.index('</aside>')]
        s.assertEqual(re.findall(r'href="([^"]+)"', nav), ['#p-'+p['id'] for p in P])
        for w in ['其他','相关','加深档','独立页','全入口','情报站']: s.assertNotIn(w, nav)
    def test_one_primary_link_each(s):
        cards = re.findall(r'<div class="card" id="p-([^"]+)">(.*?)\n    </div>', H, re.S)
        s.assertEqual([c[0] for c in cards], [p['id'] for p in P])
        for (pid, body), p in zip(cards, P):
            s.assertEqual(re.findall(r'<a class="go" href="([^"]+)"', body), [p['href']])
            s.assertNotIn('档案内', body)
    def test_old_links_resolve_and_anchor(s):
        s.assertIn('id="people"', H)
        for h in BEFORE_HREFS:
            if h.startswith('http'): continue
            f, _, a = (G/h).as_posix().partition('#'); f = Path(f); f = f/'index.html' if f.is_dir() else f
            s.assertTrue(f.exists(), h)
            if a: s.assertIn(f'id="{a}"', f.read_text())
    def test_hector_podcast_and_lenny_material_reachable(s):
        s.assertIn('href="growth/hector.html"', (X/'hector.html').read_text())
        s.assertIn('href="hector.html"', H); s.assertTrue((G/'hector.html').exists())
        s.assertIn('href="../#lenny"', H); s.assertIn('id="lenny"', (X/'index.html').read_text())
    def test_collection_is_secondary(s):
        main = H[H.index('<main'):]
        s.assertEqual(main.count('href="../creators.html"'), 1)
        s.assertLess(main.index('id="people"'), main.index('附属合集'))
        for w in ['加深档','独立页','其他','相关','合集与海外']: s.assertNotIn(f'<h2>{w}', main)
    def test_targets_exist(s):
        ids = set(re.findall(r'id="([^"]+)"', (X/'creators.html').read_text()))
        for p in P:
            f, _, a = p['href'][3:].partition('#'); s.assertTrue((X/f).exists(), f)
            if a: s.assertIn(a, ids)
        for a in re.findall(r'href="#([^"]+)"', H): s.assertIn(f'id="{a}"', H)
unittest.main()
