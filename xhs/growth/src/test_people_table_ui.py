"""人物表派生元数据与交互：排序键、未知置尾、语言证据、受众并集、清空与空态。"""
import html as H
import json
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright

D = Path(__file__).resolve().parent
G = D.parent
import sys
sys.path.insert(0, str(D))
import people_table_ui as ui
import build_index

P = json.loads((D / 'people.json').read_text())['people']


class ParseLangTags(unittest.TestCase):
    def test_parse_wan_and_plain(s):
        s.assertEqual(ui.parse_count('约 10 万', '自述'), 100000)
        s.assertEqual(ui.parse_count('12 万', '自述'), 120000)
        s.assertEqual(ui.parse_count('106,816', '事实'), 106816)
        s.assertEqual(ui.parse_count('1.7 万', '事实'), 17000)
        s.assertEqual(ui.parse_count('268.7 万', '事实'), 2687000)
        s.assertIsNone(ui.parse_count('未找到公开数值', '未找到'))

    def test_lang_needs_evidence(s):
        zh = [p for p in P if ui.content_lang(p)[0] == 'zh']
        unk = [p for p in P if ui.content_lang(p)[0] == 'unknown']
        s.assertEqual(len(zh) + len(unk), len(P))
        s.assertGreaterEqual(len(zh), 1)
        s.assertGreaterEqual(len(unk), 1)
        by = {p['id']: p for p in P}
        for pid in ('lenny', 'shreyas', 'levelsio', 'hector'):
            s.assertEqual(ui.content_lang(by[pid])[0], 'unknown', pid)
        s.assertEqual(ui.content_lang(by['kazike'])[0], 'zh')

    def test_audience_from_users_keeps_inference(s):
        by = {p['id']: p for p in P}
        tags, basis = ui.audience_tags(by['qiaomu'])
        s.assertIn('PM', tags)
        s.assertTrue(any('推断' in b for b in basis))
        tags, _ = ui.audience_tags(by['sinuo'])
        s.assertIn('PM', tags)

    def test_row_meta_preserves_display_text(s):
        for i, p in enumerate(P):
            m = ui.row_meta(p, i)
            s.assertEqual(m['x_text'], p['metrics']['x']['text'])
            s.assertEqual(m['xhs_text'], p['metrics']['xhs']['text'])
            s.assertEqual(m['ord'], i)


class RenderedMarkup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = build_index.render()

    def test_toolbar_and_data_attrs(s):
        s.assertIn('id="people-toolbar"', s.h)
        s.assertIn('people_table.js', s.h)
        for i, p in enumerate(P):
            m = ui.row_meta(p, i)
            frag = s.h[s.h.index(f'id="p-{p["id"]}"'):]
            frag = frag[:frag.index('</tr>')]
            s.assertIn(f'data-ord="{i}"', frag)
            s.assertIn(f'data-lang="{m["lang"]}"', frag)
            if m['x'] is None:
                s.assertIn('data-x=""', frag)
            else:
                s.assertIn(f'data-x="{m["x"]}"', frag)
            s.assertIn(H.escape(p['metrics']['x']['text']), frag)
            s.assertIn(H.escape(p['users'][:6]), frag)

    def test_source_fields_untouched(s):
        raw = (D / 'people.json').read_text()
        for p in P:
            s.assertIn(p['users'], raw)
            s.assertIn(p['does'], raw)


class Interaction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (G / 'index.html').write_text(build_index.render())
        cls.url = 'file://' + str((G / 'index.html').resolve())

    def test_sort_filter_clear_empty_aria(s):
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
            page = b.new_page(viewport={'width': 1280, 'height': 900})
            page.goto(s.url)
            page.wait_for_selector('#people-toolbar')

            def ids():
                return page.evaluate(
                    "() => [...document.querySelectorAll('table.cmp tbody tr')]"
                    ".filter(r => !r.hidden).map(r => r.id)"
                )

            base = ids()
            s.assertEqual(len(base), len(P))

            page.click('button[data-sort="x"][data-dir="-1"]')
            xs = page.evaluate(
                "() => [...document.querySelectorAll('table.cmp tbody tr')]"
                ".filter(r => !r.hidden).map(r => ({id:r.id, x:r.getAttribute('data-x')}))"
            )
            known = [r for r in xs if r['x'] != '']
            unknown = [r for r in xs if r['x'] == '']
            nums = [int(r['x']) for r in known]
            s.assertEqual(nums, sorted(nums, reverse=True))
            s.assertEqual([r['id'] for r in xs[-len(unknown):]], [r['id'] for r in unknown])

            page.click('button[data-sort="x"][data-dir="1"]')
            xs = page.evaluate(
                "() => [...document.querySelectorAll('table.cmp tbody tr')]"
                ".filter(r => !r.hidden).map(r => ({id:r.id, x:r.getAttribute('data-x')}))"
            )
            known = [r for r in xs if r['x'] != '']
            unknown = [r for r in xs if r['x'] == '']
            s.assertEqual([int(r['x']) for r in known], sorted(int(r['x']) for r in known))
            s.assertTrue(all(r['x'] == '' for r in xs[-len(unknown):]))

            page.click('button[data-sort="xhs"][data-dir="-1"]')
            xhs = page.evaluate(
                "() => [...document.querySelectorAll('table.cmp tbody tr')]"
                ".filter(r => !r.hidden).map(r => r.getAttribute('data-xhs')).filter(v => v !== '')"
            )
            s.assertEqual([int(v) for v in xhs], sorted((int(v) for v in xhs), reverse=True))
            s.assertIn('100000', xhs)

            page.click('button[data-sort="ord"]')
            s.assertEqual(ids(), base)

            page.click('button[data-lang="zh"]')
            expect_zh = [f'p-{p["id"]}' for p in P if ui.content_lang(p)[0] == 'zh']
            s.assertEqual(sorted(ids()), sorted(expect_zh))
            page.click('button[data-lang="all"]')
            s.assertEqual(len(ids()), len(P))

            page.click('button[data-tag="PM"]')
            pm = set(ids())
            s.assertGreater(len(pm), 0)
            page.click('button[data-tag="开发者"]')
            both = set(ids())
            s.assertGreaterEqual(len(both), len(pm))
            page.click('button[data-lang="zh"]')
            for rid in ids():
                lang = page.get_attribute(f'#{rid}', 'data-lang')
                aud = (page.get_attribute(f'#{rid}', 'data-audience') or '').split()
                s.assertEqual(lang, 'zh')
                s.assertTrue('PM' in aud or '开发者' in aud)

            page.click('button[data-clear]')
            page.click('button[data-lang="zh"]')
            if page.locator('button[data-tag="营销人"]').count():
                page.click('button[data-tag="营销人"]')
                if len(ids()) == 0:
                    s.assertFalse(page.is_hidden('#people-empty'))
            page.click('button[data-clear]')
            s.assertEqual(ids(), base)
            s.assertTrue(page.is_hidden('#people-empty'))

            s.assertEqual(page.get_attribute('button[data-sort="ord"]', 'aria-pressed'), 'true')
            page.click('button[data-sort="x"][data-dir="-1"]')
            s.assertEqual(page.get_attribute('button[data-sort="x"][data-dir="-1"]', 'aria-pressed'), 'true')
            s.assertEqual(page.get_attribute('button[data-sort="ord"]', 'aria-pressed'), 'false')

            page.set_viewport_size({'width': 390, 'height': 800})
            page.click('button[data-clear]')
            s.assertEqual(page.evaluate('document.documentElement.scrollWidth - innerWidth'), 0)
            b.close()


if __name__ == '__main__':
    unittest.main()
