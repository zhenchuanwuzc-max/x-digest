"""t230：把「知新的AI笔记」加入 xhs/growth/src/people.json（可重复运行，先删后加）。证据见 zhixin-ledger.md / zhixin-corrections.md。"""
import json
from pathlib import Path
PJ = Path(__file__).resolve().parents[2] / 'xhs/growth/src/people.json'
d = json.loads(PJ.read_text())
U = "https://www.xiaohongshu.com/explore/"; NF = '未找到公开数值'
P = "https://www.xiaohongshu.com/user/profile/686011fb000000001b023a74"
d['people'] = [p for p in d['people'] if p['id'] != 'zhixin']
d['people'].append(dict(id='zhixin', name='知新的AI笔记', ico='知', href='../zhixin.html', handle='小红书号 49626736847', tags=['小红书'],
 desc='小红书 AI 观点与资讯整理号；4 篇样本。', go='打开成长页',
 does='小红书整理 AI 访谈、外文文章和开源榜单，配少量个人评语（4 篇样本）',
 users='想了解 AI 会怎么影响工作、关注大厂动态的中文读者（推断）',
 metrics=dict(x=dict(text=NF, kind='未找到', note='未找；按要求不另找同名账号拼接身份'),
  xhs=dict(text='1.7 万', kind='事实', src=P, date='2026-11-08 主页截图', note='同屏另有 31.7 万获赞与收藏（赞藏合计）、61 关注；搜索卡显示 332 篇'),
  wx=dict(text=NF, kind='未找到'), income=dict(text=NF, kind='未找到')),
 brief=dict(who='想了解 AI 会怎么影响工作、没时间读长访谈和外文文章的中文读者（推断）',
  pain='访谈、外文长文、开源项目太多太长，不知道哪些值得看',
  solve='把别人的访谈、文章、GitHub 榜单整理成中文图文，配少量个人评语（4 篇样本里未见他自己的工具实操）',
  ocean='建议：Ocean 说观点类更容易起手（原话：『这些观点AI，我更容易做；hah』）。可从一篇原文提炼一个有依据的观点，写清作者和出处，再补产品经理判断：影响工作的哪一步、什么值得试；没实测不写实测，别人的经历不改成第一人称',
  works=[
   dict(id='w1', title='置顶观点帖：普通人怎么应对 AI（2025-09）', step='把一个外部观点拆成几节文字卡，配身边例子，最后一句提问收尾', edge='观点来源未署名；身边例子无法核实；图卡无案例、数据或实操', src=U+'68ccee2c000000001400bb08'),
   dict(id='w2', title='访谈解读：马斯克谈 AI 终局', step='用强情绪开头，再按“几条底线”分条复述访谈', edge='出处未写，平台 AI 给的出处未核；复述和评语没分开；其余 7 张图卡未读', src=U+'6addb1a6000000002403a5fa'),
   dict(id='w3', title='外文文章解读：AI 工作流该留哪些', step='署名原作者，用一二三小标题转述长文，提炼一个读者能自问的判断题，结尾一句自己的感想', edge='经历属于原作者 Katie Parrott；没给原文链接；8 张图卡与配文基本重复', src=U+'6aeb013d0000000003017268'),
   dict(id='w4', title='开源榜单：GitHub Agent Skills Top 10', step='总览一张，之后每项一张同模板卡：核心亮点、功能、场景、输入建议、使用提醒、我的结论', edge='卡上署仓库名但没有可点链接；Star 未核、不背书；未见实际安装试用', src=U+'6aec79e4000000000e02df09')],
  gap='4 篇样本以外的 328 篇未读；马斯克帖其余 7 张图卡未读。')))
PJ.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('ok', len(d['people']))

# 首页总判断：第 4 个方向「观点与外文解读」（t231：Ocean 原话说这类更容易做）
d = json.loads(PJ.read_text())
d['practice'] = [r for r in d['practice'] if r.get('topic') != '观点与外文解读：一篇原文一个判断']
d['practice'].append(dict(topic='观点与外文解读：一篇原文一个判断', bench=[
  dict(pid='zhixin', works=['w3', 'w1'], learn='把一篇长文压成一个读者能自问的判断题；观点帖分几节小标题、一节一句',
       skip='不写出处的复述；第一人称情绪标题配别人的经历；未核的排行数字'),
  dict(pid='baoyu', works=['w4', 'w1'], learn='转述新闻先写结论，正文第一句交代谁、哪天、在哪发；翻译给出处和多个入口',
       skip='他的英文资料量和工程背景')],
 who='想知道 AI 新观点、新文章跟自己工作有什么关系的职场人（推断）', level='读者现在：未知；内容指向：观点与趋势，层级多数不适用',
 pain='外文长文和访谈太长，读了也不知道跟自己的工作有什么关系',
 ocean='建议：Ocean 说这类“我更容易做”（原话『这些观点AI，我更容易做；hah』）。从一篇原文提炼一个有依据的观点，写清作者、出处、日期，再补一段产品经理判断：影响哪一步工作、什么值得试；没实测不写实测',
 check='看评论里有没有人追问原文或说“我们也遇到了”；不比较粉丝数'))
PJ.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('practice', len(d['practice']))
