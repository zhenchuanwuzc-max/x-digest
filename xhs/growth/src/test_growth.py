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
import html as _h
e_ = _h.escape
def work_card(h, wid):
    """人物页里某个代表作品卡的片段：从它的 id 到下一个作品卡 / 段落结束。"""
    i = h.index(f'id="{wid}"'); rest = h[i + 5:]
    pre = wid.rsplit('w', 1)[0]
    ends = [j for j in (rest.find('</article>'), rest.find(' id="' + pre + 'w'), rest.find('-audience"')) if j >= 0]
    return h[i:i + 5 + min(ends)]
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
        for k in ('面向谁', '痛点', 'Ocean 借鉴', '怎么验证'): s.assertEqual(top.count(f'<dt>{k}</dt>'), top.count('class="pr"'), k)
        for blk in top.split('<div class="pr">')[1:]:  # 每个方向先出对标人，再出面向谁
            s.assertLess(blk.index('class="bn"'), blk.index('<dt>面向谁</dt>'))
        s.assertGreaterEqual(top[top.index('id="steps"'):].count('<li>'), 3)
        s.assertEqual(H.count('id="p-'), len(P)); s.assertEqual(H.count('id="t-'), len(T))
    def test_each_person_own_target(s):
        targets = [p['href'] for p in P]; s.assertEqual(len(set(targets)), len(P))
        for p in P:
            s.assertNotIn('creators.html', p['href']); s.assertNotIn('#', p['href'])
            f, _ = resolve(G, p['href']); s.assertTrue(f.exists(), p['href'])
    def test_topics_reachable(s):
        for t in T:
            f, a = resolve(G, t['href']); s.assertTrue(f.exists(), t['href'])
            if a: s.assertIn(f'id="{a}"', f.read_text())

