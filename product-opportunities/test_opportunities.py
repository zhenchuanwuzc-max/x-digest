#!/usr/bin/env python3
"""Observable checks for the 2026-11-06 opportunity snapshot."""

from __future__ import annotations

import json
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
            if entry.get("sections"):
                source = " ".join(paragraph["text"] for paragraph in entry["sections"][-1]["paragraphs"])
                self.assertIn("https://", source)
        self.assertEqual(len(set(texts)), len(app.DATA["entries"]))

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

    def test_week_id_does_not_match_the_daily_panel(self):
        page = """<!doctype html><html><head><style>body{margin:0}</style></head><body>
<div class="sub" id="jm-phd"><p>更新于 2026-11-06 06:18（北京时间）</p>
<ol><li class="mc"><span class="hk">01</span><div class="ht"><h3><a href="https://www.producthunt.com/products/glasshand">Glasshand</a></h3><p>原简介</p></div><span class="heat">293</span></li></ol></div>
</body></html>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "2026-11-06.html"
            path.write_text(page, encoding="utf-8")
            self.assertEqual(app.apply_page(path), "write")
            text = path.read_text(encoding="utf-8")
            card = text.split("products/glasshand", 1)[1].split("</li>", 1)[0]
            self.assertIn("日榜显示序 1", card)
            self.assertNotIn("周榜显示序 4", card)
            self.assertEqual(card.count("data-opp="), 1)

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
            self.assertEqual(app.apply_page(path), "write")
            text = path.read_text(encoding="utf-8")
            swapped = text.split('id="jm-ghw"', 1)[1].split("</li>", 1)[0]
            self.assertIn("example/not-impeccable", swapped)
            self.assertNotIn("huashu-design", swapped)
            self.assertNotIn("product-opportunities/reports/", swapped)
            self.assertIn("待研究", swapped)

    def test_notes_follow_the_link_when_ranks_swap(self):
        swapped = FIXTURE.replace(
            '<span class="hk">01</span><div class="ht"><h3><a href="https://github.com/pbakaus/impeccable">',
            '<span class="hk">09</span><div class="ht"><h3><a href="https://github.com/pbakaus/impeccable">',
        ).replace(
            '<span class="hk">02</span><div class="ht"><h3><a href="https://github.com/thedotmack/claude-mem">',
            '<span class="hk">01</span><div class="ht"><h3><a href="https://github.com/thedotmack/claude-mem">',
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "2026-11-06.html"
            path.write_text(swapped, encoding="utf-8")
            self.assertEqual(app.apply_page(path), "write")
            text = path.read_text(encoding="utf-8")
            impeccable = text.split("pbakaus/impeccable", 1)[1].split("</li>", 1)[0]
            claude = text.split("thedotmack/claude-mem", 1)[1].split("</li>", 1)[0]
            self.assertIn("huashu-design", impeccable)
            self.assertIn("silo-memory", claude)
            self.assertNotIn("silo-memory", impeccable)

    def test_reuse_names_the_original_check_date(self):
        page = """<!doctype html><html><head><style>body{margin:0}</style></head><body>
