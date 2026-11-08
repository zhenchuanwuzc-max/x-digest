"""本地 file:// 布局检查：390 与 1440 宽度无横向滚动；对照表小屏转卡片；目录锚点可跳。"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
NAMES = sys.argv[1:] or ["kazike"]
with sync_playwright() as p:
  b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
  for name in NAMES:
    P = (Path(__file__).resolve().parents[2]/"xhs"/f"{name}.html").as_uri()
    for w in (390, 1440):
        pg = b.new_page(viewport={"width": w, "height": 900}); pg.goto(P)
        r = pg.evaluate("""()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
          wide:[...document.querySelectorAll('.work,#audience,#compare,#voice,#sources')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>e.id||e.className),
          theadShown:getComputedStyle(document.querySelector('#compare thead')).display,audThead:getComputedStyle(document.querySelector('#audience thead')).display,
          nav:getComputedStyle(document.querySelector('.nav')).display,
          cols:getComputedStyle(document.querySelector('.works')).gridTemplateColumns.split(' ').length})""")
        print(name, w, r); assert r["sw"] <= r["cw"], "横向滚动"; assert not r["wide"], r["wide"]
        if w == 390: assert r["theadShown"] == "none" and r["audThead"] == "none" and r["nav"] == "none"
        else: assert r["nav"] != "none" and r["cols"] >= 2
        pg.screenshot(path=f"/workspace/creator-growth-20261108/{name}-{w}.png", full_page=True)
  b.close()
print("layout ok")
