"""对比已部署共享生成器与本批副本在同一数据上的 xhs/index.html：去掉 target/rel 后必须完全相同；
指向模块的链接全部新标签，模块外链接不被改动；分支 xhs/index.html == 新渲染。用法：python3 check_generator.py /workspace/digests/xhs_library.py [--write]"""
import importlib.util, os, re, shutil, sys, tempfile
from pathlib import Path
W = Path(__file__).resolve().parents[2]
def load(path, name):
    tmp = Path(tempfile.mkdtemp())
    for f in Path('/workspace/digests').glob('*.py'):
        if f.name != 'xhs_library.py': os.symlink(f, tmp / f.name)
    shutil.copy(path, tmp / f'{name}.py')
    sys.path.insert(0, str(tmp))
    sp = importlib.util.spec_from_file_location(name, tmp / f'{name}.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    m.SITE = W / 'xhs'; return m
a = load(sys.argv[1], 'orig'); b = load(Path(__file__).with_name('xhs_library.py'), 'new')
d = a.load(); ra, rb = a.render(d), b.render(d)
strip = lambda h: re.sub(r'\s(target|rel)="[^"]*"', '', h)
assert strip(ra) == strip(rb), 'render differs beyond target/rel'
mod = re.findall(r'<a\b[^>]*\shref="((?:growth/|[a-z-]+\.html)[^"]*)"[^>]*>', rb)
tags = re.findall(r'<a\b[^>]*>', rb); n = 0
files = set(re.findall(r'"href": "\.\./([a-z-]+\.html)"', (W/'xhs/growth/src/people.json').read_text())) | {'creators.html', 'topic-types.html', 'topic-lip-growth.html'}
for t in tags:
    h = re.search(r'\shref="([^"]*)"', t)
    if not h: continue
    f = h.group(1).split('#')[0]
    inmod = f.startswith('growth/') or f in files
    if inmod:
        n += 1; assert 'target="_blank" rel="noopener noreferrer"' in t, t
    else:
        assert t in ra, ('non-module link changed', t)
if '--write' in sys.argv: (W/'xhs/index.html').write_text(rb)
assert rb == (W/'xhs/index.html').read_text(), 'branch xhs/index.html != new render'
print(f'OK render identical except target/rel; {n} module links open in new tab; non-module links untouched; branch index synced')
