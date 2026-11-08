"""唯一维护入口 xhs/growth/index.html 的生成器。名单唯一来源：src/people.json。
用法：python3 xhs/growth/src/build_index.py  （写 xhs/growth/index.html）"""
import json, html
from pathlib import Path
D = Path(__file__).resolve().parent
OUT = D.parent / 'index.html'
e = html.escape

def render():
    data = json.loads((D / 'people.json').read_text())
    P, C = data['people'], data['collection']
    nav = ''.join(f'  <a class="nm" href="#p-{p["id"]}"><i aria-hidden="true">{e(p["ico"])}</i>{e(p["name"])}</a>\n' for p in P)
    def extra(p):
        return ''.join(f'<a class="xtra" href="{e(x["href"])}" target="_blank" rel="noopener">附：{e(x["label"])} →</a>' for x in p.get('extra', []))
    cards = ''.join(
        f'''    <div class="card" id="p-{p["id"]}">
      <div class="ico" aria-hidden="true">{e(p["ico"])}</div>
      <h3>{e(p["name"])}</h3>
      <p>{''.join(f'<span class="tag">{e(t)}</span>' for t in p["tags"])} {e(p["desc"])}</p>
      <p class="meta">{e(p["handle"])}</p>
      <a class="go" href="{e(p["href"])}" target="_blank" rel="noopener">{e(p["go"])} →</a>{extra(p)}
    </div>
''' for p in P)
    return (D / 'head.html').read_text() + f'''<body>
<div class="shell">
<aside class="nav" aria-label="按人名">
  <div class="brand-row">
    <img src="icon.svg" width="28" height="28" alt=""/>
    <p class="brand">成长记录</p>
  </div>
  <p class="meta">按人进 · {len(P)} 人 · 私密</p>
{nav}</aside>
<main class="main">
  <h1>成长记录 · 按人进</h1>
  <p class="muted">每人一张卡、一个链接。这一页是成长记录的唯一入口。</p>
  <div class="lead">{len(P)} 人都在下面，每人一张卡。点左栏名字跳到卡片，点卡片底部的链接打开那个人的分析。</div>

  <h2 id="people">人物（{len(P)}）</h2>
  <div class="grid">
{cards}  </div>
  <p class="muted">附属合集：<a href="{e(C["href"])}" target="_blank" rel="noopener">{e(C["name"])}</a>。{e(C["note"])}</p>

  <p class="foot">私密 · <a href="./">x-digest/xhs/growth/</a> · <a href="../">小红书全入口</a> · <a href="https://zhenchuanwuzc-max.github.io/x-digest/">情报站首页</a> · 名单源 src/people.json，由 src/build_index.py 生成</p>
</main>
</div>
</body>
</html>
'''

if __name__ == '__main__':
    OUT.write_text(render())
    print('wrote', OUT)
