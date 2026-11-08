import json,re,glob,sys,os
D='/workspace/lenny/newsletter-MD/'
items=json.load(open('items.json')); used=set(items['used'])
cards={}; errs=[]
for f in sorted(glob.glob('shards/s*.json')):
    for c in json.load(open(f)): cards[c['file']]=c
BAN=['很有价值','干货','值得一读','值得一看','必读','Ocean','我当时','我们团队']
zh=lambda s:bool(re.search(r'[\u4e00-\u9fff]',s or ''))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
for fn,c in cards.items():
    t=norm(open(D+fn,errors='ignore').read()) if os.path.exists(D+fn) else ''
    for k,mx in [('title_zh',30),('audience',36),('reason',80),('angle',60)]:
        v=c.get(k,'')
        if not v or not zh(v): errs.append(f'{fn}: {k} 缺/非中文')
        elif len(v)>mx: errs.append(f'{fn}: {k} 超长 {len(v)}')
        if any(b in v for b in BAN): errs.append(f'{fn}: {k} 含禁用词')
    if fn in used and not c.get('followup'): errs.append(f'{fn}: 已用缺 followup')
    if fn not in used and c.get('followup'): errs.append(f'{fn}: 非已用却有 followup')
    ev=c.get('evidence') or []
    if len(ev)<2: errs.append(f'{fn}: evidence<2')
    for e in ev:
        if norm(e.get('quote','')) not in t: errs.append(f'{fn}: 引文找不到「{e.get("quote","")[:30]}」')
for k in ('reason','angle'):
    vals=[c.get(k) for c in cards.values()]
    d=[v for v in set(vals) if vals.count(v)>1]
    if d: errs.append(f'重复 {k}: {d}')
want=[f for f in items['all'] if f not in items['missing']]
miss=[f for f in want if f not in cards]
print('cards',len(cards),'expected',len(want),'missing',miss)
print('\n'.join(errs) or 'NO ERRORS')
if '--write' in sys.argv and not errs and not miss:
    keep=['file','title_zh','audience','reason','angle','followup','evidence']
    out={fn:{k:cards[fn].get(k,'') for k in keep[1:]} for fn in want}
    json.dump(out,open('/workspace/digests/monitors/lenny_cards_zh.json','w'),ensure_ascii=False,indent=1); print('written')
