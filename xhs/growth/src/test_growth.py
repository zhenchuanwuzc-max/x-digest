"""人物成长研究模块验收：首页三块、14 人独立目标、二级页不聚合、专题可达、旧锚点兼容、原内容不丢、生成一致。"""
import json, re, subprocess, sys, unittest
from pathlib import Path
D = Path(__file__).resolve().parent; G = D.parent; X = G.parent; W = X.parent
sys.path.insert(0, str(D)); import build_index, split_creators
M = json.loads((D/'people.json').read_text()); P, T = M['people'], M['topics']
H = (G/'index.html').read_text()
SHARED = Path('/workspace/money/ai-creators-growth.html')
BASE = '4fc0341e34eea0e07d368f34430fff95d1f20166'
PERSON_FILES = {(G/p['href']).resolve().name for p in P}
def resolve(base_dir, href):
    f, _, a = href.partition('#'); path = (base_dir/f).resolve() if f else None
    if path and path.is_dir(): path = path/'index.html'
    return path, a
def sanitized():
    h = SHARED.read_text(); h = re.sub(r'/workspace/[^<\s"\']+', '', h); return re.sub(r'/Users/[^<\s"\']+', '', h)
def old(path): return subprocess.run(['git', '-C', str(W), 'show', f'{BASE}:{path}'], capture_output=True, text=True, check=True).stdout

class Home(unittest.TestCase):
    def test_generated(s): s.assertEqual(H, build_index.render())
    def test_three_blocks_only(s):
        nav = H[H.index('<aside'):H.index('</aside>')]
        s.assertEqual(re.findall(r'href="([^"]+)"', nav), ['#total', '#people', '#topics'])
        s.assertGreaterEqual(H[H.index('id="total"'):H.index('id="people"')].count('<li>'), 3)
        s.assertEqual(H.count('id="p-'), 14); s.assertEqual(H.count('id="t-'), len(T))
    def test_each_person_own_target(s):
        targets = [p['href'] for p in P]; s.assertEqual(len(set(targets)), 14)
        for p in P:
            s.assertNotIn('creators.html', p['href']); s.assertNotIn('#', p['href'])
            f, _ = resolve(G, p['href']); s.assertTrue(f.exists(), p['href'])
    def test_topics_reachable(s):
        for t in T:
            f, a = resolve(G, t['href']); s.assertTrue(f.exists(), t['href'])
            if a: s.assertIn(f'id="{a}"', f.read_text())

class Subpages(unittest.TestCase):
    def pages(s):
        return [X/n for n in PERSON_FILES] + [X/'topic-types.html', X/'topic-lip-growth.html', G/'hector.html']
    def test_no_aggregation(s):
        for f in s.pages():
            h = f.read_text(); others = PERSON_FILES - {f.name}
            hrefs = re.findall(r'href="([^"]+)"', h)
            linked = {x.split('#')[0].split('/')[-1] for x in hrefs if not x.startswith('http')} & others
            s.assertLessEqual(len(linked), 1, (f.name, linked))  # 正文里偶尔引用一个人可以，人物聚合不行
            s.assertNotIn('href="creators.html', h, f.name)
            s.assertNotIn('id="p-', h, f.name)
    def test_back_link_and_toc_only(s):
        for f in s.pages():
            if f.name == 'hector.html' and f.parent == G: continue
            h = f.read_text(); nav = h[h.index('<aside'):h.index('</aside>')]
            ext = [x for x in re.findall(r'href="([^"]+)"', nav) if not x.startswith('#')]
            s.assertEqual(ext, ['growth/'], f.name)
    def test_internal_anchors(s):
        for f in s.pages():
            h = f.read_text(); ids = set(re.findall(r'\sid="([^"]+)"', h))
            for a in re.findall(r'href="#([^"]+)"', h): s.assertIn(a, ids, f'{f.name}#{a}')
    def test_hector_podcast_lenny_material(s):
        s.assertIn('href="growth/hector.html"', (X/'hector.html').read_text())
        s.assertIn('href="./#lenny"', (X/'lenny.html').read_text()); s.assertIn('id="lenny"', (X/'index.html').read_text())

class Migration(unittest.TestCase):
    def test_generation_consistent(s):
        out = split_creators.split(sanitized())
        for name, page in out.items(): s.assertEqual((X/name).read_text(), page, name)
    def test_no_content_lost(s):
        for sid, sec in split_creators._sections(sanitized()[sanitized().index('<body'):]):
            kind, target = split_creators.ROUTES[sid]
            if kind == 'page': s.assertIn(sec, (X/target).read_text(), sid)
            else: s.assertTrue(resolve(X, target)[0].exists(), target)
    def test_old_anchors_compat(s):
        before = set(re.findall(r'\sid="([^"]+)"', old('xhs/creators.html')))
        c = (X/'creators.html').read_text(); s.assertNotIn('<h2', c)
        rows = dict(re.findall(r'<li id="([^"]+)"><a href="([^"]+)"', c))
        s.assertEqual(before - set(rows), set())
        for i, href in rows.items():
            f, a = resolve(X, href); s.assertTrue(f.exists(), href)
            if a: s.assertIn(f'id="{a}"', f.read_text(), href)
    def test_eight_pages_only_nav_changed(s):
        pat = re.compile(r'<div class="sec">选题库</div>\s*<a href="growth/">← 成长记录</a>\s*<a href="\./">小红书全入口</a>\s*<a href="[^"]*">[^<]*</a>\s*')
        for n in ('kazike', 'zhangzala', 'baoyu', 'guizang', 'qiaomu', 'huashu', 'fankai', 'hector'):
            o = old(f'xhs/{n}.html'); new = (X/f'{n}.html').read_text()
            s.assertEqual(len(pat.findall(o)), 1, n)
            back = re.compile(r'\s*<a href="growth/">← 人物成长研究</a>\s*')
            s.assertEqual(len(back.findall(new)), 2, n)  # 侧栏 + 手机目录各一个
            s.assertEqual(re.sub(r'\s+', '', pat.sub('', o, count=1)), re.sub(r'\s+', '', back.sub('', new, count=2)), n)
unittest.main()
