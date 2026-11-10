#!/usr/bin/env python3
"""Build private /xhs/day archive + export build_day_body for the xhs hub.

Order (Ocean): picks first, then signals, then deep/raw.
"""
from __future__ import annotations
import argparse, json, html, re
from pathlib import Path
import xhs_hot_gate as hot_gate

def strip_xsec(html_text: str) -> str:
  """Public pages must not carry xsec_token / xsec_source (plain or amp-encoded)."""
  pat = r'[?&](?:amp;)?xsec_(?:token|source)=[^&#]+'
  out = re.sub(pat, '', html_text, flags=re.I)
  out = out.replace('?&amp;', '?')
  out = out.replace('&amp;&amp;', '&amp;')
  out = re.sub(r'[?&]+(?=[\'\">\\s])', '', out)
  # clean dangling ? or & before closing quote
  out = re.sub(r'\?(?=[\'"])', '', out)
  out = re.sub(r'&(?=[\'"])', '', out)
  out = re.sub(r'&amp;(?=[\'"])', '', out)
  return out

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "xhs-day-data"
SITE = ROOT / "site-repo" / "xhs" / "day"

CSS = r"""
:root{--bg:#f3f1eb;--surface:#fffcf7;--ink:#1a1c1b;--ink-2:#3d433f;--mut:#59656b;--line:#e2ddd2;--accent:#0d6b52;--accent-soft:#e4f3ec;--warn:#8a5a00;--warn-soft:#fff3d6;--ok:#1e6b3a;--ok-soft:#e6f4ea;--shadow:0 1px 2px rgba(26,28,27,.04),0 8px 24px rgba(26,28,27,.06);--r:14px;--nav-w:14rem}
*{box-sizing:border-box}html{scroll-behavior:auto}
body{margin:0;color:var(--ink);background:var(--bg);font:16.5px/1.7 "PingFang SC","Hiragino Sans GB","Noto Sans SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.shell{display:grid;grid-template-columns:var(--nav-w) minmax(0,1fr);max-width:none;margin:0 auto;min-height:100vh}
.nav{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:1.4rem 1rem 2rem;border-right:1px solid var(--line);background:linear-gradient(180deg,#f7f5ef,var(--bg))}
.nav .brand{font-weight:750;font-size:.95rem;margin:0 0 .3rem}
.nav .meta{font-size:.76rem;color:var(--mut);margin:0 0 1rem;line-height:1.45}
.nav a{display:block;color:var(--ink-2);text-decoration:none;font-size:.82rem;padding:.32rem .5rem;border-radius:8px;margin:.08rem 0}
.nav a:hover,.nav a:focus,.nav a.on{background:var(--accent-soft);color:var(--accent)}
.nav a.on{font-weight:650}
.nav .sec{font-size:.7rem;letter-spacing:.06em;color:var(--mut);margin:.9rem 0 .3rem;padding-left:.5rem}
.main{padding:1.6rem clamp(1rem,3vw,3rem) 4rem;min-width:0;max-width:78rem}
h1{font-size:clamp(1.35rem,2.2vw,1.75rem);letter-spacing:-.025em;margin:0 0 .55rem;font-weight:750;line-height:1.28}
h2{font-size:1.2rem;margin:2.4rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid var(--accent);font-weight:700;scroll-margin-top:.5rem;letter-spacing:-.01em}
h3{font-size:1rem;margin:.15rem 0 .45rem;font-weight:700}
p,li{color:var(--ink-2)}.muted{color:var(--mut);font-size:.92rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1rem 1.1rem;margin:.7rem 0;box-shadow:var(--shadow)}
.verdict{border-color:#b7d9cb;border-left:4px solid var(--accent);background:linear-gradient(180deg,#fff,#fffcf7);padding:1.15rem 1.25rem 1.2rem}
.verdict .lead{margin:0 0 .85rem;color:var(--ink);font-weight:650;font-size:1.05rem;max-width:46rem;line-height:1.75}
.verdict ul{margin:.2rem 0 .7rem;padding-left:1.15rem}
.verdict li{margin:.35rem 0}
.one{font-size:.95rem;color:var(--ok);background:var(--ok-soft);border-radius:10px;padding:.65rem .85rem;margin:.85rem 0 0;font-weight:650}
.tag{display:inline-block;font-size:11px;font-weight:650;background:var(--ok-soft);color:var(--ok);padding:.1rem .45rem;border-radius:999px;margin-left:.35rem;vertical-align:middle}
.tag.accent{background:var(--accent-soft);color:var(--accent)}
.warn{font-size:.86rem;color:var(--warn);background:var(--warn-soft);border-radius:8px;padding:.55rem .7rem;margin:.7rem 0}
a{color:var(--accent);text-underline-offset:3px}
code{font-size:.78rem;background:#efeae0;padding:.05rem .3rem;border-radius:4px}
table{width:100%;border-collapse:collapse;font-size:.86rem;background:var(--surface);margin:.5rem 0}
th,td{border:1px solid var(--line);padding:.4rem .5rem;text-align:left;vertical-align:top}th{background:#efeae0}
.tw{overflow-x:auto;margin:.5rem 0 1.2rem;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
.tw table{margin:0;min-width:36rem}
.tw th{background:#f7f5ef;font-size:.78rem;color:var(--mut)}
.tw td,.tw th{padding:.55rem .7rem}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right;font-weight:650;color:var(--accent)}
td.nowrap{white-space:nowrap}
ul.compact{margin:.2rem 0 0;padding-left:1.1rem;font-size:.84rem}
.kwgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(17.5rem,1fr));gap:1rem;align-items:stretch}
.kwcard{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1rem 1.05rem 1.05rem;box-shadow:var(--shadow);display:flex;flex-direction:column;min-height:100%}
.kwh{display:flex;align-items:baseline;justify-content:space-between;gap:.6rem;margin:0 0 .55rem;padding-bottom:.55rem;border-bottom:1px solid var(--line)}
.kwh h3{margin:0;font-size:1.02rem;font-weight:750;letter-spacing:-.01em}
.kwbadge{flex:0 0 auto;font-size:.72rem;font-weight:650;color:var(--accent);background:var(--accent-soft);padding:.18rem .5rem;border-radius:999px;white-space:nowrap}
.kwnote{margin:0 0 .7rem;font-size:.88rem;color:var(--mut);line-height:1.55}
ol.posts{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.55rem;flex:1}
ol.posts li{margin:0;padding:.55rem .6rem;border-radius:10px;background:#f7f5ef;border:1px solid transparent}
ol.posts li:hover{border-color:var(--line);background:#fff}
ol.posts a{display:block;color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;font-weight:650;font-size:.92rem;line-height:1.4}
.pmeta{display:block;margin-top:.28rem;font-size:.75rem;color:var(--mut);font-weight:500;line-height:1.4}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:1rem}
.cols .card{margin:0;padding:1.05rem 1.15rem}
.cols .card h3{margin:0 0 .55rem;font-size:1.02rem;line-height:1.35}
.cols .card p{margin:.45rem 0;font-size:.92rem}
.topics{display:grid;grid-template-columns:repeat(auto-fit,minmax(22rem,1fr));gap:1rem;align-items:start}
.pick{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1.1rem 1.15rem 1.2rem;margin:0;box-shadow:var(--shadow);position:relative}
.pick .n{position:absolute;top:.95rem;right:1rem;font-size:.72rem;font-weight:700;color:var(--mut);letter-spacing:.04em}
.pick h3{font-size:1.08rem;margin:0 1.8rem .55rem 0;font-weight:750;line-height:1.35}
.row{margin:.45rem 0;font-size:.92rem;line-height:1.55}
.row b{display:block;font-size:.72rem;color:var(--mut);font-weight:650;letter-spacing:.03em;margin-bottom:.08rem}
.insp{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:.75rem}
.insp li{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.85rem 1rem;margin:0;box-shadow:var(--shadow)}
.insp .t{font-weight:650;font-size:.95rem}
.insp .m{font-size:.8rem;color:var(--mut);margin-top:.15rem}
.insp .a{font-size:.86rem;color:var(--ink-2);margin-top:.25rem}
ul.x{margin:.4rem 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:.65rem}
ul.x li{margin:0;padding:.85rem 1rem;background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}
ul.x li b{display:block;margin-bottom:.25rem;color:var(--ink)}
.signals{margin:.3rem 0 0;padding-left:1.15rem}
.signals li{margin:.28rem 0;color:var(--ink-2);font-size:.92rem}
.foot{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--mut);font-size:.85rem}
.mob{display:none;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;gap:.35rem;margin:0 0 1rem;position:sticky;top:0;z-index:5;background:var(--bg);padding:.55rem 0}
.mob a{font-size:.78rem;background:var(--accent-soft);color:var(--accent);text-decoration:none;padding:.2rem .5rem;border-radius:999px;white-space:nowrap}
.mob a.on{background:var(--accent);color:#fff}
details.rawfold{margin:1rem 0;border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:.4rem .9rem .9rem}
details.rawfold > summary{cursor:pointer;font-weight:700;padding:.55rem 0;color:var(--ink)}
.hub-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1rem 1.05rem;margin:.6rem 0;box-shadow:var(--shadow)}
.hub-card a{color:var(--ink);text-decoration:none;font-weight:700;font-size:1.02rem}
.hub-card a:hover{color:var(--accent)}
.hub-card p{margin:.35rem 0 0;color:var(--ink-2);font-size:.9rem}
.toc a{display:inline-block;margin:0 .55rem .35rem 0;font-size:.88rem;color:var(--accent);text-decoration:none;background:var(--accent-soft);padding:.28rem .6rem;border-radius:999px}
.partial{font-size:.86rem;color:var(--warn);background:var(--warn-soft);border-radius:8px;padding:.55rem .7rem;margin:0 0 1rem}
.sec-ico{display:inline-block;margin-right:.35rem;font-style:normal;font-weight:700;opacity:.9}.brand-row{display:flex;align-items:center;gap:.55rem;margin:0 0 .3rem}.brand-row img{width:28px;height:28px;border-radius:7px;flex:0 0 auto}.rawfold{margin:.6rem 0 1.2rem;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:.4rem .9rem .7rem}.rawfold summary{cursor:pointer;font-weight:650;color:var(--accent);padding:.35rem 0}
.topics{grid-template-columns:repeat(auto-fit,minmax(18rem,1fr))}
.topics .pick{min-width:0;overflow-wrap:anywhere;background:#fffcf7;border:1px solid var(--line);border-radius:16px;padding:1rem 1.1rem 1.05rem}
.topics .pk-top{display:flex;align-items:center;justify-content:space-between;min-height:1.3rem;margin-bottom:.35rem}
.topics .pick .n{position:static}
.topics .pick h3{color:var(--accent);margin:0 0 .5rem;font-size:1.05rem}
.topics .pill{display:inline-block;font-size:.72rem;font-weight:650;background:var(--accent-soft);color:var(--accent);padding:.12rem .6rem;border-radius:999px}
.topics .who,.topics .why1{margin:.3rem 0;font-size:.92rem;line-height:1.55}
.topics .who b{font-size:.72rem;color:var(--mut);margin-right:.4rem}
.topics .refs{margin:.45rem 0 .2rem;padding-left:1.1rem;font-size:.86rem}
.topics .refs li{margin:.15rem 0}
.topics details.more{margin-top:.5rem;font-size:.88rem}
.topics details.more>summary{cursor:pointer;color:var(--accent);font-weight:650}
details.verdict-fold{margin:1rem 0 0}
details.verdict-fold>summary{cursor:pointer;font-weight:650;color:var(--mut);padding:.35rem 0}
@media(max-width:900px){
  .shell{grid-template-columns:1fr}.nav{display:none}.mob{display:flex}
  .main{padding:1.1rem 1rem 3rem}
  h2,h1{scroll-margin-top:3.6rem}
  .topics,.cols,.kwgrid,.insp{grid-template-columns:1fr}
  .mob{margin:0 -1rem .8rem;padding:.5rem 1rem}
  .kwh{flex-wrap:wrap}
}
"""

