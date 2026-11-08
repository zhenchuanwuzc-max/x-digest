#!/usr/bin/env python3
"""Generate private-site 小红书选题库 + per-draft 发布页 + creators page.

Usage:
  python3 xhs_library.py
  python3 xhs_library.py --append-note "…" [--added N]
  python3 xhs_library.py --sync-creators   # also refresh xhs/creators.html
"""
from __future__ import annotations
import argparse, html as H, json, re, shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/workspace/digests')
DATA = ROOT / 'monitors' / 'xhs_library.json'
SITE = ROOT / 'site-repo' / 'xhs'
OUT = SITE / 'index.html'
CREATORS_SRC = Path('/workspace/money/ai-creators-growth.html')
CREATORS_OUT = SITE / 'creators.html'
POST_DIR = SITE / 'post'
TZ = ZoneInfo('America/Los_Angeles')
E = H.escape

def load():
    return json.loads(DATA.read_text())

def save(d):
    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

def today():
    return datetime.now(TZ).strftime('%Y-%m-%d')

def append_increment(note: str, added: int = 0, extra_notes: list[str] | None = None):
    d = load()
    day = today()
    notes = list(extra_notes or [])
    if note:
        notes.insert(0, note)
    log = d.setdefault('changelog', [])
    if log and log[0].get('date') == day:
        log[0]['added'] = int(log[0].get('added') or 0) + int(added)
        log[0].setdefault('notes', []).extend(notes)
        if not log[0].get('title'):
            log[0]['title'] = '今日新增'
    else:
        log.insert(0, {
            'date': day, 'title': '今日新增', 'added': int(added), 'notes': notes,
        })
    d.setdefault('meta', {})['updated'] = day
    d['meta']['updated_label'] = f'{day}（America/Los_Angeles）'
    save(d)
    return d

def finished_drafts(d):
    out = []
    for key in ('main_series', 'side_series'):
        for e in d.get(key) or []:
            if e.get('draft_done') and e.get('draft'):
                out.append(e)
    return out

def _ext_for(did, name):
    """Prefer actual file on disk."""
    base = SITE / 'cards' / did
    p = base / name
    if p.exists():
        return name
    stem = Path(name).stem
    for ext in ('.jpg', '.jpeg', '.png'):
        if (base / f'{stem}{ext}').exists():
            return f'{stem}{ext}'
    return name

def _card_files(e):
    did = e['id']
    draft = e.get('draft') or {}
    files = draft.get('card_files') or []
    if not files:
        base = SITE / 'cards' / did
        if base.exists():
            files = sorted(
                [p.name for p in base.iterdir()
                 if p.suffix.lower() in ('.png', '.jpg', '.jpeg') and not p.name.startswith('_')],
                key=lambda n: n
            )
    return [_ext_for(did, f) for f in files]

# ---------- CSS shared ----------
CSS = '''
:root{--bg:#f3f1eb;--surface:#fffcf7;--ink:#1a1c1b;--ink-2:#3d433f;--mut:#59656b;--line:#e2ddd2;--accent:#0d6b52;--accent-soft:#e4f3ec;--warn:#8a5a00;--warn-soft:#fff3d6;--ok:#1e6b3a;--ok-soft:#e6f4ea;--shadow:0 1px 2px rgba(26,28,27,.04),0 8px 24px rgba(26,28,27,.06);--r:14px;--nav-w:14rem}
*{box-sizing:border-box}html{scroll-behavior:auto}
body{margin:0;color:var(--ink);background:var(--bg);font:16.5px/1.7 "PingFang SC","Hiragino Sans GB","Noto Sans SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.shell{display:grid;grid-template-columns:var(--nav-w) minmax(0,1fr);max-width:78rem;margin:0 auto;min-height:100vh}
.nav{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:1.4rem 1rem 2rem;border-right:1px solid var(--line);background:linear-gradient(180deg,#f7f5ef,var(--bg))}
.nav .brand{font-weight:750;font-size:.95rem;margin:0 0 .3rem}.nav .meta{font-size:.76rem;color:var(--mut);margin:0 0 1rem;line-height:1.45}
.nav a{display:block;color:var(--ink-2);text-decoration:none;font-size:.82rem;padding:.32rem .5rem;border-radius:8px;margin:.08rem 0}
.nav a:hover,.nav a:focus{background:var(--accent-soft);color:var(--accent)}
.nav .sec{font-size:.7rem;letter-spacing:.06em;color:var(--mut);margin:.9rem 0 .3rem;padding-left:.5rem}
.main{padding:1.6rem 1.5rem 4rem;min-width:0}
h1{font-size:clamp(1.35rem,2.2vw,1.75rem);letter-spacing:-.025em;margin:0 0 .4rem;font-weight:750;line-height:1.28}
h2{font-size:1.12rem;margin:2.1rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid var(--accent);font-weight:700;scroll-margin-top:0}
h3{font-size:1rem;margin:.15rem 0 .45rem;font-weight:700}
p,li{color:var(--ink-2)}.muted{color:var(--mut);font-size:.92rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1rem 1.1rem;margin:.7rem 0;box-shadow:var(--shadow)}
.verdict{border-color:#b7d9cb;background:linear-gradient(180deg,#f4faf7,var(--surface))}
.tag{display:inline-block;font-size:11px;font-weight:650;background:var(--accent-soft);color:var(--accent);padding:.1rem .45rem;border-radius:999px;margin-left:.3rem}
.tag.ok{background:var(--ok-soft);color:var(--ok)}
.warn{font-size:.86rem;color:var(--warn);background:var(--warn-soft);border-radius:8px;padding:.55rem .7rem}
a{color:var(--accent);text-underline-offset:3px}
code{font-size:.78rem;background:#efeae0;padding:.05rem .3rem;border-radius:4px}
code.tiny{font-size:.7rem;word-break:break-all}
table{width:100%;border-collapse:collapse;font-size:.86rem;background:var(--surface);margin:.5rem 0}
th,td{border:1px solid var(--line);padding:.4rem .5rem;text-align:left;vertical-align:top}th{background:#efeae0}
.grid2{display:grid;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr));gap:.6rem}
ul.compact{margin:.2rem 0 0;padding-left:1.1rem;font-size:.84rem}
ul.feed{margin:0;padding-left:1.2rem}
.fcard{position:relative;border-top:1px solid var(--line);padding:.7rem 0 .6rem}
.fcard time{position:absolute;top:.7rem;right:0;font-size:.72rem;color:var(--mut)}
.fr{margin:.15rem 0;font-size:.92rem;line-height:1.55}
.fr b{display:block;font-size:.74rem;color:var(--mut);font-weight:650;letter-spacing:.03em}
.fcard .fr:first-of-type{padding-right:5.5rem}
.fbtn{margin-top:.4rem;font-size:.8rem;padding:.3rem .7rem}
.mob{display:none;flex-wrap:wrap;gap:.35rem;margin:0 0 1rem}
.mob a{font-size:.78rem;background:var(--accent-soft);color:var(--accent);text-decoration:none;padding:.2rem .5rem;border-radius:999px}
.foot{margin-top:2.5rem;font-size:.86rem;color:var(--mut);border-top:1px solid var(--line);padding-top:1rem}
.btn{display:inline-flex;align-items:center;gap:.35rem;background:var(--accent);color:#fff!important;text-decoration:none;font-weight:650;font-size:.88rem;padding:.45rem .85rem;border-radius:999px;border:0;cursor:pointer}
.btn.sec{background:var(--accent-soft);color:var(--accent)!important}
.btn.ghost{background:transparent;color:var(--accent)!important;border:1px solid var(--accent)}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(7.5rem,1fr));gap:.55rem;margin:.6rem 0}
.gallery a{display:block;border-radius:10px;overflow:hidden;border:1px solid var(--line);background:#efeae0}
.gallery img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}
.draft-head{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;justify-content:space-between;margin:0 0 .4rem}
.copybox{position:relative;background:#efeae0;border-radius:10px;padding:.7rem .8rem;font-size:.88rem;white-space:pre-wrap;word-break:break-word;margin:.4rem 0}
.copybox .copybtn{position:absolute;top:.4rem;right:.4rem}
@media(max-width:900px){.shell{grid-template-columns:1fr}.nav{display:none}.mob{display:flex}.main{padding:1.1rem 1rem 3rem}}
'''

