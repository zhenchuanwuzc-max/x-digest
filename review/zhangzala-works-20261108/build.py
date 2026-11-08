"""从 9c711ed 版 xhs/zhangzala.html 生成方案 B 页面（作品拆解独立成章）。可重复运行：输入固定取 git 9c711ed。"""
import re, subprocess
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
src = subprocess.run(["git","-C",str(REPO),"show","9c711ed:xhs/zhangzala.html"],capture_output=True,text=True,check=True).stdout
XHS = "https://www.xiaohongshu.com/explore/"
def a(url, text): return f'<a href="{url.replace("&","&amp;")}" target="_blank" rel="noopener">{text}</a>'
L = {
 "400": a(XHS+"68ccbc56000000000e022358?xsec_token=ABUcpaYJnXAnMYht_N_HshQcD3ZgE-cUBYTX9jI9X7_Xw=&xsec_source=pc_user", "《2年400篇笔记，12万粉丝：做小红书的一些感想》"),
 "feishu": a(XHS+"6a1018060000000007027155?xsec_token=AB-QSO3EIltr0KEwJqPLsYnuD1Ptzjx8K3plXk1eA5-dA=&xsec_source=pc_user", "《把Claude Code接入飞书，太爽了！教程+演示》"),
 "gh": a(XHS+"6a2761520000000008032277?xsec_token=ABV4nTHPpFrx7LlpI92U9NtGNxdKD1Xd8K5PORPmqpf5E=&xsec_source=pc_user", "《我在GitHub上有超过3万星（虽然并不会写代码》"),
 "x1w": a("https://x.com/zarazhangrui/status/2070982013822333007", "X 相关帖（正文本轮待核）"),
 "tw": a(XHS+"6a31edc300000000200387f4?xsec_token=ABQSKYmEqpZfsugCKX7VlrlMwEK09rjxlMv-UP-lMOuLs=&xsec_source=pc_user", "《如何一年在Twitter涨粉7万》"),
 "slides": a(XHS+"69fe6f3a000000001a036be4?xsec_token=ABdee01Gr5r1zV2-5uGrdsl0aT1_wOrZRP4SqcdTvPqII=&xsec_source=pc_user", "《如何用AI做出超级好看的HTML Slides》"),
 "ppt": a(XHS+"6a7993e60000000028032339?xsec_token=ABMBQGh8_o0VP83IM9sGRTdCdWnFi7rn7Xxo79r2jQjz8=&xsec_source=pc_user", "《在AI-native团队里，HTML正在取代PPT》"),
 "ahead": a("https://x.com/zarazhangrui/status/2091338374447763481", "X：Everyone who’s ahead…"),
}
# 一张卡 = 一条记录；层级固定：事实 / 自述 / 观察 / 假设 / 边界
WORKS = [
 dict(id="w1", t="两年回顾帖：数字标题 + 感想 + 读者反馈", links=[L["400"]], where=("s3","阶段 3 · 节点 5a–5c · 2025-09-18 编辑"),
  f="页面显示编辑于 2025-09-18；正文和部分评论 2026-11-08 已读到。",
  s="“这是我的第415篇帖子”；两年平均约 1.7 天一篇；不接广告；“谦虚的学生、learn in public”。",
  o="标题把篇数和结果放在前面，正文是感想，后半段放读者“我做了第一个 X”的反馈。",
  h="回顾帖可能让新读者快速判断“这个人长期在写”；未验证，没有阅读或转化数据。",
  b="“12万粉丝”是标题自述，不是审计值；“2年”的起点日期未知。",
  k="攒到一定篇数后写一篇回顾，用读者行动当证据，不用粉丝数当证据。"),
 dict(id="w2", t="工具接入帖：一句讲清接进哪里", links=[L["feishu"]], where=("s5","阶段 5 · 节点 14 · 05-22（年份未知）"),
  f="正文：“用这个开源项目，可以把Claude Code无缝接入飞书…手机上也可以！”（2026-11-08 读到）",
  s=None,
  o="标题是“感受词 + 教程+演示”；正文顺序是能干什么 → 像跟同事聊天 → 手机也能用。",
  h="“接进已有工作流”比单纯推荐工具名更容易被收藏；未验证，没有收藏数据或同曝光对比。",
  b="正文没写项目名；视频没播放、评论没载入，不写演示步骤；与桥接仓库是否同一项目未知。",
  k="工具帖写清“接进你已经在用的哪个软件”，而不是只写工具名。"),
 dict(id="w3", t="身份反差帖：不会写代码 × GitHub 星", links=[L["gh"], L["x1w"]], where=("s5","阶段 5 · 节点 16b · 06-17 编辑（年份未知）"),
  f="小红书标题如上；正文：“AI时代我们应该做有观点的产品”（2026-11-08 读到）。X 帖只确认链接存在。",
  s="“3万星”是标题自述，不是当前值。",
  o="标题把身份（不会写代码）和结果（3 万星）放在一起形成反差；正文只给一句观点。",
  h="反差标题可能提高点开率；未验证。旧采集说正文后面用项目当证据，本轮没有复核，不作事实。",
  b="视频没播放、评论没载入；置顶评论内容未核实，已删掉；X 帖正文本轮没复核。",
  k="Ocean 可用真实反差：大厂 PM、不手写代码，用 AI 做出的东西直接摆出来。"),
 dict(id="w4", t="结果数字帖：一年涨粉 7 万", links=[L["tw"]], where=("s5","阶段 5 · 节点 16b · 06-16 编辑（年份未知）"),
  f="标题如上；正文自述“视频的动画和剪辑都是 Claude Code 做的”（2026-11-08 读到）。",
  s="“7万”是标题自述。",
  o="标题是“如何 + 时间 + 结果数字”；正文点明视频的动画和剪辑用 Claude Code 做。",
  h="点明“用 AI 做的”可能增加可信度；未验证。",
  b="视频没播放，涨粉方法的具体步骤未知，本页不写；旧采集里的封面数字没复核，已删掉。",
  k="作品用了什么工具，在正文一句点明。"),
 dict(id="w5", t="HTML Slides 系：结果标题与判断句标题", links=[L["slides"], L["ppt"]], where=("s5","阶段 5 · 节点 15 附近 · 05-08 等（年份未知）"),
  f="只有 2026-11-01 旧采集的标题和链接；本轮没打开原帖。",
  s=None,
  o="一篇是“如何 + 结果形容词”，一篇是“A 正在取代 B”的判断句；两篇都围绕 HTML 做演示文稿。",
  h="和节点 15 的 Frontend Slides 仓库可能是同一条作品线；只是推测，标题没写仓库名。",
  b="旧采集写的正文句数和模板数量没复核，已删掉；发布年份未知。",
  k="一个作品可以连着写：先发“怎么做出来”，再发一篇行业判断。"),
 dict(id="w6", t="X 短句：领先的人反而觉得落后", links=[L["ahead"]], where=("s5","阶段 5 · X 平台 · 日期本轮未核"),
  f="链接来自 2026-11-01 旧采集；本轮只确认链接，没复核全文和日期。",
  s=None,
  o="旧采集记下的开头是反常识判断；全文长度和内容本轮未核。",
  h="反常识短句适合做小红书封面大字；未验证。",
  b="X 互动数旧采集没复核，不展示；不能说明她在小红书怎么写。",
  k="封面一句反常识判断，正文配一个自己的现场故事。"),
]
LV = [("f","事实","f"),("s","自述","s"),("o","观察","a"),("h","假设","h"),("b","边界","b")]
def card(w):
    sid, pos = w["where"]
    rows = "".join(f'<p><span class="lv {c}">{n}</span>{w[k]}</p>' for k,n,c in LV if w.get(k))
    return (f'<article class="work card" id="{w["id"]}"><h3>代表作品 {w["id"][1]} · {w["t"]}</h3>'
            f'<p class="links">{" · ".join(w["links"])}</p><p class="muted">时间线位置：<a href="#{sid}">{pos}</a></p>'
            f'{rows}<p class="take"><b>可借鉴写法：</b>{w["k"]}</p></article>')
