"""把仓库外第四批关注证据台账导出成可公开副本 {slug}-ledger.md（规则同第三批：去链接参数、采集账号与关注关系行；按 SUB 去掉邮箱、联系人与被点名的人）。原件不改。"""
from pathlib import Path
import re
import os
import json
BASE = Path(os.environ.get('CG_PRIVATE', '/workspace/creator-growth-20261108'))  # 仓库外证据根目录
SRC = BASE / 'following-batch4'; OUT = Path(__file__).resolve().parent
# 采集账号相关的过滤词放在仓库外私有文件里，不写进公开代码
PRIV = [l.strip() for l in (BASE / 'following/private-drop-patterns.txt').read_text().splitlines() if l.strip()]
DROP = re.compile('|'.join([re.escape(x) for x in PRIV] + ['已关注', 'inventory', 'following', '关注里', '关注列表', 'xsec', '大号', '账户确认', '私有原URL', '私有原始URL', '登录态']))
def clean(t):
    t = re.sub(r'(https://www\.xiaohongshu\.com/[^\s?`）)]+)\?[^\s`）)]*', r'\1', t)
    return '\n'.join(l for l in t.splitlines() if not DROP.search(l)) + '\n'
MAP = {'heideng': ('heideng', ['ledger.md']), 'menqiang': ('menqiang', ['ledger.md']), 'lidan': ('lidan', ['ledger.md'])}
# 公开副本的替换表（邮箱、联系人、被点名的人）放在仓库外私有文件，不写进公开代码
SUB = {k: [tuple(x) for x in v] for k, v in json.loads((BASE / 'following/private-public-subs-b4.json').read_text())['sub'].items()}
for slug, (d, files) in MAP.items():
    parts = [f'# {slug} 证据台账（公开副本：已去链接参数与采集账号信息；原件在仓库外）\n']
    for n in files:
        t = clean((SRC / d / n).read_text())
        for a, b in SUB.get(slug, []): t = t.replace(a, b)
        parts.append(f'\n<!-- {n} -->\n' + t)
    (OUT / f'{slug}-ledger.md').write_text(''.join(parts)); print('ok', slug)
