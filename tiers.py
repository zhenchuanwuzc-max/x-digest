"""统一的「神」分档（按模型家族）。唯一入口：fam(name) 归一化家族名；build() 生成 tiers.json；tier_of(name) 给所有榜单用。
家族规则：小写 → 去括号内容（effort/日期/fallback 等）→ 去厂商前缀 → 连字符/下划线变空格 → 去尾部修饰词
（preview/exp/experimental/full/thinking/reasoning/high/xhigh/max/medium/low/latest/codex/chat/pro(仅 GPT)/日期 4–8 位数字）→ 别名表。
因此 Codex 视为同版本 GPT 家族的变体（GPT-5.2-Codex ∈ GPT-5.2；GPT-5.3 Codex 家族名为 GPT-5.3）。
小号排除：mini/nano/lite/instant/fast/flash-lite/distill/haiku（除非家族名本身含该词）。"""
import re,json,datetime
D='/workspace/digests'
SUF=r'(preview|exp|experimental|full|thinking|reasoning|non reasoning|high|xhigh|max|medium|low|minimal|latest|codex|chat|adaptive|instruct|it|\d{4,8})'
SMALL=r'\b(mini|nano|lite|instant|fast|distill|air|oss)\b'
ALIAS={  # 榜单特有写法 → 家族
 'claude 3.5 sonnet':'claude 3.5 sonnet','claude 3 5 sonnet':'claude 3.5 sonnet','claude 3 7 sonnet':'claude 3.7 sonnet',
 'claude 4.5 opus':'claude opus 4.5','claude 4.5 sonnet':'claude sonnet 4.5','claude 4.1 opus':'claude opus 4.1','claude 4 opus':'claude opus 4',
 'claude opus 4 1':'claude opus 4.1','claude opus 4 5':'claude opus 4.5','claude opus 4 6':'claude opus 4.6','claude opus 4 7':'claude opus 4.7','claude opus 5 5':'claude opus 5.5','claude sonnet 4 5':'claude sonnet 4.5','claude sonnet 4 6':'claude sonnet 4.6',
 'chatgpt 4o':'gpt 4o','o1 2024 12 17':'o1','o1 preview':'o1 preview','gemini 3 pro':'gemini 3 pro','gemini 2.0 pro':'gemini 2.0 pro',
 'deepseek r1 0528':'deepseek r1 0528','deepseek v3 0324':'deepseek v3','llama 3.1 405b':'llama 3.1 405b','meta llama 3.1 405b':'llama 3.1 405b','grok 4.20':'grok 4.20','grok 4.2':'grok 4.20',
}
def fam(n):
    s=n.lower().strip()
    keep=re.search(r'r1[ -]0528',s)
    s=re.sub(r'\([^)]*\)','',s)
    s=re.sub(r'^.*?·\s*','',s)  # AA 编程榜「Harness · 模型」
    s=re.sub(r'^(opus|sonnet|fable|haiku)\b',r'claude \1',s.strip())
    s=re.sub(r'\b(multi[- ]agent|beta)( \d+)?\b',' ',s)
    s=re.sub(r'^(anthropic|openai|google|meta|xai|deepseek-ai|x-ai)[/:]','',s)
    s=re.sub(r'(\d)-(\d)',r'\1.\2',s) if re.search(r'(claude|gemini|grok|gpt|qwen|llama|deepseek v|opus|sonnet)[- ]?\d+-\d(?!\d)',s) else s
    s=re.sub(r'[-_/]',' ',s); s=re.sub(r'(qwen)(\d)',r'\1 \2',s); s=re.sub(r'\bgpt (\d)',r'gpt \1',s); s=re.sub(r'\bgpt(\d)',r'gpt \1',s)
    s=re.sub(r'\s+',' ',s).strip()
    s=re.sub(r'\b(20\d\d) ?(\d\d) ?(\d\d)\b','',s).strip()
    s=re.sub(r'(\d{4}) v\d+$',r'\1',s)
    for _ in range(4): s=re.sub(r'\s+'+SUF+r'$','',s).strip()
    if s.startswith('gpt'): s=re.sub(r'\s+pro$','',s)
    s=re.sub(r'\s+',' ',s).strip()
    if keep and 'r1' in s and '0528' not in s: s=s.replace('r1','r1 0528')
    s=ALIAS.get(s,s)
    return s
def small(n,f): return bool(re.search(SMALL,n.lower())) and not re.search(SMALL,f)
def build():
    L=json.load(open(f'{D}/legacy-gods.json'));A=json.load(open(f'{D}/aa-legacy.json'))['rows']
    T=datetime.date.today();ago=lambda d:(T-datetime.timedelta(days=d)).isoformat()
    out={}
    # 现在的神：每个 now_lab，近 now_days 天内发布（AA releaseDate=家族最早发布日）、在售的家族里，AA 最高分家族
    fr={}
    for r in A:
        if small(r['model'],''): continue
        k=fam(r['model']);x=fr.setdefault((r['org'],k),dict(org=r['org'],family=k,release=r['release'],score=-1,live=False,best=''))
        x['release']=min(x['release'],r['release']);x['live']|=not r.get('deprecated')
        if r['score']>x['score']: x['score']=r['score'];x['best']=r['model'];x['slug']=r['release_slug']
    for lab in L['now_labs']:
        c=[x for x in fr.values() if x['org']==lab and x['live'] and x['release']>=ago(L['now_days'])]
        if c: b=max(c,key=lambda x:x['score']); out[b['family']]=dict(b,tier='now',name=b['best'].split(' (')[0])
    for f in L['families']:
        k=fam(f['name'])
        if k in out: continue
        if f['release']>ago(L['cutoff_days']): continue  # 太新，不进半年前/前年
        t='y2' if f['release']<=ago(L['y2_min_days']) else 'half'
        if f['release']<ago(L['y2_max_days']): continue
        out[k]=dict(family=k,name=f['name'],release=f['release'],tier=t,slug=f['aa_slug'],org=f.get('org',''))
    json.dump(dict(generated=T.isoformat(),rule=__doc__,families=out),open(f'{D}/tiers.json','w'),ensure_ascii=False,indent=1)
    return out
try: FAM=build()
except Exception as ex: FAM={};print('tiers build 失败',ex)
def tier_of(n):
    k=fam(n);f=FAM.get(k)
    if f and not small(n,k): return f
