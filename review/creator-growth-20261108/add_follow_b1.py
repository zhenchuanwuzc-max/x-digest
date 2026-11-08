"""t232/t237：把小红书关注首批 3 人加入 xhs/growth/src/people.json（可重复运行，先删后加）。
证据在仓库外 following-batch1/；图卡覆盖度见 follow_b1_cards.py。公开数据只用研究对象的公开主页与笔记，不写 Ocean 的关注关系。"""
import json
from pathlib import Path
from follow_b1_cards import COV, text
PJ = Path(__file__).resolve().parents[2] / 'xhs/growth/src/people.json'
U = "https://www.xiaohongshu.com/explore/"; PR = "https://www.xiaohongshu.com/user/profile/"; NF = '未找到公开数值'
UNK = '未核'
def metrics(uid, fans, extra):
    return dict(x=dict(text=NF, kind='未找到', note=UNK+'；不按昵称找同名账号'), xhs=dict(text=fans, kind='事实', src=PR+uid, date='2026-11-08 主页截图', note=extra),
                wx=dict(text=NF, kind='未找到', note=UNK), income=dict(text=NF, kind='未找到', note=UNK+'；课程/服务宣传不等于收入'))
def w(id, title, step, edge, nid, slug):
    return dict(id=id, title=title, step=step, edge=edge + '；' + text(COV[slug][id]), src=U + nid)