works = ('<section id="works"><h2>代表作品拆解</h2><p class="muted">这里只挑有原帖链接的作品，<b>不是确认的热门榜</b>：互动数没有可追溯来源，一律不写。只分析标题和正文里看得到的写法；'
         '视频都没播放。<span class="lv a">观察</span>是页面上看得到的写法；<span class="lv h">假设</span>是对效果或原因的猜测，没验证。</p>'
         '<div class="works">' + "".join(card(w) for w in WORKS) + '</div></section>')

AUD = [
 ("想入门 AI、但不是工程师的学习者", "从哪学、怎么学，有人带着走一遍", "学习路径和一个同在学习的人做示范",
  '<a href="#w1">卡 1</a>；<a href="#s3">阶段 3</a> 节点 5b、6', '<span class="lv s">自述</span>作者把定位说成“非技术视角学 AI”（采访摘录）；作者说读者看了内容后去看完 Karpathy 大模型教程'),
 ("想做出第一个作品的人", "有人示范不会写代码也能做出东西", "敢动手的理由和一个起点",
  '<a href="#s3">阶段 3</a> 节点 5c（卡 1 同帖评论）；<a href="#w3">卡 3</a>', '<span class="lv s">评论者自述</span>“狗牯仔的人间喜剧”说看完后用 Cursor 和 Trea 做了小程序；“芒果.beta”说受启发做出第一个视频。<span class="lv h">假设</span>卡 3 的反差标题也打中这类人'),
 ("已在用 AI 工具、想接进日常工作的人", "把工具接进已经在用的软件", "Claude Code 接入飞书的线索；具体步骤和能否照做未核",
  '<a href="#w2">卡 2</a>', '<span class="lv f">事实</span>卡 2 正文写“无缝接入飞书…手机上也可以”。<span class="lv h">假设</span>读者是职场用户，没有数据'),
 ("想做内容、做账号的人", "别人怎么做内容、用什么工具", "方法线索和工具名",
  '<a href="#w4">卡 4</a>', '<span class="lv s">自述</span>“7万”和“用 Claude Code 做动画剪辑”都是作者说法。<span class="lv h">假设</span>这类读者存在，没有数据'),
]
arows = "".join(f'<tr><td data-l="读者类型">{a}</td><td data-l="想要什么">{b}</td><td data-l="能拿走什么">{c}</td><td data-l="对应作品">{d}</td><td data-l="证据">{e}</td></tr>' for a,b,c,d,e in AUD)
audience = ('<section id="audience"><h2>谁在看，为什么愿意看</h2>'
 '<p class="muted"><b>没有真实的粉丝画像数据</b>（年龄、职业、地区都没有），也没有点击或收藏来源。下面的人群和动机都是根据作者自述、少数评论和作品内容推出来的假设，不代表全体粉丝，也没有证明哪类人真的在看。</p>'
 '<div class="tw"><table><thead><tr><th>可能的读者类型（推断）</th><th>可能想要什么</th><th>能拿走什么</th><th>对应作品</th><th>证据</th></tr></thead><tbody>' + arows + '</tbody></table></div>'
 '<h3>可能为什么能火、能传开（未验证）</h3><div class="card"><ul class="plain">'
 '<li><span class="lv s">自述</span>她在 2025-09-18 原帖里说，希望“不制造焦虑，只提供切实具体的解决方案和学习方法；不包装自己，只发表真实想法”（<a href="#w1">卡 1</a>）。<span class="lv h">假设</span>对怕被割韭菜的入门读者，这种承诺本身就是看下去的理由。</li>'
 '<li><span class="lv s">自述</span>作者说每天至少 3 位粉丝发帖 @ 她，讲自己看完后做了什么（<a href="#s3">阶段 3</a> 节点 5b）。<span class="lv h">假设</span>读者晒“我做了第一个 X”时会带上她，这可能是一条传播路径；频次是作者口述，传播效果没有数据。</li>'
 '<li><span class="lv a">分析</span>根据她“谦虚的学生、learn in public”的自述（<a href="#s3">阶段 3</a> 节点 5a），推测这种姿态可能让读者觉得是同路人而不是老师，降低入门门槛（推断）。</li>'
 '<li><span class="lv s">自述</span>她在 X 上说，受众的价值是验证 idea、找早期用户（“Signals &gt; distribution”，<a href="#s5">阶段 5</a> 节点 17）。<span class="lv a">分析</span>她把读者当作品的第一批用户，不只是流量。</li>'
 '<li>标题写法上的差别见下一节<a href="#compare">写法对照</a>，这里不重复。</li>'
 '</ul></div><p class="muted"><span class="lv b">边界</span>评论只读到 2025-09-18 一篇，另外 4 篇评论没载入；视频都没播放。旧采集里“Codex app 写给非程序员”一类标题没有链接，不作证据。不能据此推断粉丝构成或互动因果。</p></section>')