class Practice(unittest.TestCase):
    def test_advice_marked_and_evidence_named(s):
        by = {p['id']: p for p in P}
        for r in M['practice']:
            s.assertTrue(r['ocean'].startswith('建议：'), r['ocean'])
            s.assertIn('推断', r['who'])
            s.assertTrue(1 <= len(r['bench']) <= 3)
            for x in r['bench']:
                p = by[x['pid']]
                s.assertIn(f'<p class="bn"><a href="{p["href"]}" target="_blank" rel="noopener noreferrer">{p["name"]}</a>', H)
                ws = {w['id']: w for w in p['brief']['works']}
                s.assertGreaterEqual(len(x['works']), 2, x['pid'])  # 首页每个重点对标人不止一件事
                s.assertEqual(len(set(x['works'])), len(x['works']))
                bm = H[H.index(f'<p class="bn"><a href="{p["href"]}"'):]; bm = bm[:bm.index('</div>')]
                for i in x['works']:
                    s.assertIn(i, ws, (x['pid'], i))  # 首页和人物页是同一件事
                    s.assertIn(f'href="{p["href"]}#{i}" target="_blank" rel="noopener noreferrer">', bm)
                    s.assertIn(ws[i]['step'].replace('“', '&quot;')[:0] or ws[i]['step'][:10], bm.replace('&quot;', '"'))
                s.assertTrue(x['learn'] and x['skip'])
        for o in M['observations']: s.assertTrue(o.startswith('观察：'))
        for st in M['steps']: s.assertTrue(st.startswith('建议'), st)
        top = H[H.index('id="total"'):H.index('id="people"')]
        for bad in ('预计', '保证', '月入', '涨粉到', '我在大厂', '我做过', '排名第'): s.assertNotIn(bad, top)
        s.assertIn('L1', top); s.assertIn('L2', top)
    def test_brief_work_backed(s):
        for p in P:
            b = p['brief']; ws = b['works']; h = (G/p['href']).resolve().read_text()
            s.assertGreaterEqual(len(ws), 2, p['id'])  # 不只一件事；不设统一数量
            s.assertEqual(len({w['id'] for w in ws}), len(ws), p['id'])  # 不同作品卡
            s.assertEqual(len({w['step'] for w in ws}), len(ws), p['id'])  # 每条信息不同
            s.assertEqual(len({w['src'] for w in ws}), len(ws), p['id'])  # 不同一手来源
            top = h[h.index('id="brief"'):]; top = top[:top.index('</section>')]
            for w in ws:
                s.assertIn(f'id="{w["id"]}"', h, (p['id'], w['id']))
                s.assertIn(f'href="{w["src"]}"'.replace('&', '&amp;'), work_card(h, w['id']).replace('&amp;amp;', '&amp;'), (p['id'], w['id']))  # 来源属于该作品卡
                s.assertTrue(w['title'] and w['step'] and w['edge'], (p['id'], w['id']))
                s.assertIn(f'<a href="#{w["id"]}">', top, (p['id'], w['id']))  # 本页锚点，不开新页
                s.assertIn('边界：', top)
            for k in ('who', 'pain', 'solve', 'ocean'): s.assertIn(p['brief'][k][:12], h.replace('&quot;', '"').replace('&#x27;', "'"), (p['id'], k))
        s.assertEqual(len({p['id'] for p in P}), len(P)); s.assertGreaterEqual(len(P), 15)  # 人数取自数据，不写死
    def test_cards_fields_complete(s):
        tbl = H[H.index('<table class="cmp">'):H.index('</table>')]
        heads = re.findall(r'<th scope="col">([^<]+)</th>', tbl)
        s.assertEqual(heads, ['人物', '主要做什么 · 主要用户', 'X 关注者', '小红书粉丝', '公众号关注', '收入'])  # 共享列头
        s.assertIn('「未找到」= 未找到公开数值', H)
        for p in P:
            i = tbl.index(f'id="p-{p["id"]}"'); c = tbl[i:]; c = c[:c.index('</tr>')]
            s.assertIn('主要用户', c); s.assertIn(p['does'][:8], c); s.assertIn(p['users'][:8], c)
            for lab in heads[2:]: s.assertIn(f'data-l="{lab}"', c, (p['id'], lab))
            s.assertIn('<details><summary>数据口径与来源</summary>', c)
            for k, v in p['metrics'].items():
                s.assertTrue(v['kind'] != '自述' or v.get('asof'), (p['id'], k))
                lab = '自述' + (f' · {v.get("asof")}' if v.get('asof') else '') + (' · 历史' if v.get('asof', '2026') < '2026' else '')
                vis = {'事实': '<span class="k f">公开读取</span>', '自述': f'<span class="k s">{lab}</span>', '未找到': '<span class="nf">未找到</span>'}[v['kind']]
                s.assertIn(vis, c, (p['id'], k))
                s.assertIn(e_(v['text']), c, (p['id'], k))  # 完整说法（含「未找到公开数值」）在折叠来源里
            s.assertTrue('推断' in p['users'] or '自述' in p['users'], p['id'])
            s.assertIn(f'href="{p["href"]}" target="_blank" rel="noopener noreferrer"', c)
        s.assertNotIn('class="card pc"', H)
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
            x = p['metrics']['x']
            if x['kind'] == '事实': s.assertIn('2026-11-08', x['date']); s.assertRegex(x['text'], r'^[\d,]+$')
            else: s.assertEqual(x['kind'], '未找到'); s.assertTrue(x.get('note'), p['id'])  # 没有 X 时写明为什么
        for p in P: s.assertNotIn('不适用', p['metrics']['income']['text'] + p['metrics']['income'].get('note', ''))
        s.assertIn('自述 · 2025-09 · 历史', H); s.assertIn('自述 · 2023-07 · 历史', H)
        cnt = lambda k: sum(p['metrics'][k]['kind'] != '未找到' for p in P)
        s.assertEqual((cnt('x'), cnt('xhs'), cnt('wx'), cnt('income')), (14, 21, 1, 4))  # 小红书：知新 + 首批 3 + 第二批 4 + 第三批 5 + 第四批 6
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
            for k in ('面向谁', '具体痛点', '他咋做', 'Ocean 可以做'): s.assertIn(f'<dt>{k}</dt>', h[b:b + 3000])
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

