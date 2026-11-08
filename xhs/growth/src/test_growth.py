"""人物成长研究模块验收：首页实操结论+人物+专题、14 人对比卡字段与口径、人物页顶部实操摘要、跨页链接新标签、
二级页不聚合、专题可达、旧锚点兼容、原内容不丢（允许摘要与 target/rel）、生成一致。"""
import json, re, subprocess, sys, unittest
from pathlib import Path
D = Path(__file__).resolve().parent; G = D.parent; X = G.parent; W = X.parent
sys.path.insert(0, str(D)); import build_index, split_creators, page_kit
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
NF = '未找到公开数值'
def norm(h):
    """去掉 t224 允许的改动：顶部摘要、摘要样式、目录里的摘要链接、target/rel 属性。"""
    h = re.sub(r'<section class="brief" id="brief".*?</section>\n', '', h, flags=re.S).replace(page_kit.BRIEF_CSS, '')
    h = re.sub(r'\s*<a href="#brief">[^<]*</a>', '', h)
    return re.sub(r'\s(target|rel)="[^"]*"', '', h)
def old(path): return subprocess.run(['git', '-C', str(W), 'show', f'{BASE}:{path}'], capture_output=True, text=True, check=True).stdout

class Home(unittest.TestCase):
    def test_generated(s): s.assertEqual(H, build_index.render())
    def test_three_blocks_only(s):
        nav = H[H.index('<aside'):H.index('</aside>')]
        s.assertEqual(re.findall(r'href="([^"]+)"', nav), ['#total', '#steps', '#people', '#topics'])
        top = H[H.index('id="total"'):H.index('id="people"')]
        s.assertGreaterEqual(top.count('class="pr"'), 3)
        for k in ('痛点', '别人怎么解（证据）', 'Ocean 可以做', '交付样例', '怎么验证'): s.assertEqual(top.count(f'<dt>{k}</dt>'), top.count('class="pr"'), k)
        s.assertGreaterEqual(top[top.index('id="steps"'):].count('<li>'), 3)
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

