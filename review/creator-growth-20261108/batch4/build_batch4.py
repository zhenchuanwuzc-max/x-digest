"""第四批：改写 ai-creators-growth.html 中六人深描（保留 id：X、X-inflect、X-success），输出到分支内源副本。
证据：batch4/*-ledger.md 与 web-excerpts.md。用法：python3 build_batch4.py <原源文件> <输出源副本>"""
import sys,re,html,datetime as D
E=html.escape
def ts(i): return (D.datetime.fromtimestamp(((int(i)>>22)+1288834974657)/1000,D.timezone.utc)+D.timedelta(hours=8)).strftime('%Y-%m-%d')
def a(u,t): return f'<a href="{u}">{t}</a>'
F='<span class="tag">事实</span>';S='<span class="tag">自述</span>';C='<span class="tag">评论者自述</span>';A='<span class="tag">观察</span>';H='<span class="tag warn">假设</span>';B='<span class="tag warn">边界</span>'
LV='<a href="../research/ai-depth-levels-2026-10-28.html#levels">AI 使用深度 L0–L5</a>'
def tbl(head,rows): return '<div class="tw"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def ul(xs,tag='ul'): return f'<{tag}>'+''.join(f'<li>{x}</li>' for x in xs)+f'</{tag}>'
def section(p):
    k=p['id'];o=[f'<h2 id="{k}">深描 · {p["title"]}</h2>',f'<p class="muted">{p["sub"]}</p>']
    o.append('<div class="card"><h3>账号概况</h3>'+ul(p['overview'])+'</div>')
    o.append(f'<div class="card" id="{k}-timeline"><h3>成长时间线（日期 UTC+8）</h3>'+tbl(['日期','动作与作品','原文摘录','分析','边界'],p['timeline'])+'</div>')
    o.append(f'<div class="card inflect" id="{k}-inflect"><h3>拐点</h3><p class="muted">只列原文能核到的转折；数字均为本人说法，非审计。</p>'+tbl(['何时','发生了什么','之前 → 之后','可能为何有效（推断）'],p['inflect'])+'</div>')
    w=''.join(f'<div class="card" id="{k}-w{i}"><h3>代表作品 {i} · {x["t"]}</h3><p>{x["link"]} · 对应时间线：{x["where"]}</p><p>{F}{x["f"]}</p><p>{A}{x["o"]}</p><p>{H}{x["h"]}</p><p>{B}{x["b"]}</p><p><b>可借鉴写法：</b>{x["k"]}</p></div>' for i,x in enumerate(p['works'],1))
    o.append(f'<h3 id="{k}-works">代表作品拆解</h3><p class="muted">选原文读过、写法不同的作品，不是热门榜；不展示互动数。</p>'+w)
    o.append(f'<div class="card" id="{k}-audience"><h3>谁在看，为什么愿意看</h3><p class="muted">没有粉丝画像数据；按本人定位、原帖和读到的回复推断，不代表全体读者。深度沿用 {LV}，“读者现在”和“内容指向”分开写。</p>'+tbl(['可能的读者（推断）','想要什么','对应作品','证据','AI 使用深度'],p['aud'])+'<h3>可能为什么能留住人（未验证）</h3>'+ul(p['why'])+'</div>')
    o.append('<div class="card"><h3>普通内容与代表作品：写法差在哪</h3><p class="muted">'+A+'只比写法，不推效果。普通内容来源：'+p['cmp_src']+'</p>'+tbl(['维度','代表作品','普通内容'],p['cmp'])+'</div>')
    o.append('<div class="card"><h3>语气与节奏</h3>'+ul(p['voice'])+'</div>')
    o.append(f'<div class="card success" id="{k}-success"><h3>成功经验</h3><h3>① 他分享的招牌干货</h3>'+ul(p['goods'])+'<h3>② Ocean 可借鉴</h3>'+ul(p['take'],'ol')+'<h3 class="cant">③ Ocean 做不到 / 暂时别学</h3>'+ul(p['skip'])+'</div>')
    o.append('<div class="card"><h3>失败与边界 · 来源覆盖</h3>'+ul(p['limits'])+tbl(['来源','读到了','没读到'],p['cov'])+f'<p class="src">状态：<b>X 一手资料深化；小红书未核</b>（不据此判断小红书效果，不标双发）。证据台账：review/creator-growth-20261108/batch4/{k}-ledger.md（采集 2026-11-08 UTC+8）。旧版里没有可追溯原文的收入、订户、第三方估算本轮已删除。</p></div>')
    return '\n'.join(o)+'\n'

