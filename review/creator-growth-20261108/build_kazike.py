"""生成 xhs/kazike.html（卡兹克，按张咋啦页结构）。证据见 kazike-ledger.md。样式复用 xhs/zhangzala.html 的 head。"""
import re
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
zz = (REPO/"xhs/zhangzala.html").read_text(encoding="utf-8")
head = zz[:zz.index("</head>")+len("</head>")]
head = re.sub(r"<title>.*?</title>", "<title>卡兹克成长深拆 · 时间线 + 代表作品 + 受众深度 · 给 Ocean</title>", head, flags=re.S)
def a(u, t): return f'<a href="{u.replace("&","&amp;")}" target="_blank" rel="noopener">{t}</a>'
X = lambda i, t: a(f"https://x.com/Khazix0918/status/{i}", t)
W1 = a("https://mp.weixin.qq.com/s/tBN6tiV_KGbfU-8EaR9KfQ", "《今天，好像见证了属于SD时代的消亡。》")
W2 = a("https://www.huxiu.com/article/4859145.html", "三年内容方法论（虎嗅转载公众号原文）")
W3 = a("https://www.10100.com/article/149149135", "《我为什么会做AI自媒体？》OPC 演讲（转载稿）")
G1 = a("https://github.com/KKKKhazix/agent-autoloop", "GitHub：agent-autoloop")
F,S,C,A,H,B = [f'<span class="lv {c}">{n}</span>' for c,n in (("f","事实"),("s","自述"),("s","评论者自述"),("a","观察"),("h","假设"),("b","边界"))]
TH = '<thead><tr><th>#</th><th>日期（UTC+8）</th><th>当时动作 → 作品</th><th><span class="lv f">事实</span></th><th><span class="lv s">自述</span></th><th><span class="lv a">分析</span></th><th><span class="lv b">边界</span></th></tr></thead>'
def row(n,d,act,f,s,an,b):
    return f'<tr><td data-l="#">{n}</td><td data-l="日期">{d}</td><td data-l="动作与作品">{act}</td><td data-l="事实">{f}</td><td data-l="自述">{s}</td><td data-l="分析">{an}</td><td data-l="边界">{b}</td></tr>'
def stage(sid, title, q, rows, note=""):
    return f'<section id="{sid}" class="stage"><h3>{title}</h3><p class="q"><b>当时的问题：</b>{q}</p><div class="tw"><table>{TH}<tbody>{"".join(rows)}</tbody></table></div>{note}</section>'