class Practice(unittest.TestCase):
    def test_advice_marked_and_evidence_named(s):
        names = {p['name'] for p in P} | {'乔木', '宝玉', '卡兹克', '张咋啦', '花叔', 'Lenny', 'Shreyas'}
        for r in M['practice']:
            s.assertTrue(r['ocean'].startswith('建议：'), r['ocean'])
            s.assertTrue(any(n in r['evidence'] for n in names), r['evidence'])
            s.assertIn('推断', r['who'])
        for o in M['observations']: s.assertTrue(o.startswith('观察：'))
        for st in M['steps']: s.assertTrue(st.startswith('建议'), st)
        top = H[H.index('id="total"'):H.index('id="people"')]
        for bad in ('预计', '保证', '月入', '涨粉到', '我在大厂', '我做过'): s.assertNotIn(bad, top)
        s.assertIn('L1', top); s.assertIn('L2', top)
    def test_cards_fields_complete(s):
        for p in P:
            c = H[H.index(f'id="p-{p["id"]}"'):]; c = c[:c.index('</div>\n', c.index('<details'))]
            for k in ('主要做什么', '主要用户', 'X 关注者', '小红书粉丝', '公众号关注', '收入'): s.assertIn(f'<dt>{k}</dt>', c, (p['id'], k))
            s.assertIn('<details><summary>数据口径与来源</summary>', c)
            for k, v in p['metrics'].items():  # 卡片上看得到口径：公开读取 / 自述 / 未找到公开数值
                vis = {'事实': '<span class="k f">公开读取</span>', '自述': '<span class="k s">自述</span>', '未找到': f'<span class="nf">{NF}</span>'}[v['kind']]
                s.assertIn(vis, c, (p['id'], k))
            s.assertTrue('推断' in p['users'] or '自述' in p['users'], p['id'])
            s.assertIn(f'href="{p["href"]}" target="_blank" rel="noopener noreferrer"', c)
    def test_metric_rules(s):
        for p in P:
            for k, v in p['metrics'].items():
                s.assertIn(v['kind'], ('事实', '自述', '未找到'), (p['id'], k))
                s.assertNotIn('未公开', v['text'])
                if v['kind'] == '未找到': s.assertEqual(v['text'], NF, (p['id'], k))
                else: s.assertTrue(v.get('src', '').startswith('http') and v.get('date'), (p['id'], k))
                if k == 'income' and v['kind'] != '未找到':
                    s.assertTrue(v.get('note') or '营收' in v['text'], p['id'])
                    s.assertTrue(re.search(r'营收|收入|赚', v['text'] + v.get('note', '')), p['id'])
            x = p['metrics']['x']; s.assertEqual(x['kind'], '事实'); s.assertIn('2026-11-08', x['date']); s.assertRegex(x['text'], r'^[\d,]+$')
        cnt = lambda k: sum(p['metrics'][k]['kind'] != '未找到' for p in P)
        s.assertEqual((cnt('x'), cnt('xhs'), cnt('wx'), cnt('income')), (14, 2, 1, 4))
    def test_brief_on_every_person_page(s):
        seen = {k: set() for k in ('who', 'pain', 'solve', 'ocean')}
        for p in P:
            f = (G/p['href']).resolve(); h = f.read_text()
            s.assertEqual(h.count('id="brief"'), 1, f.name)
            b = h.index('id="brief"'); main = h.index('<main')
            s.assertGreater(b, main)
            heading = h.rfind('<h1', main, b); heading = heading if heading >= 0 else h.rfind('<h2', main, b)
            s.assertGreater(heading, 0, f.name)  # 标题在摘要之前
            between = h[heading:b]
            s.assertLessEqual(between.count('<p'), 2, f.name)  # 只隔着简介
            s.assertNotIn('class="card"', between, f.name)
            for k in ('面向谁', '具体痛点', '本人怎么解决', 'Ocean 可以做'): s.assertIn(f'<dt>{k}</dt>', h[b:b + 3000])
            s.assertTrue(p['brief']['ocean'].startswith('建议：'), p['id'])
            s.assertTrue('推断' in p['brief']['who'] or '自述' in p['brief']['who'], p['id'])
            for k in seen:
                s.assertNotIn(p['brief'][k], seen[k], (p['id'], k)); seen[k].add(p['brief'][k])
            s.assertIn('href="#brief"', h[h.index('<aside'):h.index('</aside>')], f.name)
    def test_cross_page_links_new_tab(s):
        pages = [G/'index.html', G/'hector.html', X/'creators.html', X/'topic-types.html', X/'topic-lip-growth.html'] + [(G/p['href']).resolve() for p in P]
        for f in pages:
            for t in re.findall(r'<a\b[^>]*>', f.read_text()):
                h = re.search(r'\shref="([^"]*)"', t)
                if not h: continue
                if h.group(1).startswith('#'): s.assertNotIn('target=', t, (f.name, t))
                else: s.assertIn('target="_blank" rel="noopener noreferrer"', t, (f.name, t))
        s.assertNotIn('http-equiv="refresh"', (X/'creators.html').read_text())
        s.assertNotIn('location.', (X/'creators.html').read_text())
    def test_entry_pages_open_module_in_new_tab(s):
        files = PERSON_FILES | {'creators.html', 'topic-types.html', 'topic-lip-growth.html'}
        for f in (X/'index.html', X/'plan.html'):
            n = 0
            for t in re.findall(r'<a\b[^>]*>', f.read_text()):
                h = re.search(r'\shref="([^"]*)"', t)
                if h and (h.group(1).startswith('growth/') or h.group(1).split('#')[0] in files):
                    n += 1; s.assertIn('target="_blank" rel="noopener noreferrer"', t, (f.name, t))
            s.assertGreater(n, 0, f.name)

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
            if kind == 'page': s.assertIn(norm(sec), norm((X/target).read_text()), sid)
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
            s.assertEqual(new.count('id="brief"'), 1, n)  # t224 允许的唯一新增：顶部实操摘要
            new = norm(new)
            back = re.compile(r'\s*<a href="growth/">← 人物成长研究</a>\s*')
            s.assertEqual(len(back.findall(new)), 2, n)  # 侧栏 + 手机目录各一个
            s.assertEqual(re.sub(r'\s+', '', norm(pat.sub('', o, count=1))), re.sub(r'\s+', '', back.sub('', new, count=2)), n)
class NoCompatTraffic(unittest.TestCase):
    def test_no_internal_links_to_compat(s):
        bad = []
        for f in W.rglob('*.html'):
            if 'review' in f.parts or f == X/'creators.html' or '.git' in f.parts: continue
            if re.search(r'href="[^"]*creators\.html', f.read_text(errors='ignore')): bad.append(str(f.relative_to(W)))
        s.assertEqual(bad, [])
    def test_podcast_header_single_back(s):
        h = (G/'hector.html').read_text(); bar = h[h.index('<div class="filebar">'):]; bar = bar[:bar.index('<span')]
        s.assertEqual(re.findall(r'href="([^"]+)"', bar), ['./'])
unittest.main()