NEW = [
 dict(id='lulu-ai', name='Lulu的AI野路子', ico='L', href='../lulu-ai.html', handle='小红书号 8748271280', tags=['小红书'],
  desc='小红书 AI 入门视频号；3 篇样本只看标题与描述。', go='打开成长页',
  does='以学习者身份做 AI 入门视频：GitHub、Skill 清单、RAG 学习记录（3 篇样本）',
  users='想入门 AI 编程 / Vibe Coding 的非技术人（推断）',
  metrics=metrics('65340940000000000301e006', '1.1 万', '同屏 9.7 万获赞与收藏（赞藏合计）、213 关注'),
  brief=dict(who='想入门 AI 编程、Vibe Coding 的非技术人（推断）', pain='GitHub、Skill、RAG 这些词听过，不知道从哪下手',
   solve='以“我也在学”的身份做真人出镜视频，把一个工具或概念压成零基础入口（只看标题与描述）',
   ocean='建议：学她“先给一个核心动作”的入门写法和清单写出处；Ocean 写自己真做过的一步，不写没做过的效果',
   works=[w('w1', '置顶：零基础学 GitHub', '核心动作：有想法先上 GitHub 搜类似项目，存下来二创；另建议刷 Explore 追新工具', '视频未播放；评论问 GitHub 打不开，作者回复未给办法', '6a490dc200000000070247cc', 'lulu-ai'),
          w('w2', '工具清单：自媒体全链路 5 个 Skill', '按选题到发布的流程排 5 个 Skill，其中一项写明“卡兹克开源”', '“70% 交给 AI”是自述未核', '6aa29e290000000026032c73', 'lulu-ai'),
          w('w3', '学习记录：RAG', '把“找不到适合小白的资料 → 用 Claude Code 追问梳理”写成内容', '学习过程是自述；没给参考资料来源', '6a4666a00000000006033756', 'lulu-ai')],
   gap='只看 3 篇视频的标题与描述（按 Ocean 要求不看视频）；其余笔记未读；日期无年份。')),
 dict(id='laoa-jinjie', name='老A的AI进阶实操', ico='A', href='../laoa-jinjie.html', handle='小红书号 27765125436', tags=['小红书'],
  desc='小红书 AI 产品经理课程 + 工具图卡号；与「老A的AI研究所」是两个账号，分开研究。', go='打开成长页',
  does='做 Skill 场景清单、Agent 设计模式图解等图卡，置顶 AI 产品经理转型课程（3 篇样本）',
  users='想转 AI 产品经理的人；在找好用 Skill 的 AI 工具用户（推断）',
  metrics=metrics('638efeda0000000024017551', '3.3 万', '同屏 19.6 万获赞与收藏（赞藏合计）、3.7 万关注'),
  brief=dict(who='想转 AI 产品经理、或在找好用 Skill 的人（推断）', pain='不知道该装哪些 Skill、Agent 设计讲不清、转行没体系',
   solve='干货图卡按场景分表、给入门最小集和流程；置顶放自家课程大纲，评论区问价转私信',
   ocean='建议：借他的清单结构（按场景分表 → 先装 3 个 → 4 步流程），补上他缺的“适合谁”和可点来源；课程导流部分只观察（Ocean 账号方向仍在摸索，是否相关待定）',
   works=[w('w1', '置顶：0 基础 3 个月转型 AI 产品经理（课程）', '10 页课程宣传：人群分类、服务细节、7 个模块大纲（12/20/20/12/12/24 课时 + 求职陪跑）', '课程宣传是自述：价格、交付、学员结果、收入都未核', '68400c5a0000000023017490', 'laoa-jinjie'),
          w('w2', '2026 用上这些 Skills', '6 张场景表（Agent 基础能力、设计、编程、营销、办公、写作）+ 先装 3 个基础 Skill + 4 步工作流', '卡内“热度”数未核；只有名称没有链接', '6aec15e3000000000602e32a', 'laoa-jinjie'),
          w('w3', '图解 12 种 Agent Harness 设计模式', '首页一张架构图，其后是署名 Bella 的飞书文档截图，逐个讲 12 个模式', '主体是他人署名文档；出处与授权未说明，原创性不判定', '6aaf9aa20000000027008c0b', 'laoa-jinjie')],
   gap='3 篇样本，图卡 29 页全读；评论展开、其余笔记未读。')),
 dict(id='karl-aigc', name='Karl的AIGC产品丨光之年', ico='K', href='../karl-aigc.html', handle='小红书号 27247756200', tags=['小红书'],
  desc='小红书 AI 产品经理求职内容 + 陪跑训练营号；3 篇样本。', go='打开成长页',
  does='围绕 AI 产品经理求职做 MBTI 岗位卡、Agent 项目/教程截图合集，置顶 1v1 陪跑训练营（3 篇样本）',
  users='想转行或求职 AI 产品经理的人（推断）',
  metrics=metrics('6593d82500000000220006c0', '4.2 万', '同屏 31.9 万获赞与收藏（赞藏合计）、4.6 万关注；主页有蓝色认证标，类型未核'),
  brief=dict(who='想转行或求职 AI 产品经理的人（推断）', pain='缺能写进简历的项目、不知道自己适合哪类产品岗',
   solve='同一模板做系列卡（MBTI 四栏），把项目表和教程站截图打包成资源帖，置顶陪跑训练营',
   ocean='建议：借 MBTI 帖“同一模板做系列 + 自带免责”的写法；资源帖要标题与内容一致、写清出处；求职与课程导流只作观察，是否与 Ocean 方向相关待定',
   works=[w('w1', '置顶：AI 产品经理 1v1 陪跑训练营', '9 页：宣传封面 → offer 拼图 → 六大项目 → 六项服务（诊断到 offer 谈薪）→ 私信“产品” → 7 模块 108 课时总览 → 模块 4/5/6 详情', '“1000+真实offer”等是宣传自述，交付与收入未核', '6ae17516000000003401d377', 'karl-aigc'),
          w('w2', 'MBTI × 产品经理', '封面后 8 页同一模板，每页一组（多为两型，第 9 页只列 ESFJ），分适配方向 / 优势 / 工作习惯 / 避雷点，自带“只作参考”免责', '性格与岗位匹配不是测评结论', '6aed9cee000000002a00d651', 'karl-aigc'),
          w('w3', '10 个练完可以放进简历的 Agent 项目', '首页项目表（项目 / 处理方式 / 技术路线 / 数据集），之后是「从0开始学AI Agent」教程站截图', '标题与主体不一致：主体是未署名的教程站截图；可运行性与授权未核', '6ad34999000000001a033c90', 'karl-aigc')],
   gap='3 篇样本，图卡 32 页全读；评论展开、其余笔记未读。')),
]
d = json.loads(PJ.read_text())
ids = {p['id'] for p in NEW}
d['people'] = [p for p in d['people'] if p['id'] not in ids] + NEW
# 首页总判断：只把写法可借鉴的作品放进已有方向；求职/课程导流只观察（Ocean 账号方向仍在摸索，不替他定）
BENCH = {'公开学 AI 的过程，作品比感想多': dict(pid='lulu-ai', works=['w3', 'w1'], learn='把“卡在哪、怎么问 AI 解开”写成学习记录；入门帖先给一个核心动作', skip='没拆解的“70% 交给 AI”；不给参考资料来源'),
         '把 AI 用进真实工作，一帖一个操作': dict(pid='laoa-jinjie', works=['w2', 'w3'], learn='工具清单按场景分表，先给最小起步集，再给一条流程；讲概念先给一张总图', skip='未核的热度数；评论区问价转私信')}
for r in d['practice']:
    r['bench'] = [b for b in r['bench'] if b['pid'] not in ids]
    if r['topic'] in BENCH: r['bench'].append(BENCH[r['topic']])
assert all(t in {r['topic'] for r in d['practice']} for t in BENCH)
PJ.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('ok', len(d['people']))