JS = r"""
(function(){
  var ids=%IDS%, links=document.querySelectorAll('[data-s]');
  function cur(){
    var y=window.scrollY+80, c=ids[0];
    for(var i=0;i<ids.length;i++){var el=document.getElementById(ids[i]); if(el&&el.offsetTop<=y) c=ids[i];}
    if(window.innerHeight+window.scrollY>=document.body.scrollHeight-2) c=ids[ids.length-1];
    links.forEach(function(a){var on=a.getAttribute('data-s')===c; a.classList.toggle('on',on);
      if(on&&a.parentNode.classList.contains('mob')){var p=a.parentNode; p.scrollLeft=a.offsetLeft-p.clientWidth/2+a.clientWidth/2;}});
  }
  window.addEventListener('scroll',cur,{passive:true}); window.addEventListener('hashchange',cur); cur();
})();
"""


def esc(s: str) -> str:
  return html.escape(s or "", quote=False)


def link_or_text(item: dict) -> str:
  title = esc(item.get("title") or "待核")
  author = esc(item.get("author") or "")
  likes = esc(item.get("likes") or "")
  note = esc(item.get("note") or "")
  url = (item.get("url") or "").strip()
  bits = []
  if url:
    bits.append(f'<a href="{html.escape(url, True)}" target="_blank" rel="noopener">{title}</a>')
  else:
    bits.append(title)
  meta = " · ".join(x for x in [author, likes] if x)
  if meta:
    bits.append(f'<span class="muted"> · {meta}</span>')
  if note:
    bits.append(f'<div class="muted" style="margin-top:.15rem">{note}</div>')
  return "".join(bits)


