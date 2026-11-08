import sys,pathlib
from playwright.sync_api import sync_playwright
p=pathlib.Path(__file__).resolve().parents[3]/'xhs/creators.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/google-chrome")
    for w in (390,1440):
        pg=b.new_page(viewport={'width':w,'height':900});pg.goto(p.as_uri())
        r=pg.evaluate('''()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
          wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1 && !e.closest('.tw')}).slice(0,5).map(e=>e.tagName+'.'+e.className)})''')
        print(w,r); assert r['sw']<=r['cw'] and not r['wide'],r
        for k in ['lenny','justinwelsh-audience','swyx-success']:
            pg.goto(p.as_uri()+'#'+k); assert pg.evaluate(f'document.getElementById("{k}").getBoundingClientRect().top')<5
    b.close()
print('layout ok')
