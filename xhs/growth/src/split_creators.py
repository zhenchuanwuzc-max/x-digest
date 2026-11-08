"""把共享源 ai-creators-growth.html（已由 sync_creators 去敏）切成人物页 / 专题页 / 旧锚点兼容页。

唯一规则表：ROUTES（旧 h2 段 id → 去向）。人物、专题的名单与标题取自 people.json。
split(html) -> {相对 xhs/ 的文件名: 内容}。不复制正文：每段只进一个文件；兼容页只放链接。
"""
import html as H, json, re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from page_kit import with_brief, blankify, BRIEF_CSS

D = Path(__file__).resolve().parent
META = json.loads((D / 'people.json').read_text())
PEOPLE = {p['id']: p for p in META['people']}
TOPICS = {t['id']: t for t in META['topics']}

# 旧段 id → ('page', 新文件) 渲染进该页；('moved', 目标) 已被独立页取代，只做兼容跳转
ROUTES = {
    **{k: ('page', 'topic-types.html') for k in ('takeaways', 'pm', 'career', 'tools', 'lip', 'bigco', 'ai', 'sources')},
    'lip-growth': ('page', 'topic-lip-growth.html'),
    **{k: ('page', f'{k}.html') for k in ('lenny', 'shreyas', 'ali', 'swyx', 'levelsio', 'justinwelsh')},
    **{k: ('moved', f'{k}.html') for k in ('kazike', 'guizang', 'huashu', 'baoyu', 'qiaomu', 'fankai')},
    'zara': ('moved', 'zhangzala.html'),
    'overseas': ('moved', 'growth/#people'),
}
SUB_LABELS = {'timeline': '成长时间线', 'inflect': '拐点', 'works': '代表作品', 'audience': '谁在看', 'success': '成功经验'}
BACK = '<a href="growth/">← 人物成长研究</a>'
TOC_CSS = '<style>.nav .sub{padding-left:1.2rem;font-size:.82rem}</style>'


def _sections(body):
    """main 内按 h2 切段，返回 [(id, html)]；末尾 foot 丢弃（各页自带）。"""
    main = body[body.index('<main'):body.index('</main>')]
    end = main.find('<p class="foot">')
    main = main[:end] if end >= 0 else main
    starts = [m.start() for m in re.finditer(r'<h2[\s>]', main)]
    out = []
    for a, b in zip(starts, starts[1:] + [len(main)]):
        m = re.match(r'<h2[^>]*\sid="([^"]+)"', main[a:])
        if not m:
            raise SystemExit(f'creators split: h2 without id at {a}')
        out.append((m.group(1), main[a:b]))
    return out


def _text(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def _toc(sid, sec, person):
    h2 = _text(re.search(r'<h2[^>]*>(.*?)</h2>', sec, re.S).group(1)).replace('深描 · ', '').rstrip(' ★')
    items = [f'<a href="#{sid}">{H.escape(h2)}</a>']
    if person:
        for i in re.findall(rf'\sid="({re.escape(sid)}-[a-z]+)"', sec):
            lab = SUB_LABELS.get(i[len(sid) + 1:])
            if lab:
                items.append(f'<a class="sub" href="#{i}">{lab}</a>')
    else:
        for i, t in re.findall(r'<h3[^>]*\sid="([^"]+)"[^>]*>(.*?)</h3>', sec, re.S):
            items.append(f'<a class="sub" href="#{i}">{H.escape(_text(t))}</a>')
    return ''.join(items)


def _page(head, title, brand, toc, content):
    head = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', head, count=1, flags=re.S)
    return (head.replace('</head>', TOC_CSS + '</head>', 1) + '<body>\n<div class="shell">\n'
            f'<aside class="nav" aria-label="本页目录">\n  <p class="brand">{H.escape(brand)}</p>\n  {BACK}\n'
            f'  <div class="sec">本页</div>\n  {toc}\n</aside>\n<main class="main">\n<nav class="mob-nav" aria-label="返回">{BACK}</nav>\n{content}'
            '<p class="foot">私密 · 人物成长研究 · <a href="growth/">← 返回首页</a></p>\n</main>\n</div>\n</body>\n</html>\n')


def _compat(head, ids_to_target):
    rows = ''.join(f'<li id="{H.escape(i)}"><a href="{H.escape(t)}">{H.escape(i)} → {H.escape(t)}</a></li>\n'
                   for i, t in ids_to_target)
    head = re.sub(r'<title>.*?</title>', '<title>已迁移 · 人物成长研究</title>', head, count=1, flags=re.S)
    return (head + '<body>\n<main class="main" style="max-width:40rem;margin:0 auto">\n'
            '<h1>此页已拆分</h1>\n<p class="muted">原「对标完整档案」已拆成人物页和专题页。'
            '请从 <a href="growth/">人物成长研究首页</a> 进入；旧链接请点下面对应条目。</p>\n'
            f'<ul class="compat">\n{rows}</ul>\n</main>\n</body>\n</html>\n')


def split(html):
    head, body = html[:html.index('<body')], html[html.index('<body'):]
    secs = _sections(body)
    unknown = [s for s, _ in secs if s not in ROUTES]
    if unknown:
        raise SystemExit(f'creators split: 未登记的段 {unknown}，请在 ROUTES 里指定去向')
    pages, compat = {}, []
    for sid, sec in secs:
        kind, target = ROUTES[sid]
        ids = [sid] + [i for i in re.findall(r'\sid="([^"]+)"', sec) if i != sid]
        for i in ids:
            compat.append((i, target if kind == 'moved' else f'{target}#{i}'))
        if kind == 'page':
            pages.setdefault(target, []).append((sid, sec))
    out = {}
    for fname, parts in pages.items():
        pid = fname[:-5]
        person = PEOPLE.get(pid)
        toc = '\n  '.join(_toc(s, sec, bool(person)) for s, sec in parts)
        content = ''.join(sec for _, sec in parts)
        if person:
            title = brand = person['name']
            content = with_brief(content, pid, '</p>\n', start='</h2>')
            toc = '<a href="#brief">实操摘要</a>\n  ' + toc
            for x in person.get('extra', []):
                content += f'<p class="muted">附：<a href="{H.escape(x["page_href"])}">{H.escape(x["label"])} →</a></p>\n'
        else:
            t = TOPICS[pid]
            title = brand = t['name']
        page = _page(head, f'{title} · 人物成长研究', brand, toc, content)
        if person:
            page = page.replace('</head>', BRIEF_CSS + '</head>', 1)
        out[fname] = blankify(page)
    vid = re.search(r'<div class="card verdict" id="verdict"', body)
    if vid:
        compat.insert(0, ('verdict', 'growth/#total'))
    out['creators.html'] = blankify(_compat(head, compat))
    return out
