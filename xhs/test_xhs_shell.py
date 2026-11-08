import re
import subprocess
import unittest
from pathlib import Path

import apply_xhs_shell

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
    def test_shell_css_fills_the_nav_remainder(self):
        # Ocean 2026-11-08: 小红书站内宽屏铺满，主区占满侧栏外宽度，不再窄栏居中。
        css = SHELL.read_text(encoding="utf-8")
        compact = re.sub(r"\s+", "", css)
        main_rule = re.search(r"(?<![\w-])\.main\{([^}]*)\}", compact).group(1)
        self.assertIn("justify-self:stretch", main_rule)
        self.assertIn("max-width:none", main_rule)
        self.assertNotIn("68rem", compact)
        self.assertIn(".nav:has(>details.navg)", compact)
        self.assertIn(".shell:has(details.navg).mob{display:none;}", compact)

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
        self.assertEqual(sorted(hrefs), sorted(HUB_HREFS))
        grouped = re.findall(
            r'<details class="navg"(?: open)?><summary>(.*?)</summary>(.*?)</details>',
            nav,
        )
        by_group = {name: re.findall(r'href="([^"]+)"', body) for name, body in grouped}
        self.assertEqual(
            by_group,
            {
                "今天": ["#top", "#xhs", "#feed"],
                "选题": ["#picks", "#insp", "#xdiff", "#tingji"],
                "素材与对标": ["#lenny", "#deep", "#raw", "#bench", "#profiles", "#growth"],
                "库与计划": [
                    "#tools",
                    "curriculum.html",
                    "#drafts",
                    "#pos",
                    "#plan",
                    "#main",
                    "#side",
                    "#log",
                ],
            },
        )
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

    def test_restamp_old_hub_keeps_groups_and_is_stable(self):
        old = subprocess.check_output(
            ["git", "show", "main:xhs/index.html"], text=True
        )
        once = apply_xhs_shell.stamp_hub_nav(
            apply_xhs_shell.stamp_link(old, "xhs-shell.css")
        )
        twice = apply_xhs_shell.stamp_hub_nav(
            apply_xhs_shell.stamp_link(once, "xhs-shell.css")
        )
        self.assertEqual(once, twice)
        self.assertIn("<summary>今天</summary>", once)
        self.assertIn('href="growth/"', once)
        self.assertIn("小红书 · 全入口", once)
        self.assertGreater(len(once), 150_000)

    def test_group_hub_links_matches_shipped_nav_and_keeps_new_ids(self):
        shipped = apply_xhs_shell.group_hub_links(apply_xhs_shell._shipped_entries())
        self.assertEqual(shipped + apply_xhs_shell.HUB_TAIL, apply_xhs_shell.HUB_NAV)
        extra = apply_xhs_shell._shipped_entries() + [
            ("fresh", "新信号", "#fresh"),
        ]
        html = apply_xhs_shell.group_hub_links(extra)
        today = re.search(r"<summary>今天</summary>(.*?)</details>", html).group(1)
        self.assertIn('href="#fresh"', today)
        self.assertIn('data-s="fresh"', today)
        self.assertNotIn('href="#fresh"', html.split("</details>", 1)[1])
        self.assertEqual(
            apply_xhs_shell.shell_link("../xhs-shell.css"),
            '<link rel="stylesheet" href="../xhs-shell.css" data-xhs-shell>',
        )


if __name__ == "__main__":
    unittest.main()
