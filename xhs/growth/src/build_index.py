"""唯一研究首页 xhs/growth/index.html：①实操结论 ②14 人对比卡 ③专题。元数据唯一来源 src/people.json。
用法：python3 xhs/growth/src/build_index.py"""
import json, html
from pathlib import Path
import sys
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from page_kit import blankify
OUT = D.parent / 'index.html'
e = html.escape
LABELS = (('x', 'X 关注者'), ('xhs', '小红书粉丝'), ('wx', '公众号关注'), ('income', '收入'))


def _metric(v):
    tag = {'事实': '<span class="k f">公开读取</span>', '自述': '<span class="k s">自述</span>', '未找到': ''}[v['kind']]  # 未找到：文字本身即标注
    cls = ' class="nf"' if v['kind'] == '未找到' else ''
    return f'<span{cls}>{e(v["text"])}</span>{tag}'


def _sources(p):
    li = []
    for key, lab in LABELS:
        v = p['metrics'][key]
        bits = [lab + '：' + e(v['text'])]
        if v.get('date'): bits.append(e(v['date']))
        if v.get('note'): bits.append(e(v['note']))
        if v.get('src'): bits.append(f'<a href="{e(v["src"])}">来源</a>')
        li.append('<li>' + ' · '.join(bits) + '</li>')
    return '<details><summary>数据口径与来源</summary><ul>' + ''.join(li) + '</ul></details>'


def render():
    data = json.loads((D / 'people.json').read_text())
    P, T, pos = data['people'], data['topics'], data['positioning']
    rows = ''.join(
        f'''    <div class="pr">
      <h3>{e(r["who"])}</h3>
      <p class="lv">{e(r["level"])}</p>
      <dl><dt>痛点</dt><dd>{e(r["pain"])}</dd><dt>别人怎么解（证据）</dt><dd>{e(r["evidence"])}</dd>
      <dt>Ocean 可以做</dt><dd>{e(r["ocean"])}</dd><dt>交付样例</dt><dd>{e(r["deliver"])}</dd><dt>怎么验证</dt><dd>{e(r["check"])}</dd></dl>
    </div>
''' for r in data['practice'])
    steps = ''.join(f'<li>{e(s)}</li>' for s in data['steps'])
    obs = ''.join(f'<li>{e(s)}</li>' for s in data['observations'])
    people = ''.join(
        f'''    <div class="card pc" id="p-{p["id"]}">
      <h3><span class="ico" aria-hidden="true">{e(p["ico"])}</span><a href="{e(p["href"])}">{e(p["name"])}</a></h3>
      <p class="meta">{e(p["handle"])}</p>
      <dl><dt>主要做什么</dt><dd>{e(p["does"])}</dd><dt>主要用户</dt><dd>{e(p["users"])}</dd>
      {''.join(f'<dt>{lab}</dt><dd>{_metric(p["metrics"][k])}</dd>' for k, lab in LABELS)}</dl>
      {_sources(p)}
      <a class="go" href="{e(p["href"])}">{e(p["go"])} →</a>
    </div>
''' for p in P)
    topics = ''.join(
        f'''    <a class="card" id="t-{t["id"]}" href="{e(t["href"])}">
      <h3>{e(t["name"])}</h3>
      <p>{e(t["desc"])}</p>
    </a>
''' for t in T)
    page = (D / 'head.html').read_text() + f'''<body>
<div class="shell">
<aside class="nav" aria-label="本页目录">
  <div class="brand-row">
    <img src="icon.svg" width="28" height="28" alt=""/>
    <p class="brand">人物成长研究</p>
  </div>
  <p class="meta">首页 · 私密</p>
  <a href="#total">实操结论</a>
  <a href="#steps">先做什么</a>
  <a href="#people">人物（{len(P)}）</a>
  <a href="#topics">专题（{len(T)}）</a>
</aside>
<main class="main">
  <h1>人物成长研究</h1>
  <h2 id="total">实操结论：面向谁 → 痛点 → 怎么解 → Ocean 可以做</h2>
  <p class="muted">按 Ocean 的定位（<a href="{e(pos["src"])}">{e(pos["src_label"])}</a>：{e(pos["text"])}）从 14 人证据里挑出三类人群。{e(data["total_source"])}</p>
  <div class="prs">
{rows}  </div>
  <h2 id="steps">先做什么（建议的小实验顺序）</h2>
  <ol class="steps">{steps}</ol>
  <ul class="obs">{obs}</ul>

  <h2 id="people">人物（{len(P)}）</h2>
  <p class="muted">X 关注者为 2026-11-08 19:14（UTC+8）公共读取；其余数字均注明是本人说法和披露日期，找不到写「未找到公开数值」，不等于没有账号。收入口径不同，不排名、不相加。</p>
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
    return blankify(page)


if __name__ == '__main__':
    OUT.write_text(render())
    print('wrote', OUT)