POST_CSS = '''
:root{--bg:#f3f1eb;--surface:#fffcf7;--ink:#1a1c1b;--ink-2:#3d433f;--mut:#59656b;--line:#e2ddd2;--accent:#0d6b52;--accent-soft:#e4f3ec}
*{box-sizing:border-box}html{scroll-behavior:auto}
body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.65 "PingFang SC","Hiragino Sans GB","Noto Sans SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:28rem;margin:0 auto;padding:1rem 1rem 3.5rem}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem;font-size:.82rem}
.topbar a{color:var(--accent);text-decoration:none}
h1{font-size:1.25rem;margin:0 0 .6rem;line-height:1.35;font-weight:750}
.row{display:flex;gap:.4rem;flex-wrap:wrap;margin:.4rem 0 .8rem}
button,.btn{appearance:none;border:0;border-radius:999px;padding:.45rem .85rem;font-weight:650;font-size:.86rem;cursor:pointer;background:var(--accent);color:#fff}
button.sec,.btn.sec{background:var(--accent-soft);color:var(--accent)}
.gallery{display:flex;flex-direction:column;gap:.7rem;margin:1rem 0}
.gallery figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.gallery img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;background:#efeae0}
.gallery figcaption{display:flex;justify-content:space-between;padding:.45rem .7rem;font-size:.8rem;color:var(--mut)}
.gallery a{color:var(--accent)}
.label{font-size:.78rem;font-weight:700;color:var(--mut);margin:1rem 0 .3rem;letter-spacing:.04em}
.box{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.85rem .9rem 2.4rem;white-space:pre-wrap;word-break:break-word;font-size:.92rem;color:var(--ink-2)}
.box .copy{position:absolute;right:.55rem;bottom:.55rem}
.toast{position:fixed;left:50%;bottom:1.4rem;transform:translateX(-50%);background:#1a1c1b;color:#fff;padding:.45rem .9rem;border-radius:999px;font-size:.82rem;opacity:0;pointer-events:none;transition:opacity .2s;z-index:9}
.toast.show{opacity:1}
.hint{font-size:.8rem;color:var(--mut);margin:.3rem 0 .8rem}
'''