def _first_sentence(text: str, cap: int = 80) -> str:
  t = (text or "").strip()
  m = re.search(r"[。！？!?；;]", t)
  if m:
    t = t[: m.end()]
  return t if len(t) <= cap else t[:cap].rstrip() + "…"


def _ref_short(item: dict) -> str:
  item = item or {}
  url = (item.get("url") or "").strip()
  title = esc(item.get("title") or "")
  if not url and not title:
    return ""
  likes = esc(item.get("likes") or "")
  meta = f'<span class="muted"> · {likes}</span>' if likes else ""
  if url:
    return f'<li><a href="{html.escape(url, True)}" target="_blank" rel="noopener">{title or "链接"}</a>{meta}</li>'
  return f"<li>{title}{meta}</li>"


def render_picks(picks: list) -> str:
  """Short cards: title / who / why first sentence / 1-2 refs; full text + hand folded."""
  if not picks:
    return '<div class="topics"><p class="muted">今天暂无汇总选题。</p></div>'
  out = []
  for i, p in enumerate(picks, 1):
    flag = f'<span class="pill">{esc(p["flag"])}</span>' if p.get("flag") else ""
    why = p.get("why", "")
    refs = "".join(_ref_short(p.get(k) or {}) for k in ("peer", "recent"))
    refs_html = f'<ul class="refs">{refs}</ul>' if refs else ""
    who = f'<p class="who"><b>适合谁</b>{esc(p.get("who",""))}</p>' if p.get("who") else ""
    why1 = f'<p class="why1">{esc(_first_sentence(why))}</p>' if why else ""
    more_rows = [
      f'<div class="row"><b>同类最高赞</b>{link_or_text(p.get("peer") or {})}</div>',
      f'<div class="row"><b>最近最高赞</b>{link_or_text(p.get("recent") or {})}</div>',
    ]
    if why:
      more_rows.append(f'<div class="row"><b>为什么是今天</b>{esc(why)}</div>')
    if p.get("hand"):
      more_rows.append(f'<div class="row"><b>动手</b>{esc(p.get("hand",""))}</div>')
    out.append(f'''
<article class="pick" id="p{i}">
  <div class="pk-top">{flag}<span class="n">#{i:02d}</span></div>
  <h3>{esc(p.get("title",""))}</h3>
  {who}{why1}{refs_html}
  <details class="more"><summary>展开全文与动手</summary>{"".join(more_rows)}</details>
</article>''')
  return f'<div class="topics">{"".join(out)}</div>'


