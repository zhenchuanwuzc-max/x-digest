"""把仓库外第二批关注证据台账导出成可公开的副本 {slug}-ledger.md：去掉链接参数、采集账号名与关注状态行；原件不改。"""
import re
from pathlib import Path
DROP = re.compile(r'AI具身牛马|已关注|inventory|following|关注里|关注列表|xsec|大号|5098143774|账户确认|私有原URL|关注列表')
def clean(t):
    t = re.sub(r'(https://www\.xiaohongshu\.com/[^\s?`）)]+)\?[^\s`）)]*', r'\1', t)
    return '\n'.join(l for l in t.splitlines() if not DROP.search(l)) + '\n'
SRC = Path('/workspace/creator-growth-20261108/following-batch2')
OUT = Path(__file__).resolve().parent
MAP = {'laoa-yanjiusuo': ('lao-a-yanjiusuo', ['ledger.md', 'n2_vibecoding/supplement-ledger.md', 'third-post-ledger.md']),
       'jason-effi': ('jason', ['ledger.md', 'n2_hook/ledger.md', 'n3_reach/ledger.md']),
       'accio-work': ('accio-work', ['ledger.md', 'n2_multistore_video/ledger.md', 'n3_naming/ledger.md']),
       'zhiwei': ('zhiwei', ['ledger.md'])}
for slug, (d, files) in MAP.items():
    parts = [f'# {slug} 证据台账（公开副本：已去链接参数与采集账号信息；原件在仓库外）\n']
    for n in files:
        parts.append(f'\n<!-- {n} -->\n' + clean((SRC / d / n).read_text()))
    (OUT / f'{slug}-ledger.md').write_text(''.join(parts))
    print('ok', slug)