class Zhixin(unittest.TestCase):
    """第 15 人（小红书只读采集）的口径：更正后的采集时间、图卡内嵌阅读数不当数据、别人经历不归他、未核出处不当事实。"""
    h = (X/'zhixin.html').read_text()
    def test_capture_time_corrected(s):
        s.assertIsNone(re.search(r'20:[1-3]\d', s.h))  # 采集只写日期；20:20–30 作废
        s.assertIn('2026-11-08', s.h)
    def test_embedded_reads_not_used_as_data(s):
        for n in ('2179', '5069'):
            for m in re.finditer(n, s.h): s.assertIn('排版元素', s.h[m.start():m.start() + 80])
    def test_attribution_boundaries(s):
        s.assertIn('Katie', s.h); s.assertIn('经历属于', s.h)
        s.assertIn('未核，不作事实', s.h)  # 平台 AI 给的访谈出处
        s.assertIn('不背书', s.h); s.assertIn('署仓库名', s.h)  # GitHub 卡有仓库署名，不能写成全无出处
        s.assertIn('编辑于 2025-09-23', s.h); s.assertIn('评论最早 2025-09-19', s.h)
        s.assertIn('2026.11.04', s.h); s.assertIn('2天前', s.h)
    def test_no_invented_level_or_growth(s):
        s.assertIn('不写增长轨迹', s.h)
        z = next(p for p in P if p['id'] == 'zhixin')
        s.assertEqual(z['metrics']['xhs']['kind'], '事实'); s.assertEqual(z['metrics']['xhs']['date'], '2026-11-08 主页截图')
        s.assertIn('『这些观点AI，我更容易做；hah』', z['brief']['ocean']); s.assertTrue(z['brief']['ocean'].startswith('建议：'))

class OceanPositioning(unittest.TestCase):
    """t241：账号身份仍在摸索——首页与源都不得把定位写死。"""
    def test_home_matches_source_and_not_fixed(s):
        pos = json.loads((G/'src/people.json').read_text())['positioning']['text']
        s.assertIn('账号方向仍在探索', pos); s.assertIn(pos, H)
        for bad in ('大厂产品经理，讲进门后', '不求职', '按 Ocean 的定位'): s.assertNotIn(bad, pos + H)
        d = json.loads((G/'src/people.json').read_text()); n = len({b['pid'] for r in d['practice'] for b in r['bench']})
        s.assertIn(f'出自 {n} 位人物页', H); s.assertNotIn('创作中心 · 定位', H)

class FollowBatch1(unittest.TestCase):
    """小红书关注首批 3 人：覆盖度来自 follow_b1_cards.COV；公开页不泄露关注关系与带 token 链接。"""
    IDS = ('lulu-ai', 'laoa-jinjie', 'karl-aigc')
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b1_cards as f; s.f = f
        s.h = {i: (X/f'{i}.html').read_text() for i in s.IDS}
    def test_coverage_complete_and_counted_from_pages(s):
        for i in s.IDS:
            s.assertEqual(s.f.gaps(i), {}, i)
            for w, c in s.f.COV[i].items():
                if c != s.f.VIDEO: s.assertEqual(sorted(c['read']), list(range(1, c['total'] + 1)), (i, w))
        s.assertEqual(len(s.f.COV['karl-aigc']['w3']['read']), 14)
        for h in s.h.values():
            for bad in ('待补', '部分可读', '待重试'): s.assertNotIn(bad, h)
    def test_video_scope(s):
        s.assertIn('只看标题和描述', s.h['lulu-ai']); s.assertNotIn('视频未看待补', s.h['lulu-ai'])
    def test_privacy(s):
        for h in s.h.values():
            for bad in ('xsec', 'following', '关注名单', '5098143774'): s.assertNotIn(bad, h)
        for i in s.IDS:
            L = (Path(__file__).resolve().parents[3]/f'review/creator-growth-20261108/{i}-ledger.md').read_text()
            for bad in ('xsec', 'AI具身牛马', '已关注', 'following'): s.assertNotIn(bad, L)
    def test_neutral_heading_entry_and_no_fixed_positioning(s):
        for h in s.h.values():
            s.assertNotIn('AI具身牛马', h); s.assertIn('<h2>可借鉴的做法</h2>', h)
            s.assertIn('不是按“最新”排序筛出的热门', h)  # t239：实际入口是主页置顶/近期
            for bad in ('定位里', '定位内', '不求职', '远高于', '互动最高'): s.assertNotIn(bad, h)
        for p in P:
            if p['id'] in s.IDS: s.assertNotIn('定位', p['brief']['ocean'])
    def test_boundaries(s):
        s.assertIn('不合并', s.h['laoa-jinjie']); s.assertIn('老A的AI研究所', s.h['laoa-jinjie'])
        for i in ('laoa-jinjie', 'karl-aigc'):
            s.assertIn('不判断归属或抄袭', s.h[i]); s.assertIn('不当交付或收入', s.h[i])
        s.assertIn('标题与主体不一致', s.h['karl-aigc'])
        for p in P:
            if p['id'] in s.IDS:
                s.assertEqual(p['metrics']['income']['kind'], '未找到'); s.assertEqual(p['metrics']['x']['kind'], '未找到')
                s.assertEqual(p['metrics']['xhs']['date'], '2026-11-08 主页截图')