STAGES = [
 stage("s1","阶段 1 · 2022 年底以前：产品与设计背景","AI 出来后，自己这类“执行层”工作会不会被替代。",[
  row(1,"2022 年底（月份自述）","在公司推动全员用 ChatGPT，把它接进微信群服务客户 → "+W3,"—","“GPT出来第七天我们就把它接进了微信群服务客户，第三天，微信号就被封了”；之前“一直是产品经理，在互联网金融领域做设计、做产品”","起点是一次产品尝试和一次失败，不是内容计划","演讲转载稿；X 帖里他又自称“一年前…完全不懂开发的设计师”，两种身份说法并存，不合并")]),
 stage("s2","阶段 2 · 2023-02 起：公众号起号","没有粉丝，写什么能被看见。",[
  row(2,"2023-02-26（演讲自述）","公众号写下第一篇 → "+W3,"—","“2023年2月26日写下第一篇文章”","—","旧资料另有 2-25 的说法，本页只用本人说法"),
  row(3,"2023 年初（2025 年回顾）","第二篇写 Stable Diffusion 画美女教程 → 回顾见 "+W1,"回顾文全文已读","“只有可怜的30个粉丝，每篇文章的阅读量不到100…第二篇…阅读量破了万，也为我积累了最初的500个粉丝”","工具上手教程是最早被看见的内容","第二篇原文没找到，标题以本人复述为准")]),
 stage("s3","阶段 3 · 2023：AI 视频预告片与剧组","做出一个别人没做过的东西。",[
  row(4,"2023（月份本轮未核）","用 AI 做《流浪地球》系列预告片 → 回顾见 "+W3,"—","“我们做了整整五个晚上，但当时国内几乎没人用AI视频做内容，所以它莫名其妙就火了”；之后结识郭帆","作品让身份从“讲 AI”变成“用 AI 做东西”（分析）","预告片原帖与播放数据本轮没核，不写数字"),
  row(5,"2024-10（演讲自述）","加入《流浪地球3》剧组做 AI 相关工作 → "+W3,"—","“2024年10月正式加入剧组做AI相关的工作，一干就是两年”","—","—")]),
 stage("s4","阶段 4 · 2024–2026 年中：从账号到公司与 IP","账号做大后，怎么把经验变成团队能力。",[
  row(6,"2024-10（演讲自述）","公众号行业榜单登顶 → "+W3,"—","“2024年10月就登顶了，之后连续一年多稳坐第一”；“全平台加起来已经一百多万，公众号也快破了”","—","榜单名称和原始榜单本轮未核；粉丝数是自述"),
  row(7,"2026-05-18","给公司经纪团队做内部分享后公开方法论 → "+W2,"全文已读（转载）","分享是为了“服务我们签约的所有MCN的博主们”；“小红书也才马上才摸到10万粉”","角色从博主变成带团队的人","常读约 30% 等内部指标是自述，不能当审计数据"),
  row(8,"2026-07-08（转载日期）","OPC 演讲讲为什么做 IP → "+W3,"全文已读（转载）","“唯一能跳出这个金字塔的东西，叫IP”","—","转载稿可能有编辑，个别句子不通顺")]),
 stage("s5","阶段 5 · 2026：上 X、学开发、开源","从“写 AI”到“自己搭 Agent 系统”，怎么让更多人用上。",[
  row(9,"2026-01-23",X("2014662983474090260","X 帖：Skills 管理三件套"),"帖子全文已读","“更多的还是从一个非编程专业用户角度出发…普通用户用起来实在太难太难了”","明确把读者设成不会编程的普通用户","—"),
  row(10,"2026-11-02",X("2117054043868860521","X 长文：折腾一年的 Agent 自动化系统")+" · "+X("2117054331849720246","配套帖"),"配套帖全文已读","“一年前，我是一个完全不懂开发的设计师”；“百万月活的公益产品…9000 star”","—","X 长文正文接口读不到，未读；star 和月活是自述"),
  row(11,"2026-11-02",X("2117187358760354067","X：10 万粉纪念"),"帖子全文已读","“2026.1.12～2026.11.2 294天，从0到1，10万粉”","—","这是 X 账号的自述，不是公众号；旧版把“294 天”当未证实的公众号说法，现已更正"),
  row(12,"2026-11-04 / 11-06",X("2117861191305609408","开源 Agent-Autoloop")+" · "+X("2118682277102391312","Windows 兼容")+" · "+G1,"帖子全文已读；仓库首页存在","“发之前其实战战兢兢的，怕大家觉得这就是个玩具”；“开源没几天，已经3.5K的Star”","长文讲经历，次日给仓库","star 是自述，未独立核")]),
]
# 代表作品
LV = [("f","事实","f"),("s","自述","s"),("o","观察","a"),("h","假设","h"),("b","边界","b")]
WORKS = [
 dict(id="w1",t="怀旧回顾：用一条产品新闻讲一个时代",links=[W1],where=("s2","阶段 2 · 起号回顾（写于 2025）"),
  f="公众号全文已读。从 liblib 2.0 公告切入，回顾 WebUI、ComfyUI、ControlNet、LoRA 的年代，结尾“工具会消失，但是品味，却永远不会。”",
  s="把自己起号时 30 粉、第二篇破万阅读、500 粉嵌在文中。",
  o="大量单句成段；先新闻、再个人闪回、再行业回顾、最后落到“品味”。",
  h="老读者的共同记忆加上作者亲历数字，可能让这类回顾比纯资讯更容易被转发；没有转发数据。",
  b="只读了公众号正文，没看评论区。",k="写行业变化时，把自己当年的一个具体数字放进去。"),
 dict(id="w2",t="方法论公开：把内部分享写成长文",links=[W2],where=("s4","阶段 4 · 节点 7"),
  f="全文已读（虎嗅转载）。三步：获取信息、找角度、创作；举了七夕“民政局排队离婚”和 DeepSeek 9.9 两个角度例子。",
  s="“如果一篇内容能爆，30%在获取信息的能力上，60%在找角度的能力上，最后10%才是创作本身”；自称“内容领域上的小学生”。",
  o="每一步都配一个跨领域类比（《人类简史》、美第奇效应、喜剧“三番”）。",
  h="同行和团队成员可能把它当操作手册收藏；没有数据。",
  b="文中的常读、赞阅比等是他自己的内部标准，不是行业审计。",k="方法论文每一条配一个反例或真实案例。"),
 dict(id="w3",t="演讲：为什么做 IP",links=[W3],where=("s4","阶段 4 · 节点 8"),
  f="转载稿全文已读。三个判断：人处理信息跟不上 AI 产内容；注意力总量恒定；普通人难辨真假 → “人们会选择信息源，而不是信息本身”。",
  s="起点、预告片、剧组经历都在这篇里自述。",
  o="自我介绍先给数据和破壁作品，再讲判断，最后给结论。",
  h="“选信息源”的说法也解释了他为什么持续露出个人经历；这是推断。",
  b="转载稿，原视频没看。",k="对外讲为什么做，先讲一个让自己焦虑的问题。"),
 dict(id="w4",t="X 短帖：用一个场景讲两个模型的性格",links=[X("2115691027860443268","X：Claude 和 Codex 的性格差异")],where=("s5","阶段 5"),
  f="全文已读。场景：每周下载 20 个 Excel 拼表；GPT 给鼠标脚本，Claude 反问为什么不直接写 SQL。",
  s=None,o="只用一段对话，没有结论句，靠两个回答的反差。",
  h="办公场景人人熟悉，读者容易拿自己对号；没有验证。",
  b="评论区没读。",k="比较两个工具时，给同一个任务，各写一句回答。"),
 dict(id="w5",t="一年复盘 + 次日开源：从经历到仓库",links=[X("2117054331849720246","X：一年复盘配套帖"),X("2117861191305609408","X：开源 Agent-Autoloop"),G1],where=("s5","阶段 5 · 节点 10–12"),
  f="配套帖和开源帖全文已读；仓库首页简介：“让你的命令行 Agent 在后台自己接活、自己跟进到底”。",
  s="“一年前，我连CI是什么都不知道，半年前，我甚至连CDN是什么都不知道”；“怕大家觉得这就是个玩具”。",
  o="先讲个人一年的变化，第二天给能用的仓库，再补 Windows 支持。",
  h="“不懂开发的设计师”这个起点，可能让同样不会编程的读者觉得自己也能试；没有验证。",
  b="X 长文正文读不到；视频没看；star、月活都是自述。",k="复盘发完，第二天把能用的东西放出来。"),
]
def card(w):
    sid,pos=w["where"]; rows="".join(f'<p><span class="lv {c}">{n}</span>{w[k]}</p>' for k,n,c in LV if w.get(k))
    return f'<article class="work card" id="{w["id"]}"><h3>代表作品 {w["id"][1]} · {w["t"]}</h3><p class="links">{" · ".join(w["links"])}</p><p class="muted">时间线位置：<a href="#{sid}">{pos}</a></p>{rows}<p class="take"><b>可借鉴写法：</b>{w["k"]}</p></article>'
