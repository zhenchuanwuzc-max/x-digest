"""合并后一次性修正共享数据 /workspace/digests/monitors/xhs_library.json 里 benchmark_profiles[].profile_url：
creators.html#x（兼容页）→ 规范人物页。只改这一字段；先备份；已是新值则跳过（可重复运行）。
用法：python3 fix_profile_urls.py [--dry-run] [数据文件]"""
import json, os, shutil, sys, tempfile
MAP = {f'creators.html#{k}': f'{k}.html' for k in ('kazike', 'guizang', 'huashu', 'baoyu', 'qiaomu', 'fankai', 'lenny', 'shreyas', 'ali', 'swyx', 'levelsio')}
MAP['creators.html#justin'] = 'justinwelsh.html'
MAP['creators.html#zara'] = 'zhangzala.html'
def apply(d):
    n = 0
    for c in d.get('benchmark_profiles') or []:
        u = c.get('profile_url')
        if u in MAP: c['profile_url'] = MAP[u]; n += 1
    return n
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--dry-run']
    path = args[0] if args else '/workspace/digests/monitors/xhs_library.json'
    d = json.load(open(path)); n = apply(d)
    left = [c.get('profile_url') for c in d.get('benchmark_profiles') or [] if 'creators.html' in (c.get('profile_url') or '')]
    print('changed', n, 'left', left)
    if left: sys.exit('unexpected creators.html links remain')
    if '--dry-run' in sys.argv or n == 0: sys.exit(0)
    shutil.copy2(path, path + '.bak-before-profile-urls')
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path)); os.close(fd)
    with open(tmp, 'w') as f: f.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, path)
