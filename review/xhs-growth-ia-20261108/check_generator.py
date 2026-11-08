"""对比原/改共享生成器在同一数据上的 xhs/index.html 渲染：只允许成长入口一行不同；并核对分支 xhs/index.html 已同步该行。"""
import difflib, importlib.util, sys
sys.path.insert(0, "/workspace/digests")
from pathlib import Path
W = Path(__file__).resolve().parents[2]
def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    m.SITE = W / 'xhs'; return m
a = load(sys.argv[1], 'orig'); b = load(W / 'review/xhs-growth-ia-20261108/xhs_library.py', 'new')
d = a.load()
import copy; sys.path.insert(0, str(W / 'review/xhs-growth-ia-20261108')); import fix_profile_urls
d_new = copy.deepcopy(d); fix_profile_urls.apply(d_new)
ra, rb = a.render(d), b.render(d_new)
diff = [l for l in difflib.unified_diff(ra.split('<'), rb.split('<'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
print('\n'.join(diff))
allowed_old = {*(f'a href="{u}">' for u in fix_profile_urls.MAP), *(f'a class="btn sec" href="{u}">完整档案' for u in fix_profile_urls.MAP), 'a href="creators.html">', 'b>对标博主完整档案', '/b>', '/a>（与本地研究页同步，已去本地路径）。', 'a class="btn" href="creators.html">打开完整档案 →', 'a href="creators.html#lip-growth">对标档案 · 怎么涨 &amp; 变现', 'span>13 位深描 + 分类对照，内容比本页摘要完整得多。'}
assert all(any(l[1:].startswith(a) for a in allowed_old) for l in diff if l[0] == '-'), [l for l in diff if l[0] == '-' and not any(l[1:].startswith(a) for a in allowed_old)]
idx = (W / 'xhs/index.html').read_text()
for l in diff:
    if l[0] == '+': assert '<' + l[1:] in idx, l
print('OK only profiles/growth link lines differ; branch xhs/index.html synced')