class FollowBatch2(unittest.TestCase):
    """小红书关注第二批 3 人：覆盖度来自 follow_b2_cards.COV；隐私、品牌身份、积分与视频范围边界。"""
    IDS = ('laoa-yanjiusuo', 'jason-effi', 'accio-work', 'zhiwei')
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b2_cards as f; s.f = f
        s.h = {i: (X/f'{i}.html').read_text() for i in s.IDS}
    def test_coverage(s):
        for i in s.IDS:
            s.assertEqual(s.f.gaps(i), {}, i)
        s.assertEqual(sum(c['total'] for c in s.f.COV['laoa-yanjiusuo'].values()), 37)
        s.assertEqual(s.f.COV['jason-effi']['w2'], s.f.VIDEO); s.assertEqual(s.f.COV['accio-work']['w2'], s.f.VIDEO)
        for i in ('jason-effi', 'accio-work', 'zhiwei'): s.assertIn('只看标题和描述', s.h[i])
        s.assertEqual(set(s.f.COV['zhiwei'].values()), {s.f.VIDEO})
        for h in s.h.values():
            for bad in ('待补', '部分可读', '待重试'): s.assertNotIn(bad, h)
    def test_multiple_actions_with_sources(s):
        for p in P:
            if p['id'] in s.IDS:
                ws = p['brief']['works']; s.assertGreaterEqual(len(ws), 2)
                s.assertEqual(len({w['src'] for w in ws}), len(ws))
                for w in ws: s.assertIn(w['src'], s.h[p['id']]); s.assertNotIn('?', w['src'])
    def test_privacy(s):
        for i, h in s.h.items():
            for bad in ('xsec', 'following', '关注名单', '5098143774', 'AI具身牛马', '/workspace/'): s.assertNotIn(bad, h)
            L = (Path(__file__).resolve().parents[3]/f'review/creator-growth-20261108/{i}-ledger.md').read_text()
            for bad in ('xsec', 'AI具身牛马', '5098143774', '已关注', 'following', 'inventory'): s.assertNotIn(bad, L)
    def test_codex_fixes(s):
        for i in ('jason-effi', 'accio-work', 'zhiwei'):
            s.assertNotIn('视频未播放', s.h[i]); s.assertIn('未主动播放、未观看', s.h[i])
        s.assertNotIn('至少 3 位读者', s.h['jason-effi'])
        for h in s.h.values():  # 可见评论放事实格，“假设”格只放未验证的推断
            for m in re.finditer(r'<span class="lv h">假设</span>(.*?)</', h): s.assertNotIn('可见评论', m.group(1))
            s.assertIn('可见评论与回复', h)
    def test_boundaries(s):
        s.assertIn('不合并', s.h['laoa-yanjiusuo']); s.assertIn('老A的AI进阶实操', s.h['laoa-yanjiusuo'])
        s.assertIn('不判断归属或抄袭', s.h['laoa-yanjiusuo']); s.assertIn('不当交付或收入', s.h['laoa-yanjiusuo'])
        A = s.h['accio-work']
        s.assertIn('不推断法律主体', A); s.assertIn('Credits 是积分', A); s.assertIn('活动期，不等于发布日', A)
        s.assertIn('不当作者原文', s.h['jason-effi'])
        Z = s.h['zhiwei']; s.assertIn('标题描述层分析', Z); s.assertIn('不是完整通读', Z); s.assertIn('不当经营事实', Z); s.assertIn('不是创业结果', Z)
        for h in s.h.values():
            s.assertIn('不是按“最新”排序筛出的热门', h); s.assertIn('<h2>可借鉴的做法</h2>', h)
            for bad in ('爆款', '小号优先', '新帖主池'): s.assertNotIn(bad, h)
        for p in P:
            if p['id'] in s.IDS:
                s.assertEqual(p['metrics']['income']['text'], NF); s.assertEqual(p['metrics']['x']['kind'], '未找到')