CMP = [
 ("可带走的东西", "开源项目接入飞书（<a href=\"#w2\">卡 2</a>，正文可见）；模板（<a href=\"#w5\">卡 5</a>，只有标题，待核）", "纯观点、活动预告"),
 ("身份反差", "不会写代码 × GitHub 星（<a href=\"#w3\">卡 3</a>）", "没有前后对比"),
 ("标题写法", "如何 + 结果、教程+演示、数字结果、A 正在取代 B（<a href=\"#w4\">卡 4</a>、<a href=\"#w5\">卡 5</a>）", "直播预告、随感"),
 ("形式", "正文一两句（<a href=\"#w2\">卡 2</a>、<a href=\"#w3\">卡 3</a> 可见）；视频未播放，主体内容未知", "图文预告"),
]
rows = "".join(f'<tr><td data-l="维度">{d}</td><td data-l="代表作品">{x}</td><td data-l="普通帖">{y}</td></tr>' for d,x,y in CMP)
compare = ('<section id="compare"><h2>普通帖与代表作品：写法差在哪</h2><p class="muted"><span class="lv a">观察</span>只比较标题和正文写法，<b>不是因果</b>：没有同曝光对比，也不展示互动数。“普通帖”一列只是 2026-11-01 旧采集的主页浏览印象，没有逐篇来源，整列待核。</p>'
           '<div class="tw"><table><thead><tr><th>维度</th><th>代表作品</th><th>普通帖（旧采集印象，待核）</th></tr></thead><tbody>' + rows + '</tbody></table></div></section>')
