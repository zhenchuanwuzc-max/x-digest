"""对比原/改共享生成器在同一数据上的 xhs/index.html 渲染：只允许成长入口一行不同；并核对分支 xhs/index.html 已同步该行。"""
import difflib, importlib.util, sys
sys.path.insert(0, "/workspace/digests")
from pathlib import Path
W = Path(__file__).resolve().parents[2]
import os, shutil, tempfile
def load(path, name):
    """放进临时目录并链接 /workspace/digests 的同级模块，两边加载条件一致。"""
    tmp = Path(tempfile.mkdtemp())
    for f in Path('/workspace/digests').glob('*.py'):
        if f.name != 'xhs_library.py': os.symlink(f, tmp / f.name)
    shutil.copy(path, tmp / f'{name}.py')
    sp = importlib.util.spec_from_file_location(name, tmp / f'{name}.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    m.SITE = W / 'xhs'; return m
a = load(sys.argv[1], 'orig'); b = load(W / 'review/xhs-growth-ia-20261108/xhs_library.py', 'new')
d = a.load()
import copy; sys.path.insert(0, str(W / 'review/xhs-growth-ia-20261108')); import fix_profile_urls
d_new = copy.deepcopy(d); fix_profile_urls.apply(d_new)
ra, rb = a.render(d), b.render(d_new)
REPL = [('<a href="creators.html"><b>对标博主完整档案</b></a>（与本地研究页同步，已去本地路径）。</p>', '<a href="growth/"><b>人物成长研究</b></a>（每人一页，与本地研究页同步）。</p>'),
        ('<a class="btn" href="creators.html">打开完整档案 →</a>', '<a class="btn" href="growth/">打开人物成长研究 →</a>'),
        ('<span>13 位深描 + 分类对照，内容比本页摘要完整得多。</span>', '<span>14 人各一页，另有分类对照等专题。</span>'),
        ('<a href="creators.html#lip-growth">对标档案 · 怎么涨 &amp; 变现</a>', '<a href="topic-lip-growth.html">专题 · learn-in-public 怎么涨 &amp; 变现</a>')]
REPL += [(f'href="{o}"', f'href="{n}"') for o, n in fix_profile_urls.MAP.items()]
exp = ra
for o, n in REPL: exp = exp.replace(o, n)
assert exp == rb, [l for l in difflib.unified_diff(exp.split('<'), rb.split('<'), lineterm='', n=0)][:20]
idx = (W / 'xhs/index.html').read_text()
for o, n in REPL:
    if o in ra: assert n in idx and o not in idx, n
assert rb == idx, 'branch xhs/index.html != new render'
print('OK new render == old render + exact whitelist replacements (links and entry labels); branch xhs/index.html synced', 'branch index == new render:', rb == idx)
