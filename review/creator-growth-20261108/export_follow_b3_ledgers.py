"""把仓库外第三批关注证据台账导出成可公开副本 {slug}-ledger.md（规则同第二批：去链接参数、采集账号与关注关系行）。原件不改。"""
from pathlib import Path
import re
import os
BASE = Path(os.environ.get('CG_PRIVATE', '/workspace/creator-growth-20261108'))  # 仓库外证据根目录
SRC = BASE / 'following-batch3'; OUT = Path(__file__).resolve().parent
# 采集账号相关的过滤词放在仓库外私有文件里，不写进公开代码
PRIV = [l.strip() for l in (BASE / 'following/private-drop-patterns.txt').read_text().splitlines() if l.strip()]
DROP = re.compile('|'.join([re.escape(x) for x in PRIV] + ['已关注', 'inventory', 'following', '关注里', '关注列表', 'xsec', '大号', '账户确认', '私有原URL', '私有原始URL', '登录态']))
def clean(t):
    t = re.sub(r'(https://www\.xiaohongshu\.com/[^\s?`）)]+)\?[^\s`）)]*', r'\1', t)
    return '\n'.join(l for l in t.splitlines() if not DROP.search(l)) + '\n'
MAP = {'keruiji': ('keruiji', ['ledger.md']), 'will': ('will', ['ledger.md']), 'huguagua': ('huguagua', ['ledger.md']), 'claire': ('claire', ['ledger.md']), 'fufujie': ('fufujie', ['ledger.md'])}
# 公开副本里不点名被提及的去世者，也不把简介里 @ 的另一账号写成归属
SUB = {'fufujie': [('（读者自述，评论正文疑似宣传性质，真实性未核）', '（读者自述，真实性未核）'), ('，不同位置口径不同，均未核；仅记录页面可见文字。', '；见文末复核附注：不同位置写法不同，未判为矛盾，均未核。')], 'huguagua': [('“你没有说服你还不成功”（按图上可见字记录）', '“你没有说明你还不成功”（原采集笔误记作“说服”，已按 p4 截图更正）')], 'claire': [('“t老师”', '一位'), ('t老师', '该博主'), ('@吟游诗人茶仔', '@另一账号（未点开）')]}
for slug, (d, files) in MAP.items():
    parts = [f'# {slug} 证据台账（公开副本：已去链接参数与采集账号信息；原件在仓库外）\n']
    for n in files:
        t = clean((SRC / d / n).read_text())
        for a, b in SUB.get(slug, []): t = t.replace(a, b)
        parts.append(f'\n<!-- {n} -->\n' + t)
    (OUT / f'{slug}-ledger.md').write_text(''.join(parts)); print('ok', slug)
