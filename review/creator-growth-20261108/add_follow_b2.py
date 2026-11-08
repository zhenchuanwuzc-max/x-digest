"""关注第二批 3 人加入 xhs/growth/src/people.json（可重复运行，先删后加）。证据在仓库外 following-batch2/；覆盖度见 follow_b2_cards.py。
不写采集者的关注关系；首页方向只放写法可借鉴的作品。"""
import json
from pathlib import Path
from follow_b2_cards import COV, text
from add_follow_b1 import metrics, PJ, U  # noqa: 复用口径（导入会重跑首批，结果不变）
def w(id, title, step, edge, nid, slug):
    return dict(id=id, title=title, step=step, edge=edge + '；' + text(COV[slug][id]), src=U + nid)
NEW = [
 dict(id='laoa-yanjiusuo', name='老A的AI研究所', ico='研', href='../laoa-yanjiusuo.html', handle='小红书号 95852065618', tags=['小红书'],
  desc='小红书 AI 产品经理课程 + 项目合集 / Skill 清单号；与「老A的AI进阶实操」是两个账号，分开研究。', go='打开成长页',
  does='做 Vibe Coding 项目合集、产品经理 Skill 清单等图卡，置顶 AI 产品经理求职特训班（3 篇样本）',
  users='想转 AI 产品经理的人；想用 AI 做小应用、找产品类 Skill 的人（推断）',
  metrics=metrics('6355eca2000000001901e148', '3.5 万', '同屏 20.8 万获赞与收藏（赞藏合计）、3.8 万关注'),
  brief=dict(who='想转 AI 产品经理、想用 AI 做出第一个小应用的人（推断）', pain='转行缺体系；不知道从哪类项目、哪些 Skill 开始',
   solve='先给一张总表让读者挑，再一页一项写清功能、技术栈或场景；置顶放自家课程，评论区问价转私信',
   ocean='建议：借“总表 → 一页一项”的合集结构，补上他缺的署名和可点来源；只放自己真做过的项目；课程导流只观察',
   works=[w('w1', '置顶：AI 产品经理求职特训班（课程）', '11 页课程宣传：亮点与人群 → 服务 → offer 拼图 → 1V1 记录 → 7 个模块大纲', '课程宣传是自述：价格、交付、学员结果、收入未核；与老A进阶实操置顶课程相似，只记相似', '68382470000000002301d83f', 'laoa-yanjiusuo'),
          w('w2', '近一个月 Vibe Coding 作品集', '第 1 页 12 个案例总表（案例 / 场景 / 验证重点），之后一页一个项目写功能、技术栈、第一步', '各页无署名、无来源，是否本人实操未核', '6ae55d380000000015006632', 'laoa-yanjiusuo'),
          w('w3', '产品经理必装的十大 Skill', '一页一个 Skill，统一“一句话定位 + 三个应用场景”', '卡内无仓库链接，“github上哈”未核；功能未实测', '6aeae925000000000602f5c8', 'laoa-yanjiusuo')],
   gap='3 篇样本，图卡 37 页全读；其余笔记、1 条回复未读。')),
 dict(id='jason-effi', name='杰森的效率工坊', ico='J', href='../jason-effi.html', handle='小红书号 jason_effi_lab', tags=['小红书'],
  desc='小红书 AI Agent 工具 + Obsidian 教程号；2 篇图文全读、1 篇视频只看描述。', go='打开成长页',
  does='写 Codex / Claude Code 一类 Agent 工具的安装接入教程，视频讲 Hook 等概念（3 篇样本）',
  users='在用 Codex、Claude Code、Obsidian 的人（推断）',
  metrics=metrics('60935957000000000101fbf7', '2.1 万', '同屏 18.1 万获赞与收藏（赞藏合计）、12 关注'),
  brief=dict(who='在用 Codex、Claude Code、Obsidian 的人（推断）', pain='想给 Agent 加能力，又怕装坏、泄露密钥、规则不被执行',
   solve='教程先列“这篇整理了”，把安全要求写进安装提示词，再讲怎么接进已在用的工具，最后给可复用模板',
   ocean='建议：借“安全步骤写进提示词 + 可复用模板”的教程写法；工具数字和额度标读取日期；Ocean 只写自己真装过的',
   works=[w('w3', 'Agent Reach 安装详解', '平台权限表 → 环境表 → 带十条安全要求的安装提示词 → 关闭隐式调用 → 调研提示词模板', '两处仓库名不一致，未核；读者提醒有封号风险', '6a5c8234000000001101475f', 'jason-effi'),
          w('w2', 'Agent Hook 深度教程（视频）', '描述先问“规则总被 AI 忽略怎么办”，再列为什么更稳、何时用、怎么从 0 做', '视频未看；评论区平台 AI 总结不当原文', '6a8eba9d000000000502929d', 'jason-effi'),
          w('w1', '让你的 Agent 用上 Gemini 全家桶', '能做什么 → 安装 → 在 AGENTS.md / CLAUDE.md 写规则 → 4 个场景 → 免费额度表', '仓库、命令、额度未核且可能变化', '6adf0fc300000000170369e3', 'jason-effi')],
   gap='图文 2 篇 17 页全读；视频按范围只看标题描述；首屏其余 13 篇只看标题。')),
 dict(id='accio-work', name='Accio Work', ico='Ac', href='../accio-work.html', handle='小红书号 63078419557', tags=['小红书', '品牌号'],
  desc='小红书 AI 电商工具品牌号（简介自述“王牌兄弟@阿里国际站”）；3 种动作各 1 篇。', go='打开成长页',
  does='产品升级图文按商家类型讲功能、场景短视频、评论区征名活动（3 篇样本）',
  users='在 1688 / 国际站开店的商家与运营（推断）',
  metrics=metrics('693f73140000000032029ad5', '1.2 万', '同屏 4.5 万获赞与收藏（赞藏合计）、10 关注；昵称旁有认证蓝标，类型未核'),
  brief=dict(who='在 1688 / 国际站开店的商家与运营（推断）', pain='数据分散、上新慢、周报耗时',
   solve='升级帖按商家类型分页讲痛点；视频描述写一个具体麻烦再转到变化；征名活动给现成选项降低评论门槛',
   ocean='建议：借“按读者类型分页讲同一个工具”和“问一个答得出的问题 + 现成选项”的评论设计；不照搬宣传示例数字和积分奖励',
   works=[w('w1', 'Accio × 1688 生意助手升级', '每页一个痛点 + 产品截图，按定制型工厂 / 现货批发商 / 跨境供应商分场景，结尾评论区许愿', '示例数字是宣传，未核', '6aec1bfa000000001a03361f', 'accio-work'),
          w('w2', '多店运营周报（视频）', '描述：挨个登后台、写周报的麻烦 → “但是！绑定后”三条变化', '视频未看；省时说法未核', '6aead456000000000502f1fc', 'accio-work'),
          w('w3', '万亿身价，在线求名分（征中文名）', '6 个候选名 + 可原创 + 写明奖励（Credits 积分）和截止时间', '积分不是现金；未见发奖或采纳结果；58 条评论只读首屏', '6aec790e0000000016012404', 'accio-work')],
   gap='图文 2 篇 9 页全读；视频只看描述；征名评论未读完。')),
 dict(id='zhiwei', name='知危', ico='危', href='../zhiwei.html', handle='小红书号 4953699768', tags=['小红书'],
  desc='小红书商业/行业分析视频号；2 篇视频只看标题描述（标题描述层分析）。', go='打开成长页',
  does='做商业与行业话题视频，标题用“现象 + 数字 + 疑问”（2 篇样本，视频未看）',
  users='想了解新消费、想开店、关心行业变化的人（推断）',
  metrics=metrics('6006722f0000000001007574', '11.6 万', '同屏 25.6 万获赞与收藏（赞藏合计）、6 关注'),
  brief=dict(who='想了解新消费、想开店、关心行业变化的人（推断）', pain='看到一个生意火了，想知道赚不赚钱、能不能做',
   solve='标题把一个正在火的现象、一个数字和读者心里的疑问放在一起（只看标题与描述，视频未看）',
   ocean='建议：借“现象 + 可核数字 + 读者疑问”的标题写法，正文写清数字来源；不转述未核的毛利、门店数',
   works=[w('w1', '拼豆与“口红经济”（视频）', '标题：现象 + “毛利高达90%” + “口红经济”；评论在算成本、问该不该开店', '视频未看；毛利数字是标题主张，未核', '69ba14e40000000022003390', 'zhiwei'),
          w('w2', '网吧真赚钱吗（视频）', '标题：“方圆3公里开20家” + “真赚钱吗？”；封面“复兴了，但未必赚钱”', '视频未看；数量与盈利未核；评论为空', '6aed665b000000002c001c93', 'zhiwei')],
   gap='标题描述层：2 篇视频只看标题、描述与可见评论；首屏无图文。')),
]
d = json.loads(PJ.read_text())
ids = {p['id'] for p in NEW}
d['people'] = [p for p in d['people'] if p['id'] not in ids] + NEW
# 首页每个方向最多 3 位重点对标人（已满），第二批只进人物名单，不挤进方向
BENCH = {}
for r in d['practice']:
    r['bench'] = [b for b in r['bench'] if b['pid'] not in ids]
    if r['topic'] in BENCH: r['bench'].append(BENCH[r['topic']])
assert all(t in {r['topic'] for r in d['practice']} for t in BENCH)
PJ.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('ok', len(d['people']))