AUD = [
 ("不会编程、想用上 AI 工具的普通用户","有人把复杂工具讲到能用","上手路径和“设计师也能学会”的示范",'<a href="#s5">阶段 5</a> 节点 9；<a href="#w5">卡 5</a>',S+"他说文章“从一个非编程专业用户角度出发”","读者现在：未知（可能 L0–L2，推断）<br>内容指向：工具和 Skills 上手；具体到哪层看篇目"),
 ("想自己搭 Agent 自动化的人","一套跑过一年的系统和能改的代码","仓库和架构思路",'<a href="#w5">卡 5</a>；X 长文评论区',C+"“我也国庆那段时间想搭一个，但是搭的一坨狗屎”；“这个自动化系统没开源吗？”；“最大的问题，是 token 不够。”","读者现在：未知。评论者尝试过搭建，不等于工具链进生产<br>内容指向：L4（自述系统含中台和插件）；是否到 L5 数据闭环未核"),
 ("做内容的同行和团队成员","可照做的方法和判断标准","三步法和角度例子",'<a href="#w2">卡 2</a>',S+"分享是为了服务“签约的所有MCN的博主们”","读者现在：未知<br>内容指向：内容方法，不是 AI 使用深度，层级不适用"),
 ("想找可信 AI 信息源的人","不用自己判断每条消息真假","一个持续露出的个人信息源",'<a href="#w3">卡 3</a>',S+"“人们会选择信息源，而不是信息本身”","读者现在：未知<br>内容指向：资讯和观点，层级未知"),
]
arows="".join(f'<tr><td data-l="读者类型">{a_}</td><td data-l="AI 使用深度">{d}</td><td data-l="想要什么">{b_}</td><td data-l="能拿走什么">{c_}</td><td data-l="对应作品">{w_}</td><td data-l="证据">{e}</td></tr>' for a_,b_,c_,w_,e,d in AUD)
audience=('<section id="audience"><h2>谁在看，为什么愿意看</h2><p class="muted"><b>没有真实的粉丝画像数据</b>。人群和动机根据作者自述、X 评论和作品内容推断，不代表全体读者。</p>'
 '<div class="tw"><table><thead><tr><th>可能的读者类型（推断）</th><th>AI 使用深度</th><th>可能想要什么</th><th>能拿走什么</th><th>对应作品</th><th>证据</th></tr></thead><tbody>'+arows+'</tbody></table></div>'
 '<p class="depth"><b>深度怎么标：</b>沿用 <a href="../research/ai-depth-levels-2026-10-28.html#levels">AI 使用深度水位</a> 的 L0–L5（定义见<a href="zhangzala.html#audience">张咋啦页</a>）；分开写读者现在和内容指向，层级不是职业类别。</p>'
 '<h3>可能为什么能火、能传开（未验证）</h3><div class="card"><ul class="plain">'
 f'<li>{S}他认为读者选的是信息源（<a href="#w3">卡 3</a>）。{H}长期公开个人经历、失败和作品，可能是在攒“信任这个人”，而不是单篇流量。</li>'
 f'<li>{S}他说找角度是三步里最重要的一步（<a href="#w2">卡 2</a>）。{A}代表作品都有一个反差点：时代葬礼、两个模型的对话、设计师搭 Agent。</li>'
 f'<li>{S}他要求“保持谦逊…你只是爱分享了一点”（<a href="#w2">卡 2</a>）。{H}弱者口吻可能降低读者的距离感。</li>'
 f'<li>{C}X 长文评论里有人说“用心好文，慢慢消化学习”，也有人追问开源和封号问题。{B}只读到 API 返回的 25 条，不能代表全部评论。</li>'
 '</ul></div></section>')