def X(u): return lambda i,t: a(f'https://x.com/{u}/status/{i}',t)
L=X('lennysan');SH=X('shreyas');AL=X('AliAbdaal');SW=X('swyx');PL=X('levelsio');JW=X('thejustinwelsh')
M1=a('https://www.lennysnewsletter.com/p/1000000','《1,000,000》（2025-03-04）')
P=[]
P.append(dict(id='lenny',title='Lenny Rachitsky ★',sub='X '+a('https://x.com/lennysan','@lennysan')+' · 2026-11-08 API 读到 457,527 关注者 · '+a('https://www.lennysnewsletter.com/','lennysnewsletter.com')+' · 你本地 Lenny 库的源头。',
overview=[F+'X 简介 “Deeply researched product, growth, and career advice”，2007-08 建号。',S+'里程碑文：订阅破一百万；“Roughly half are PMs, but over a quarter are founders”（'+M1+'）。',A+'X 上主要是 newsletter / 播客的分发：嘉宾金句、要点帖、产品发布（薪酬基准、杂志、礼物指南），很少写长观点。'],
timeline=[
 ['约 2019（按“just over five years ago”粗略推算）','离开 Airbnb，先在 Medium 写“学到了什么” → '+M1,'“The reason I started writing was to crystallize my own thinking”','写作起点是整理自己，不是做媒体','年份按“just over five years ago”推算'],
 ['早期（月份未核）','迁到 Substack；两篇外部客座文冷启动；marketplace 系列带来一次大涨','“Two guest posts in other newsletters to kick things off (in July)”；“A popular series of posts that led to a large spike (in late November)”','早期增长靠借别人的读者 + 一个系列','文中只写月份，年份未核'],
 ['约 9 个月后（自述）','约 9 个月后加付费档','“nine months in… I decided to add the paid plan”','先确认自己还写得动，再收费（本人说当时已写了 36 篇）','付费数字本轮没有原文，不写'],
 [ts('1400248719035957248'),L('1400248719035957248','X：65,000 订阅里程碑'),'“New milestone: 65,000 subscribers”','—','自述'],
 ['此后（自述）','停掉 Maven 课，开播客','“didn’t bring me enough joy”；“The podcast takes less work and generates more revenue than the newsletter”','newsletter 给播客导流','收入金额未披露'],
 ['2025-03-04',M1,'“one million subscribers”；“none of them have done a damn thing”（付费广告等）；“over 5,000 other newsletters recommend my newsletter”','增长归因：口碑 + Substack 推荐','全是自述'],
 [ts('2117731838760464398')+' 起',L('2117731838760464398','X：免费公开薪酬基准')+' · '+L('2118057419079340489','X：纸质杂志')+' · '+L('2117660747555856859','X：第六年礼物指南'),'“now available for free”；“Eight hand-picked posts, perfect-bound”；“sixth (!!) annual gift guide”','从内容扩到工具和实体产品','都是近一周帖，效果未知']],
inflect=[
 ['约 2019','Medium → Substack（'+M1+'）','打算再创业的前 PM → 周更作者','邮箱资产无论做不做公司都有用（本人说法）'],
 ['约 9 个月后','加付费档','免费实验 → 承诺至少再写一年','先验证“还写得动、读者觉得有用”'],
 ['Substack 推荐功能上线后','本人说那天是曲线拐点','线性 → 加速','仍取决于别的作者愿不愿推荐，即口碑'],
 ['此后几年','客座文成为最受欢迎的内容','一个人写 → 编辑别人的经验','他说每篇客座文要陪作者改 10+ 小时']],
works=[
 dict(t='里程碑问答：把增长归因讲清楚',link=M1,where='2025-03',f='全文已读。用读者提问的形式，讲团队构成、早期增长、哪些渠道没用、播客 vs newsletter 的工时账。',o='每个问题都给具体数字（每篇 10–30 小时、每集 3–5 小时）和一条可迁移的建议。',h='对想做 newsletter 的人，这比“坚持就好”更可信；没有数据。',b='数字和归因都是本人说法。',k='里程碑时，用读者的真实问题组织一篇复盘。'),
 dict(t='免费工具发布帖',link=L('2117731838760464398','X：薪酬基准'),where='2026-11',f='帖子全文已读：说明能查什么（岗位、地点、基本工资和股权）、数据从哪来（合作方 Pave）、更新频率（每月）。',o='一帖讲清“谁能用、用来干嘛、数据可信在哪”。',h='有评论认为这类表格会被截图用于 offer 讨论；只读 20 条。',b='数据质量未核。',k='发布工具时写清数据来源和更新频率。'),
 dict(t='一句话现场见闻',link=L('2117721820426355145','X：建筑师 1.5 年 → 8 分钟'),where='2026-11',f='帖子全文已读：转述一位建筑师说，原来 1.5 年的出图工作现在用 AI 8 分钟。',o='没有观点，只有一个具体对比，留给读者讨论。',h='这种可被质疑的具体数字容易引来大量回复；本轮没读这条的回复。',b='是二手转述，未核实。',k='用一个具体的前后对比开启讨论，但写清是谁说的。'),
 dict(t='年度固定栏目：礼物指南',link=L('2117660747555856859','X：第六年礼物指南'),where='2026-11',f='帖子全文已读：第六年，“There are no affiliate links here”，并建议把文章丢给 AI agent 帮忙挑礼物。',o='固定栏目 + 声明无利益 + 一个 AI 用法小提示。',h='每年同期出现，读者会等；本人说“people ping me asking when the new list will be out”。',b='是否带来订阅未知。',k='做一个每年同期的固定栏目。')],
aud=[
 ['产品经理','怎么做产品、怎么升职','卡 1、薪酬基准（卡 2）',S+'“Roughly half are PMs”（'+M1+'）','读者现在：未知<br>内容指向：方法为主；涉及 AI 应用，本轮材料不足以分级'],
 ['创业者','增长、定价、招人','嘉宾访谈、要点帖',S+'“over a quarter are founders”','读者现在：未知<br>内容指向：经营问题，层级不适用'],
 ['正在找工作 / 谈薪的人','岗位和薪酬信息','卡 2、远程高薪岗位帖',C+'“Pay transparency also changes hiring conversations… An India cut of this would be very welcome.”','读者现在：未知<br>内容指向：不适用'],
 ['工程、设计、增长等相邻岗位','PM 技能','播客、客座文',S+'相邻岗位是“the segment growing fastest”','读者现在：未知<br>内容指向：未知']],
why=[S+'他把增长归因于“publishing something valuable… over and over and over”（'+M1+'）。'+A+'X 帖几乎都在给可用的东西：工具、清单、嘉宾要点。',S+'客座文是最受欢迎的内容。'+H+'他的平台本身成了嘉宾愿意来的理由，形成循环；未验证。',C+'所读 20 条中，有数条追问岗位或地区细分（P&amp;L、增长岗、印度）。'+B+'只读 20 条。'],
cmp_src=L('2116158428208828713','Happy Halloween')+' · '+L('2115839249581003104','“What everyone calls \'prepping\' is really just shopping”')+'（均为 2026-10-30，全文已读）。',
cmp=[['开头','“Announcing:” + 一个能用的东西','一句玩笑或节日问候'],['读者拿走什么','工具、清单、方法','一个笑点'],['形式','分段说明 + 链接','一句 + 图']],
voice=[F+'常用 “Announcing:”、编号清单、“Pro tip:”。',F+'会主动声明利益关系：“I\'m not making any money from the sale of this magazine.”',S+'“prioritize stamina over anything else”（'+M1+'）。',A+'节奏：本轮 25 条原创里，多数是节目和产品分发帖。'],
goods=['<b>'+M1+'</b>：增长归因、团队、工时账。','<b>客座文机制</b>：本人说每篇陪作者改 10+ 小时。','<b>免费工具</b>：薪酬基准、礼物指南等固定栏目。'],
take=['用读者的真实问题写一次复盘。','做一个每年/每季固定出现的栏目。','发布东西时写清数据来源和利益关系。'],
skip=['周更长文 + 每周一到两期播客，本人说“basically a 40-hour job”。','客座文和嘉宾资源：需要已有的大平台。','用英文 PM 圈的订阅网络增长。'],
limits=['<b>数字</b>：订阅、读者构成、工时都是本人说法；旧版的 CNBC、Growth In Reverse 收入数字本轮没重读，已删除。','<b>平台</b>：播客、YouTube、Slack 社区没读；小红书未核。','<b>评论</b>：只读薪酬基准帖 20 条回复。'],
cov=[['X','资料（API）+ 2026-10-29～11-07 原创 25 条 + 2021-06 帖 3 条 + 2023–2026 关键词搜索 20 条','2019–2020 的帖子（搜索未返回）'],['网站原文','《1,000,000》全文','早期 Medium 文；付费文章'],['评论','1 帖 20 条','其他'],['小红书','无','未核']]))