voice = ('<section id="voice"><h2>语气、节奏与可借鉴写法</h2><div class="card"><ul class="plain">'
 '<li><span class="lv s">自述</span>她自称“谦虚的学生、learn in public”（<a href="#w1">卡 1</a>）。<span class="lv a">分析</span>据此推断语气偏学习者分享，是研究者判断。</li>'
 '<li><span class="lv a">观察</span>已读到的正文很短，一两句（<a href="#w2">卡 2</a>、<a href="#w3">卡 3</a>）；视频未播放，其余内容未知。</li>'
 ''
 '<li><span class="lv f">事实</span>飞书官方文章写明“Zara（小红书博主‘张咋啦’）”，即小红书和 X 是同一人；两边语气是否一致没逐篇比较。</li>'
 '<li><span class="lv s">自述</span>节奏有两个口径：约 1.5 天一篇（采访）和约 1.7 天一篇（2025-09-18 原帖），见<a href="#s3">阶段 3</a>，不合并。</li>'
 '</ul></div><pre class="tpl">【标题】我用 [工具] 做了 [可拿走的结果]（附模板/清单）\n【封面】一句话结果 + 数字或前后对比\n【正文 1–3 句】给什么 → 谁适用 → 一句反差\n【资产】模板截图 / Prompt / 仓库 / 检查清单\n【话题】3–5 个圈层标签\n【别】30 分钟完整版口播（图文改成一页清单）</pre></section>')

out = src
out = re.sub(r'<section id="archive">.*?</details></section>\n?', '', out, flags=re.S)
i = out.index('<section id="limits">'); out = out[:i] + works + "\n" + audience + "\n" + compare + "\n" + voice + "\n" + out[i:]
# 目录
out = out.replace('  <a href="#limits">失败与边界</a>', '  <a href="#works">代表作品拆解</a>\n  <a href="#audience">谁在看</a>\n  <a href="#compare">写法对照</a>\n  <a href="#voice">语气与节奏</a>\n  <a href="#limits">失败与边界</a>')
out = out.replace('  <a href="#archive">旧版留档</a>\n', '')
out = out.replace('  <a href="#timeline">时间线</a>\n  <a href="#limits">边界</a>\n  <a href="#for-ocean">借鉴</a>\n  <a href="#archive">留档</a>',
                  '  <a href="#timeline">时间线</a>\n  <a href="#works">作品</a>\n  <a href="#audience">受众</a>\n  <a href="#compare">对照</a>\n  <a href="#voice">语气</a>\n  <a href="#limits">边界</a>\n  <a href="#for-ocean">借鉴</a>\n  <a href="#sources">来源</a>')
