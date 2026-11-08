"""对比原/改共享生成器在同一数据上的 xhs/index.html 渲染：只允许成长入口一行不同；并核对分支 xhs/index.html 已同步该行。"""
import difflib, importlib.util, sys
sys.path.insert(0, "/workspace/digests")
from pathlib import Path
W = Path(__file__).resolve().parents[2]
def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    m.SITE = W / 'xhs'; return m
a = load(sys.argv[1], 'orig'); b = load(W / 'review/xhs-growth-20261108/xhs_library.py', 'new')
d = a.load()
ra, rb = a.render(d), b.render(d)
diff = [l for l in difflib.unified_diff(ra.split('<li>'), rb.split('<li>'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
print('\n'.join(diff))
assert len(diff) == 2 and '成长记录专属入口' in diff[0] and '人物成长分析 · 14 人' in diff[1], diff
new_li = diff[1][1:]
assert new_li in (W / 'xhs/index.html').read_text(), 'branch xhs/index.html not synced'
print('OK only growth line differs; branch index synced')