P.append(dict(id='shreyas',title='Shreyas Doshi',sub='X '+a('https://x.com/shreyas','@shreyas')+' · 2026-11-08 API 读到 405,419 关注者 · 前 Stripe PM；产品判断力短帖 + 教练 + Maven 课。',
overview=[F+'X 简介：“Led a couple of Stripe\'s most successful products from early days. Prev Twitter, Google, Yahoo. Now advising founders, coaching executives, teaching what I know”。',S+'Maven 页：Stripe Connect、Stripe Terminal，“Stripe\'s first PM Manager”（'+a('https://maven.com/shreyas-doshi','Maven')+'）。',A+'X 上写的几乎都是一个主题：产品人的判断力，而不是工具或新闻。'],
timeline=[
 ['2021-05 之前','Twitter、Google、Yahoo、Stripe 做产品','Maven 页 “led a couple of Stripe\'s most successful products from their early days”','大厂一线履历是他所有判断的底气','履历是本人说法'],
 [ts('1395913907777073153'),SH('1395913907777073153','X：离开 Stripe'),'“After 5+ years at Stripe, today was my last day”；'+SH('1395913912676016128','下一帖')+'：“startup advising, some investing &amp; maybe publishing the product book”','离职时没有明确的内容计划','—'],
 [ts('1399042778613485578'),SH('1399042778613485578','X：产品管理框架线程'),'“A thread of product management frameworks”','离职约九天后发框架合集线程','线程正文本轮没读到；旧版提到的 LNO 是否出自此线程未核'],
 [ts('1424535807411376129'),SH('1424535807411376129','X：为何离开'),'“my son’s age, almost 2 decades of non-stop work, and my interest in spending a lot more time advising startups”','—','—'],
 ['2026（读于 11-08）',a('https://maven.com/shreyas-doshi','Maven 页'),'课程 “World-class Product Sense in Practice”，“helped 3000+ students”；工作坊 “Advanced Product Taste… AI-pilled”','教学产品化','学员数是平台页自述'],
 [ts('2108301324102279535'),SH('2108301324102279535','X：执行型 PM 难找工作'),'“Product Managers who’ve historically viewed their role as “my main job is to execute” are finding it way harder to get hired”','讨论 PM 自我定位与招聘差异；部分评论把它联系到 AI','—']],
inflect=[
 ['2021-05','离开 Stripe（'+SH('1395913907777073153','X')+'）','雇员 → 顾问/教练/写作','有一线履历后再公开教'],
 ['2021-05-31','框架线程（'+SH('1399042778613485578','X')+'）','零散推文 → 可收藏的框架合集','首帖把内容定位为框架合集；正文与收藏效果未核'],
 ['此后','Maven 课 + 工作坊','免费短帖 → 付费课','课名和 X 主题一致：判断力、品味']],
works=[
 dict(t='框架合集线程',link=SH('1399042778613485578','X：PM 框架线程'),where='2021-05',f='首帖全文已读：“A thread of product management frameworks”，并写清给谁（PM、产品负责人、创始人）。',o='首帖只说是什么、给谁，正文放在线程里。',h='合集形式适合收藏；未验证。',b='线程后续各条没读到。',k='写合集时第一句写清“给谁”。'),
 dict(t='一句话判断：两种 PM',link=SH('2108301324102279535','X：执行 vs 让产品成功'),where='2026-10',f='全文已读：对比“my main job is to execute”和“my main job is to make the product successful”两种自我定位。',o='两个引号里的原话对照，读者自己对号入座。',h='回复里很多人补充自己行业的例子（设计、地产），说明这个对比容易迁移；只读 20 条。',b='“更难被录用”是他的观察，没有数据。',k='用两句原话对照两种做法。'),
 dict(t='反常识：别再“多和用户聊”',link=SH('2110393175525454315','X：Henry Ford 与 top 20%'),where='2026-10',f='全文已读：分点说平均水平的人该多和用户聊，但前 20% 已经聊够了，“Judgment matters most”。',o='先承认常规建议，再划出它不适用的人群。',h='让自认为高于平均的读者感到被说中；推断。',b='“前 20%”是他的划分，没有依据数据。',k='反驳一个常见建议时，先说它对谁仍然成立。'),
 dict(t='投票帖：让读者自评',link=SH('2106144360563974300','X：你身边同事的 Taste')+' · '+SH('2107490235559088231','X：你最常犯哪个错'),where='2026-10',f='全文已读：让读者给同事的品味打分、选自己最常犯的错。',o='问题本身就是他课程的主题（Taste、错误）。',h='投票帖可能用来测课程选题；推断。',b='投票结果没读。',k='用投票问读者，顺便验证下一个课题。')],
aud=[
 ['中高级产品经理','升职、判断力','卡 2、卡 3',C+'“quickest test i\'ve found: ask a pm what happened to the feature a month after it shipped”','读者现在：未知<br>内容指向：判断力，层级不适用；AI 只作为背景（“agent executes faster”出现在回复里）'],
 ['创始人','产品策略、招人标准','框架线程、执行 vs 结果',S+'Maven 页列出其顾问对象','读者现在：未知<br>内容指向：不适用'],
 ['设计、工程等相邻岗位','把产品判断迁移到本职','卡 2',C+'“Same shift in design. “Deliver the screens” is getting cheaper every month.”','读者现在：未知<br>内容指向：不适用']],
why=[A+'主题极窄：只讲产品人的思考质量。'+S+'“the best (and really the only) path… is to greatly improve the quality of your thinking”（'+SH('2107254835364135176','X')+'）。',H+'Stripe 等履历让抽象判断有可信度；未验证。',C+'“执行 vs 结果”帖回复多是补充自己领域的例子，也有一条与主题无关的投诉。'+B+'只读 20 条。'],
cmp_src=SH('2111619188649508974','求助：纳什维尔医疗')+' · '+SH('2111629593820201365','感谢转发')+'（2026-10-18，全文已读）。',
cmp=[['开头','一个判断或对比','一个私人求助'],['读者拿走什么','一个自查问题','—'],['形式','短段落、分点','一两句']],
voice=[F+'常用 “Periodic reminder:”、“Something that’s changed…”、编号原因。',F+'很少用表情和网络梗，像资深同事说话。',A+'节奏：本轮 API 返回 19 条帖子，覆盖 2026-10-03～10-18。'],
goods=['<b>框架线程</b>：'+SH('1399042778613485578','2021-05 PM 框架合集')+'。','<b>判断力短帖</b>：执行 vs 结果、别迷信“多聊用户”。','<b>Maven 课</b>：Product Sense、Product Taste（'+a('https://maven.com/shreyas-doshi','Maven')+'）。'],
take=['一条帖只讲一个判断，用两句原话对照。','反驳常见建议时先说它对谁仍成立。','用投票问读者，验证下一个选题。'],
skip=['Stripe 早期产品负责人的履历背书。','顾问 + 教练的收入结构：需要高管人脉。','英文 PM 圈的语境，中文要换例子。'],
limits=['<b>线程</b>：LNO 等具体框架的正文本轮没读到，旧版 Thread Reader 链接是第三方存档，不当一手资料。','<b>数字</b>：学员数是 Maven 页说法；旧版 LinkedIn 履历日期本轮没重读。','<b>评论</b>：只读 1 帖 20 条。','<b>平台</b>：LinkedIn、课程本身没读；小红书未核。'],
cov=[['X','资料（API）+ 2026-10 返回帖子 19 条 + 2021-04～09 搜索 15 条 + 框架线程首帖','2022–2025 的帖子；线程正文'],['网站','Maven 讲师页','课程内容'],['评论','1 帖 20 条','其他'],['小红书','无','未核']]))

