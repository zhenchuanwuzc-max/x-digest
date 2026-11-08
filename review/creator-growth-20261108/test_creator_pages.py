"""成长人物页结构测试（卡兹克、宝玉、歸藏、向阳乔木）。python3 review/creator-growth-20261108/test_creator_pages.py"""
import re, unittest
from html.parser import HTMLParser
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
PAGES = {"kazike": dict(banned=["爆款","746","万赞","中位数","4855","9158","4874","300 万","13 场","160 位","六位数"], ledger="kazike-ledger.md"),
 "baoyu": dict(banned=["263.2k","偏薄专页","爆款","115.5万"], ledger="baoyu-ledger.md"),
 "guizang": dict(banned=["183.8k","7.8万","2.5万","2000 付费","11万","爆款"], ledger="guizang-ledger.md"),
 "qiaomu": dict(banned=["134.1k","六万多","3 万","爆款"], ledger="qiaomu-ledger.md"),
 "huashu": dict(banned=["72.3k","10–20 万/项目","爆款"], ledger="huashu-ledger.md"),
 "fankai": dict(banned=["46.0k","会员价目","爆款"], ledger="fankai-ledger.md"),
 "hector": dict(banned=["爆款"], ledger="hector-ledger.md")}
ORDER = ["brief","overview","timeline","works","audience","compare","voice","limits","for-ocean","sources"]
class P(HTMLParser):
    def __init__(s): super().__init__(); s.ids=[]; s.hrefs=[]; s.top=[]; s.d=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t=="a" and a.get("href","").startswith("#"): s.hrefs.append(a["href"][1:])
        if t=="section":
            if s.d==0 and "id" in a: s.top.append(a["id"])
            s.d+=1
    def handle_endtag(s,t):
        if t=="section": s.d-=1
class T(unittest.TestCase):
    def each(self):
        for name,cfg in PAGES.items():
            html=(REPO/"xhs"/f"{name}.html").read_text(encoding="utf-8"); p=P(); p.feed(html); yield name,cfg,html,p
    def test_structure(self):
        for n,c,h,p in self.each():
            self.assertEqual(p.top, ORDER, n)
            d={i for i in p.ids if p.ids.count(i)>1}; self.assertFalse(d,(n,d))
            bad=[x for x in p.hrefs if x not in p.ids]; self.assertFalse(bad,(n,bad))
    def test_banned(self):
        for n,c,h,p in self.each():
            for b in c["banned"]: self.assertNotIn(b,h,(n,b))
    def test_evidence(self):
        for n,c,h,p in self.each():
            self.assertTrue((Path(__file__).parent/c["ledger"]).exists())
            for w in re.findall(r'<article class="work card" id="(w\d)">(.*?)</article>',h,re.S):
                self.assertRegex(w[1],r'href="https://',n)
                for lv in ('lv f">事实','lv a">观察','lv h">假设','lv b">边界'): self.assertIn(lv,w[1],(n,w[0],lv))
            sec=re.search(r'<section id="sources">.*?</section>',h,re.S).group(0)
            for k in ("X","小红书","评论","作品原文","状态："): self.assertIn(k,sec,(n,k))
            aud=re.search(r'<section id="audience">.*?</section>',h,re.S).group(0)
            self.assertIn('../research/ai-depth-levels-2026-10-28.html#levels',aud)
            self.assertEqual(aud.count('读者现在：'),aud.count('内容指向：'))
            self.assertNotRegex(aud,r'\d+(\.\d+)?%')
            self.assertNotIn("<script",h)
    def test_growth_index_links(self):
        g=(REPO/"xhs/growth/index.html").read_text(encoding="utf-8")
        for n in PAGES: self.assertIn(f'../{n}.html',g)
if __name__=="__main__": unittest.main(verbosity=1)