def render_insp(items: list) -> str:
  if not items:
    return ""
  lis = []
  for it in items:
    t = esc(it.get("title", ""))
    url = (it.get("url") or "").strip()
    title_html = f'<a href="{html.escape(url, True)}" target="_blank" rel="noopener">{t}</a>' if url else t
    lis.append(
      f'<li><div class="t">{title_html}</div>'
      + (f'<div class="m">{esc(it.get("author",""))} · {esc(it.get("likes",""))} likes</div>'
         if it.get("likes") else f'<div class="m">{esc(it.get("author",""))}</div>')
      + f'<div class="a">{esc(it.get("angle",""))}</div></li>'
    )
  return (
    '<h2 id="insp">进选题的灵感</h2>'
    f'<ul class="insp">{"".join(lis)}</ul>'
    '<p class="muted">完整池在选题库「灵感池」归档；这里只放已进今日选题的要点。</p>'
  )


def nav_links(ids_labels: list[tuple[str, str]]) -> str:
  return "".join(f'<a href="#{i}" data-s="{i}">{lab}</a>' for i, lab in ids_labels)


def latest_day_file(data_dir: Path | None = None) -> Path | None:
  data_dir = data_dir or DATA
  files = sorted(data_dir.glob("20*.json"), reverse=True)
  return files[0] if files else None