P.append(dict(id='ali',title='Ali Abdaal',sub='X '+a('https://x.com/AliAbdaal','@AliAbdaal')+' · 2026-11-08 API 读到 356,649 关注者 · 医生 → YouTube 效率内容 → 课程、书、App。主平台是 YouTube，本轮没看视频。',
overview=[F+'X 简介：“Building @superfocusHQ… Doctor turned Entrepreneur, YouTuber, New York Times Bestselling author: Feel-Good Productivity.”',S+'About 页：2017 年在剑桥读医时开 YouTube；团队“over 20 employees”（'+a('https://aliabdaal.com/about/','About')+'）。',A+'X 不是他的主战场：近期原创多是招聘、产品、向关注者提问。']
,timeline=[
 ['2017（自述）',a('https://aliabdaal.com/about/','About 页'),'“I started my YouTube channel in 2017 initially as a content marketing driver for the business”；“52 videos in 6 months… 1,000 subscribers”','频道起点是给自己的医学申请辅导生意引流','—'],
 ['2018–2020（自述）','做住院医，同时做视频','“the channel grew to 100,000 subscribers that year”（2018）','业余期','自述'],
 ['2020-08（自述）','暂停医生工作','“In August 2020, I took a break from Medicine”；“In 2020, we grew to 1 million subscribers, and the business hit $1m in annual revenue”','全职化','数字为自述'],
 ['2020 年末（自述）',a('https://aliabdaal.com/newsletter/celebrate-every-win-big-or-small/','LifeNotes 2024-04-22'),'Part-Time YouTuber Academy 首期：“We expected like 12 people to sign up, but 350+ people ended up signing up”；截图 “$259k”','课程成为生意转折','截图本页没看到原图'],
 ['2023（自述）','出版 Feel-Good Productivity','About 页“instant New York Times and Sunday Times bestseller”','—','—'],
 ['2024-04（自述）','Productivity Lab 首期','“sold 477 of the 500 spots”','社区/课程继续扩','—'],
 [ts('2059918988147044502')+' 起',AL('2059918988147044502','X：CreatorGrid')+' · '+AL('2096840353446006930','X：Superfocus 小组件'),'“it all came from the problems we were having with our own apps”','从内容创作者转向做软件和创作者营销平台','新业务成绩未知']],
inflect=[
 ['2017','为辅导生意开 YouTube','内容做引流 → 内容本身成主业','分享自己的学习方法，主业身份可信'],
 ['2020-08','暂停行医，全职','业余 → 全职 + 团队','疫情导致出国计划取消（本人说法）'],
 ['2020 年末','YouTuber Academy 首期','广告/赞助 → 课程','本人说预期 12 人，实际 350+'],
 ['2026（起始时间未核）','Superfocus、CreatorGrid 推广帖','教效率 → 做效率 App 和营销平台','未知']],
works=[
 dict(t='公开日记式 newsletter',link=a('https://aliabdaal.com/newsletter/celebrate-every-win-big-or-small/','LifeNotes：Celebrate every win'),where='发表于 2024-04-22；回顾 2020 年末课程首期，对应 2024 年 Productivity Lab 节点',f='全文已读：讲一次产品上线的当天过程，顺带回顾 2020 课程首期，结尾三条个人 takeaway。',o='用一天的场景串起团队、数字和感受；“this weekly email is basically my public journal”。',h='故事比清单更让读者愿意读完；未验证。',b='截图和收入是自述。',k='复盘写成“那天发生了什么”，结尾再给两三条做法。'),
 dict(t='向关注者提问',link=AL('2083884396264767991','X：WordPress 替代品')+' · '+AL('2086401006015820041','X：VPS 上看 markdown'),where='2026-08',f='全文已读：问“agent-editable”的建站工具、在 VPS 终端里看 markdown 的方法。',o='把自己的真实工作问题直接抛出来。',h='他自述用 Cursor SSH 到 VPS，并在找能让 agent 编辑、非技术同事也能写的建站方案；推断他在把 AI 工具用到自己的业务里。',b='WordPress 帖回复只读到 2 条。',k='把自己卡住的真实问题发出来，比发结论更容易得到回复。'),
 dict(t='对话体小故事',link=AL('2071135928220094782','X：神经外科朋友'),where='2026-06',f='全文已读：用“Me/Him”对话讲一个朋友怎么面对辛苦。',o='对话体，最后落到一个心态。',h='医生身份让这类故事可信；推断。',b='回复没读。',k='用一段真实对话讲一个观点。'),
 dict(t='产品招募帖',link=AL('2108148562101985569','X：CreatorGrid')+' · '+AL('2090073185433624667','X：Superfocus 招 Founding Members'),where='2026',f='全文已读：讲自己做创作者时的痛点 → 做了什么 → 合作品牌 → 申请链接。',o='用 8 年创作者经历给新产品背书。',h='已有受众先被转成早期用户；推断。',b='产品成绩未知。',k='新产品先讲你自己被什么问题折磨过。')],
aud=[
 ['学生和年轻职场人','学习方法、效率','书、YouTube（未看）',S+'早期视频“about life as a medical student and how to study more effectively”','读者现在：未知<br>内容指向：效率方法，层级不适用'],
 ['想做 YouTube / 一人生意的人','怎么做频道、怎么做课','YouTuber Academy、LifeNotes',S+'课程首期 350+ 人报名','读者现在：未知<br>内容指向：不适用'],
 ['在用 AI 工具管内容和网站的创作者','工具推荐','卡 2',C+'有人推荐开源 Next.js 建站方案','读者现在：未知（回复太少）<br>内容指向：需求指向 agent 编辑网站，可能涉及 L4；没有实际工作流证据，暂不定级']],
why=[S+'他说几乎所有好事都来自 2016 年开个人网站（'+AL('1786063137323491638','X')+'）。'+A+'他的内容一直围绕“自己正在做的事”。',H+'医生 → 创业者的身份反差让效率内容更可信；未验证。',B+'X 上只读到 2 条回复，受众判断主要靠本人说法。'],
cmp_src=AL('2111417644637467094','liberal arts 词源')+' · '+AL('2117325379899928663','同人小说更新')+'（2026-10/11，全文已读）。',
cmp=[['开头','一个故事或真实问题','一个冷知识或个人爱好'],['读者拿走什么','做法、工具、机会','一个有趣的事实'],['形式','分段长帖','一两句']],
voice=[F+'开头常用 “hey gang”，小写、口语、表情。',F+'newsletter 自称“public journal”。',A+'X 上频率不高：API 返回 24 条，跨 2026-05～11。'],
goods=['<b>LifeNotes 周信</b>：公开日记式复盘。','<b>YouTuber Academy / Productivity Lab</b>：课程和社区（本人说法见时间线）。','<b>Feel-Good Productivity</b>：书。'],
take=['复盘写成一天的场景。','把真实卡点发出来问。','新产品先讲自己的痛点。'],
skip=['医生转创业者的身份反差。','20+ 人团队的课程和 App 生意。','“教人做 YouTube”的赛道，和你的 PM 定位不同。'],
limits=['<b>主平台没看</b>：YouTube 视频本轮没看，频道成长只用 About 页自述。','<b>数字</b>：订阅、营收、报名人数都是本人说法；旧版的 Publish Press、LinkedIn、Passionfroot 数字本轮没重读，已删除。','<b>评论</b>：只读 2 条。','<b>小红书</b>：未核。'],
cov=[['X','资料（API）+ 2026-05～11 返回帖子 24 条 + 2024-04～06 返回帖子 25 条','2017–2023 的帖子'],['网站','About 页；LifeNotes 一篇全文','书；课程；其他周信'],['YouTube','无','全部视频'],['评论','1 帖 2 条','其他'],['小红书','无','未核']]))

