import re
"""生成 xhs/seven/index.html（七步工作台）。唯一数据源：同目录 seven.json（由 review/xhs-seven-20261108/import_seven.py 从私有工作包导入）。
无 JS；左目录同页锚点立即跳；跨页与外链新标签。"""
import json, html
from pathlib import Path
D = json.loads((Path(__file__).parent / 'seven.json').read_text()); e = html.escape
def note(n):
    """来源说明：URL 单独做链接，附注作文字。"""
    m = re.match(r'(https?://[^\s，（(]+)(.*)$', n)
    return ext(m.group(1), '原文') + e(m.group(2)) if m else e(n)


def ext(u, t): return f'<a href="{e(u)}" target="_blank" rel="noopener noreferrer">{e(t)}</a>'
def tbl(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td data-l="{head[i]}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def ul(xs): return '<ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
S = {s['id']: s for s in D['steps']}
def head(sid):
    s = S[sid]
    return (f'<section id="{sid}" class="card"><h2>{s["n"]} · {e(s["name"])}</h2>'
            f'<p class="st"><span class="k">产物</span>{e(s["out"])}<br><span class="k">状态</span><b>{e(s["state"])}</b><br><span class="k">缺口</span>{e(s["gap"])}</p>')
src = D['source']; s1, s2, s3, s4, s5, s6, s7 = (D[k] for k in ('step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7'))
body = []
body.append(head('s1') + f'<p class="mut">原文：{e(s1["article"])}</p><h3>内容方向候选</h3>' +
  tbl(['方向', '依据', '怎么验证'], [[e(x['name']), e(x['basis']), e(x['validate'])] for x in s1['content_directions']]) +
  '<h3>变现假设（有条件才考虑）</h3>' + tbl(['假设', '前提条件'], [[e(x['name']), e(x['condition'])] for x in s1['monetization_hypotheses']]) +
  f'<p><b>{e(s1["decision"])}</b></p></section>')
lat = [[ext(x['url'], x['title']), e(x['author']) + '<br><span class="mut">粉丝 ' + (f"{x['followers_verified']}（已核）" if x['followers_verified'] else '未核') + '</span>', e(x['published_raw']), f"赞 {x['counts_2026_11_08']['likes']} / 藏 {x['counts_2026_11_08']['collects']} / 评 {x['counts_2026_11_08']['comments']}",
        ('同期倾向（相对日期，绝对日未核）' if x['comparable_same_period'] else '不可比：' + e(x['why_not'])), e(x['coverage']), e('、'.join(x['categories'])) + '<br><span class="mut">' + e(x['categories_note']) + '</span>',
        e(x['skeleton']), e(x['author_claims']), e(x['borrowable_action']), e(x['limits'])] for x in s2['latest']]
body.append(head('s2') + f'<p class="mut">原文：{e(s2["article"])}</p><h3>最新池（{len(s2["latest"])} 条）</h3><p class="mut">{e(s2["latest_scan"])}。数字为 2026-11-08 页面读数。</p>' +
  (tbl(['笔记', '作者', '时间（页面原样）', '赞藏评', '同期比较', '读了什么', '分类', '骨架', '作者自述 / 未核', '可借写法（我们的建议）', '边界'], lat, 'wide') if lat else '<p>暂无。</p>') +
  '<h3>历史池（主页置顶 / 近期，不代表近期趋势）</h3>' + ul([f'<a href="{e(h["href"])}" target="_blank" rel="noopener noreferrer">{e(h["name"])}</a> — {e(h["note"])}' for h in s2['historical']]) + '</section>')
body.append(head('s3') + '<div class="g3">' + ''.join(f'<div><h3>{t}</h3>{ul([e(x) for x in s3[k]])}</div>' for t, k in (('已知（Ocean 原话）', 'facts'), ('内容边界', 'boundaries'), ('探索中的假设', 'hypotheses'), ('留空，不替 Ocean 定', 'left_blank'))) + '</div></section>')
r4 = [[e(r['cat']), e(r['identify']), e(r['need']), e(r['promise']), e(r['suggested_title']) + '<br><span class="mut">我们的建议，不是真实爆款</span>' + ''.join(f'<br><span class="mut">最新骨架《{e(x["title"])}》：{e(x["skeleton"])}</span>' for x in r['latest_refs']), e(r['source_status']) + '<br><span class="mut">' + note(r['source_note']) + '</span>'] for r in s4]
body.append(head('s4') + f'<p class="mut">{e(D["step4_note"])}</p>' + tbl(['类', '怎么识别', '读者要什么', '开头与正文要兑现', '建议题（候选）', '来源状态'], r4, 'wide') + '</section>')
body.append(head('s5') + f'<div class="draft"><p class="dt">《{e(s5["title"])}》<span class="tag">草稿 · 未发布</span></p>' + ''.join(f'<p>{e(p)}</p>' for p in s5['body']) +
  f'<p class="mut">标签候选：{e(" ".join(s5["tags"]))} · 依据：{ext(s5["source"], "原文")}</p></div></section>')
body.append(head('s6') + tbl(['建议题', '字数'], [[e(k), str(v)] for k, v in s6['titles'].items()]) +
  f'<p>超 20 字：{e("、".join(s6["title_over_20"]) or "无")}；稿内禁词与第一人称命中：{e("、".join(s6["draft_banned_hits"]) or "无")}。</p>'
  '<h3>人工检查清单（未做）</h3>' + ul(['读一遍去 AI 腔，标题只借机制不套“绝了/彻底解决”', '每个事实能点开来源', '别人的经历不改成第一人称', '没做过的实操不写成做过']) + '</section>')
body.append(head('s7') + '<p class="flow">' + ' → '.join(e(x) for x in s7['workflow']) + '</p>' + f'<p>{e(s7["rolling_order"])}</p><p class="mut">{e(s7["window"])}；{e(s7["rules"])}。</p>' +
  tbl(['复盘字段', '当前值'], [[e(k), '—'] for k in s7['review_fields']]) + '</section>')
nav = ''.join(f'<a href="#{s["id"]}">{s["n"]} · {e(s["name"])}</a>' for s in D['steps'])
summary = tbl(['步', '产物', '状态', '缺口'], [[f'<a href="#{s["id"]}">{s["n"]} {e(s["name"])}</a>', e(s['out']), e(s['state']), e(s['gap'])] for s in D['steps']], 'sum')
CSS = """:root{--bg:#f7f4ec;--sf:#fffcf7;--ink:#1a1a18;--ink2:#3a3a36;--mut:#6a6a62;--line:#e6e0d4;--hi:#ffe566;--his:#fff6c8}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.65 "PingFang SC","Noto Sans SC",system-ui,sans-serif}
.shell{display:grid;grid-template-columns:13.5rem minmax(0,1fr)}.nav{position:sticky;top:0;height:100vh;overflow:auto;padding:1.2rem .9rem;border-right:1px solid var(--line)}
.nav a{display:block;color:var(--ink2);text-decoration:none;font-size:.86rem;padding:.3rem .5rem;border-radius:8px}.nav a:hover{background:var(--his)}.nav .b{font-weight:750;margin:0 0 .4rem}
.main{padding:1.4rem clamp(1rem,3vw,2.2rem) 4rem;min-width:0}h1{font-size:1.6rem;margin:0 0 .4rem}h2{font-size:1.1rem;margin:0 0 .5rem;border-bottom:3px solid var(--hi);padding-bottom:.3rem}h3{font-size:.98rem;margin:1rem 0 .3rem}
.card{background:var(--sf);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem;margin:0 0 1rem}.mut{color:var(--mut);font-size:.88rem}.st{background:var(--his);border-radius:10px;padding:.5rem .7rem;font-size:.9rem}
.k{display:inline-block;min-width:2.6em;font-size:.72rem;font-weight:700;color:#6a5a00;margin-right:.3rem}.tag{font-size:.72rem;background:#fff0d6;color:#8a5a00;border-radius:999px;padding:.05rem .45rem;margin-left:.4rem}
.tw{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.86rem;background:#fff}th,td{border:1px solid var(--line);padding:.4rem .5rem;text-align:left;vertical-align:top}th{background:#efeae0;font-size:.78rem}
table.wide{min-width:52rem}.g3{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:.6rem}.draft{border-left:3px solid var(--hi);padding:.2rem .9rem}.dt{font-weight:700}.flow{font-size:.88rem}
a{color:var(--ink)}.mob{display:none;flex-wrap:wrap;gap:.3rem;margin:0 0 .8rem}.mob a{font-size:.8rem;background:var(--his);padding:.15rem .5rem;border-radius:999px;text-decoration:none;color:var(--ink)}
@media(max-width:900px){.shell{grid-template-columns:1fr}.nav{display:none}.mob{display:flex}}
@media(max-width:700px){.tw{overflow:visible}.tw table,.tw tbody,.tw tr,.tw td{display:block;width:100%;min-width:0}.tw thead{display:none}.tw tr{border:1px solid var(--line);border-radius:10px;margin:0 0 .6rem;padding:.4rem .6rem}.tw td{border:0;padding:.15rem 0;overflow-wrap:anywhere}.tw td::before{content:attr(data-l);display:block;font-size:.7rem;font-weight:650;color:var(--mut)}}"""
page = f"""<!DOCTYPE html>
<html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>七步工作台 · 小红书</title><style>{CSS}</style></head>
<body><div class="shell"><aside class="nav" aria-label="目录"><p class="b">七步工作台</p><a href="../" target="_blank" rel="noopener noreferrer">← 小红书入口</a><a href="#top">总览</a>{nav}<a href="#src">来源与边界</a></aside>
<main class="main" id="top"><nav class="mob" aria-label="移动目录"><a href="../" target="_blank" rel="noopener noreferrer">← 入口</a>{''.join(f'<a href="#{s["id"]}">{s["n"]}</a>' for s in D['steps'])}<a href="#src">来源</a></nav>
<h1>七步工作台</h1><p class="mut">按{ext(src['url'], '文子的小红书冷启动长文')}的七步整理（{e(D['asof'])}）。作者说法和我们的建议分开写；账号方向仍在探索，下面都是候选、草稿和草案：未选定变现、未发布、未排期。</p>
<section class="card"><h2>七步一览</h2>{summary}</section>
{''.join(body)}
<section id="src" class="card"><h2>来源与边界</h2>{ul([ext(src['url'], src['title']) + f'（{e(src["author"])}；{e(src["read"])}）', e(D['analysis_note']), '最新池只用研究对象的公开笔记；不公开账号个人数据与关注名单。', '不改 routine、不自动发帖。'])}</section>
</main></div></body></html>
"""
out = Path(__file__).resolve().parents[1] / 'index.html'; out.write_text(page); print('ok seven', len(page))