class FollowBatch3(unittest.TestCase):
    """第三批（可瑞吉）：标题描述层；不照搬虚构经历说法；自述薪资不当收入；隐私。"""
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b3_cards as f; s.f = f; s.h = (X/'keruiji.html').read_text()
        s.p = next(p for p in P if p['id'] == 'keruiji')
    def test_scope_and_coverage(s):
        s.assertEqual(s.f.gaps('keruiji'), {}); s.assertEqual(set(s.f.COV['keruiji'].values()), {s.f.VIDEO})
        for w in ('标题描述层分析', '不是完整通读', '未主动播放、未观看'): s.assertIn(w, s.h)
        s.assertNotIn('视频未看待补', s.h)
    def test_no_fake_experience_advice(s):
        s.assertIn('不照搬“说做过我的实习生”', s.h); s.assertIn('虚假履历风险', s.p['brief']['ocean'])
        for bad in ('虚构经历', '造假', '欺诈', '骗'): s.assertNotIn(bad, s.h)  # 视频未看，不对作者下判断
        take = re.search(r'<h2>可借鉴的做法</h2>(.*?)</section>', s.h, re.S).group(1)
        for m in re.finditer(r'<li>(.*?)</li>', take):
            if '实习生' in m.group(1): s.assertTrue('不' in m.group(1) or '风险' in m.group(1), m.group(1))
    def test_self_reported_numbers_not_income(s):
        s.assertEqual(s.p['metrics']['income']['text'], NF); s.assertEqual(s.p['metrics']['wx']['text'], NF)
        s.assertIn('不合算', s.h); s.assertIn('不当收入', s.h)
        for bad in ('年收入约', '年薪约', '存款约', '万元年'): s.assertNotIn(bad, s.h)
    def test_privacy_and_links(s):
        L = (Path(__file__).resolve().parents[3]/'review/creator-growth-20261108/keruiji-ledger.md').read_text()
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')  # 采集账号过滤词在仓库外
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        for t in (s.h, L):
            for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态'] + priv: s.assertNotIn(bad, t)
        s.assertNotIn('发布时间不同', s.h); s.assertNotIn('普通内容', s.h)
        for w in s.p['brief']['works']: s.assertIn(w['src'], s.h); s.assertNotIn('?', w['src'])

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
class FollowBatch3Will(unittest.TestCase):
    """第三批 Will：图文全读；时间存疑不当新帖；自述年薪/课程销量不当收入；归属与隐私。"""
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b3_cards as f; s.f = f; s.h = (X/'will.html').read_text()
        s.p = next(p for p in P if p['id'] == 'will')
    def test_coverage_and_links(s):
        s.assertEqual(s.f.gaps('will'), {}); s.assertIn('已读 8/8', s.h); s.assertIn('已读 6/6', s.h)
        s.assertIn('explore/6ae6e6fd000000002301106d', s.h); s.assertIn('《上新：如何系统学习AI产品的UX设计？》', s.h)
        s.assertIn('explore/6546fd84000000001e02c4ed', s.h); s.assertIn('《我的12年职场路，4个重要认知》', s.h)
    def test_time_and_money_claims(s):
        for w in ('时间存疑', '不当最新新帖', '不当收入', '只等了约 6 秒'): s.assertIn(w, s.h)
        for bad in ('20 秒', '统一等待', '编辑刷新了', '标题描述层', '普通内容'): s.assertNotIn(bad, s.h)
        s.assertEqual(s.p['metrics']['income']['text'], '未找到公开数值'); s.assertEqual(s.p['metrics']['wx']['text'], '未找到公开数值')
    def test_privacy(s):
        L = (Path(__file__).resolve().parents[3]/'review/creator-growth-20261108/will-ledger.md').read_text()
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        for t in (s.h, L):
            for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态'] + priv: s.assertNotIn(bad, t)
            s.assertIsNone(re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', t))  # 公开邮箱不抄录
class FollowBatch3Huguagua(unittest.TestCase):
    """第三批胡呱呱：图文全读；同一梗图形式不夸大；不补身份收入；不照搬素材；隐私。"""
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b3_cards as f; s.f = f; s.h = (X/'huguagua.html').read_text()
        s.p = next(p for p in P if p['id'] == 'huguagua')
    def test_coverage_and_claims(s):
        s.assertEqual(s.f.gaps('huguagua'), {}); s.assertIn('已读 4/4', s.h); s.assertIn('已读 5/5', s.h)
        for w in ('不夸大成两种商业模式', '不是事实报道', '不照搬梗图', '不迁移作者的身份', '你没有说明你还不成功'): s.assertIn(w, s.h)
        for bad in ('普通内容', '说服你', '标题描述层'): s.assertNotIn(bad, s.h)
        s.assertEqual(s.p['metrics']['income']['text'], '未找到公开数值')
    def test_privacy(s):
        L = (Path(__file__).resolve().parents[3]/'review/creator-growth-20261108/huguagua-ledger.md').read_text()
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        for t in (s.h, L):
            for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态', 'channel_type'] + priv: s.assertNotIn(bad, t)
class FollowBatch3Claire(unittest.TestCase):
    """第三批 Claire：图文全读；去世/病况只是转述；“收入破百万”不当收入；不点名、不跨平台认归属；隐私。"""
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b3_cards as f; s.f = f; s.h = (X/'claire.html').read_text()
        s.p = next(p for p in P if p['id'] == 'claire')
        s.L = (Path(__file__).resolve().parents[3]/'review/creator-growth-20261108/claire-ledger.md').read_text()
    def test_coverage_and_claims(s):
        s.assertEqual(s.f.gaps('claire'), {}); s.assertIn('已读 7/7', s.h)
        for w in ('不当收入', '口径未写明', '不诊断', '不跨平台认定归属', '只看标题'): s.assertIn(w, s.h)
        for bad in ('普通内容', '人民币', '净利润一百多万', '吟游诗人'): s.assertNotIn(bad, s.h)
        s.assertEqual(s.p['metrics']['income']['text'], '未找到公开数值')
    def test_privacy(s):
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        for t in (s.h, s.L):
            for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态', 'channel_type', 't老师', '吟游诗人'] + priv: s.assertNotIn(bad, t)
class FollowBatch3NoHeatCompare(unittest.TestCase):
    """第三批四页：不把两篇互动数放在一起比（各条目自己的底栏数可留）。"""
    def test_no_cross_post_engagement(s):
        for slug in ('keruiji', 'will', 'huguagua', 'claire', 'fufujie'):
            h = (X/f'{slug}.html').read_text(); cmp = h[h.index('id="compare"'):h.index('id="voice"')]
            s.assertNotIn('底栏数差很多', h); s.assertNotIn('底栏', cmp); s.assertNotIn('能火', h); s.assertIn('<h3>可见评论与作者回应</h3>', h)
class FollowBatch3Fufujie(unittest.TestCase):
    """第三批付付姐：视频标题描述层；100w 不当收入；宣传自述不审计；权益写法不判矛盾；不断言水军；隐私。"""
    def setUp(s):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b3_cards as f; s.f = f; s.h = (X/'fufujie.html').read_text()
        s.p = next(p for p in P if p['id'] == 'fufujie')
        s.L = (Path(__file__).resolve().parents[3]/'review/creator-growth-20261108/fufujie-ledger.md').read_text()
    def test_claims(s):
        s.assertEqual(s.f.COV['fufujie']['w1'], s.f.VIDEO); s.assertIn('已读 9/9', s.h); s.assertIn('标题描述层', s.h)
        for w in ('不当作者收入', '不判为矛盾', '不当另一售价', '未审计'): s.assertIn(w, s.h)
        for bad in ('疑似宣传', '水军', '口径不一致', '已赚到100w', '普通内容'): s.assertNotIn(bad, s.h)
        s.assertNotIn('疑似宣传', s.L)
        s.assertEqual(s.p['metrics']['income']['text'], '未找到公开数值')
    def test_privacy(s):
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        for t in (s.h, s.L):
            for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态', 'channel_type'] + priv: s.assertNotIn(bad, t)
class FollowBatch4(unittest.TestCase):
    """第四批（黑灯、门腔）：覆盖完整；年份不推；中性评论标题；不比热度；自述不当事实；不推照片身份身体；隐私。"""
    @classmethod
    def setUpClass(c):
        import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'))
        import follow_b4_cards as f; c.f = f; R = Path(__file__).resolve().parents[3]/'review/creator-growth-20261108'
        c.H = {k: (X/f'{k}.html').read_text() for k in ('heideng', 'menqiang', 'lidan', 'pupu-wanzi', 'sinuo', 'taozi')}
        c.L = {k: (R/f'{k}-ledger.md').read_text() for k in ('heideng', 'menqiang', 'lidan', 'pupu-wanzi', 'sinuo', 'taozi')}
        c.Pp = {p['id']: p for p in P}
    def test_common(s):
        for k, h in s.H.items():
            s.assertEqual(s.f.gaps(k), {}); s.assertIn('<h3>可见评论与作者回应</h3>', h)
            cmp = h[h.index('id="compare"'):h.index('id="voice"')]
            s.assertNotIn('底栏', cmp); s.assertNotIn('能火', h); s.assertNotIn('普通内容', h)
            s.assertEqual(s.Pp[k]['metrics']['income']['text'], '未找到公开数值')
    def test_heideng(s):
        h = s.H['heideng']
        for w in ('已读 1/1', '已读 7/7', '初发年份未知', '不当现在可购买', '不等于票房', '原因未说明', '只是作者自述'): s.assertIn(w, h)
    def test_menqiang(s):
        h = s.H['menqiang']
        for w in ('已读 16/16', '未主动播放、未观看', '标题描述层', '不推地点、身份', '不当小号', '关系未'): s.assertIn(w, h)
        for bad in ('减脂成功', '瘦了', '日本'): s.assertNotIn(bad, h)
    def test_lidan(s):
        h = s.H['lidan']
        for w in ('已读 5/5', '未主动播放、未观看', '标题描述层', '2024-08-12', '不推健康', '不当新帖', '读者说法'): s.assertIn(w, h)
    def test_pupu(s):
        h = s.H['pupu-wanzi']
        for w in ('已读 12/12', '未主动播放、未观看', '标题描述层', '是否商业合作未知', '不当实测', 'LIVE 动态未看'): s.assertIn(w, h)
        for bad in ('广告', '假评论', '软文'): s.assertNotIn(bad, h)
    def test_sinuo(s):
        h = s.H['sinuo']
        for w in ('已读 1/1', '已读 4/4', '平台 AI', '不当讲者原话', '演讲视频未看', '不当实际爆款', '未实测', '自述，未核'): s.assertIn(w, h)
        for bad in ('演讲已读', '讲者原话：'): s.assertNotIn(bad, h)
    def test_taozi(s):
        h = s.H['taozi']
        for w in ('未主动播放、未观看', '不是作者原话', '编辑于 2025-08-26', '不是首发日期', '自述，未核', '不比热度', '只看标题'): s.assertIn(w, h)
        for bad in ('年入百万', '爆款', '视频里她说'): s.assertNotIn(bad, h)
    def test_privacy(s):
        pf = Path('/workspace/creator-growth-20261108/following/private-drop-patterns.txt')
        priv = [l.strip() for l in pf.read_text().splitlines() if l.strip()] if pf.exists() else []
        names = json.loads(Path('/workspace/creator-growth-20261108/following/private-public-subs-b4.json').read_text())['banned'] if Path('/workspace/creator-growth-20261108/following/private-public-subs-b4.json').exists() else []  # 被替换掉的名字在仓库外
        for k in s.H:
            for t in (s.H[k], s.L[k]):
                for bad in ['xsec', 'following', 'inventory', '/workspace/', '登录态', 'channel_type'] + names + priv: s.assertNotIn(bad, t, k)
                s.assertIsNone(re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', t), k)
unittest.main()
