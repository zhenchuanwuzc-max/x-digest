"""把仓库外私有工作包 latest-topic-library/seven-step-pack.json 转成仓库内唯一公开源 xhs/seven/src/seven.json。
- 私有相对路径换成公开人物页；去掉链接参数与采集账号；不公开关注名单。
- 每步的“产物 / 状态 / 缺口”由 STEPS 表 + 实际数据计算，不手写“已完成”。可重复运行。"""
import json, re
from pathlib import Path
PACK = Path('/workspace/creator-growth-20261108/latest-topic-library/seven-step-pack.json')
OUT = Path(__file__).resolve().parents[2] / 'xhs/seven/src/seven.json'
P = json.loads(PACK.read_text())
HIST = [dict(name='知新的AI笔记', href='../zhixin.html', note='主页置顶 + 近期 4 篇'),
        dict(name='Lulu的AI野路子', href='../lulu-ai.html', note='主页置顶 + 近期 3 篇（视频只看标题描述）'),
        dict(name='老A的AI进阶实操', href='../laoa-jinjie.html', note='主页置顶 + 近期 3 篇'),
        dict(name='Karl的AIGC产品丨光之年', href='../karl-aigc.html', note='主页置顶 + 近期 3 篇')]
PRIV = {'../following-batch1 老A Skills 图卡已读全': '老A的AI进阶实操 Skills 帖，图卡 10/10 已读（见人物页）'}
def clean_url(u): return re.sub(r'\?.*$', '', u)
s2 = P['step2']; latest = []
for x in s2['latest_pool']:
    y = dict(x); y['url'] = clean_url(y['url']); latest.append(y)
cmp_n = sum(x['comparable_same_period'] for x in latest)
s4 = [dict(r, source_note=PRIV.get(r['source_note'], r['source_note']), latest_refs=[dict(title=x['title'], skeleton=x['skeleton']) for i in r.get('latest_refs', []) for x in s2['latest_pool'] if x['source_id'] == i]) for r in P['step4']]
can = sum(r['source_status'].startswith('可写') for r in s4)
T6 = {t: len(t) for t in [r['suggested_title'] for r in P['step4']] + [P['step5']['title']]}
S6 = dict(P['step6'], titles=T6, title_over_20=[k for k, v in T6.items() if v > 20])
STEPS = [
 dict(id='s1', n=1, name='变现候选', out=f"{len(P['step1']['content_directions'])} 个内容方向候选 + {len(P['step1']['monetization_hypotheses'])} 个变现假设（各写验证条件）",
      state='均未选定', gap='要发几篇后看收藏与评论提问再收敛；不采购、不启动服务'),
 dict(id='s2', n=2, name='找同期对标', out=f"历史池 {len(HIST)} 个人物页；最新池 {len(latest)} 条（同期倾向 {cmp_n} 条，均为相对日期），{s2['counts']['followers_verified_lt_10k']} 位作者粉丝 <1万 已核",
      state='最新样本少，爆款未证实', gap=s2['pending']),
 dict(id='s3', n=3, name='探索版账号档案', out=f"已知 {len(P['step3']['facts'])} 条 · 边界 {len(P['step3']['boundaries'])} 条 · 假设 {len(P['step3']['hypotheses'])} 条",
      state='探索中', gap='留空：' + '、'.join(P['step3']['left_blank'])),
 dict(id='s4', n=4, name='七类选题库', out=f"7 类识别标准 + 7 个建议题（{can} 个可写，其余待找源）",
      state='建议候选，不是真实爆款', gap=f"{'/'.join(r['cat'] for r in s4 if r['latest_refs'])} 已挂最新样本骨架，其余 {sum(not r['latest_refs'] for r in s4)} 类待采；分类可交叉"),
 dict(id='s5', n=5, name='挑题候选稿', out=f"1 篇候选稿《{P['step5']['title']}》", state='草稿，未发布', gap='等 Ocean 审核'),
 dict(id='s6', n=6, name='人工检查', out=f"程序自查：{len(S6['titles'])} 个标题，超 20 字 {len(S6['title_over_20'])} 个，稿内禁词命中 {len(S6['draft_banned_hits'])} 处",
      state='程序检查过；人工检查未做', gap='Ocean 读稿、去 AI 味、核对来源'),
 dict(id='s7', n=7, name='排期复盘', out=f"{len(P['step7']['workflow'])} 个状态的流转 + 复盘字段表", state='排期只是草案；0 篇已发布',
      gap='无复盘数据；不改 routine、不自动发帖')]
OUT.write_text(json.dumps(dict(
 source=P['source'], analysis_note='作者说法与我们的建议分开写；“养号 3–5 天、iOS 流量更稳、AI 味会被限流、出来至少 70 分、超过 90% 新手”等是作者说法，未核实，不照搬。',
 steps=STEPS, step1=P['step1'], step2=dict(article=s2['article'], historical=HIST, latest=latest, latest_scan=s2['latest_scan'], pending=s2['pending'], counts=s2['counts']),
 step3=P['step3'], step4=s4, step4_note=P['step4_note'], step5=P['step5'], step6=S6, step7=P['step7'],
 asof='2026-11-08'), ensure_ascii=False, indent=1))
print('ok', len(latest), cmp_n, can)