P.append(dict(id='swyx',title='swyx（Shawn Wang）',sub='X '+a('https://x.com/swyx','@swyx')+' · 2026-11-08 API 读到 211,796 关注者 · Learn in Public → Latent Space → AI Engineer 大会。',
overview=[F+'X 简介列出 smol_ai、cognition、temporalio、aidotengineer、latentspacepod 等关联。',S+'《The Rise of the AI Engineer》提出“AI Engineer”这个岗位名，并宣布办大会（'+a('https://www.latent.space/p/ai-engineer','原文')+'）。',A+'X 上是高频的活动、播客、合作方推广，夹杂个人吐槽。'],
timeline=[
 ['2018-06-19',a('https://swyx.io/learn-in-public','《Learn In Public》'),'“have a habit of creating learning exhaust”；“the biggest beneficiary of you trying to help past you is future you”','个人宣言，他本人之后多年反复转发','—'],
 [ts('1009174159690264579'),SW('1009174159690264579','X：发布 Learn In Public'),'“Learn In Public.”','—','—'],
 [ts('1403396619895152645'),SW('1403396619895152645','X：第 8 种译文'),'“There are now at least 8 translations of this essay!”','后来出现多种译文','译本数为本人说法'],
 ['网页标注 2023-06-30（时区未核）；X 发布帖 '+ts('1674826723068903425'),a('https://www.latent.space/p/ai-engineer','《The Rise of the AI Engineer》')+' · '+SW('1674826723068903425','X 发布帖'),'“The emerging (and least cringe) version of this role seems to be: AI Engineer”；“have never run a 500 person conference”','用一篇文给一类人命名，同时开大会','—'],
 [ts('1707174366654697826'),SW('1707174366654697826','X：首届 AI Engineer Summit 日程'),'“The inaugural AI Engineer Summit schedule… Oct 8-10, SF and virtual”','—','—'],
 ['2026-11',SW('2118905788915982341','X：每周跟踪 Anthropic IPO')+' · '+SW('2119140818690974203','X：AIE CODE 嘉宾'),'“weekly coverage of the Anthropic IPO all the way until it does or doesn\'t happen”','媒体 + 大会两条线并行','—']],
inflect=[
 ['2018','《Learn In Public》','个人学习笔记 → 有多种译文的宣言','一句话可复述；鼓励读者行动'],
 ['2023-06','给“AI Engineer”命名 + 开大会','写作者 → 社群组织者','先有命名，再有聚集的场所'],
 ['此后','播客、newsletter、大会并行','—','旧版写“大会是主要收入”来自 Changelog 转录，本轮没重读，不写']],
works=[
 dict(t='宣言文：Learn In Public',link=a('https://swyx.io/learn-in-public','swyx.io'),where='2018',f='全文已读：一条总规则 + 一串具体动作（写博客、在会上讲、做开源、总结会议）。',o='每个抽象建议后面都跟着能马上做的动作。',h='可执行清单让人愿意转给别人；未验证。',b='影响力只能看到他自述的译本数。',k='写宣言时每条都配一个能马上做的动作。'),
 dict(t='命名文：The Rise of the AI Engineer',link=a('https://www.latent.space/p/ai-engineer','Latent Space'),where='2023-06（网页标注）',f='全文已读：论证为什么会出现新岗位、和 ML 工程师的区别，最后宣布大会。',o='先命名，再给“这群人”一个聚会地点。',h='命名让读者有了身份认同；推断。',b='岗位趋势是他的判断。',k='给你观察到的一类人起个名字。'),
 dict(t='持续栏目承诺',link=SW('2118905788915982341','X：每周 IPO 跟踪'),where='2026-11',f='全文已读：承诺每周跟踪，直到上市或不上市。',o='把一次热点变成固定栏目。',h='回复里很多人说要跟着看、列出自己关心的指标；只读 20 条。',b='后续是否坚持未知。',k='把热点做成有期限的固定追踪。')],
aud=[
 ['AI 应用工程师','跟上工具和模型、找同行','卡 2、播客、大会',S+'文章写给“Software Engineers working on productionizing AI APIs and OSS models”','读者现在：未知<br>内容指向：面向 AI 应用工程；具体 L3/L4 需看实际流程，本轮不定级'],
 ['关注 AI 公司的投资/行业人士','财务和行业分析','卡 3',C+'“I\'d watch three numbers more than narrative: revenue mix (API vs seats), inference margin…”','读者现在：未知<br>内容指向：不适用'],
 ['想转行或成长的开发者','学习方法','卡 1',S+'自述至少 8 种译本','读者现在：未知<br>内容指向：学习方法，层级不适用']],
why=[A+'他的两篇代表作都在给读者一个身份：公开学习的人、AI 工程师。',H+'大会和播客让读者能见到彼此，而不只是读他；未验证。',C+'IPO 帖回复里多人列自己要看的指标。'+B+'只读 20 条。'],
cmp_src=SW('2119164641301696891','“never ever forget”')+' · '+SW('2119116259921191413','“they are starting to believe”')+'（2026-11-08，全文已读）。',
cmp=[['开头','一个宣言或命名','一个梗或一句话'],['读者拿走什么','身份、方法、聚会','笑点'],['形式','长文 + 发布帖','一句 + 链接/图']],
voice=[F+'小写、梗多、感叹号多：“incredibly hyped”、“best swag game in the business”。',A+'节奏：25 条原创集中在 2026-11-06～11-08 三天，大会前密集发。',A+'长文严肃、X 上随意，两种语气分得很开。'],
goods=['<b>'+a('https://swyx.io/learn-in-public','Learn In Public')+'</b>。','<b>'+a('https://www.latent.space/p/ai-engineer','The Rise of the AI Engineer')+'</b>。','<b>Latent Space 播客 + AI Engineer 大会</b>。'],
take=['辅系列直接用“公开学习”的姿态。','给你观察到的一类人起名字。','热点做成有期限的固定追踪。'],
skip=['办大会和招赞助。','工程师社群的深度技术内容。','高频活动推广的发帖节奏。'],
limits=['<b>收入</b>：旧版 Changelog 转录和 Sidestack 目录的数字本轮没重读，已删除。','<b>平台</b>：播客、AINews、大会内容没看；小红书未核。','<b>评论</b>：只读 1 帖 20 条。'],
cov=[['X','资料（API）+ 2026-11-06～08 原创 25 条 + 2018–2023 关键词搜索 20 条','2024–2026-10 的大部分帖子'],['网站','两篇代表作全文','播客、newsletter 其他文章'],['评论','1 帖 20 条','其他'],['小红书','无','未核']]))