def _load_shell():
    mod = getattr(_load_shell, "mod", None)
    if mod is not None:
        return mod
    import importlib.util
    path = SITE / "apply_xhs_shell.py"
    spec = importlib.util.spec_from_file_location("apply_xhs_shell_nav", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"missing {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _load_shell.mod = mod
    return mod

def _nav(d, day_ids=None):
    """Sidebar: day signals first, then library long-lived."""
    day_ids = list(day_ids or [])
    day_ids = [(i, lab) for i, lab in day_ids if i not in ("day-foot", "foot", "notes")]
    lib_items = [
        ("lib", "库长驻", None),
        ("tools", "长驻工具", "#tools"),
        ("curriculum", "课表", "curriculum.html"),
        ("drafts", "已成稿", "#drafts"),
        ("pos", "定位", "#pos"),
        ("plan", "发布计划", "#plan"),
        ("main", "主线系列", "#main"),
        ("side", "辅线「我学 AI」", "#side"),
        ("tingji", "听记选题", "#tingji"),
        ("bench", "对标动态", "#bench"),
        ("profiles", "对标档案", "#profiles"),
        ("growth", "起号与变现", "#growth"),
        ("log", "更新记录", "#log"),
    ]
    entries = []
    mob = []
    for i, lab in day_ids:
        entries.append((i, E(lab), f"#{i}"))
        mob.append(f'<a href="#{i}">{E(lab)}</a>')
    for i, lab, href in lib_items:
        if href is None:
            continue
        entries.append((i, E(lab), href))
        mob.append(f'<a href="{href}">{E(lab)}</a>')
    links_s = _load_shell().group_hub_links(entries)
    links_s += (
        '<div class="sec">完整页</div>'
        '<a href="growth/">成长记录专属入口 →</a>'
        '<a href="day/">往期日页归档 →</a>'
    )
    mob_s = "".join(mob)
    mob_s += (
        '<a href="growth/">成长记录</a>'
        '<a href="day/">往期日页</a>'
    )
    meta = d.get("meta") or {}
    brand = E(meta.get("title", "小红书"))
    updated = E(meta.get("updated_label", ""))
    aside = (
        '<aside class="nav">'
        '<div class="brand-row"><img src="icon.svg" width="28" height="28" alt=""/>'
        f'<p class="brand" style="margin:0">{brand}</p></div>'
        f'<p class="meta">私密全入口 · {updated}<br>不进入公开周报</p>'
        + links_s +
        "</aside>"
    )
    return aside, mob_s


def _plan(d):
    pp = d.get('publish_plan') or {}
    items = pp.get('items') or []
    rows = []
    for it in items:
        st = it.get('status') or ''
        if st == '成稿':
            badge = '<span class="tag ok">成稿</span>'
        elif st == '大纲':
            badge = '<span class="tag">大纲</span>'
        else:
            badge = '<span class="tag" style="background:#eee;color:#666">待写</span>'
        if it.get('text_href') and it.get('images_href'):
            links = (f'<a href="{E(it["text_href"])}">查看文字</a>'
                     f' · <a href="{E(it["images_href"])}">查看图片</a>')
        else:
            links = '<span class="muted">待写</span>'
        rows.append(
            f"<tr><td>{int(it.get('seq') or 0)}</td>"
            f"<td>{E(it.get('date',''))}</td>"
            f"<td><code>{E(it.get('id',''))}</code></td>"
            f"<td>{E(it.get('title',''))}</td>"
            f"<td>{E(it.get('track',''))}</td>"
            f"<td>{badge}</td>"
            f"<td>{links}</td></tr>"
        )
    rhythm = E(pp.get('rhythm') or '')
    return f'''<h2 id="plan">发布计划</h2>
<p class="muted">{rhythm}。routine 可改 <code>publish_plan.items</code> 的日期与状态。</p>
<table>
<thead><tr><th>序号</th><th>计划日期</th><th>集数</th><th>标题</th><th>主线/辅线</th><th>状态</th><th>查看</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>'''


def _curriculum(d):
    c = d.get('curriculum') or {}
    if not c:
        return ''
    lc = c.get('lenny_capacity') or {}
    tot = c.get('totals') or {}
    cad = c.get('cadence') or {}
    by = tot.get('by_module') or {}
    chips = ''.join(
        f'<span class="tag" style="margin:.15rem">{E(k)} · {int(v)}</span>'
        for k, v in by.items()
    )
    top = c.get('top5_next') or []
    top_rows = ''.join(
        f"<tr><td><code>{E(t.get('id',''))}</code></td>"
        f"<td>{E(t.get('title',''))}</td>"
        f"<td>{E(t.get('why',''))}</td></tr>"
        for t in top
    )
    mod_html = []
    for m in c.get('modules') or []:
        mid = E(m.get('id', ''))
        lessons = m.get('lessons') or []
        rows = []
        for les in lessons:
            st = les.get('status') or ''
            if st == '已成稿':
                badge = '<span class="tag ok">已成稿</span>'
            elif st.startswith('素材'):
                badge = '<span class="tag">素材槽</span>'
            else:
                badge = '<span class="tag" style="background:#eee;color:#666">待写</span>'
            rows.append(
                f"<tr id=\"cu-{E(les.get('id',''))}\">"
                f"<td><code>{E(les.get('id',''))}</code></td>"
                f"<td>{E(les.get('title',''))}{badge}</td>"
                f"<td>{E(les.get('one_liner',''))}</td>"
                f"<td>{E(str(les.get('source') or ''))}</td>"
                f"<td>{E(str(les.get('ocean_case') or ''))}</td></tr>"
            )
        for les in m.get('tingji_slots') or []:
            rows.append(
                f"<tr><td><code>{E(les.get('id',''))}</code></td>"
                f"<td>{E(les.get('title',''))}<span class=\"tag\">素材槽→{E(str(les.get('maps_to') or ''))}</span></td>"
                f"<td>{E(les.get('one_liner',''))}</td>"
                f"<td>{E(str(les.get('source') or ''))}</td>"
                f"<td>{E(str(les.get('ocean_case') or ''))}</td></tr>"
            )
        credit = E(m.get('credit') or m.get('blurb') or '')
        mod_html.append(
            f'<h3 id="mod-{mid}">{E(m.get("name",""))} '
            f'<span class="muted">（{int(m.get("count") or len(lessons))} 节）</span></h3>'
            f'<p class="muted">{credit}</p>'
            f'<table><thead><tr><th>编号</th><th>标题</th><th>一句话</th><th>来源</th><th>Ocean案例</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>'
        )
    return (
        f'<h2 id="curriculum">课表</h2>'
        f'<div class="card verdict">'
        f'<p style="margin:0 0 .4rem"><strong>{E(c.get("positioning",""))}</strong></p>'
        f'<p class="muted" style="margin:0 0 .6rem">{E(c.get("voice",""))}</p>'
        f'<p style="margin:0 0 .4rem">总节数（课表列出）<strong>{int(tot.get("lessons_listed") or 0)}</strong>'
        f' · 模块 <strong>{int(tot.get("modules") or 0)}</strong>'
        f' · Lenny 推荐容量 <strong>{E(str(lc.get("recommended_series_count","")))}</strong></p>'
        f'<p class="muted" style="margin:0 0 .5rem">Lenny 池 {int(lc.get("pool_total") or 0)}'
        f' → usable {int(lc.get("usable_md") or 0)}'
        f' → craft {int(lc.get("craft_pm_hits") or 0)}'
        f' → 去重可用扩展 {int(lc.get("deduped_available_beyond_mapped") or 0)}'
        f'（已映射 M={int(lc.get("currently_mapped_to_M") or 0)}）</p>'
        f'<div>{chips}</div>'
        f'<p class="muted" style="margin:.7rem 0 0">节奏：{E(cad.get("main",""))}；'
        f'{E(cad.get("side_ai",""))}；{E(cad.get("notes",""))}</p>'
        f'<p class="hint" style="margin:.5rem 0 0">{E(c.get("tingji_note",""))}</p>'
        f'</div>'
        f'<h3>接下来优先写的 5 节</h3>'
        f'<table><thead><tr><th>ID</th><th>标题</th><th>为什么先写</th></tr></thead>'
        f'<tbody>{top_rows}</tbody></table>'
        + ''.join(mod_html)
    )


def _growth_count():
    """人数取自成长页唯一名单 xhs/growth/src/people.json；缺文件时不写数字。"""
    try:
        return f" · {len(json.loads((SITE / 'growth' / 'src' / 'people.json').read_text())['people'])} 人"
    except (OSError, ValueError, KeyError):
        return ""


def _hub_today(d):
    """Long-lived tools strip; today intel embedded via build_day_body in render()."""
    return (
        '<h2 id="tools"><span class="sec-ico" aria-hidden="true">▣</span> 长驻工具</h2>'
        '<div class="card"><ul class="feed" style="margin:0">'
        '<li><a href="curriculum.html"><b>课表</b></a> — 主线/辅线进度</li>'
        '<li><a href="#drafts"><b>已成稿发布页</b></a> — 可复制正文与图卡</li>'
        f'<li><a href="growth/"><b>人物成长分析{_growth_count()}</b></a> — 按人名进，唯一入口</li>'
        '<li><a href="#pos">定位</a> · <a href="#plan">发布计划</a> · '
        '<a href="#main">主线系列</a> · <a href="#growth">起号</a></li>'
        '<li><a href="day/"><b>往期日页归档</b></a> — 旧 daily/、feed/ 仍留档不进导航</li>'
        "</ul></div>"
    )


def _daily(d):
    # backward name kept for callers; hub replaces the old daily dump
    return _hub_today(d)


def _pos(d):
    p = d.get('positioning') or {}
    rules = ''.join(f'<li>{E(r)}</li>' for r in (p.get('rules') or []))
    pillars = ' · '.join(E(x) for x in (p.get('pillars') or []))
    return f'''<h2 id="pos">定位</h2>
<div class="card verdict">
  <p style="margin:0 0 .5rem;font-size:1.05rem"><strong>{E(p.get('line',''))}</strong></p>
  <p class="muted" style="margin:0 0 .5rem">三大支柱：{pillars}</p>
  <ul style="margin:0">{rules}</ul>
  <p class="warn" style="margin:.8rem 0 0">{E((d.get('meta') or {}).get('privacy',''))}</p>
</div>'''

def _main(d):
    rows = []
    for e in d.get('main_series') or []:
        badge = '<span class="tag ok">已成稿</span>' if e.get('draft_done') else '<span class="tag">大纲</span>'
        post = f' · <a href="post/{E(e["id"])}.html"><b>发布页</b></a>' if e.get('draft_done') else ''
        lenny = ''
        if e.get('lenny_url'):
            lenny = (f'<a href="{E(e["lenny_url"])}" target="_blank" rel="noopener">Lenny 原文</a>'
                     f'<br><code class="tiny">{E(e.get("lenny_file",""))}</code>')
        rows.append(
            f"<tr id=\"{E(e['id'])}\"><td><code>{E(e['id'])}</code></td><td>{E(e.get('pillar',''))}</td>"
            f"<td>{E(e.get('title',''))}{badge}{post}</td>"
            f"<td>{lenny}</td></tr>"
        )
    return f'''<h2 id="main">主线系列 M01–M20</h2>
<p class="muted">理解问题 → 定优先级 → 写文档 → 开会对齐 → 推进落地 → 复盘 → 用 AI 提效。Lenny 链接仅挂在大纲/素材列；成稿请走「发布页」。</p>
<table>
<thead><tr><th>ID</th><th>步骤</th><th>标题</th><th>素材（Lenny）</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>'''

def _draft_gallery(e):
    did = e['id']
    files = _card_files(e)
    draft = e.get('draft') or {}
    imgs = ''
    for i, fn in enumerate(files, 1):
        src = f'cards/{did}/{fn}'
        imgs += (f'<a href="{E(src)}" target="_blank" rel="noopener" title="图{i}">'
                 f'<img src="{E(src)}" alt="{E(did)} 图{i}" loading="lazy"></a>')
    zip_name = draft.get('zip') or f'{did}-cards.zip'
    zip_href = f'cards/{did}/{zip_name}'
    zip_link = ''
    if (SITE / 'cards' / did / zip_name).exists() or files:
        zip_link = f'<a class="btn sec" href="{E(zip_href)}">下载 ZIP</a>'
    title = draft.get('title') or draft.get('cover_title') or e.get('title', '')
    return f'''<div class="card" id="draft-{E(did)}">
  <div class="draft-head">
    <h3 style="margin:0">{E(did)} · {E(title)} <span class="tag ok">已成稿</span></h3>
    <span>
      <a class="btn" href="post/{E(did)}.html">发布页</a>
      {zip_link}
    </span>
  </div>
  <p class="muted" style="margin:0 0 .4rem">共 {len(files) or draft.get('n_cards') or '?'} 张图 · 点图放大 · 发布页可一键复制正文/话题</p>
  <div class="gallery">{imgs or '<p class="muted">图片生成中…</p>'}</div>
</div>'''

def _drafts(d):
    blocks = [_draft_gallery(e) for e in finished_drafts(d)]
    return f'''<h2 id="drafts">已成稿发布页</h2>
<p class="muted">每篇有独立发布页（标题/图片/正文/话题/评论引导）。发布页与成稿区<strong>不含</strong> Lenny 原文链接。</p>
{''.join(blocks)}'''

def _side(d):
    cards = []
    for e in d.get('side_series') or []:
        badge = '<span class="tag ok">已成稿</span>' if e.get('draft_done') else '<span class="tag">待写</span>'
        post = f' <a class="btn" href="post/{E(e["id"])}.html" style="margin-left:.4rem">发布页</a>' if e.get('draft_done') else ''
        cards.append(f'<div class="card" id="{E(e["id"])}"><strong>{E(e["id"])}</strong> · {E(e.get("title",""))}{badge}{post}</div>')
    return f'''<h2 id="side">辅线「我学 AI 的过程」</h2>
<p class="muted">穿插主线之间，服务「把活干好」，不抢主线课表。</p>
{''.join(cards)}'''

def _tingji(d):
    cards = []
    for t in d.get('tingji_topics') or []:
        ep = t.get('episode') or ''
        ep_link = f'<a href="#{E(ep)}"><code>{E(ep)}</code></a>' if ep else ''
        lenny = ''
        if t.get('lenny_url'):
            lenny = f' · <a href="{E(t["lenny_url"])}" target="_blank" rel="noopener">Lenny 原文</a>'
            if t.get('lenny_file'):
                lenny += f' <code class="tiny">{E(t["lenny_file"])}</code>'
        cards.append(
            f'''<div class="card">
  <h3>{E(t.get('id',''))} · {E(t.get('title',''))} <span class="tag">{E(t.get('theme',''))}</span></h3>
  <p><strong>问题模式（脱敏）：</strong>{E(t.get('pattern',''))}</p>
  <p class="muted" style="margin:0">映射：{ep_link} · {E(t.get('episode_note',''))}{lenny}</p>
</div>'''
        )
    return f'''<h2 id="tingji">听记选题</h2>
<p class="muted">从真实会议里抽象出的复发工作问题。网页仅脱敏课纲；源文件路径不出现在本页。</p>
{''.join(cards)}'''

def _num(x):
    try: return float(str(x).replace(',', '').replace('万', 'e4'))
    except ValueError: return None

def _feed_card(i):
    what = i.get('what') or i.get('text', '')
    lk, sv = i.get('likes', ''), i.get('saves', '')
    parts = [f'{E(lk)} 赞' if lk else '', f'{E(sv)} 收藏' if sv else '', E(i.get('other', ''))]
    data = ' · '.join(x for x in parts if x) or '未记录'
    nl, ns = _num(lk), _num(sv)
    if ns is not None and (nl is None or ns > nl):
        data += ' <span class="tag">收藏型</span>'
    use = i.get('use', '')
    btn = f'<a class="btn sec fbtn" href="{E(i["url"])}" target="_blank" rel="noopener">看原帖 →</a>' if i.get('url') else ''
    rows = f'<p class="fr"><b>他发了什么</b>{E(what)}</p><p class="fr"><b>数据</b>{data}</p>'
    if use:
        rows += f'<p class="fr"><b>你能怎么用</b>{E(use)}</p>'
    return f'<div class="fcard"><time>{E(i.get("date", ""))}</time>{rows}{btn}</div>'

def _feed(d):
    """对标博主动态：按博主分组，每条三行卡片。
    item 字段：date who what likes saves other use url（旧 text 字段兜底）。
    use 里写集号要写全名，如「第 07 集·用 AI 提效」。"""
    f = d.get('benchmark_feed') or {}
    items = f.get('items') or []
    bios = f.get('creators') or {}
    if not items:
        body = f'<div class="card muted">{E(f.get("note","本次无新可借鉴。"))}</div>'
    else:
        groups = {}
        for i in sorted(items, key=lambda x: x.get('date', ''), reverse=True):
            groups.setdefault(i.get('who', ''), []).append(i)
        body = ''.join(
            f'<div class="card fgroup"><h3>{E(w)} <span class="muted" style="font-weight:400;font-size:.85rem">· {len(g)} 条</span></h3>'
            + (f'<p class="muted" style="margin:0 0 .5rem">{E(bios[w])}</p>' if bios.get(w) else '')
            + ''.join(_feed_card(i) for i in g) + '</div>'
            for w, g in groups.items()
        )
    return f'''<h2 id="bench">对标博主动态</h2>
<p class="muted">按博主分组，最新的在前。「收藏型」= 收藏比点赞多，说明大家存下来要用。</p>{body}'''

def _profiles(d):
    cards = []
    for c in d.get('benchmark_profiles') or []:
        inf = ''.join(f'<li>{E(x)}</li>' for x in (c.get('inflect') or []))
        st = ''.join(f'<li>{E(x)}</li>' for x in (c.get('steal') or []))
        href = c.get('profile_url') or 'creators.html'
        cards.append(
            f'''<div class="card">
  <h3><a href="{E(href)}">{E(c.get('name',''))}</a></h3>
  <p class="muted" style="margin:0 0 .4rem">{E(c.get('why',''))}</p>
  <p style="margin:0 0 .2rem"><strong>拐点</strong></p><ul style="margin:.2rem 0 .6rem">{inf}</ul>
  <p style="margin:0 0 .2rem"><strong>可借鉴</strong></p><ul style="margin:.2rem 0 .6rem">{st}</ul>
  <a class="btn sec" href="{E(href)}">完整档案</a>
</div>'''
        )
    return f'''<h2 id="profiles">对标博主档案</h2>
<p class="muted">下方为摘要。完整时间线 / 拐点表 / 成功经验三列 / 收入与来源见
<a href="growth/"><b>人物成长研究</b></a>（每人一页，与本地研究页同步）。</p>
<div class="card verdict" style="display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;justify-content:space-between">
  <span>14 人各一页，另有分类对照等专题。</span>
  <a class="btn" href="growth/">打开人物成长研究 →</a>
</div>
{''.join(cards)}'''

LENNY_DIR = Path('/workspace/lenny/newsletter-MD')
LENNY_CARDS = ROOT / 'monitors' / 'lenny_cards_zh.json'
LENNY_USED = ROOT / 'monitors' / 'xhs_lenny_used.json'
LENNY_CSS = (
    '.lz-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr));gap:.9rem;align-items:start}'
    '.lz{min-width:0;overflow-wrap:anywhere;background:#fffcf7;border:1px solid var(--line);border-radius:16px;padding:.9rem 1rem}'
    '.lz h3{color:var(--accent);font-size:1.02rem;margin:.3rem 0 .45rem;line-height:1.4}'
    '.lz p{margin:.28rem 0;font-size:.9rem;line-height:1.55}'
    '.lz p b{display:block;font-size:.7rem;color:var(--mut);font-weight:650;letter-spacing:.03em}'
    '.lz .pill{display:inline-block;font-size:.7rem;font-weight:650;background:var(--accent-soft);color:var(--accent);padding:.1rem .55rem;border-radius:999px;margin:0 .3rem .2rem 0}'
    '.lz .pill.mut{background:#efece5;color:var(--mut)}'
    '.lz details{margin-top:.4rem;font-size:.8rem;color:var(--mut)}.lz details>summary{cursor:pointer}'
    '.lz-grp>summary{cursor:pointer;font-weight:700;padding:.5rem 0;color:var(--ink)}'
)


def _lenny_meta(fname):
    """front matter url + H1 中文部分（无卡片元数据时的机械兜底）。"""
    path = LENNY_DIR / fname
    if not path.exists():
        return None
    head = path.read_text(errors='ignore')[:4000]
    url = (re.search(r'^url:\s*"?([^"\n]+)"?', head, re.M) or [None, ''])[1]
    h1 = (re.search(r'^#\s+(.+)$', head, re.M) or [None, ''])[1]
    zh = h1.split(' — ')[0].strip() if ' — ' in h1 else ''
    return {'url': url.strip(), 'h1_zh': zh}


def _lenny_status(pool):
    used_doc = {}
    if LENNY_USED.exists():
        used_doc = json.loads(LENNY_USED.read_text())
    used = list(dict.fromkeys(
        [x.get('file', '') for x in (pool.get('used_links') or [])]
        + list(pool.get('used') or []) + list(used_doc.get('used') or [])))
    groups = [
        ('cand', '候选 · 下一批可写', list(pool.get('next_candidates') or [])),
        ('used', '已用 · 可复盘与延伸', used),
        ('map', '课表已映射', list(pool.get('curriculum_mapped') or [])[:25]),
        ('unused', '未用样例', [f for f in (pool.get('unused_sample') or []) if f not in set(used)][:15]),
    ]
    status = {}
    for key, _label, files in groups:
        for f in files:
            if f:
                status.setdefault(f, []).append(key)
    return groups, status


LENNY_PILL = {'cand': '候选', 'used': '已用', 'map': '课表映射', 'unused': '未用样例'}


def _lenny_card(f, st, cards):
    c = cards.get(f) or {}
    meta = _lenny_meta(f)
    pills = ''.join(f'<span class="pill">{LENNY_PILL[k]}</span>' for k in st)
    url = (meta or {}).get('url') or ''
    if not url.startswith(('https://', 'http://')):
        url = ''
    link = f'<a href="{E(url)}" target="_blank" rel="noopener">Lenny 原文</a>' if url else '原文链接缺失'
    if meta is None:
        return (f'<article class="lz">{pills}<span class="pill mut">本地库缺原文</span>'
                f'<h3>原文缺失，未解读</h3><details><summary>溯源</summary><code>{E(f)}</code></details></article>')
    if not (c.get('title_zh') and c.get('reason') and c.get('audience') and c.get('angle')):
        t = meta.get('h1_zh') or '（无中文标题）'
        return (f'<article class="lz">{pills}<span class="pill mut">未解读</span><h3>{E(t)}</h3>'
                f'<p class="muted">尚未逐篇阅读，暂无推荐理由 / 面向用户 / 切入视角。</p><p>{link}</p>'
                f'<details><summary>溯源</summary><code>{E(f)}</code></details></article>')
    fu = f'<p><b>可复盘 / 延伸</b>{E(c["followup"])}</p>' if ('used' in st and c.get('followup')) else ''
    ev = ''.join(f'<li>「{E(x.get("quote",""))}」· {E(x.get("section",""))}</li>' for x in (c.get('evidence') or []))
    return (f'<article class="lz">{pills}<h3>{E(c["title_zh"])}</h3>'
            f'<p><b>推荐理由</b>{E(c["reason"])}</p><p><b>面向用户</b>{E(c["audience"])}</p>'
            f'<p><b>切入视角</b>{E(c["angle"])}</p>{fu}<p>{link}</p>'
            f'<details><summary>溯源</summary><code>{E(f)}</code><ul>{ev}</ul></details></article>')


def _lenny(d):
    pool = d.get('lenny_pool') or {}
    home = pool.get('home_url') or 'https://www.lennysnewsletter.com/'
    cards = json.loads(LENNY_CARDS.read_text()) if LENNY_CARDS.exists() else {}
    groups, status = _lenny_status(pool)
    seen, parts, done = set(), [], 0
    for key, label, files in groups:
        items = [f for f in dict.fromkeys(files) if f and f not in seen]
        seen.update(items)
        if not items:
            continue
        body = ''.join(_lenny_card(f, status[f], cards) for f in items)
        done += sum(1 for f in items if _lenny_meta(f) is not None and all((cards.get(f) or {}).get(k) for k in ('title_zh', 'reason', 'audience', 'angle')))
        opened = ' open' if key == 'cand' else ''
        parts.append(f'<details class="lz-grp"{opened}><summary>{label}（{len(items)}）</summary>'
                     f'<div class="lz-grid">{body}</div></details>')
    return (f'<style>{LENNY_CSS}</style><h2 id="lenny">Lenny 素材池</h2>'
            f'<p class="muted">本地库共 {E(str(pool.get("all_count","?")))} 篇；本块展示 {len(seen)} 篇，'
            f'已逐篇解读 {done} 篇，其余标「未解读」或「本地库缺原文」。一篇只出现在一个分组，标签显示它的全部状态。'
            f' · <a href="{E(home)}" target="_blank" rel="noopener">lennysnewsletter.com</a></p>'
            + ''.join(parts))

def _growth(d):
    g = d.get('growth') or {}
    lis = ''.join(f'<li>{E(x)}</li>' for x in (g.get('bullets') or []))
    return f'''<h2 id="growth">起号与变现</h2>
<div class="card"><h3>{E(g.get('title','起号与变现'))}</h3><ul>{lis}</ul>
<p class="muted" style="margin:.6rem 0 0">完整 learn-in-public 涨粉/变现见
<a href="topic-lip-growth.html">专题 · learn-in-public 怎么涨 &amp; 变现</a></p></div>'''

def _log(d):
    blocks = []
    for i, e in enumerate(d.get('changelog') or []):
        added = e.get('added')
        head = f"{E(e.get('date',''))} · {E(e.get('title') or '更新')}"
        if added:
            head += f" · 今日新增 {int(added)} 条" if i == 0 else f" · 新增 {int(added)} 条"
        notes = ''.join(f'<li>{E(n)}</li>' for n in (e.get('notes') or []))
        blocks.append(f'<div class="card"><h3>{head}</h3><ul>{notes}</ul></div>')
    return f'''<h2 id="log">更新记录</h2>
<p class="muted">按日期倒序。routine 追加请改 monitors/xhs_library.json 或运行 <code>python3 xhs_library.py --append-note "…"</code>。</p>
{''.join(blocks)}'''

def _merged_from_digest(d):
    """原日报「小红书选题推荐」tab 已下掉，内容并入本页（去重）：
    当前建议 + 选题卡（与主线/辅线标题重复的去掉）→「今日选题推荐」；起号最快办法 → 并在「起号与变现」下；灵感池 → 「灵感池」。
    定位、课表本页已有，不重复。返回 (picks_html, growth_html, lgc_html, css)。"""
    import importlib.util as _u, re as _re, os as _os
    base = _os.path.dirname(_os.path.abspath(__file__))
    def _load(name):
        sp = _u.spec_from_file_location(name, _os.path.join(base, name + '.py'))
        m = _u.module_from_spec(sp); sp.loader.exec_module(m); return m
    picks = growth = lgc = css = ''
    def _blk(h, start):
        i = h.find(start)
        if i < 0: return ''
        depth = 0
        for t in _re.finditer(r'<(/?)div\b[^>]*>', h[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: return h[i:i + t.end()]
        return ''
    norm = lambda t: _re.sub(r'[\W_]+', '', _re.sub(r'<[^>]+>', '', t)).lower()
    have = set()
    for k in ('main_series', 'side_series', 'main', 'side', 'tingji_topics'):
        for e in (d.get(k) or []):
            if isinstance(e, dict) and e.get('title'): have.add(norm(e['title']))
    try:
        X = _load('xhs_section'); h = X.panel(); css += X.CSS
        adv = _blk(h, '<div class="xha">')
        adv = _re.sub(r'<div class="warn"[^>]*>[^<]*</div>', '', adv)
        cards, seen, n = [], set(), 0
        pos = 0
        while True:
            i = h.find('<div class="xhc">', pos)
            if i < 0: break
            c = _blk(h[i:], '<div class="xhc">'); pos = i + max(len(c), 1)
            t = _re.search(r'<h3>\s*\d+\.\s*([^<]+)', c)
            key = norm(t.group(1)) if t else c
            if key in have or key in seen: n += 1; continue
            seen.add(key); cards.append(c)
        g = _blk(h, '<div class="xhg">')
        upd = _re.search(r'更新于 ([^<]+)</span>', h)
        if adv or cards:
            picks = (f'<h2 id="picks">今日选题推荐</h2><div id="xhs"><p class="muted">原日报「小红书选题推荐」并入此处 · 更新于 {E(upd.group(1)) if upd else "待核"}'
                     f' · 共 {len(cards)} 条' + (f'（与主线/辅线重复的 {n} 条已去掉）' if n else '') + '</p>'
                     + adv + ''.join(cards) + '</div>')
        if g: growth = f'<div id="xhs">{g}</div>'
    except Exception as ex:
        print('选题推荐并入失败，跳过', ex)
    try:
        L = _load('inspiration_section'); p = L.panel()
        if p:
            css += L.CSS
            m = _re.match(r'<section\b[^>]*>\s*<div class="ph"><h1>[^<]*</h1>(?:<span class="pd">([^<]*)</span>)?</div>([\s\S]*)</section>\s*$', p)
            if m:
                lgc = f'<h2 id="lgc">灵感池</h2><div id="xhs-lgc"><p class="muted">{E(m.group(1) or "")}</p>{m.group(2)}</div>'
    except Exception as ex:
        print('灵感池并入失败，跳过', ex)
    return picks, growth, lgc, css


def render(d) -> str:
    """Full hub: picks -> signals(+Lenny) -> deep/raw -> library long-lived."""
    import re as _re
    import xhs_day_build as dayb

    day = dayb.load_day()
    day_css = dayb.CSS
    day_body = ""
    day_ids: list[tuple[str, str]] = []
    if day:
        day_body, day_ids = dayb.build_day_body(
            day,
            archive_href="day/",
            hub_href="#tools",
            hub_label="库长驻",
        )
        date_s = E(day.get("date", ""))
        day_body = _re.sub(
            r'<h1 id="top">.*?</h1>|<h1 id=\'top\'>.*?</h1>',
            f'<h2 id="top"><span class="sec-ico" aria-hidden="true">▶</span> 今天写啥 · {date_s}</h2>',
            day_body,
            count=1,
        )

    lenny_html = _lenny(d)
    lenny_html = lenny_html.replace(
        '<h2 id="lenny">Lenny 素材池</h2>',
        '<h2 id="lenny"><span class="sec-ico" aria-hidden="true">◈</span> Lenny · 素材池信号</h2>',
        1,
    )

    insert_at = None
    for anchor in ("id=\"deep\"", "id='deep'", 'id="raw"', "id='raw'",
                   'id="notes"', "id='notes'", 'id="day-foot"', "id='day-foot'"):
        pos = day_body.find(anchor)
        if pos >= 0:
            h2 = day_body.rfind("<h2", 0, pos)
            insert_at = h2 if h2 >= 0 else pos
            break
    if day_body and insert_at is not None:
        day_body = day_body[:insert_at] + lenny_html + day_body[insert_at:]
    elif day_body:
        day_body = day_body + lenny_html
    else:
        day_body = lenny_html

    # Place lenny in nav after last signal, before deep/raw
    new_ids: list[tuple[str, str]] = []
    placed = False
    for i, lab in list(day_ids):
        if (not placed) and i in ("deep", "raw", "notes", "day-foot"):
            new_ids.append(("lenny", "Lenny"))
            placed = True
        new_ids.append((i, lab))
    if not placed:
        last_sig = -1
        for idx, (i, _) in enumerate(new_ids):
            if i in ("xhs", "feed", "insp", "xdiff"):
                last_sig = idx
        if last_sig >= 0:
            new_ids.insert(last_sig + 1, ("lenny", "Lenny"))
        else:
            new_ids.append(("lenny", "Lenny"))
    day_ids = new_ids

    nav, mob = _nav(d, day_ids=day_ids)
    meta = d.get("meta") or {}
    _, growth_x, _, xcss = _merged_from_digest(d)

    lib_body = "\n".join([
        _hub_today(d),
        _curriculum(d), _pos(d), _plan(d), _main(d), _drafts(d), _side(d), _tingji(d),
        _feed(d), _profiles(d), _growth(d) + growth_x, _log(d),
    ])

    hub_extra = (
        ".brand-row{display:flex;align-items:center;gap:.55rem;margin:0 0 .3rem}"
        ".brand-row img{width:28px;height:28px;border-radius:7px;flex:0 0 auto}"
        ".sec-ico{display:inline-block;margin-right:.35rem;font-style:normal;font-weight:700;opacity:.9}"
        ".rawfold{margin:.6rem 0 1.2rem;background:var(--surface);border:1px solid var(--line);"
        "border-radius:var(--r);padding:.4rem .9rem .7rem}"
        ".rawfold summary{cursor:pointer;font-weight:650;color:var(--accent);padding:.35rem 0}"
    )

    title = E(meta.get("title", "小红书"))
    updated = E(meta.get("updated_label", ""))
    parts = [
        "<!DOCTYPE html>",
        '<html lang="zh-Hans">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="robots" content="noindex,nofollow">',
        '<link rel="icon" href="icon.svg" type="image/svg+xml">',
        f"<title>{title} · 全入口 · 私密</title>",
        f"<style>{CSS}{day_css}{xcss}{hub_extra}"
        "@media(max-width:700px){.main table{display:block;overflow-x:auto;max-width:100%}}</style>",
        _load_shell().shell_link("xhs-shell.css"),
        "</head><body>",
        '<div class="shell">',
        nav,
        '<main class="main">',
        f'<nav class="mob">{mob}</nav>',
        f"<h1>{title} · 全入口</h1>",
        f'<p class="muted">今天的选题与信号在上 · 库长驻在下 · 更新 {updated} · 旧 daily/、feed/ 留档不进导航</p>',
        day_body,
        lib_body,
        '<p class="foot">私密页 · 仅 x-digest · 由 <code>xhs_library.py</code> + <code>xhs_day_build.py</code> 生成 · 公开 sanitize 不得收录本目录</p>',
        "</main></div></body></html>",
    ]
    return "".join(parts)


def render_post(e) -> str:
    did = e['id']
    draft = e.get('draft') or {}
    title = draft.get('title') or draft.get('cover_title') or e.get('title', '')
    body = draft.get('body') or draft.get('caption') or ''
    tags = draft.get('hashtags') or ''
    cta = draft.get('cta') or ''
    files = _card_files(e)
    zip_name = draft.get('zip') or f'{did}-cards.zip'
    figs = []
    for i, fn in enumerate(files, 1):
        src = f'../cards/{did}/{fn}'
        figs.append(
            f'<figure><a href="{E(src)}" target="_blank" rel="noopener">'
            f'<img src="{E(src)}" alt="图{i}" loading="lazy"></a>'
            f'<figcaption><span>图{i}</span>'
            f'<a href="{E(src)}" download="{E(did)}-{i:02d}{Path(fn).suffix}">下载</a>'
            f'</figcaption></figure>'
        )
    # SAFETY: post page must not contain Lenny URLs
    return f'''<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>发布 · {E(did)} · {E(title)}</title>
<style>{POST_CSS}</style>
<link rel="stylesheet" href="../xhs-fluid.css" data-xhs-fluid>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a href="../">← 选题库</a>
    <span class="muted">{E(did)} · 发布页</span>
  </div>
  <h1 id="title">{E(title)}</h1>
  <div class="row">
    <button type="button" onclick="copyText(document.getElementById('title').innerText,this)">复制标题</button>
    <a class="btn sec" href="../cards/{E(did)}/{E(zip_name)}">下载全部图片 ZIP</a>
  </div>
  <p class="hint">长按图片可保存到相册；或点「下载」。按顺序传到小红书图文。</p>
  <div class="gallery" id="images">{''.join(figs) or '<p class="hint">图片尚未生成</p>'}</div>

  <div class="label" id="text">正文</div>
  <div class="box" id="body">{E(body)}<button class="copy sec" type="button" onclick="copyText(document.getElementById('body').innerText.replace(/复制正文$/,'').trim(),this)">复制正文</button></div>

  <div class="label">话题标签</div>
  <div class="box" id="tags">{E(tags)}<button class="copy sec" type="button" onclick="copyText(document.getElementById('tags').innerText.replace(/复制话题$/,'').trim(),this)">复制话题</button></div>

  <div class="label">评论区引导</div>
  <div class="box" id="cta">{E(cta)}<button class="copy sec" type="button" onclick="copyText(document.getElementById('cta').innerText.replace(/复制引导$/,'').trim(),this)">复制引导</button></div>
</div>
<div class="toast" id="toast">已复制</div>
<script>
async function copyText(t, btn){{
  t=(t||'').trim();
  try{{ await navigator.clipboard.writeText(t); }}
  catch(e){{
    const a=document.createElement('textarea'); a.value=t; document.body.appendChild(a); a.select();
    document.execCommand('copy'); a.remove();
  }}
  const toast=document.getElementById('toast');
  toast.classList.add('show');
  if(btn){{ const o=btn.textContent; btn.textContent='已复制'; setTimeout(()=>btn.textContent=o,1200); }}
  setTimeout(()=>toast.classList.remove('show'),1200);
}}
</script>
</body>
</html>
'''

def sync_creators():
    """共享源 → 人物页 / 专题页 / creators.html 兼容页。切分规则在站点仓库 xhs/growth/src/split_creators.py。"""
    if not CREATORS_SRC.exists():
        raise SystemExit(f'missing {CREATORS_SRC}')
    html = CREATORS_SRC.read_text()
    # strip private local paths
    html = re.sub(r'/workspace/[^<\s\"\']+', '', html)
    html = re.sub(r'/Users/[^<\s\"\']+', '', html)
    import importlib.util
    spec = importlib.util.spec_from_file_location('split_creators', SITE / 'growth' / 'src' / 'split_creators.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    out_dir = CREATORS_OUT.parent
    outs = mod.split(html)
    for name, page in outs.items():
        for bad in ('/workspace/', '/Users/', 'sources_private', '听记知识库/会议'):
            if bad in page:
                raise SystemExit(f'creators leak: {bad} in {name}')
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, page in outs.items():
        (out_dir / name).write_text(page)
        print(f'wrote {out_dir / name} ({len(page)} bytes)')
    return CREATORS_OUT

def build_posts(d):
    POST_DIR.mkdir(parents=True, exist_ok=True)
    urls = []
    for e in finished_drafts(d):
        html = render_post(e)
        # refuse Lenny links on post pages
        if 'lennysnewsletter.com' in html or 'Lenny 原文' in html:
            raise SystemExit(f'post page must not contain Lenny links: {e["id"]}')
        path = POST_DIR / f'{e["id"]}.html'
        path.write_text(html)
        urls.append(f'https://zhenchuanwuzc-max.github.io/x-digest/xhs/post/{e["id"]}.html')
        print(f'wrote {path}')
    return urls

def build():
    d = load()
    SITE.mkdir(parents=True, exist_ok=True)
    sync_creators()
    post_urls = build_posts(d)
    html = render(d)
    # day raw notes may cite local paths — strip before publish check
    html = re.sub(r'/workspace/[^<\s\"\']+', '', html)
    html = re.sub(r'/Users/[^<\s\"\']+', '', html)
    for bad in ('/workspace/', 'sources_private', '逐字稿.md', '听记知识库/会议', 'aliyuque', 'antfin'):
        if bad in html:
            raise SystemExit(f'refuse publishable leak: {bad!r}')
    OUT.write_text(html)
    print(f'wrote {OUT} ({len(html)} bytes)')
    return OUT, post_urls

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--append-note', default='')
    ap.add_argument('--added', type=int, default=0)
    ap.add_argument('--sync-creators', action='store_true')
    args = ap.parse_args(argv)
    if args.append_note or args.added:
        append_increment(args.append_note, added=args.added)
    if args.sync_creators and not (args.append_note or args.added):
        sync_creators()
        return
    build()

if __name__ == '__main__':
    main()
