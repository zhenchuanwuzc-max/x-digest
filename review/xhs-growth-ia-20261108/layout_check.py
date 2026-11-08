import pathlib, sys
from playwright.sync_api import sync_playwright
W = pathlib.Path(__file__).resolve().parents[2]; O = pathlib.Path(sys.argv[1]); O.mkdir(parents=True, exist_ok=True)
PAGES = ['xhs/growth/index.html', 'xhs/lenny.html', 'xhs/justinwelsh.html', 'xhs/kazike.html', 'xhs/topic-types.html', 'xhs/topic-lip-growth.html', 'xhs/creators.html']
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for w in (390, 1440):
        for pg_path in PAGES:
            pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto((W/pg_path).as_uri())
            ov = pg.evaluate('document.documentElement.scrollWidth > innerWidth')
            if ov: bad.append((w, pg_path))
            pg.screenshot(path=str(O/f'{pg_path.replace("/", "_")}-{w}.png'))
            pg.close()
    b.close()
print('overflow', bad or 'none')
sys.exit(1 if bad else 0)
