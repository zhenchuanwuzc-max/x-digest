"""把仓库外首批关注证据台账导出成可公开的副本 {slug}-ledger.md：去掉链接里的 xsec 等参数、采集账号名与关注状态行。
原件留在仓库外 following-batch1/，不改。"""
import re
from pathlib import Path
SRC = Path('/workspace/creator-growth-20261108/following-batch1')
OUT = Path(__file__).resolve().parent
MAP = {'lulu-ai': 'lulu', 'laoa-jinjie': 'lao-a-jin-jie', 'karl-aigc': 'karlaigc'}
DROP = re.compile(r'AI具身牛马|已关注|inventory|following|关注里|关注列表')
def clean(t):
    t = re.sub(r'(https://www\.xiaohongshu\.com/[^\s?`）)]+)\?[^\s`）)]*', r'\1', t)
    return '\n'.join(l for l in t.splitlines() if not DROP.search(l)) + '\n'
for slug, d in MAP.items():
    parts = [f'# {slug} 证据台账（公开副本：已去链接参数与采集账号信息；原件在仓库外）\n']
    for n in ('ledger.md', 'supplement-ledger.md', 'final-gap-ledger.md'):
        p = SRC / d / n
        if p.exists(): parts.append(f'\n<!-- {n} -->\n' + clean(p.read_text()))
    (OUT / f'{slug}-ledger.md').write_text(''.join(parts))
    print('ok', slug)