def load_day(date: str | None = None, data_dir: Path | None = None) -> dict | None:
  data_dir = data_dir or DATA
  if date:
    f = data_dir / f"{date}.json"
    return json.loads(f.read_text()) if f.exists() else None
  f = latest_day_file(data_dir)
  return json.loads(f.read_text()) if f else None


def build_day_body(
  data: dict,
  *,
  archive_href: str = "index.html",
  hub_href: str = "../",
  hub_label: str = "小红书",
) -> tuple[str, list[tuple[str, str]]]:
  """Main HTML + nav ids. Order: picks -> signals -> deep/raw.
  layout == "hot_first"（2026-11-09 起，Ocean 顺序）走 build_hot_first_body。"""
  if data.get("layout") == "hot_first":
    return build_hot_first_body(data, archive_href=archive_href, hub_href=hub_href, hub_label=hub_label)
  date = data["date"]
  sec = data.get("sections") or {}
  meta = data.get("meta") or {}
  ids_labels: list[tuple[str, str]] = []
  body_parts: list[str] = []

  lead = data.get("daily_lead") or data.get("summary") or ""
  signals = data.get("signals") or []
  signal_lis = "".join(f"<li>{esc(s)}</li>" for s in signals)
  one = data.get("one_liner") or ""
  muted_top = meta.get("daily_muted") or "私密页 · 日报 + 推荐流 + 灵感合并；选题已去重。"

  ids_labels.append(("top", "今天写啥"))
  ul = ("<ul class='signals'>" + signal_lis + "</ul>") if signal_lis else ""
  one_html = ("<p class='one'>" + esc(one) + "</p>") if one else ""
  lead_html = ("<p class='lead'>" + esc(lead) + "</p>") if lead else ""
  body_parts.append(f"<h1 id='top'>今天写啥 · {esc(date)}</h1>")
  body_parts.append(hot_gate.rule_p())

  # 1) FIRST: 候选短卡（唯一一套推荐卡）
  ids_labels.append(("picks", "汇总建议选题"))
  body_parts.append("<h2 id='picks'><span class='sec-ico' aria-hidden='true'>✎</span> 汇总建议选题</h2>")
  body_parts.append(render_picks(data.get("picks") or []))

  fold_bits = f"<p class='muted'>{esc(muted_top)}</p>{lead_html}{ul}{one_html}"
  if not data.get("complete") or not sec.get("keywords_html"):
    fold_bits += "<p class='partial'>本页为合并前摘要：部分日报/推荐流区块未回填，完整留档见旧 daily/、feed/。</p>"
  elif not sec.get("feed_cat_html"):
    fold_bits += "<p class='partial'>当日无推荐流侦察合并进本页（推荐流自 11-04 起有档）。日报关键词/细看/X 缺口仍在下方。</p>"
  body_parts.append(
    "<details class='verdict-fold'><summary>今日判断与采集口径（默认折叠）</summary>"
    f"<div class='card verdict'>{fold_bits}</div></details>"
  )

  # 2a) 热词最高赞
  if sec.get("keywords_html"):
    ids_labels.append(("xhs", "热词最高赞"))
    body_parts.append("<h2 id='xhs'><span class='sec-ico' aria-hidden='true'>🔥</span> 热词最高赞 · 小红书今天在聊什么</h2>")
    body_parts.append("<p class='muted'>按热词分组，每组列出该词下最高赞帖；写选题前先扫这里。</p>")
    body_parts.append(sec["keywords_html"])

  # 2b) 本日最热兴趣
  if sec.get("feed_cat_html") or sec.get("feed_hot_html") or sec.get("feed_obs_html"):
    ids_labels.append(("feed", "本日最热兴趣"))
    body_parts.append("<h2 id='feed'><span class='sec-ico' aria-hidden='true'>◎</span> 本日最热兴趣 · 推荐流信号</h2>")
    fm = meta.get("feed_muted") or ""
    fw = meta.get("feed_warn") or ""
    if fm:
      body_parts.append(f"<p class='muted'>{esc(fm)}</p>")
    if fw:
      body_parts.append(f"<div class='warn'>{esc(fw)}</div>")
    if sec.get("feed_verdict_html"):
      body_parts.append(sec["feed_verdict_html"])
    if sec.get("feed_cat_html"):
      body_parts.append("<h3 id='cat'>分类占比</h3>")
      body_parts.append(sec["feed_cat_html"])
    if sec.get("feed_hot_html"):
      body_parts.append("<h3 id='hot'>爆款拆解</h3>")
      body_parts.append(sec["feed_hot_html"])
    if sec.get("feed_obs_html"):
      body_parts.append("<h3 id='obs'>关键观察</h3>")
      body_parts.append(sec["feed_obs_html"])

  # 2c) Ocean 灵感
  insp = render_insp(data.get("inspiration") or [])
  if insp:
    old_h = '<h2 id="insp">进选题的灵感</h2>'
    new_h = '<h2 id="insp"><span class="sec-ico" aria-hidden="true">&#10022;</span> Ocean 灵感 · 点赞进选题</h2>'
    insp = insp.replace(old_h, new_h)
    ids_labels.append(("insp", "Ocean 灵感"))
    body_parts.append(insp)

  # 2d) X 热帖差异化
  if sec.get("xonly_html") or sec.get("deeper_html"):
    ids_labels.append(("xdiff", "X 热帖差异化"))
    body_parts.append("<h2 id='xdiff'><span class='sec-ico' aria-hidden='true'>✕</span> X 热帖差异化</h2>")
    body_parts.append("<p class='muted'>X 上已热、小红书还没人讲透的角度；以及 Ocean 能讲更深的切口。</p>")
    if sec.get("xonly_html"):
      body_parts.append("<h3 id='xonly'>X 上有、小红书还没人讲的</h3>")
      body_parts.append(sec["xonly_html"])
    if sec.get("deeper_html"):
      body_parts.append("<h3 id='deeper'>Ocean 能讲得更深的地方</h3>")
      body_parts.append(sec["deeper_html"])

  # 3) 细看 + 原始
  if sec.get("deep_html"):
    ids_labels.append(("deep", "细看"))
    body_parts.append("<h2 id='deep'><span class='sec-ico' aria-hidden='true'>▣</span> 细看三条</h2>")
    body_parts.append(sec["deep_html"])

  raw_bits = []
  if sec.get("raw_daily_html"):
    raw_bits.append("<h3>热搜原始数据</h3>" + sec["raw_daily_html"])
  if sec.get("raw_feed_html"):
    raw_bits.append("<h3>推荐流原始高赞</h3>" + sec["raw_feed_html"])
  if raw_bits:
    ids_labels.append(("raw", "原始数据"))
    body_parts.append(
      "<h2 id='raw'><span class='sec-ico' aria-hidden='true'>▤</span> 原始数据</h2>"
      "<details class='rawfold'><summary>展开原始表（默认折叠）</summary>"
      + "".join(raw_bits)
      + "</details>"
    )

  if sec.get("notes_html"):
    ids_labels.append(("notes", "来源说明"))
    body_parts.append("<h2 id='notes'>来源与说明</h2>")
    body_parts.append(sec["notes_html"])

  ah = html.escape(archive_href, True)
  hh = html.escape(hub_href, True)
  body_parts.append(
    f"<p class='foot' id='day-foot'>私密 · 约 07:00（台北）更新 · "
    f"<a href='{ah}'>往期日页</a> · "
    f"<a href='{hh}'>{esc(hub_label)}全入口</a></p>"
  )
  return strip_xsec("".join(body_parts)), ids_labels


