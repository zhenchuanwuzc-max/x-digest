"""七步工作台：每步有产物/状态/缺口；样本池按实际条数；不夸大；隐私；链接规则；入口与工作台同源。"""
import html, json, re, unittest
from pathlib import Path
X = Path(__file__).resolve().parents[2]; D = json.loads((X/'seven/src/seven.json').read_text())
H = (X/'seven/index.html').read_text(); HUB = (X/'index.html').read_text()
class Seven(unittest.TestCase):
    def test_seven_steps_have_product_state_gap(s):
        s.assertEqual([x['name'] for x in D['steps']], ['变现候选', '找同期对标', '探索版账号档案', '七类选题库', '挑题候选稿', '人工检查', '排期复盘'])
        for x in D['steps']:
            for k in ('out', 'state', 'gap'): s.assertTrue(x[k].strip(), (x['id'], k))
            s.assertIn(f'id="{x["id"]}"', H); s.assertIn(x['state'], H)
    def test_pools_counted_not_inflated(s):
        lat = D['step2']['latest']; n = sum(x['comparable_same_period'] for x in lat)
        c = D['step2']['counts']
        s.assertIn(f"新帖主池 {c['main_pool']} 条（小号候选优先 {c['small_priority']}、粉丝未核次列 {c['followers_unverified']}）；旧帖编辑独列 {c['edited_old']}", D['steps'][1]['out'])
        s.assertIn('爆款未证实', H); s.assertIn('不是真实爆款', H)
        for x in lat:
            s.assertEqual(x['search']['sort_actually_used'], '最新')
            if not x['comparable_same_period']: s.assertTrue(x['why_not'])
        for bad in ('已证实爆款', '已选定', '已排期'): s.assertNotIn(bad, H)
    def test_counts_from_data(s):
        lat = D['step2']['latest']; c = D['step2']['counts']; g = [x for x in lat if x['format'] == '图文']
        s.assertEqual((c['opened'], c['image_posts'], c['image_cards_read'], c['videos_title_only']), (len(lat), len(g), sum(x['cards_read'] for x in g), len(lat) - len(g)))
        s.assertIn(f"打开 {c['opened']} 篇：图文 {c['image_posts']} 篇共读 {c['image_cards_read']} 张卡", H)
        for x in lat: s.assertTrue(x['skeleton'] and x['author_claims'] and x['borrowable_action'])
        for cat in ('痛点', '数字', '资源'): s.assertTrue(next(r for r in D['step4'] if r['cat'] == cat)['latest_refs'], cat)
    def test_source_links_are_bare_urls(s):
        for u in re.findall(r'href="(http[^"]*)"', H): s.assertRegex(u, r'^https://[\x21-\x7e]+$')
    def test_title_check_recomputed(s):
        t = D['step6']['titles']; s.assertEqual(t, {k: len(k) for k in [r['suggested_title'] for r in D['step4']] + [D['step5']['title']]}); s.assertEqual(D['step6']['title_over_20'], [k for k in t if len(k) > 20])
    def test_t244_new_first_small_priority(s):
        lat = D['step2']['latest']; t = [x['tier'] for x in lat]
        s.assertEqual(t, sorted(t, key=list(D['step2']['tiers']).index), 'tier order')
        for x in lat:
            if x['tier'] == 'small_priority': s.assertTrue(x['followers_verified'] and x['comparable_same_period'])
            if x['followers_verified'] is None: s.assertNotEqual(x['tier'], 'small_priority')
            if x['tier'] == 'edited_old': s.assertFalse(x['comparable_same_period'])
        c = D['step2']['counts']; s.assertEqual(c['main_pool'], sum(x['tier'] != 'edited_old' for x in lat))
        for k in D['step2']['tiers']: s.assertEqual(c[k], t.count(k), k)
        L = ' '.join(D['step2']['selection_logic'])
        for w in ('旧帖近期编辑退出新帖主池', '不设固定粉丝门槛', '不按历史累计赞或粉赞比判爆款', '未核不叫小号'): s.assertIn(w, L)
        for bad in ('1万以下', '<1万', '低于1万'): s.assertNotIn(bad, H)
        s.assertEqual(H.count('已验证低粉爆款'), H.count('不称已验证低粉爆款'))
        s.assertLess(H.index('小号候选'), H.index('粉丝未核（次列'))
        s.assertLess(H.index('粉丝未核（次列'), H.index('旧帖近期编辑（独列'))
    def test_t246_daily_topic_block_on_hub(s):
        NS = json.loads((X/'topics/src/new-small.json').read_text())
        s.assertEqual(NS['rules'], D['step2']['selection_logic']); s.assertEqual([c['url'] for c in NS['candidates']], [x['url'] for x in D['step2']['latest']])
        m = re.search(r'<h2 id="newsmall">.*?</div>', HUB, re.S); s.assertTrue(m); b = m.group(0)
        s.assertLess(HUB.index('id="top"'), HUB.index('id="newsmall"')); s.assertLess(HUB.index('id="newsmall"'), HUB.index('id="tools"'))
        for r in NS['rules']: s.assertIn(html.escape(r), b)
        s.assertLess(b.index('小号候选'), b.index('粉丝未核（次列')); s.assertLess(b.index('粉丝未核（次列'), b.index('旧帖近期编辑（独列'))
        s.assertNotIn('xsec', b); s.assertIn('href="#newsmall"', HUB); s.assertIn('../#newsmall', H)
        for t in re.findall(r'<a\b[^>]*href="https[^"]*"[^>]*>', b): s.assertIn('target="_blank"', t)
    def test_status_words(s):
        for w in ('均未选定', '草稿，未发布', '人工检查未做', '排期只是草案', '探索中'): s.assertIn(w, H)
        for w in ('养号 3–5 天', 'iOS'): s.assertIn(w, D['analysis_note'])
        s.assertIn('未核实，不照搬', H)
    def test_privacy(s):
        for t in (H, json.dumps(D, ensure_ascii=False)):
            for bad in ('xsec', 'AI具身牛马', 'following', 'ledger.md', '关注名单里', '/workspace/', '/Users/', 'sources_private', 'xiaohongshu.com/user'): s.assertNotIn(bad, t)
    def test_links_and_no_js(s):
        s.assertNotIn('<script', H)
        for t in re.findall(r'<a\b[^>]*>', H):
            href = re.search(r'href="([^"]*)"', t).group(1)
            if href.startswith('#'): s.assertNotIn('target=', t)
            else: s.assertIn('target="_blank" rel="noopener noreferrer"', t)
    def test_hub_entry_same_source(s):
        s.assertIn('<a href="seven/" target="_blank" rel="noopener noreferrer"><b>七步工作台</b></a>', HUB)
        for x in D['steps']: s.assertIn(f'seven/#{x["id"]}', HUB); s.assertIn(x['state'], HUB)
if __name__ == '__main__': unittest.main()