P.append(dict(id='levelsio',title='Pieter Levels（levelsio）',sub='X '+a('https://x.com/levelsio','@levelsio')+' · 2026-11-08 API 读到 990,458 关注者 · 独立做产品、公开收入。',
overview=[F+'X 简介直接列各产品月收入（如 “$68K/m”“$44K/m”），这是他本人展示的数字，未核。',S+'“Only 4 out of 70+ projects I ever did made money and grew”（2021-11，'+a('https://levels.io/photoai-14000-lines-raw-php-revenue','levels.io 归档标题')+'）。',A+'X 上混合三类：做产品的进度、对 AI/平台的强烈意见、生活与政治吐槽。'],
timeline=[
 ['2014-03-01',a('https://levels.io/12-startups-12-months/','《I\'m Launching 12 Startups in 12 Months》'),'“My challenge is to actually finish and launch my projects”','用公开承诺逼自己发布','—'],
 ['2014–2015','#nomads（12 startups 计划中的一项，序号未核）、Remote OK（归档标题 “How I built Remote | OK and launched it to #1 on Product Hunt”，2015 年 4 月段）','标题已读','挑战之后出现的产品','与挑战的归属、早期何时收费未核'],
 ['2018-02-26','归档标题 “I just passed $52,843 in monthly revenue”','标题已读','公开收入成为固定内容','正文没读'],
 ['2019-05-30','归档标题 “It took 4 years to reach $1m annual revenue with Nomad List and Remote OK”','标题已读','—','正文没读'],
 ['2023-07-03',a('https://levels.io/photoai-14000-lines-raw-php-revenue','Photo AI 帖存档'),'“almost 14,000 lines of raw PHP”；“1,872 paying customers making $61,808 per month”','2023 年已公开 AI 产品及收入','收入自述'],
 [ts('1735086690321023267'),PL('1735086690321023267','X：一个月砍掉 20% 成本'),'“replaced lots of human work with GPT4 API robots”','连成本优化都公开','—'],
 [ts('2119132202952798369'),PL('2119132202952798369','X：用 Claude Code 设计家具'),'“Claude Code can design furniture part by part and then give you a bill of materials”','把 AI 用法延伸到生活','—']],
inflect=[
 ['2014-03','12 个月 12 个项目','想法多、不发布 → 每月发布','公开承诺 + 截止日期'],
 ['此后','Nomad List、Remote OK 等','试验 → 少数产品存活','本人说 70+ 项目里只有 4 个赚钱；早期何时收费未核'],
 ['2023','Photo AI 等 AI 产品','目录站 → AI 产品','本人强调原始技术栈（raw PHP）']],
works=[
 dict(t='公开承诺帖',link=a('https://levels.io/12-startups-12-months/','12 startups'),where='2014',f='全文已读：问题（完不成、不敢发）→ 规则（每月一个）→ 自己的定义 → 进度表。',o='把个人挑战写成别人能围观的项目。',h='围观让他更难放弃；推断。',b='12 个项目的完成情况没逐个核。',k='公开一个有截止日期的小挑战。'),
 dict(t='收入 + 技术栈反差帖',link=a('https://levels.io/photoai-14000-lines-raw-php-revenue','Photo AI 14,000 行 PHP'),where='2023-07',f='全文已读：四句话——代码量、不用框架、付费人数、月收入。',o='用“土技术 + 高收入”的反差。',h='反差引发技术圈争论，争论带来传播；推断。',b='收入是自述。',k='一个反差事实比一段道理更容易被转。'),
 dict(t='AI 用法外溢到生活',link=PL('2119132202952798369','X：家具'),where='2026-11',f='全文已读：讲家具贵、Claude Code 能出零件清单、朋友用它设计桌子。',o='从自己装修的具体痛点出发。',h='回复里有人追问“谁来组装”“真实成本”，也有人分享自己做的 CAD 工具；只读 20 条。',b='设计能否落地没验证。',k='讲 AI 用法时从一个非技术的生活痛点出发。'),
 dict(t='立规矩：反 AI 回复',link=PL('2118746285071028248','X：AI 回复')+' · '+PL('2118737314943754500','X：公开拉黑名单'),where='2026-11',f='全文已读：批评 AI 自动回复，说要公开拉黑名单。',o='强硬表态，直接点名后果。',h='让真人回复者觉得被保护；推断。',b='有争议，本页不评价。',k='（不建议照搬）')],
aud=[
 ['独立开发者 / 想做副业的程序员','做产品和赚钱的真实例子','卡 1、卡 2',S+'帖子常带收入和成本','读者现在：未知<br>内容指向：产品与经营，卡 1、卡 2 不据此定 AI 层级'],
 ['尝试 AI/CAD 工具的人','能照做的例子','卡 3',C+'“I built my own little cad app with MCP”','读者现在：出现 MCP 工具实践自述，具体层级未核<br>内容指向：用 Claude Code 做设计的尝试，层级未核'],
 ['数字游民','城市和远程工作','Nomad List',S+'早期大量旅居内容','读者现在：未知<br>内容指向：不适用']],
why=[A+'几乎每个增长节点都对应一个可以打开的产品。',S+'公开收入是他长期做法；'+H+'具体数字让读者愿意追更，也引来质疑；未验证。',C+'家具帖回复里既有兴奋也有专业木工泼冷水。'+B+'只读 20 条。'],
cmp_src=PL('2118663337433030792','巴拉圭加密')+' · '+PL('2118769886881055063','欧盟吐槽')+'（2026-11-06/07，全文已读）。',
cmp=[['开头','我做了/发现了什么','一个对政治或地区的看法'],['读者拿走什么','可试的做法和数字','立场'],['形式','截图、数字、链接','一两句']],
voice=[F+'短句、直接、常带具体金额（“$300/mo”“$30,000”）。',F+'情绪强：“go nuclear”“you\'re an asshole”。',A+'节奏：API 返回 23 条，只覆盖 2026-11-06～11-08，发帖极频繁。'],
goods=['<b>'+a('https://levels.io/12-startups-12-months/','12 startups in 12 months')+'</b>。','<b>Photo AI 等公开收入帖</b>。','<b>MAKE</b>：归档标题显示 2018-03 上 Product Hunt。'],
take=['公开一个有截止日期的小挑战。','用反差事实代替道理。','讲 AI 用法从生活痛点出发。'],
skip=['十多年产品积累和近百万关注者。','激烈的政治和对骂语气。','全职独立开发、旅居的生活方式。'],
limits=['<b>收入</b>：全是本人说法；旧版 open 页、第三方汇总已删除。','<b>原文</b>：多数早期内容只读了归档标题，正文没读。','<b>评论</b>：只读 1 帖 20 条。','<b>小红书</b>：未核。'],
cov=[['X','资料（API）+ 2026-11-06～08 返回帖子 23 条 + 2023-12 搜索 13 条 + 2015–2019 搜索 20 条（多为回复）','2014–2022 的大部分原创'],['网站','12 startups 全文；Photo AI 帖存档；归档标题列表','MAKE；各产品本身'],['评论','1 帖 20 条','其他'],['小红书','无','未核']]))

