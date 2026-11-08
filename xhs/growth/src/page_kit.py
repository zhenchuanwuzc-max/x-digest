"""人物成长研究模块共用的两件事：人物页顶部实操摘要、跨页链接开新标签。所有生成器都从这里取，避免各写一份。"""
import html as H, json, re
from pathlib import Path

META = json.loads((Path(__file__).resolve().parent / 'people.json').read_text())
PEOPLE = {p['id']: p for p in META['people']}
BRIEF_CSS = ('<style>.brief{border:1px solid #c5d8e0;background:#f3f8fa;border-radius:12px;padding:.8rem 1rem;margin:0 0 1.2rem}'
             '.brief h2{margin:0 0 .5rem;font-size:1.02rem;border:0;padding:0}.brief dl{display:grid;grid-template-columns:7.5em minmax(0,1fr);gap:.3rem .7rem;margin:0}'
             '.brief dt{font-weight:650;color:#1f4f63}.brief dd{margin:0}@media(max-width:560px){.brief dl{grid-template-columns:1fr}.brief dt{margin-top:.3rem}}</style>')


def brief_html(pid):
    b = PEOPLE[pid]['brief']
    rows = [('面向谁', b['who']), ('具体痛点', b['pain']), ('本人怎么解决', b['solve']), ('Ocean 可以做', b['ocean'])]
    return ('<section class="brief" id="brief" aria-label="实操摘要"><h2>实操摘要</h2><dl>'
            + ''.join(f'<dt>{k}</dt><dd>{H.escape(v)}</dd>' for k, v in rows)
            + '</dl></section>\n')


def with_brief(html, pid, after, start=None):
    """在标题简介结束处插入摘要。start=None 时 after 须在全页唯一；否则取 start 字面量之后第一个 after。
    页面有 </head> 时补样式（片段不补，由调用方自己补）。"""
    if 'id="brief"' in html:
        return html
    if start is None:
        assert html.count(after) == 1, (pid, after[:40])
        i = html.index(after)
    else:
        i = html.index(after, html.index(start))
    i += len(after)
    html = html[:i] + brief_html(pid) + html[i:]
    return html if BRIEF_CSS in html else html.replace('</head>', BRIEF_CSS + '</head>', 1)


_A = re.compile(r'<a\b([^>]*?)\shref="([^"]*)"([^>]*)>')


def blankify(html):
    """跨页链接（非 # 开头）一律新标签 + noopener noreferrer；页内锚点不动。"""
    def fix(m):
        pre, href, post = m.group(1), m.group(2), m.group(3)
        if href.startswith('#'):
            return m.group(0)
        attrs = re.sub(r'\s(target|rel)="[^"]*"', '', pre + post)
        return f'<a{attrs} href="{href}" target="_blank" rel="noopener noreferrer">'
    return _A.sub(fix, html)
