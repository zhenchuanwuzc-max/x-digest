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
    def test_one_card_each(s):
        for p in P: s.assertEqual(H.count(f'id="p-{p["id"]}"'), 1); s.assertEqual(H.count(f'href="{p["href"]}"'), 1)
    def test_old_links_and_anchor(s):
        s.assertIn('id="people"', H)
        for h in BEFORE_HREFS: s.assertIn(f'href="{h}"', H)
        s.assertTrue((G/'hector.html').exists())
    def test_targets_exist(s):
        ids = set(re.findall(r'id="([^"]+)"', (X/'creators.html').read_text()))
        for p in P:
            f, _, a = p['href'][3:].partition('#'); s.assertTrue((X/f).exists(), f)
            if a: s.assertIn(a, ids)
        for a in re.findall(r'href="#([^"]+)"', H): s.assertIn(f'id="{a}"', H)
unittest.main()
