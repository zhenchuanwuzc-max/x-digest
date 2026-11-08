"""390/1440 两宽：无横向溢出；人物页首屏能看到实操摘要标题（摘要顶端在首屏内）；首页首屏有实操结论。截图放仓库外。"""
import sys, pathlib
from playwright.sync_api import sync_playwright
W = pathlib.Path(__file__).resolve().parents[2] / 'xhs'
OUT = pathlib.Path('/workspace/creator-growth-20261108/t227/shots')
PAGES = ['growth/index.html', 'kazike.html', 'zhangzala.html', 'lenny.html', 'levelsio.html', 'hector.html', 'topic-types.html', 'creators.html']
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w, h in ((390, 844), (1280, 800), (1440, 900)):
        pg = b.new_page(viewport={'width': w, 'height': h})
        for n in PAGES:
            pg.goto((W / n).as_uri()); pg.wait_for_timeout(150)
            ov = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
            if ov > 1: bad.append((n, w, 'overflow', ov))
            sel = '#total' if n.startswith('growth') else ('#brief' if n not in ('topic-types.html', 'creators.html') else None)
            if sel:
                top = pg.evaluate(f'document.querySelector("{sel}").getBoundingClientRect().top')
                if top > h - 60: bad.append((n, w, 'not first screen', top))
            if n.startswith('growth'):  # 对比表：桌面单元格内容高度不应远超文字（不留大块空白）
                gaps = pg.evaluate('''[...document.querySelectorAll("table.cmp tbody tr")].map(r=>r.getBoundingClientRect().height)''')
                if max(gaps) > (420 if w < 820 else 140): bad.append((n, w, 'row too tall', max(gaps)))
            if n.startswith('growth'):  # 展开全部「数据口径与来源」后仍不能撑破页面
                pg.evaluate('document.querySelectorAll("table.cmp details").forEach(d=>d.open=true)')
                ov2 = pg.evaluate('Math.max(document.documentElement.scrollWidth-innerWidth, document.querySelector("table.cmp").getBoundingClientRect().right-document.querySelector(".main").getBoundingClientRect().right)')
                if ov2 > 1: bad.append((n, w, 'details open overflow', ov2))
                pg.screenshot(path=str(OUT / f'growth-details-open-{w}.png'), full_page=False)
                pg.evaluate('document.querySelectorAll("table.cmp details").forEach(d=>d.open=false)')
            pg.screenshot(path=str(OUT / f'{n.replace("/", "_")}-{w}.png'))
        pg.screenshot  # noqa
    b.close()
print('BAD', bad) if bad else print('OK', len(PAGES) * 3, 'views')
sys.exit(1 if bad else 0)
