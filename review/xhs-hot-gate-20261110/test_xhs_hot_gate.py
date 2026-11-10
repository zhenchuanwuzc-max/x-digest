#!/usr/bin/env python3
import unittest
import xhs_hot_gate as g

class HotGate(unittest.TestCase):
    def test_near7(self):
        self.assertTrue(g.meets_hot_threshold(200, 0, 3))
        self.assertTrue(g.meets_hot_threshold(0, 300, 7))
        self.assertFalse(g.meets_hot_threshold(199, 299, 2))
        self.assertTrue(g.meets_hot_threshold(678, 1320, 1))
    def test_mid(self):
        self.assertTrue(g.meets_hot_threshold(500, 0, 8))
        self.assertTrue(g.meets_hot_threshold(0, 800, 30))
        self.assertFalse(g.meets_hot_threshold(499, 799, 10))
        self.assertFalse(g.meets_hot_threshold(600, 700, 31))
    def test_unknown_age_or_counts(self):
        self.assertFalse(g.meets_hot_threshold(1000, 1000, None))
        self.assertFalse(g.meets_hot_threshold(None, None, 2))
    def test_parse_counts_and_age(self):
        self.assertEqual(g.parse_counts_text("赞 678 / 藏 1320 / 评 47（读取）"), (678, 1320))
        self.assertEqual(g.parse_counts_text("赞 未显示 / 藏 未显示 / 评：未显示"), (None, None))
        self.assertEqual(g.age_days_from_relative("详情页“昨天 00:59 河南”"), 1)
        self.assertEqual(g.age_days_from_relative("2天前"), 2)
        self.assertEqual(g.age_days_from_relative("6天前 北京"), 6)
    def test_rule_text(self):
        self.assertIn("近7天赞≥200或藏≥300", g.RULE_TEXT)
        self.assertIn("8到30天赞≥500或藏≥800", g.RULE_TEXT)
        self.assertIn("小号只是达标后的加分", g.RULE_TEXT)

if __name__ == "__main__":
    unittest.main()