# 头部图例
out = out.replace('<span class="lv b">边界</span>写不能怎么用。', '<span class="lv b">边界</span>写不能怎么用；作品卡里再分<span class="lv a">观察</span>（看得到的写法）和<span class="lv h">假设</span>（效果或原因，没验证）。')
# 给 Ocean：去重与改写
out = out.replace('<li>点赞高不等于方法有效：旧爆款表只有标题与点赞，没有同曝光对照，不作因果。</li>',
                  '<li>代表作品的写法对照只是观察，没有互动数据和同曝光对比，不能当成方法有效的证明。</li>')
out = out.replace('<li>每帖给一件能拿走的东西，并写清一个限制。</li>', '<li>每帖给一件能拿走的东西，并写清一个限制；不用“干货满满”“赋能”这类空词。</li>')
# 来源：补旧采集线索与本轮待核
out = out.replace('<a href="https://x.com/zarazhangrui/status/2079395028485488707" target="_blank" rel="noopener">X 80k 帖</a></li></ul>',
  '<a href="https://x.com/zarazhangrui/status/2079395028485488707" target="_blank" rel="noopener">X 80k 帖</a></li>'
  '<li>2026-11-01 旧采集（只作线索，互动数不展示）：卡 5、卡 6 的链接，以及 <a href="https://x.com/zarazhangrui/status/2086111492018221523" target="_blank" rel="noopener">X：Tragedy of the Cognitive Commons</a>。</li></ul>')
out = out.replace('桥接项目名称关系；小红书开始时间。</p>', '桥接项目名称关系；小红书开始时间；卡 5、卡 6 的原帖正文与日期。</p>')
out = out.replace('采集 2026-11-01 · 重写 2026-11-08（UTC+8）', '采集 2026-11-01 · 重写 2026-11-08 · 作品拆解独立成章（UTC+8）')
# 样式
css = ('.lv.h{background:#f1e8fb}\n.works{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));gap:.8rem}\n'
 '.work{margin:0;overflow-wrap:anywhere}.work h3{margin:.1rem 0 .4rem}.work p{margin:.35rem 0}.work .take{border-top:1px dashed var(--line);padding-top:.45rem}\n'
 '#compare .tw table,#audience .tw table{min-width:36rem}\n'
 '@media(max-width:700px){#compare .tw,#audience .tw{overflow:visible}#compare .tw table,#compare .tw tbody,#compare .tw tr,#compare .tw td,#audience .tw table,#audience .tw tbody,#audience .tw tr,#audience .tw td{display:block;width:100%;min-width:0}'
 '#compare .tw thead,#audience .tw thead{display:none}#compare .tw tr,#audience .tw tr{border:1px solid var(--line);border-radius:12px;padding:.55rem .7rem;margin:0 0 .7rem;background:#fff}'
 '#compare .tw td,#audience .tw td{border:0;padding:.22rem 0;overflow-wrap:anywhere}#compare .tw td::before,#audience .tw td::before{content:attr(data-l);display:block;font-size:.7rem;font-weight:650;color:var(--mut)}}\n')
out = out.replace('details.arch>summary{cursor:pointer;font-weight:700;padding:.6rem 0}\n', css)
for need in ['id="audience"', 'href="#audience">受众', '#audience .tw thead', 'id="works"', 'href="#works"', '.lv.h', '干货满满', 'Cognitive Commons', '卡 5、卡 6 的原帖正文', '#sources">来源']:
    assert need in out, need
assert 'id="archive"' not in out and 'details.arch' not in out
(REPO/"xhs"/"zhangzala.html").write_text(out, encoding="utf-8")
print("ok", len(out))
