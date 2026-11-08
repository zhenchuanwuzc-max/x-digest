"""第 2 批人物页共用渲染（结构与 build_kazike.py 相同；卡兹克页不走这里，保持原样）。"""
import re, datetime as _D
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
import sys; sys.path.insert(0, str(REPO/"xhs/growth/src"))
from page_kit import with_brief, blankify
def a(u, t): return f'<a href="{u.replace("&","&amp;")}" target="_blank" rel="noopener">{t}</a>'
F,S,C,A,H,B = [f'<span class="lv {c}">{n}</span>' for c,n in (("f","事实"),("s","自述"),("s","评论者自述"),("a","观察"),("h","假设"),("b","边界"))]
TH = '<thead><tr><th>#</th><th>日期（UTC+8）</th><th>当时动作 → 作品</th><th><span class="lv f">事实</span></th><th><span class="lv s">自述</span></th><th><span class="lv a">分析</span></th><th><span class="lv b">边界</span></th></tr></thead>'
def row(n,d,act,f,s,an,b):
    return f'<tr><td data-l="#">{n}</td><td data-l="日期">{d}</td><td data-l="动作与作品">{act}</td><td data-l="事实">{f}</td><td data-l="自述">{s}</td><td data-l="分析">{an}</td><td data-l="边界">{b}</td></tr>'
def stage(sid,title,q,rows,note=""):
    return f'<section id="{sid}" class="stage"><h3>{title}</h3><p class="q"><b>当时的问题：</b>{q}</p><div class="tw"><table>{TH}<tbody>{"".join(rows)}</tbody></table></div>{note}</section>'
LV = [("f","事实","f"),("s","自述","s"),("o","观察","a"),("h","假设","h"),("b","边界","b")]
def card(w):
    sid,pos=w["where"]; rows="".join(f'<p><span class="lv {c}">{n}</span>{w[k]}</p>' for k,n,c in LV if w.get(k))
    return f'<article class="work card" id="{w["id"]}"><h3>代表作品 {w["id"][1]} · {w["t"]}</h3><p class="links">{" · ".join(w["links"])}</p><p class="muted">时间线位置：<a href="#{sid}">{pos}</a></p>{rows}<p class="take"><b>可借鉴写法：</b>{w["k"]}</p></article>'