CMP=[("开头","具体场景或新闻（<a href=\"#w1\">卡 1</a>、<a href=\"#w4\">卡 4</a>）","直接说更新了什么"),
 ("个人经历","有：起号数字、一年学开发（<a href=\"#w1\">卡 1</a>、<a href=\"#w5\">卡 5</a>）","几乎没有"),
 ("读者能拿走什么","方法、仓库、可对照的场景（<a href=\"#w2\">卡 2</a>、<a href=\"#w5\">卡 5</a>）","一条信息或一张榜单"),
 ("形式","长文、对话式短帖","简短更新")]
crow="".join(f'<tr><td data-l="维度">{d}</td><td data-l="代表作品">{x}</td><td data-l="普通内容">{y}</td></tr>' for d,x,y in CMP)
compare=('<section id="compare"><h2>普通内容与代表作品：写法差在哪</h2><p class="muted"><span class="lv a">观察</span>只比较写法，不是因果；不展示互动数。普通内容一列来自同期 X 帖原文：'
 +X("2116054660851311061","Qwen 观察")+" · "+X("2116801460579234047","AIHOT 榜单更新")+" · "+X("2119083614382219734","重置监控")+'（2026-10-30～11-07，全文已读）。</p>'
 '<div class="tw"><table><thead><tr><th>维度</th><th>代表作品</th><th>普通内容</th></tr></thead><tbody>'+crow+'</tbody></table></div></section>')