HOT_FIRST_CSS = (
  ".hf article.post{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:.9rem 1.05rem;margin:.8rem 0;box-shadow:var(--shadow)}"
  ".hf article.post h3{margin:0 0 .4rem;font-size:1.02rem}"
  ".hf dl{display:grid;grid-template-columns:7.5em minmax(0,1fr);gap:.2rem .8rem;margin:.4rem 0;font-size:.92rem}"
  ".hf dt{color:var(--mut)}.hf dd{margin:0;overflow-wrap:anywhere}"
  ".hf .why{margin:.3rem 0 0;padding-left:1.1rem}.hf .why li{margin:.2rem 0}"
  ".hf .flag{display:inline-block;font-size:.75rem;font-weight:650;color:var(--warn);background:var(--warn-soft);border-radius:999px;padding:.05rem .5rem;margin-left:.4rem;vertical-align:middle}"
  ".hf .tw td{overflow-wrap:anywhere}"
  "@media(max-width:600px){.hf dl{grid-template-columns:1fr}.hf dd{margin-bottom:.3rem}}"
)


def build_hot_first_body(data: dict, *, archive_href: str = "index.html", hub_href: str = "../",
                         hub_label: str = "小红书", hub: bool | None = None) -> tuple[str, list[tuple[str, str]]]:
  """Ocean 2026-11-09 顺序：什么火（或暂未确认热帖）-> 帖子与数据（不折叠）+ 每帖可能原因 -> 建议 ->
  主题×关键词×证据对应 -> 辅助信号 -> 关键词覆盖与待核库 -> 说明。
  hub=True（嵌入入口页）时，帖子与覆盖改用 *_hub_html，避免和入口页「新帖小号」块重复。"""
  if hub is None:
    hub = archive_href != "index.html"
  date = data["date"]
  sec = data.get("sections") or {}
  meta = data.get("meta") or {}
  pick = lambda k: (sec.get(k + "_hub_html") if hub and sec.get(k + "_hub_html") else sec.get(k + "_html")) or ""
  ids: list[tuple[str, str]] = [("top", "今天什么火")]
  parts = [f"<style>{HOT_FIRST_CSS}</style>", f"<h1 id='top'>今天写啥 · {esc(date)}</h1>", "<div class='hf'>"]
  if meta.get("daily_muted"):
    parts.append(f"<p class='muted'>{esc(meta['daily_muted'])}</p>")
  parts.append(hot_gate.rule_p())
  hot = (sec.get("hot_html") or "").strip()
  parts.append(hot if hot else hot_gate.empty_hot_html())
  order = [("xhs", "帖子与原因", "帖子、数据与可能原因", "posts"),
           ("picks", "建议选题", "建议怎么写", "picks"),
           ("deep", "主题对应", "主题 × 关键词 × 证据对应", "map"),
           ("feed", "推荐流", "推荐流", "feed"),
           ("insp", "X 新赞", "Ocean 灵感 · X 新赞", "insp"),
           ("xdiff", "X 早报旁证", "X 早报旁证", "xdiff"),
           ("raw", "覆盖与待核", "关键词覆盖与待核库", "raw"),
           ("watch", "观察中", None, "watch"),
           ("notes", "来源说明", "来源与说明", "notes")]
  for i, nav_lab, h2, key in order:
    if key == "watch":
      watch = (sec.get("watch_html") or "").strip()
      if not watch:
        continue
      ids.append((i, nav_lab))
      parts.append(hot_gate.wrap_watch(watch))
      continue
    body = pick(key)
    if not body:
      continue
    ids.append((i, nav_lab))
    parts.append(f"<h2 id='{i}'>{esc(h2)}</h2>")
    parts.append(body)
  parts.append("</div>")
  ah = html.escape(archive_href, True)
  hh = html.escape(hub_href, True)
  parts.append(f"<p class='foot' id='day-foot'>私密 · <a href='{ah}'>往期日页</a> · <a href='{hh}'>{esc(hub_label)}全入口</a></p>")
  return strip_xsec("".join(parts)), ids