P.append(dict(id='justinwelsh',title='Justin Welsh',sub='X '+a('https://x.com/thejustinwelsh','@thejustinwelsh')+' · 2026-11-08 API 读到 594,123 关注者 · 一人公司；LinkedIn 起家。',
overview=[F+'X 简介：“I write The Saturday Essay for 200,000+ ambitious people living and working on their own terms.”',S+'“passed $10M in total revenue, five years and nine months after launching”（'+a('https://justinwelsh.me/essays/my-10m-journey','My complete $10M journey')+'）。',A+'X 上几乎全是一句话格言，夹着固定的导流帖（免费指南、周刊）。'],
timeline=[
 ['起点（自述）',a('https://justinwelsh.me/essays/my-10m-journey','$10M 文'),'“I started on LinkedIn, talking about building a SaaS unicorn as the CRO”','先用老本行积累关注','—'],
 ['早期（自述）','做咨询服务','“Your first business should be a high-touch, high-value service”','先服务再产品','—'],
 ['2020-04-16（自述）','The LinkedIn Playbook，$50','“in the first month, I made $10,482”','第一个数字产品，主题和咨询不同','自述'],
 ['此后（自述）','升级为 The LinkedIn Operating System','“Over the next 15 months, The LinkedIn Playbook brought in $75K.”；“The second version grossed $186k in 3 months.”','内容和产品同题后卖得更好','自述'],
 ['此后（具体年份未核）','关掉 $15k MRR 的社区','“It was a $15k MRR business, but I felt like I had to be on Slack 24/7.”','为生活方式砍业务','自述'],
 ['2021-12',JW('1469087817150124042','X：solopreneur playbook'),'“One niche - 100 true fans - One massive problem - One systematized solution”','X 上同样的格言体','—'],
 ['2022-01（自述）','开 newsletter','“So, in January of 2022, I launched this newsletter”','邮箱资产','—'],
 ['2024-01-16（自述）','The Creator MBA','“it sold $1.6M in six days”','旗舰课','自述'],
 ['2025-06-07',a('https://justinwelsh.me/essays/my-10m-journey','发表 $10M 回顾文'),'“My complete $10M journey (all 23 steps)”','把以上历史整理成 23 步','发表时间与文中事件时间分开'],
 ['2026-11',JW('2119075112519405945','X：免费指南导流'),'“How I built my little one-person business to $15M in profit”','导流帖反复发','$15M 是本人说法，和 $10M 文口径不同（利润 vs 营收、时点不同），不合并']],
inflect=[
 ['早期','LinkedIn 日更','高管 → 内容作者','用老本行的经验找到声音'],
 ['2020-04','$50 小课','咨询 → 数字产品','DM 里的问题告诉他该卖什么（本人说法）'],
 ['2024-01','Creator MBA','小课 → 旗舰课','本人说用了“18-week, personalized launch plan”']],
works=[
 dict(t='23 步复盘长文',link=a('https://justinwelsh.me/essays/my-10m-journey','$10M journey'),where='2025-06-07 发表',f='全文已读：标题为 23 步复盘，含 18 周发布计划等节点。',o='按编号步骤分段叙述。',h='结构整齐便于截图转发；未验证。',b='全部数字自述。',k='复盘写成编号步骤。'),
 dict(t='一句话格言',link=JW('2118328001708388635','X：职业建议')+' · '+JW('2119084224040812927','X：做 vs 卖'),where='2026-11',f='全文已读：“most career advice is just people defending a path they already took.”',o='一句反常识，两行对仗。',h='回复里很多人补充自己的经历，说明容易引起共鸣；只读 20 条。',b='同一句会重复发（'+JW('2118721869381591085','11-06')+'、'+JW('2119084224040812927','11-07')+'）。',k='把一个观点压成一句对仗。'),
 dict(t='固定导流帖',link=JW('2118742791295566103','X：Saturday Essay'),where='2026-11',f='本轮样本中，格言帖之间穿插周刊或免费指南链接帖。',o='格言与固定导流帖交替出现。',h='可能用于承接关注；实际转化未知。',b='转化效果未知。',k='在常发的内容旁放一个固定入口。')],
aud=[
 ['想离开公司、做一人生意的上班族','可以照做的路径','卡 1',S+'他建议“Build it to 60% or 70% of your salary”再全职','读者现在：未知<br>内容指向：经营方法，层级不适用'],
 ['已经在做内容的创作者','怎么变现','Creator MBA、周刊',S+'课程面向“creative entrepreneurs”','读者现在：未知<br>内容指向：不适用'],
 ['被职场消耗的人','共鸣和许可','卡 2',C+'“A lot of advice is just someone\'s personal experience dressed up as a universal rule.”','读者现在：未知<br>内容指向：不适用']],
why=[A+'本轮样本里格言帖与导流帖交替出现。',S+'“100% organic social posting… I never ran any paid ads”。',C+'回复多是认同和补充自身经历，也有调侃。'+B+'只读 20 条。'],
cmp_src='本轮 25 条原创几乎都是格言或导流，没有找到明显的普通生活帖；对照改用导流帖本身：'+JW('2117919870801113304','周刊导流')+'。',
cmp=[['开头','一句反常识','“If you enjoyed this…”'],['读者拿走什么','一个观点','一个链接'],['形式','一到两句','固定模板']],
voice=[F+'句式固定：“The older I get…”、“If you can… you\'ll…”。',F+'同一句话会隔天再发。',A+'节奏：25 条原创覆盖 2026-11-02～11-08，一天三四条。'],
goods=['<b>'+a('https://justinwelsh.me/essays/my-10m-journey','My complete $10M journey')+'</b>。','<b>The Saturday Essay</b> 周刊。','<b>The LinkedIn Operating System / Creator MBA</b>（本人说法）。'],
take=['内容主题和产品主题一致。','先副业做到工资的六七成再全职（他的建议）。','复盘写成编号步骤。'],
skip=['一天三四条格言的发帖量。','重复发同一句话的做法，在中文平台可能被认为水。','英文 LinkedIn 起家的环境。'],
limits=['<b>数字</b>：$10M、$1.6M、$15M 等都是本人说法，口径不同不合并；旧版 LinkedIn 2024/2025 年终帖本轮没重读，已删除。','<b>平台</b>：LinkedIn、周刊、课程没读；小红书未核。','<b>评论</b>：只读 1 帖 20 条。'],
cov=[['X','资料（API）+ 2026-11-02～08 原创 25 条 + 2021-12 帖 4 条 + 2026-10 搜索 1 条','2019–2021 早期 LinkedIn 内容'],['网站','$10M 文全文','周刊其他期；课程'],['评论','1 帖 20 条','其他'],['小红书','无','未核']]))