voice=('<section id="voice"><h2>语气、节奏与可借鉴写法</h2><div class="card"><ul class="plain">'
 f'<li>{F}结尾固定求互动：“随手点个赞、在看、转发三连吧…我们，下次再见。”（<a href="#w1">卡 1</a>）</li>'
 f'<li>{F}口语和自嘲：“一个老狗的失落”“全部拉满算求”。{A}正式观点用很口语的话说。</li>'
 f'<li>{A}长文大量单句成段，用来控制停顿（<a href="#w1">卡 1</a>）。</li>'
 f'<li>{S}公众号文章“经常4、5千字”（<a href="#w2">卡 2</a>）。{A}2026-10-27 到 11-07 的 X 原创帖抓到 16 条，多为短更新，长内容另发 X 文章。</li>'
 f'<li>{F}X 简介和帖子反复出现“愿我们永远对世界保持好奇”。</li>'
 '</ul></div><pre class="tpl">【开头】一条具体新闻或一个工作场景\n【中段】我当年 / 我这一年的一个具体数字或失败\n【反差】大家第一反应会怎么写，我换一个角度\n【资产】方法、仓库或可对照的例子\n【结尾】落到品味或好奇心，再求一次互动</pre><p class="muted">模板是分析产物，不是作者原话。</p></section>')
limits=('<section id="limits"><h2>失败与边界</h2><div class="card"><ul>'
 '<li><b>自述里的失败</b>：微信号接 GPT 第三天被封（<a href="#s1">阶段 1</a>）；方法论里说会“追热点追慢了焦虑得睡不着”“憋了四五千字最后数据很差”。</li>'
 '<li><b>平台差异</b>：他自己说公众号之外“其他的平台我们自己做的也不是特别好”；不能用公众号或 X 的成绩推断小红书。</li>'
 '<li><b>身份说法</b>：演讲说是互金产品经理，X 帖说是设计师；两者都是自述，本页并列。</li>'
 '<li><b>数字</b>：粉丝、star、月活、常读比例都是自述；榜单、预告片播放、商单报价等本轮没有原始数据，不写。</li>'
 '</ul></div></section>')
forocean=('<section id="for-ocean"><h2>给 Ocean（「AI具身牛马」）的借鉴</h2><p class="muted"><span class="lv a">分析</span>研究者建议，不是成功公式。</p><div class="grid2">'
 '<div class="card"><h3>可借鉴</h3><ol><li>写工具时把读者设成“不会编程的人”，像他在 Skills 帖里说的那样。</li><li>复盘发完第二天给能用的东西（清单、模板或仓库）。</li><li>比较两个工具，用同一个办公场景写两句回答。</li><li>先想大家第一反应会怎么写，再换角度。</li></ol></div>'
 '<div class="card"><h3>不适用</h3><ul><li>剧组经历、公司和 MCN 团队照搬不了。</li><li>公众号榜单位置和长期积累不是起号速度。</li><li>他的小红书本人说做得一般，不能当小红书打法范本。</li></ul></div></div></section>')
COV=[("X","资料 + 2026-10-27～11-07 原创帖 16 条 + 2026-01 帖 25 条（API）","X 长文正文（接口 404）；2026-01 之前的帖"),
 ("小红书","无","主页、笔记、评论都没读：上午遇到 300013 安全限制，按规定停止。只有作者自述“马上才摸到10万粉”"),
 ("评论","X 长文对话 25 条（API 返回范围）","公众号评论、小红书评论"),
 ("作品原文","公众号 SD 回顾全文；方法论全文（转载）；OPC 演讲全文（转载）；GitHub 仓库首页","预告片原帖与视频；第二篇 SD 教程原文；PIKA、Genie 等旧版逐拆篇目")]
