"""校验：每个榜单按档打印命中行；列出该榜有同厂商模型但零命中的家族；列出“疑似漏标”（归一化名以家族名开头但未命中）。"""
import json,sys,importlib.util,collections
sys.path.insert(0,'/workspace/digests')
import lb_section as M, tiers as T
def boards(mod):
    day,cur,_,_=mod.load();out={}
    for k,src in [('aa',cur['aa']),('aac',mod.load_aac()),('gdp',mod.load_gdp()),('text',cur['text']),('webdev',cur['webdev'])]:
        if not src or not src.get('rows'): continue
        rows=[x for x in src['rows'] if x['rank']<=100 or mod.god(x['model'])]
        out[k]=mod.aa_legacy(rows) if k=='aa' else rows
    return out
def counts(mod):
    return {k:collections.Counter(g['tier'] for x in r if (g:=mod.god(x['model']))) for k,r in boards(mod).items()}
if __name__=='__main__':
    if len(sys.argv)>1:
        sp=importlib.util.spec_from_file_location('old',sys.argv[1]);old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
        print('BEFORE',{k:dict(v) for k,v in counts(old).items()})
    print('AFTER ',{k:dict(v) for k,v in counts(M).items()})
    for k,rows in boards(M).items():
        print(f'\n=== {k} ({len(rows)} 行)')
        for t in ('now','half','y2'):
            hit=[x['model'] for x in rows if (g:=M.god(x['model'])) and g['tier']==t]
            print(f' [{M.TIER[t]}] {len(hit)}:',' | '.join(hit))
        orgs={(x.get('org') or '').lower() for x in rows}; names=' '.join(T.fam(x['model']) for x in rows)
        for f,v in T.FAM.items():
            n=sum(1 for x in rows if T.tier_of(x['model']) is v)
            if n==0 and f.split()[0] in names:
                tok=f.split()[1:]; import re; near=[x['model'] for x in rows if re.search(r'\b'+re.escape(f)+r'\b',T.fam(x['model']))]
                print(f'  MISS {v["tier"]} {f}: '+(f'疑似漏配 {near}' if near else '本榜无该家族任何配置（同厂商有其他模型）'))
        sus=[x['model'] for x in rows if not M.god(x['model']) and any(T.fam(x['model']).startswith(f+' ') for f in T.FAM)]
        if sus: print('  未标但以家族名开头（应为小号/独立家族，人工确认）:',sus)