<div class="sub" id="jm-ghw"><p>更新于 2026-11-08 07:00（北京时间）</p>
<ol><li class="mc"><span class="hk">04</span><div class="ht"><h3><a href="https://github.com/pbakaus/impeccable">pbakaus/impeccable</a></h3><p>原简介</p></div><span class="heat">+10</span></li>
<li class="mc"><span class="hk">01</span><div class="ht"><h3><a href="https://example.com/new-agent">New Agent</a></h3><p>新</p></div><span class="heat">+1</span></li></ol></div>
</body></html>"""
        research = {
            "date": "2026-11-08",
            "boards": ["jm-ghw"],
            "items": [
                {
                    "product": "impeccable",
                    "match_href": "https://github.com/pbakaus/impeccable",
                    "panel": "jm-ghw",
                    "status": "reuse",
                    "verified_on": "2026-11-06",
                    "report": "impeccable.html",
                    "summary": ["沿用 11 月 6 日的核验。", "仓库仍是设计技能，不是新的用户数统计。"],
                    "meta": "显示序随当天榜单。",
                    "sources": ["https://github.com/pbakaus/impeccable"],
                },
                {
                    "product": "new-agent",
                    "match_href": "https://example.com/new-agent",
                    "panel": "jm-ghw",
                    "status": "pending",
                    "summary": ["这一天还没有核验。", "待研究。"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            research_dir = Path(tmp) / "research"
            research_dir.mkdir()
            (research_dir / "2026-11-08.json").write_text(json.dumps(research), encoding="utf-8")
            path = Path(tmp) / "2026-11-08.html"
            path.write_text(page, encoding="utf-8")
            original = app.RESEARCH_DIR
            app.RESEARCH_DIR = research_dir
            try:
                self.assertEqual(app.apply_page(path), "write")
                self.assertEqual(app.apply_page(path), "same")
            finally:
                app.RESEARCH_DIR = original
            text = path.read_text(encoding="utf-8")
            self.assertIn("核验于 2026-11-06", text)
            self.assertIn("product-opportunities/reports/impeccable.html", text)
            pending = text.split("example.com/new-agent", 1)[1].split("</li>", 1)[0]
            self.assertIn("待研究", pending)
            self.assertNotIn("opp-more", pending)
            self.assertNotIn("11 月 6 日的核验", pending)

    def test_missing_report_does_not_link(self):
        page = FIXTURE.replace("2026-11-06", "2026-11-09")
        research = {
            "date": "2026-11-09",
            "boards": ["jm-ghw"],
            "items": [
                {
                    "product": "impeccable",
                    "match_href": "https://github.com/pbakaus/impeccable",
                    "panel": "jm-ghw",
                    "status": "ready",
                    "verified_on": "2026-11-09",
                    "report": "does-not-exist.html",
                    "summary": ["分析已经写了。", "报告文件还没有进仓库。"],
                    "meta": "当天核验。",
                    "sources": ["https://github.com/pbakaus/impeccable"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            research_dir = Path(tmp) / "research"
            research_dir.mkdir()
            (research_dir / "2026-11-09.json").write_text(json.dumps(research), encoding="utf-8")
            path = Path(tmp) / "page.html"
            path.write_text(page, encoding="utf-8")
            original = app.RESEARCH_DIR
            app.RESEARCH_DIR = research_dir
            try:
                self.assertEqual(app.apply_page(path), "write")
            finally:
                app.RESEARCH_DIR = original
            text = path.read_text(encoding="utf-8")
            self.assertIn("分析已经写了", text)
            self.assertNotIn("does-not-exist.html", text)
            self.assertNotIn('href="product-opportunities/reports/does-not-exist.html"', text)

    def test_reports_link_back_to_the_same_tab(self):
        with tempfile.TemporaryDirectory() as tmp:
            app.REPORT_DIR = Path(tmp)
            try:
                written = app.write_reports()
                self.assertEqual(len(written), len({item["slug"] for item in app.DATA["entries"]}))
                by_slug = {path.stem: path.read_text(encoding="utf-8") for path in written}
            finally:
                app.REPORT_DIR = Path(__file__).resolve().parent / "reports"
        self.assertIn("../../index.html#jm-ghw", by_slug["impeccable"])
        self.assertIn("../../2026-11-06.html#jm-ghw", by_slug["impeccable"])
        self.assertIn("../../index.html#jm-phd", by_slug["rerun"])
        self.assertIn("显示序 5", by_slug["rerun"])
        self.assertIn("price1:29", by_slug["rerun"])
        self.assertIn("不引用提示词", by_slug["dsh-purge"])
        self.assertIn("../../index.html#jm-ph", by_slug["glasshand"])
        self.assertIn("../../index.html#jm-phd", by_slug["glasshand"])
        self.assertIn("../../index.html#jm-ph", by_slug["pushary"])
        self.assertIn("../../index.html#jm-ph", by_slug["beacon"])
        self.assertNotIn("#jm-phd", by_slug["beacon"])
        self.assertNotIn("#jm-phm", by_slug["beacon"])
        for text in by_slug.values():
            self.assertIn('id="what"', text)
            self.assertIn('id="sources"', text)
            self.assertIn("未", text)
            self.assertNotIn("/tmp/", text)
            self.assertNotIn("/workspace/", text)
            self.assertLess(text.find("目录"), text.find("<main>"))


if __name__ == "__main__":
    unittest.main()