cov="".join(f'<tr><td data-l="来源">{p}</td><td data-l="读到了">{r}</td><td data-l="没读到">{n}</td></tr>' for p,r,n in COV)
sources=('<section id="sources"><h2>来源与待核</h2><p><b>状态：初步深化</b>。X 和公众号原文已补一手资料；小红书一手资料缺失，待解除限制后补。</p>'
 '<div class="tw"><table><thead><tr><th>来源</th><th>读到了</th><th>没读到</th></tr></thead><tbody>'+cov+'</tbody></table></div>'
 '<ul class="plain"><li>证据台账：<code>review/creator-growth-20261108/kazike-ledger.md</code>（采集 2026-11-08，UTC+8）。</li>'
 '<li>旧采集线索（2026-11-04/05，本轮未复核，只留链接）：'+a("https://mp.weixin.qq.com/s/PwM38eRIS4M8tjergbscYg","PIKA 上手评测")+" · "+a("https://mp.weixin.qq.com/s/J8raD9KkcIjf3LE1VF-yxg","两周 10 技巧")+" · "+a("https://mp.weixin.qq.com/s/5ZUzMj2yqavPeXJu2T0cTQ","2023 早期专访")+" · "+a("https://juejin.cn/post/7625574757921636367","风格 Skill 开源")+" · "+a("https://bingqiangzhou.github.io/posts/digital-life-khazix-analysis/","晚点聊 109 学习笔记（二手）")+'。</li></ul>'
 '<p><span class="tag warn">待核</span>：小红书主页与笔记；预告片发布日期与原帖；公众号榜单原始来源；X 长文正文；公司和 MCN 规模；第二篇 SD 教程原文。</p></section>')
overview=('<section id="overview"><h2>账号概况</h2><div class="grid2">'
 '<div class="card"><h3>平台</h3><p>主阵地：微信公众号「数字生命卡兹克」（本人演讲自述）。X：'+a("https://x.com/Khazix0918","@Khazix0918")+'，2022-02 建号，2026-01 起活跃（本人帖自述 294 天）。小红书：本人说有账号，本轮未读。</p></div>'
 '<div class="card"><h3>定位</h3><p>'+S+'做 IP，让读者把他当信息源（<a href="#w3">卡 3</a>）；2026 年起多写自己用 Agent 做开发的过程。</p></div></div></section>')
nav=('<div class="shell"><aside class="nav" aria-label="目录"><p class="brand">卡兹克深拆</p><p class="meta">私密 · 写给 Ocean<br>一手资料采集 2026-11-08（UTC+8）<br>初步深化 · 小红书待补</p>'
 '<div class="sec">选题库</div><a href="growth/">← 成长记录</a><a href="./">小红书全入口</a><a href="creators.html#kazike">对标档案 · 卡兹克</a>'
 '<div class="sec">本页</div><a href="#overview">账号概况</a><a href="#timeline">五阶段时间线</a><a href="#s1">1 · 起点</a><a href="#s2">2 · 公众号起号</a><a href="#s3">3 · 预告片与剧组</a><a href="#s4">4 · 公司与 IP</a><a href="#s5">5 · X 与开源</a>'
 '<a href="#works">代表作品拆解</a><a href="#audience">谁在看</a><a href="#compare">写法对照</a><a href="#voice">语气与节奏</a><a href="#limits">失败与边界</a><a href="#for-ocean">给 Ocean</a><a href="#sources">来源与待核</a></aside>'
 '<main class="main"><nav class="mob-nav" aria-label="移动目录"><a href="#overview">概况</a><a href="#timeline">时间线</a><a href="#works">作品</a><a href="#audience">受众</a><a href="#compare">对照</a><a href="#voice">语气</a><a href="#limits">边界</a><a href="#for-ocean">借鉴</a><a href="#sources">来源</a></nav>'
 '<header><h1>数字生命卡兹克 成长深拆</h1><p class="muted">按“阶段 → 当时的问题 → 动作 → 作品”排，每条附原始链接。<span class="lv f">事实</span>可从原文核到；<span class="lv s">自述</span>是本人说法；<span class="lv a">分析</span>/<span class="lv a">观察</span>是研究者归纳；<span class="lv h">假设</span>未验证；<span class="lv b">边界</span>写不能怎么用。时间统一 UTC+8，查不到写未知。</p></header>')
works=('<section id="works"><h2>代表作品拆解</h2><p class="muted">只选原文读过、写法各不相同的作品，不是热门榜；不展示互动数。</p><div class="works">'+"".join(card(w) for w in WORKS)+'</div></section>')
timeline='<section id="timeline"><h2>五阶段时间线</h2>'+"".join(STAGES)+'</section>'
html=head+"\n<body>\n"+nav+"\n"+overview+"\n"+timeline+"\n"+works+"\n"+audience+"\n"+compare+"\n"+voice+"\n"+limits+"\n"+forocean+"\n"+sources+"\n</main></div>\n</body>\n</html>\n"
(REPO/"xhs/kazike.html").write_text(html,encoding="utf-8"); print("ok",len(html))