def render_day(data: dict, all_dates: list[str]) -> str:
  """Archive day page shell; body order from build_day_body."""
  date = data["date"]
  idx = all_dates.index(date) if date in all_dates else -1
  prev_d = all_dates[idx + 1] if 0 <= idx < len(all_dates) - 1 else None
  next_d = all_dates[idx - 1] if idx > 0 else None
  md = date[5:].replace("-", "/")
  meta = data.get("meta") or {}
  body, ids_labels = build_day_body(
    data, archive_href="index.html", hub_href="../", hub_label="小红书",
  )
  ids_labels = list(ids_labels) + [("day-foot", "页脚")]
  nav_prev = f'<a href="{prev_d}.html">← {prev_d[5:]}</a>' if prev_d else ""
  nav_next = f'<a href="{next_d}.html">{next_d[5:]} →</a>' if next_d else ""
  nav_meta = meta.get("nav_meta") or f"私密 x-digest · {date} · 日页归档"
  ids_js = json.dumps([i for i, _ in ids_labels])
  script = JS.replace("%IDS%", ids_js)
  parts = [
    "<!DOCTYPE html>",
    '<html lang="zh-CN">',
    "<head>",
    '<meta charset="utf-8"/>',
    '<meta name="viewport" content="width=device-width, initial-scale=1"/>',
    '<meta name="robots" content="noindex,nofollow"/>',
    f"<title>今天写啥 · {esc(date)} · 归档</title>",
    f"<style>{CSS}</style>",
    '<link rel="stylesheet" href="../xhs-shell.css" data-xhs-shell>',
    "</head><body>",
    '<div class="shell">',
    '<aside class="nav">',
    '<div class="brand-row"><img src="../icon.svg" alt=""/>'
    f'<p class="brand" style="margin:0">每日选题 · {esc(md)}</p></div>',
    f'<p class="meta">{esc(nav_meta)}</p>',
    '<div class="sec">本页</div>',
    nav_links(ids_labels),
    '<div class="sec">其他</div>',
    '<a href="index.html">往期日页</a>',
    '<a href="../">小红书全入口</a>',
    nav_prev,
    nav_next,
    "</aside>",
    '<main class="main">',
    f'<nav class="mob">{nav_links(ids_labels)}<a href="../">小红书</a></nav>',
    body,
    "</main></div>",
    f"<script>{script}</script>",
    "</body></html>",
  ]
  return strip_xsec("".join(parts))


