"""Observable contract for the Xiaohongshu shell.

The hub keeps one full entry. Its nav groups the old links and leaves the
growth record as its own page. Day pages keep the same centered column.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
HUB = ROOT / "index.html"
SHELL = ROOT / "xhs-shell.css"
DAY_PAGES = [ROOT / "day" / "index.html", *sorted((ROOT / "day").glob("2026-*.html"))]

HUB_HREFS = [
    "#top",
    "#picks",
    "#xhs",
    "#feed",
    "#insp",
    "#xdiff",
    "#lenny",
    "#deep",
    "#raw",
    "#tools",
    "curriculum.html",
    "#drafts",
    "#pos",
    "#plan",
    "#main",
    "#side",
    "#tingji",
    "#bench",
    "#profiles",
    "#growth",
    "#log",
    "growth/",
    "day/",
]
GROUPS = ["今天", "选题", "素材与对标", "库与计划"]


def aside(html):
    match = re.search(r'<aside class="nav">(.*?)</aside>', html, re.S)
    if not match:
        raise AssertionError("page has no aside.nav")
    return match.group(1)


def attr_ids(html):
    return set(re.findall(r"""\bid\s*=\s*["']([^"']+)["']""", html))


class ShellContract(unittest.TestCase):
    def test_shell_css_centers_main_in_the_nav_remainder(self):
        css = SHELL.read_text(encoding="utf-8")
        compact = re.sub(r"\s+", "", css)
        self.assertIn("justify-self:center", compact)
        self.assertIn("width:min(68rem,calc(100% - 3rem))", compact)
        self.assertIn("max-width:68rem", compact)
        self.assertIn(".nav:has(>details.navg)", compact)
        self.assertIn(".shell:has(details.navg).mob{display:none}", compact)

    def test_pages_load_shell_last_in_head(self):
        for page in [HUB, *DAY_PAGES]:
            html = page.read_text(encoding="utf-8")
            href = "xhs-shell.css" if page.parent == ROOT else "../xhs-shell.css"
            needle = f'<link rel="stylesheet" href="{href}" data-xhs-shell></head>'
            self.assertIn(needle, html, page.relative_to(REPO))

    def test_hub_groups_every_old_link_and_keeps_growth_outside(self):
        html = HUB.read_text(encoding="utf-8")
        nav = aside(html)
        self.assertEqual(re.findall(r"<summary>(.*?)</summary>", nav), GROUPS)
        self.assertEqual(nav.count('<details class="navg" open>'), 2)
        self.assertEqual(nav.count("<details"), 4)
        hrefs = re.findall(r'href="([^"]+)"', nav)
        self.assertEqual(hrefs, HUB_HREFS)
        tail = nav.rsplit("</details>", 1)[-1]
        self.assertIn('href="growth/"', tail)
        self.assertIn("成长记录专属入口", tail)
        self.assertIn('href="day/"', tail)
        ids = attr_ids(html)
        for href in hrefs:
            if href.startswith("#"):
                self.assertIn(href[1:], ids, href)
            else:
                target = (HUB.parent / href)
                self.assertTrue(
                    target.exists() or (target / "index.html").exists(), href
                )
        mob = re.search(r'<nav class="mob">(.*?)</nav>', html, re.S).group(1)
        for href in HUB_HREFS:
            self.assertIn(f'href="{href}"', mob)

    def test_hub_stays_a_full_entry(self):
        html = HUB.read_text(encoding="utf-8")
        self.assertIn("小红书 · 全入口", html)
        self.assertIn("id='picks'", html)
        self.assertIn("id=\"p1\"", html)
        self.assertNotIn('http-equiv="refresh"', html)
        self.assertGreater(len(html), 150_000)


if __name__ == "__main__":
    unittest.main()
