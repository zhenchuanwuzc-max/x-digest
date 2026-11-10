#!/usr/bin/env python3
"""Day/hub pages honor interaction thresholds (2026-11-10)."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, '/workspace/digests')
import xhs_day_build as dayb
import xhs_hot_gate as gate
import json

DAY = Path('/workspace/xhs-hot-gate-20261110/xhs/day')
HUB = Path('/workspace/xhs-hot-gate-20261110/xhs/index.html')
DATA = Path('/workspace/digests/xhs-day-data')

class DayHotGate(unittest.TestCase):
    def test_rule_on_all_days(self):
        for f in DAY.glob('2026-*.html'):
            t = f.read_text()
            self.assertIn('热帖门槛', t, f.name)
            self.assertNotIn('xsec_token', t, f.name)
            self.assertNotIn('xsec_source', t, f.name)

    def test_nov09_no_qualified(self):
        t = (DAY / '2026-11-09.html').read_text()
        self.assertIn('今天没有达标热帖', t)
        self.assertIn('观察中（未达标）', t)
        self.assertNotIn('选题热帖：新帖、小号优先', t)
        # low-engagement title only inside watch fold
        watch = t.split('id="watch"', 1)[1]
        before = t.split('id="watch"', 1)[0]
        self.assertIn('AI产品经理面试｜今年最能筛人的一轮是', watch)
        self.assertNotIn('id="ns-s-6af00cd20000000003015240"', before)
        self.assertIn('id="ns-s-6af00cd20000000003015240"', watch)
        d = json.loads((DATA / '2026-11-09.json').read_text())
        self.assertEqual(d.get('picks'), [])

    def test_nov10_qualified_present(self):
        t = (DAY / '2026-11-10.html').read_text()
        self.assertIn('平克马', t)
        self.assertIn('不知渭河', t)
        self.assertIn('热帖门槛', t)
        self.assertNotIn('选题热帖：新帖、小号优先', t)
        self.assertTrue(gate.meets_hot_threshold(678, 1320, 1))
        self.assertTrue(gate.meets_hot_threshold(605, 818, 2))

    def test_hub_no_newsmall_stack(self):
        t = HUB.read_text()
        self.assertNotIn('id="newsmall"', t)
        self.assertNotIn('选题热帖：新帖、小号优先', t)
        self.assertIn('平克马', t)
        self.assertIn('热帖门槛', t)
        # 暂未确认 must not sit above today's hot post
        if '暂未确认热帖' in t:
            self.assertGreater(t.find('暂未确认热帖'), t.find('平克马'))

if __name__ == '__main__':
    unittest.main()