def render_index(all_dates: list[str], by_date: dict) -> str:
  cards = []
  for d in all_dates:
    data = by_date.get(d) or {}
    one = data.get("one_liner") or data.get("daily_lead") or data.get("summary") or ""
    n = len(data.get("picks") or [])
    cards.append(
      f'<a class="card" href="{d}.html" style="display:block;text-decoration:none;color:inherit">'
      f"<strong>{esc(d)}</strong>"
      f'<span class="muted" style="margin-left:.6rem">{n} 条选题</span>'
      f'<p class="muted" style="margin:.4rem 0 0">{esc(one)[:160]}</p></a>'
    )
  date_nav = "".join(f'<a href="{d}.html">{d[5:]}</a>' for d in all_dates)
  toc = "".join(f'<a href="{d}.html">{d[5:]}</a>' for d in all_dates)
  parts = [
    "<!DOCTYPE html>",
    '<html lang="zh-CN">',
    "<head>",
    '<meta charset="utf-8"/>',
    '<meta name="viewport" content="width=device-width, initial-scale=1"/>',
    '<meta name="robots" content="noindex,nofollow"/>',
    f"<title>每日选题 · 往期归档</title>",
    f"<style>{CSS}</style>",
    '<link rel="stylesheet" href="../xhs-shell.css" data-xhs-shell>',
    "</head><body>",
    '<div class="shell"><aside class="nav">',
    '<div class="brand-row"><img src="../icon.svg" alt=""/><p class="brand" style="margin:0">每日选题 · 归档</p></div>',
    '<p class="meta">私密 · 日页留档（日常看小红书全入口）</p>',
    '<div class="sec">导航</div><a href="../">小红书全入口</a>',
    '<div class="sec">日期</div>', date_nav,
    '</aside><main class="main">',
    "<h1>往期日页归档</h1>",
    '<p class="muted">日常请打开 <a href="../">小红书全入口</a>。本目录只留按日归档；旧 daily/、feed/ 仍留档但不进导航。</p>',
    f'<div class="toc">{toc}</div>',
    "".join(cards),
    '<p class="foot">私密页，勿外传。</p>',
    "</main></div></body></html>",
  ]
  return "".join(parts)


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--data", type=Path, default=DATA)
  ap.add_argument("--out", type=Path, default=SITE)
  args = ap.parse_args()
  args.out.mkdir(parents=True, exist_ok=True)
  files = sorted(args.data.glob("20*.json"), reverse=True)
  by_date = {}
  for f in files:
    data = json.loads(f.read_text())
    by_date[data["date"]] = data
  dates = sorted(by_date.keys(), reverse=True)
  for d in dates:
    html_out = render_day(by_date[d], dates)
    (args.out / f"{d}.html").write_text(html_out)
    print("wrote", d, "bytes", len(html_out))
  (args.out / "index.html").write_text(render_index(dates, by_date))
  print("wrote index", len(dates), "days")


if __name__ == "__main__":
  main()

