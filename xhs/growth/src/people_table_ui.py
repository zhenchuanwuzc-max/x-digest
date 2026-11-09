"""人物对比表的排序键 / 内容语言 / 受众标签：只从 people.json 已有字段派生，不改源描述。"""
import re

# 受众标签：从「主要用户」文案归纳，可多选；推断原文仍保留在页面上
AUDIENCE_RULES = (
    ('PM', r'PM|产品经理|产品负责人'),
    ('开发者', r'开发者|程序员|工程师|独立开发'),
    ('创作者', r'创作者|自媒体'),
    ('AI工具使用者', r'AI\s*\S{0,4}工具|用 AI|学 AI|AI 编程|[Vv]ibe [Cc]oding|Skill|AI 产品|Codex|Claude Code|Obsidian|在用 '),
    ('设计师', r'设计'),
    ('职场人', r'职场|上班|打工人'),
    ('学生', r'学生|校招|实习|大学生'),
    ('创业者', r'创业|老板|一人公司|个人事业|独立经营'),
    ('营销人', r'营销'),
    ('商家运营', r'开店|商家|1688|国际站'),
    ('知识付费受众', r'知识付费'),
    ('非技术人', r'非技术|非程序员'),
    ('读者/观众', r'观众|读者'),
)


def parse_count(text, kind):
    """把展示文案解析成排序用整数；未知返回 None。不改展示原文。"""
    if kind == '未找到' or not text or '未找到' in text:
        return None
    t = text.replace(',', '').replace('，', '').replace(' ', '')
    m = re.search(r'约?(\d+(?:\.\d+)?)万', t)
    if m:
        return int(float(m.group(1)) * 10000)
    m = re.search(r'(\d+)', t)
    if m:
        return int(m.group(1))
    return None


def content_lang(person):
    """内容语言：有中文内容/中文平台证据 → zh；否则 unknown（只出现在「全部」）。不按姓名/国籍猜。"""
    users = person.get('users') or ''
    does = person.get('does') or ''
    tags = set(person.get('tags') or [])
    basis = []
    if '中文' in users or '中文' in does:
        basis.append('文案含「中文」')
    hit = tags & {'小红书', '公众号'}
    if hit:
        basis.append('tags含' + '、'.join(sorted(hit)))
    if '小红书' in does or '公众号' in does:
        basis.append('does含中文平台')
    for key, lab in (('xhs', '小红书粉丝'), ('wx', '公众号关注')):
        v = person['metrics'][key]
        if v['kind'] in ('事实', '自述') and '未找到' not in (v.get('text') or ''):
            basis.append(f'{lab}有数值（{v["text"]}）')
    if basis:
        return 'zh', basis
    return 'unknown', ['无中文内容平台或「中文」字样证据，不猜']


def audience_tags(person):
    """从 users 文案匹配标签；返回 (tags, basis)。原文含「推断」时 basis 标明属推断。"""
    users = person.get('users') or ''
    tags = [name for name, pat in AUDIENCE_RULES if re.search(pat, users)]
    basis = [f'匹配「{t}」← users' for t in tags]
    if '推断' in users:
        basis.append('users 原文含「推断」，标签同属推断非实测身份')
    elif tags:
        basis.append('users 原文未标推断')
    if not tags:
        basis.append('users 未命中已知受众词，不编标签')
    return tags, basis


def row_meta(person, ord_index):
    """一行表的派生元数据（排序键 + 语言 + 受众）。"""
    mx = person['metrics']['x']
    mh = person['metrics']['xhs']
    lang, lang_basis = content_lang(person)
    tags, tag_basis = audience_tags(person)
    return {
        'ord': ord_index,
        'x': parse_count(mx['text'], mx['kind']),
        'xhs': parse_count(mh['text'], mh['kind']),
        'lang': lang,
        'lang_basis': lang_basis,
        'audience': tags,
        'audience_basis': tag_basis,
        'x_text': mx['text'],
        'xhs_text': mh['text'],
    }