def ts(i):
    """X 帖 id → UTC+8 时间（雪花 id 自带毫秒时间戳）。"""
    return (_D.datetime.fromtimestamp((((int(i)>>22)+1288834974657)/1000),_D.timezone.utc)+_D.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
def ul(items): return '<ul class="plain">'+"".join(f"<li>{i}</li>" for i in items)+'</ul>'
def render(c):
    zz=(REPO/"xhs/zhangzala.html").read_text(encoding="utf-8")
    head=zz[:zz.index("</head>")+len("</head>")]
    head=re.sub(r"<title>.*?</title>",f"<title>{c['name']}成长深拆 · 时间线 + 代表作品 + 受众深度 · 给 Ocean</title>",head,flags=re.S)
    nst=len(c["stages"])
    nav=(f'<div class="shell"><aside class="nav" aria-label="目录"><p class="brand">{c["short"]}深拆</p><p class="meta">私密 · 写给 Ocean<br>一手资料采集 2026-11-08（UTC+8）<br>'+c.get("meta","X 一手资料深化 · 小红书未核")+'</p>'+
     '<a href="growth/">← 人物成长研究</a>'+
     f'<div class="sec">本页</div><a href="#brief">实操摘要</a><a href="#overview">账号概况</a><a href="#timeline">{nst}阶段时间线</a>'+"".join(f'<a href="#s{i+1}">{i+1} · {t}</a>' for i,t in enumerate(c["stage_nav"]))+
     '<a href="#works">代表作品拆解</a><a href="#audience">谁在看</a><a href="#compare">写法对照</a><a href="#voice">语气与节奏</a><a href="#limits">失败与边界</a><a href="#for-ocean">给 Ocean</a><a href="#sources">来源与待核</a></aside>'
     '<main class="main"><nav class="mob-nav" aria-label="移动目录"><a href="growth/">← 人物成长研究</a><a href="#brief">摘要</a><a href="#overview">概况</a><a href="#timeline">时间线</a><a href="#works">作品</a><a href="#audience">受众</a><a href="#compare">对照</a><a href="#voice">语气</a><a href="#limits">边界</a><a href="#for-ocean">借鉴</a><a href="#sources">来源</a></nav>'
     f'<header><h1>{c["name"]} 成长深拆</h1><p class="muted">按“阶段 → 当时的问题 → 动作 → 作品”排，每条附原始链接。<span class="lv f">事实</span>可从原文核到；<span class="lv s">自述</span>是本人说法；<span class="lv a">分析</span>/<span class="lv a">观察</span>是研究者归纳；<span class="lv h">假设</span>未验证；<span class="lv b">边界</span>写不能怎么用。时间统一 UTC+8，查不到写未知。</p></header>')
    overview='<section id="overview"><h2>账号概况</h2><div class="grid2">'+"".join(f'<div class="card"><h3>{h}</h3><p>{p}</p></div>' for h,p in c["overview"])+'</div></section>'
    timeline=f'<section id="timeline"><h2>{nst}阶段时间线</h2>'+"".join(c["stages"])+'</section>'
    works='<section id="works"><h2>代表作品拆解</h2><p class="muted">只选原文读过、写法各不相同的作品，不是热门榜；不展示互动数。</p><div class="works">'+"".join(card(w) for w in c["works"])+'</div></section>'
    arows="".join(f'<tr><td data-l="读者类型">{a_}</td><td data-l="AI 使用深度">{d}</td><td data-l="想要什么">{b_}</td><td data-l="能拿走什么">{c_}</td><td data-l="对应作品">{w_}</td><td data-l="证据">{e}</td></tr>' for a_,b_,c_,w_,e,d in c["aud"])
    audience=('<section id="audience"><h2>谁在看，为什么愿意看</h2><p class="muted"><b>没有真实的粉丝画像数据</b>。人群和动机根据'+c.get("aud_basis","作者自述、X 评论和作品内容")+'推断，不代表全体读者。</p>'
     '<div class="tw"><table><thead><tr><th>可能的读者类型（推断）</th><th>AI 使用深度</th><th>可能想要什么</th><th>能拿走什么</th><th>对应作品</th><th>证据</th></tr></thead><tbody>'+arows+'</tbody></table></div>'
     '<p class="depth"><b>深度怎么标：</b>沿用 <a href="../research/ai-depth-levels-2026-10-28.html#levels">AI 使用深度水位</a> 的 L0–L5（定义见<a href="zhangzala.html#audience">张咋啦页</a>）；分开写读者现在和内容指向，层级不是职业类别。</p>'
     '<h3>可能为什么能火、能传开（未验证）</h3><div class="card">'+ul(c["why"])+'</div></section>')
    crow="".join(f'<tr><td data-l="维度">{d}</td><td data-l="代表作品">{x}</td><td data-l="普通内容">{y}</td></tr>' for d,x,y in c["cmp"])
    compare=('<section id="compare"><h2>普通内容与代表作品：写法差在哪</h2><p class="muted"><span class="lv a">观察</span>只比较写法，不是因果；不展示互动数。'+c["cmp_note"]+'</p>'
     '<div class="tw"><table><thead><tr><th>维度</th><th>代表作品</th><th>普通内容</th></tr></thead><tbody>'+crow+'</tbody></table></div></section>')
    voice=('<section id="voice"><h2>语气、节奏与可借鉴写法</h2><div class="card">'+ul(c["voice"])+f'</div><pre class="tpl">{c["tpl"]}</pre><p class="muted">模板是分析产物，不是作者原话。</p></section>')
    limits='<section id="limits"><h2>失败与边界</h2><div class="card"><ul>'+"".join(f"<li>{x}</li>" for x in c["limits"])+'</ul></div></section>'
    forocean=('<section id="for-ocean"><h2>'+c.get("ocean_head","给 Ocean（「AI具身牛马」）的借鉴")+'</h2><p class="muted"><span class="lv a">分析</span>研究者建议，不是成功公式。</p><div class="grid2">'
     '<div class="card"><h3>可借鉴</h3><ol>'+"".join(f"<li>{x}</li>" for x in c["take"])+'</ol></div>'
     '<div class="card"><h3>不适用</h3><ul>'+"".join(f"<li>{x}</li>" for x in c["skip"])+'</ul></div></div></section>')
    cov="".join(f'<tr><td data-l="来源">{p}</td><td data-l="读到了">{r}</td><td data-l="没读到">{n}</td></tr>' for p,r,n in c["cov"])
    sources=('<section id="sources"><h2>来源与待核</h2><p><b>状态：'+c.get("status_head","X 一手资料深化；小红书未核")+'</b>。'+c["status"]+'</p>'
     '<div class="tw"><table><thead><tr><th>来源</th><th>读到了</th><th>没读到</th></tr></thead><tbody>'+cov+'</tbody></table></div>'
     f'<ul class="plain"><li>证据台账：<code>review/creator-growth-20261108/{c["slug"]}-ledger.md</code>（采集 2026-11-08，UTC+8）。</li>'+"".join(f"<li>{x}</li>" for x in c["src_extra"])+'</ul>'
     '<p><span class="tag warn">待核</span>：'+c["todo"]+'</p></section>')
    html=head+"\n<body>\n"+nav+"\n"+overview+"\n"+timeline+"\n"+works+"\n"+audience+"\n"+compare+"\n"+voice+"\n"+limits+"\n"+forocean+"\n"+sources+"\n</main></div>\n</body>\n</html>\n"
    html=blankify(with_brief(html,c['slug'],'</header>'))
    (REPO/f"xhs/{c['slug']}.html").write_text(html,encoding="utf-8"); print("ok",c["slug"],len(html))
