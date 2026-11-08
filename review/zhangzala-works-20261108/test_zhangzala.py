"""钉住张咋啦页结构：python3 review/zhangzala-works-20261108/test_zhangzala.py"""
import re, sys, unittest
from html.parser import HTMLParser
from pathlib import Path
PAGE = Path(__file__).resolve().parents[2] / "xhs" / "zhangzala.html"
ORDER = ["overview", "timeline", "works", "audience", "compare", "voice", "limits", "for-ocean", "sources"]
REMOVED = ["archive", "old-milestones", "old-breakout", "pieces", "x-top", "viral", "appendix"]
BANNED = ["爆款", "294", "中位数", "70,001", "旧版留档", "收藏比", "万赞", "爆款顶"]

class P(HTMLParser):
    def __init__(s): super().__init__(); s.ids=[]; s.hrefs=[]; s.top=[]; s.depth=0; s.sec=0
    def handle_starttag(s, t, a):
        a=dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t=="a" and a.get("href","").startswith("#"): s.hrefs.append(a["href"][1:])
        if t=="section":
            if s.sec==0 and "id" in a: s.top.append(a["id"])
            s.sec+=1
    def handle_endtag(s, t):
        if t=="section": s.sec-=1

class T(unittest.TestCase):
    @classmethod
    def setUpClass(c):
        c.html=PAGE.read_text(encoding="utf-8"); c.p=P(); c.p.feed(c.html)
    def test_order(self): self.assertEqual(self.p.top, ORDER)
    def test_unique_ids(self):
        d={i for i in self.p.ids if self.p.ids.count(i)>1}; self.assertFalse(d, d)
    def test_anchors(self):
        bad=[h for h in self.p.hrefs if h not in self.p.ids]; self.assertFalse(bad, bad)
    def test_removed(self):
        for i in REMOVED: self.assertNotIn(i, self.p.ids)
        self.assertNotIn("<details", self.html)
    def test_banned(self):
        for b in BANNED: self.assertNotIn(b, self.html, b)
    def test_six_cards(self):
        cards=re.findall(r'<article class="work card" id="(w\d)">(.*?)</article>', self.html, re.S)
        self.assertEqual([c[0] for c in cards], [f"w{i}" for i in range(1,7)])
        for cid, body in cards:
            self.assertRegex(body, r'href="https://', cid)
            for lv in ('lv f">事实', 'lv a">观察', 'lv h">假设', 'lv b">边界'): self.assertIn(lv, body, (cid, lv))
            self.assertIn('href="#s', body, cid)
    def test_no_watched_video_claim(self):
        for b in ["视频里", "视频中展示", "视频演示了", "看完视频"]: self.assertNotIn(b, self.html)
    def test_nav_covers_sections(self):
        nav=re.search(r'<aside class="nav".*?</aside>', self.html, re.S).group(0)
        mob=re.search(r'<nav class="mob-nav".*?</nav>', self.html, re.S).group(0)
        for i in ORDER: self.assertIn(f'href="#{i}"', nav, i)
        for i in ["works","audience","compare","voice"]: self.assertIn(f'href="#{i}"', mob, i)
    def test_compare_mobile_cards(self):
        self.assertIn('#audience .tw thead', self.html); self.assertIn('data-l="维度"', self.html); self.assertIn('data-l="读者类型"', self.html)
    def test_audience_no_demographics(self):
        sec=re.search(r'<section id="audience">.*?</section>', self.html, re.S).group(0)
        self.assertIn('没有真实的粉丝画像数据', sec)
        for c in ['#w1','#w2','#w3','#w4']: self.assertIn(f'href="{c}"', sec)
        self.assertNotRegex(sec, r'\d+(\.\d+)?%')

if __name__=="__main__": unittest.main(verbosity=1)