src,out=sys.argv[1],sys.argv[2]
t=open(src).read()
for p in P:
    k=p['id']
    m=re.search(r'<h2 id="%s">.*?(?=<h2 id=")'%k,t,re.S); assert m,k
    t=t[:m.start()]+section(p)+'\n'+t[m.end():]
css='.tw{overflow-x:auto;max-width:100%}.tw table{min-width:40rem}'
if css not in t: t=t.replace('</style>',css+'\n</style>',1)
t=t.replace('<li>X：本回合只读 <code>get_users_by_usernames</code> + <code>public_metrics</code>（2026-10-31）。Justin Welsh 粉丝以 X 现读为准（表内若缺则深描不写死）。</li>','<li>X：本回合只读 <code>get_users_by_usernames</code> + <code>public_metrics</code>（2026-10-31）。海外六人深描已于 2026-11-08 用 X 原帖和本人网站重写，关注者数为 2026-11-08 读数。</li>')
for old,new in [('<li>Lenny：<a href="https://www.lennysnewsletter.com/p/1000000">1M 文</a>；<a href="https://www.cnbc.com/make-it/2024/01/11/lenny-rachitsky-podcast-brings-in-more-than-500k-a-year-heres-how.html">CNBC</a>；Growth In Reverse 旧复盘（待核现况）。</li>','<li>Lenny：<a href="https://www.lennysnewsletter.com/p/1000000">1M 文</a>；X 原帖。</li>'),
 ('<li>Shreyas：LinkedIn 履历；Maven；LNO Thread Reader。</li>','<li>Shreyas：X 原帖；Maven 讲师页。</li>'),
 ('<li>Ali：aliabdaal.com LifeNotes；LinkedIn Jan 财务；Publish Press / Passionfroot 访谈。</li>','<li>Ali：aliabdaal.com About 与 LifeNotes；X 原帖。</li>'),
 ('<li>swyx：swyx.io；latent.space；Changelog Friends 转录；Sidestack 目录。</li>','<li>swyx：swyx.io；latent.space；X 原帖。</li>'),
 ('<li>levelsio：levels.io 博文（$52k/月、Photo AI）；open 页历史；MAKE。</li>','<li>levelsio：levels.io（12 startups、Photo AI、归档标题）；X 原帖。</li>'),
 ('<li>Justin Welsh：justinwelsh.me $10M 文；LinkedIn 2024/2025 年终帖。</li>','<li>Justin Welsh：justinwelsh.me $10M 文；X 原帖。</li>')]:
    assert old in t,old; t=t.replace(old,new)
open(out,'w').write(t); print('ok',len(t))
