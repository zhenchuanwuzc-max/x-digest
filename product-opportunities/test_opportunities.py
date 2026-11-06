#!/usr/bin/env python3
"""Observable checks for the 2026-11-06 opportunity snapshot."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import apply_opportunities as app

FIXTURE = """<!doctype html><html><head><style>body{margin:0}</style></head><body>
<div class="chips"><button id="tab-jm-ghw">本周涨星</button><button id="tab-jm-ghd">今日涨星</button><button id="tab-jm-ghn">新项目</button></div>
<div class="sub" id="jm-ghw"><p>更新于 2026-11-06 06:18（北京时间）</p>
<ol><li class="mc"><span class="hk">01</span><div class="ht"><h3><a href="https://github.com/pbakaus/impeccable">pbakaus/impeccable</a></h3><p>原简介</p></div><span class="heat">+10,921<small>本周星 · 总 103,844</small></span></li>
<li class="mc"><span class="hk">02</span><div class="ht"><h3><a href="https://github.com/thedotmack/claude-mem">thedotmack/claude-mem</a></h3></div><span class="heat">+8,822</span></li></ol></div>
<div class="sub" id="jm-ghd"><li class="mc"><span class="hk">01</span><a href="https://github.com/pbakaus/impeccable">别的日榜</a></li></div>
</body></html>
"""

OTHER_DAY = FIXTURE.replace("2026-11-06 06:18（北京时间）", "2026-11-07 06:18（北京时间）")
SWAPPED = FIXTURE.replace("https://github.com/pbakaus/impeccable", "https://github.com/example/not-impeccable", 1)


class OpportunityTests(unittest.TestCase):
    def test_summary_angles_are_specific(self):
        app.validate(app.DATA)
        texts = []
        for entry in app.DATA["entries"]:
            blob = "".join(item["text"] for item in entry["summary"])
            self.assertGreaterEqual(blob.count("。"), 2)
            self.assertLessEqual(blob.count("。"), 4)
            texts.append(blob)
            source = " ".join(paragraph["text"] for paragraph in entry["sections"][-1]["paragraphs"])
            self.assertIn("https://", source)
        self.assertEqual(len(set(texts)), 10)

    def test_second_apply_matches_and_keeps_original_heat(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.html"
            path.write_text(FIXTURE, encoding="utf-8")
            limited = [item for item in app.DATA["entries"] if item["slug"] in {"impeccable", "claude-mem"}]
            original_entries = app.DATA["entries"]
            app.DATA["entries"] = limited
            try:
                self.assertEqual(app.apply_page(path), "write")
                once = path.read_text(encoding="utf-8")
                self.assertEqual(app.apply_page(path), "same")
                self.assertEqual(path.read_text(encoding="utf-8"), once)
            finally:
                app.DATA["entries"] = original_entries
        self.assertIn("+10,921", once)
        self.assertIn("原简介", once)
        self.assertIn("本周涨星", once)
        self.assertIn("今日涨星", once)
        self.assertEqual(once.count('data-opp="impeccable"'), 1)
        self.assertIn("product-opportunities/reports/impeccable.html", once)
        self.assertNotIn("data-opp=", once.split('id="jm-ghd"', 1)[1])
        self.assertIn("huashu-design", once)
        self.assertIn("silo-memory", once)

    def test_other_day_is_not_annotated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "later.html"
            path.write_text(OTHER_DAY, encoding="utf-8")
            self.assertEqual(app.apply_page(path), "skip")
            self.assertNotIn("data-opp", path.read_text(encoding="utf-8"))

    def test_rank_with_different_repo_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "swapped.html"
            path.write_text(SWAPPED, encoding="utf-8")
            with self.assertRaises(ValueError):
                app.apply_page(path)

    def test_reports_link_back_to_the_same_tab(self):
        with tempfile.TemporaryDirectory() as tmp:
            app.REPORT_DIR = Path(tmp)
            try:
                written = app.write_reports()
                self.assertEqual(len(written), 10)
                by_slug = {path.stem: path.read_text(encoding="utf-8") for path in written}
            finally:
                app.REPORT_DIR = Path(__file__).resolve().parent / "reports"
        self.assertIn("../../index.html#jm-ghw", by_slug["impeccable"])
        self.assertIn("../../2026-11-06.html#jm-ghw", by_slug["impeccable"])
        self.assertIn("../../index.html#jm-phd", by_slug["rerun"])
        self.assertIn("显示序 5", by_slug["rerun"])
        self.assertIn("price1:29", by_slug["rerun"])
        self.assertIn("不引用提示词", by_slug["dsh-purge"])
        for text in by_slug.values():
            self.assertIn('id="what"', text)
            self.assertIn('id="sources"', text)
            self.assertIn("未", text)
            self.assertNotIn("/tmp/", text)
            self.assertNotIn("/workspace/", text)
            self.assertLess(text.find("目录"), text.find("<main>"))


if __name__ == "__main__":
    unittest.main()
