"""唯一研究首页 xhs/growth/index.html 的生成器：①跨人物结论 ②人物导航 ③专题导航。
元数据唯一来源：src/people.json。用法：python3 xhs/growth/src/build_index.py"""
import json, html
from pathlib import Path
D = Path(__file__).resolve().parent
OUT = D.parent / 'index.html'
e = html.escape


def render():
    data = json.loads((D / 'people.json').read_text())
    P, T = data['people'], data['topics']
    total = ''.join(f'<li><span class="tag">{e(x["tag"])}</span> {e(x["text"])}</li>' for x in data['total'])
    people = ''.join(
        f'''    <a class="card" id="p-{p["id"]}" href="{e(p["href"])}">
      <h3><span class="ico" aria-hidden="true">{e(p["ico"])}</span>{e(p["name"])}</h3>
      <p>{e(p["desc"])}</p>
      <p class="meta">{e(p["handle"])} · {e(p["go"])} →</p>
    </a>
''' for p in P)
    topics = ''.join(
        f'''    <a class="card" id="t-{t["id"]}" href="{e(t["href"])}">
      <h3>{e(t["name"])}</h3>
      <p>{e(t["desc"])}</p>
    </a>
''' for t in T)
    return (D / 'head.html').read_text() + f'''<body>
<div class="shell">
<aside class="nav" aria-label="本页目录">
  <div class="brand-row">
    <img src="icon.svg" width="28" height="28" alt=""/>
    <p class="brand">人物成长研究</p>
  </div>
  <p class="meta">首页 · 私密</p>
  <a href="#total">跨人物结论</a>
  <a href="#people">人物（{len(P)}）</a>
  <a href="#topics">专题（{len(T)}）</a>
</aside>
<main class="main">
  <h1>人物成长研究</h1>
  <h2 id="total">跨人物结论</h2>
  <ul class="total">{total}</ul>
  <p class="muted">{e(data["total_source"])}</p>

  <h2 id="people">人物（{len(P)}）</h2>
  <div class="grid">
{people}  </div>

  <h2 id="topics">专题（{len(T)}）</h2>
  <div class="grid">
{topics}  </div>

  <p class="foot">私密 · <a href="../">小红书创作中心</a> · <a href="https://zhenchuanwuzc-max.github.io/x-digest/">情报站首页</a></p>
</main>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    OUT.write_text(render())
    print('wrote', OUT)
