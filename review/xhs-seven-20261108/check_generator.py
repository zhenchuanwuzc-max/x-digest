"""对比已部署共享生成器与本批镜像在同一数据上的 xhs/index.html：去掉七步入口块、去掉 target/rel 后必须完全相同；
七步与人物成长链接全部新标签；分支 xhs/index.html == 新渲染。用法：python3 check_generator.py /workspace/digests/xhs_library.py [--write]"""
import importlib.util, os, re, shutil, sys, tempfile
from pathlib import Path
W = Path(__file__).resolve().parents[2]
def load(path, name):
    tmp = Path(tempfile.mkdtemp())
    for f in Path('/workspace/digests').glob('*.py'):
        if f.name != 'xhs_library.py': os.symlink(f, tmp / f.name)
    shutil.copy(path, tmp / f'{name}.py'); sys.path.insert(0, str(tmp))
    sp = importlib.util.spec_from_file_location(name, tmp / f'{name}.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    m.SITE = W / 'xhs'; return m
a = load(sys.argv[1], 'orig'); b = load(Path(__file__).with_name('xhs_library.py'), 'new')
d = a.load(); ra, rb = a.render(d), b.render(d)
strip = lambda h: re.sub(r'\s(target|rel)="[^"]*"', '', h)
block = re.search(r'<li><a href="seven/"[^>]*>.*?</ol></li>', rb, re.S)
assert block and block.group(0).count('<li>') == 1 + 7, 'seven block missing or not 7 steps'
ns = re.search(r'<h2 id="newsmall">.*?</div>', rb, re.S)
assert ns and '小号' in ns.group(0), 'daily new-small block missing'
rest = rb.replace(block.group(0), '').replace(ns.group(0), '')
rest = re.sub(r'<a [^>]*href="#newsmall"[^>]*>[^<]*</a>', '', rest)
assert strip(ra) == strip(rest), 'render differs beyond seven + newsmall blocks and target/rel'
for t in re.findall(r'<a\b[^>]*href="https://www.xiaohongshu.com[^"]*"[^>]*>', ns.group(0)): assert 'target="_blank"' in t and 'xsec' not in t, t
for t in re.findall(r'<a\b[^>]*href="(?:seven|growth)/[^"]*"[^>]*>', rb): assert 'target="_blank" rel="noopener noreferrer"' in t, t
import tempfile as _t
for bad in ('{', '{"steps":null}', '{"steps":[{}]}', '{"steps":[]}', '{"rules":[],"tiers":{},"candidates":[]}', '{"rules":[],"tiers":{},"candidates":[],"scope":"x"}'):
    t0 = Path(_t.mkdtemp()); (t0/'topics/src').mkdir(parents=True); (t0/'topics/src/new-small.json').write_text(bad); keep = b.SITE; b.SITE = t0; assert b._daily_new_small() == '', bad; b.SITE = keep
    t = Path(_t.mkdtemp()); (t/'seven/src').mkdir(parents=True); (t/'seven/src/seven.json').write_text(bad)
    keep = b.SITE; b.SITE = t; assert b._seven_entry() == '', bad; b.SITE = keep
if '--write' in sys.argv: (W / 'xhs/index.html').write_text(rb)
assert (W / 'xhs/index.html').read_text() == rb, 'branch xhs/index.html != new render'
print('OK only seven block added; seven/growth links new tab; branch index synced')
