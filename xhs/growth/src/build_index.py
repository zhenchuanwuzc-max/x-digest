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
    # 自述数字带短年月；早于 2026 的再标「历史」，免得被当成当前数
    lab = '自述' + (f' · {v["asof"]}' if v.get('asof') else '') + (' · 历史' if v.get('asof', '2026') < '2026' else '')
    tag = {'事实': '<span class="k f">公开读取</span>', '自述': f'<span class="k s">{e(lab)}</span>', '未找到': ''}[v['kind']]  # 未找到：文字本身即标注
    if v['kind'] == '未找到':  # 表格里短写，图例说明含义；完整说法留在来源折叠里
        return '<span class="nf">未找到</span>'
    return f'<span class="v"><span>{e(v["text"])}</span> {tag}</span>'  # 值和口径标签同一格，手机两列网格里不拆行


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
    by = {p['id']: p for p in P}

    def bench(x):
        p = by[x['pid']]; ws = {w['id']: w for w in p['brief']['works']}
        items = ''.join(f'<li><a href="{e(p["href"])}#{e(i)}">{e(ws[i]["title"])}</a>：{e(ws[i]["step"])}'
                        f'（<a href="{e(ws[i]["src"])}">一手来源</a>）</li>' for i in x['works'])
        return (f'<div class="bm"><p class="bn"><a href="{e(p["href"])}">{e(p["name"])}</a></p>'
                f'<p class="bw">做了这些事：</p><ol class="bws">{items}</ol>'
                f'<p class="bl"><b>学这一步</b>{e(x["learn"])}</p><p class="bs"><b>别照搬</b>{e(x["skip"])}</p></div>')
    rows = ''.join(
        f'''    <div class="pr">
      <h3>{e(r["topic"])}</h3>
      <div class="bms">{''.join(bench(x) for x in r["bench"])}</div>
      <dl><dt>面向谁</dt><dd>{e(r["who"])}<span class="lv">{e(r["level"])}</span></dd><dt>痛点</dt><dd>{e(r["pain"])}</dd>
      <dt>Ocean 借鉴</dt><dd>{e(r["ocean"])}</dd><dt>怎么验证</dt><dd>{e(r["check"])}</dd></dl>
    </div>
''' for r in data['practice'])
    steps = ''.join(f'<li>{e(s)}</li>' for s in data['steps'])
    obs = ''.join(f'<li>{e(s)}</li>' for s in data['observations'])
    people = ''.join(
        f'''    <tr id="p-{p["id"]}">
      <th scope="row" data-l="人物"><a href="{e(p["href"])}">{e(p["name"])}</a><span class="hd">{e(p["handle"])}</span>{_sources(p)}</th>
      <td data-l="主要做什么 · 主要用户"><span class="does">{e(p["does"])}</span><span class="usr">用户：{e(p["users"])}</span></td>
      {''.join(f'<td data-l="{lab}" class="m">{_metric(p["metrics"][k])}</td>' for k, lab in LABELS)}
    </tr>
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
  <h2 id="total">总判断：对标谁 → 他做了什么 → Ocean 借鉴哪一步</h2>
  <p class="muted">按 Ocean 的定位（<a href="{e(pos["src"])}">{e(pos["src_label"])}</a>：{e(pos["text"])}）选三个方向，每个方向先看对标的人和他的具体作品，再看面向谁、痛点和可借鉴的一步。{e(data["total_source"])}</p>
  <div class="prs">
{rows}  </div>
  <h2 id="steps">先做什么（建议的小实验顺序）</h2>
  <ol class="steps">{steps}</ol>
  <ul class="obs">{obs}</ul>

  <h2 id="people">人物（{len(P)}）</h2>
  <p class="muted">X 关注者为 2026-11-08 19:14（UTC+8）公共读取；其余数字均注明是本人说法和披露日期，找不到写「未找到公开数值」，不等于没有账号。收入口径不同，不排名、不相加。</p>
  <p class="legend">「未找到」= 未找到公开数值，不等于没有账号或没有收入；绿色「公开读取」= 本次实测，黄色「自述」= 本人说法并标年月。</p>
  <table class="cmp">
    <thead><tr><th scope="col">人物</th><th scope="col">主要做什么 · 主要用户</th>{''.join(f'<th scope="col">{lab}</th>' for _, lab in LABELS)}</tr></thead>
    <tbody>
{people}    </tbody>
  </table>

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
