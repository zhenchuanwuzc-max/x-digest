"""生成 xhs/hector.html（Hector Serrano 成长深拆；播客全文对照仍在 xhs/growth/hector.html）。证据见 hector-ledger.md。"""
from creator_page_lib import *
X=lambda i,t: a(f"https://x.com/hectorserrranoo/status/{i}",t)
L=lambda i,t: a(f"https://x.com/lennysan/status/{i}",t)
TR='<a href="growth/hector.html">播客全文对照（站内）</a>'
c=dict(slug="hector",name="Hector Serrano（@hectorserrranoo）",short="Hector",
stage_nav=["足球与业余内容","加入 Wispr Flow","一个人做所有广告","付费 UGC 体系","公司频道与个人号"],
overview=[("平台与身份",'X：'+a("https://x.com/hectorserrranoo","@hectorserrranoo")+'，2024-01 建号，2026-11-08 API 读到 20,377 关注者，简介 “marketing hire #2 @wisprflow”。<b>身份已核</b>：Lenny 官方帖写 “Hector Serrano (@hectorserrranoo)… joined @WisprFlow at 19”（'+L("2116927042759635132","Lenny 帖")+'），本人引用该节目（'+X("2116933059945873449","本人帖")+'），三方一致。小红书未核。'),
 ("定位",A+'他首先是公司内容负责人，不是独立博主：本轮主要核到“替公司做内容 → 搭创作者体系”；个人号增长原因未知。'+S+'“i do paid ads and founder led content not ai ugc/organic ugc”（'+X("2118423005818958154","X")+'）。')],
stages=[
 stage("s1","阶段 1 · 19 岁前：足球和业余内容","职业足球和家庭压力之间怎么选。",[
  row(1,ts("2104378428317204605"),X("2104378428317204605","X：放弃足球的经过"),"帖子全文已读","“at 19 the weight of my whole family landed on me”；“somehow the content i had been making on the side led me to joining wispr in 2024, pre product”","业余做内容是后来入行的门票","家庭经历是本人叙述")]),
 stage("s2","阶段 2 · 2024：退出一级联赛，海投进 Wispr","没有经验，怎么进一家创业公司。",[
  row(2,"2026-11-01（播客发布）","节目里回忆入职 → "+TR,"全文对照页已有（Ocean 提供的文字稿，音频未核）","“I had just quit Division I soccer three days before…I applied to 200 positions. I found some company called Wispr Flow.”","—","职位和日期以本人口述为准")]),
 stage("s3","阶段 3 · 约一年半：自己做所有广告","产品早期，广告谁来做。",[
  row(3,"2026-11-01（播客）","一个人做广告 → "+TR,"全文对照页已有","“I was the one making every single ad for a year and a half, so I made hundreds and hundreds…of ads”","大量亲手做的经验，后来变成给创作者的指导","—"),
  row(4,"2026-11-01（播客）","先试自然 UGC → "+TR,"全文对照页已有","“two and a half months, it was like 500 million views…they didn't necessarily lead to a lot of conversions”","播放量高不等于转化，是他转向付费 UGC 的原因","播放量为口述")]),
 stage("s4","阶段 4 · 付费 UGC：从一个人到一群创作者","怎么把自己会做的事交给很多创作者。",[
  row(5,"2026-11-01（播客）","Smart retainer 保底补差 → "+TR,"全文对照页已有","“we're going to do 25 videos and we're going to pay you $1,500. As long as you hit that quota…”","用保底降低创作者门槛","具体金额是举例"),
  row(6,ts("2116933059945873449"),X("2116933059945873449","X：引用节目"),"帖子全文已读；回复 18 条","“2 years ago i was making every single ad myself / now we have an army of creators”","一句话前后对比，是他的个人叙事主线","—")]),
 stage("s5","阶段 5 · 2026：公司 YouTube 频道和个人号","内容除了卖产品，还能干什么。",[
  row(7,ts("2105128803291046107"),X("2105128803291046107","X：创始人品牌"),"帖子全文已读","“the hardest part of building a founder led brand is getting the founder bought in”；公司 YouTube “14k subs on yt in 1 month”","—","订阅数是本人说法"),
  row(8,ts("2105126617043681676"),X("2105126617043681676","X：内容吸引人才"),"帖子全文已读","“a lot of our new hires at wispr have brought up our yt channel”","内容也用来招人","—"),
  row(9,ts("2117351027930542178"),X("2117351027930542178","X：招 YouTube 主持人"),"帖子全文已读","“hiring a youtube host…build one of the best youtube channels in the world with me”","节目播出后在扩内容团队","—")])],
works=[
 dict(id="w1",t="个人故事长帖：放弃足球",links=[X("2104378428317204605","X：放弃足球")],where=("s1","阶段 1"),
  f="帖子全文已读。父亲被裁、自己 19 岁退役、业余内容带他进 Wispr，结尾 “most people never suffer and that's why they'll never build anything beautiful”。",
  o="全小写、短句分段，情绪浓；把职业选择讲成家庭故事。",h="个人苦难叙事容易让年轻读者代入；没有数据。",b="家庭细节无法核实；回复没读。",k="讲转行时，讲清当时逼你做决定的那件事。"),
 dict(id="w2",t="一句话前后对比",links=[X("2116933059945873449","X：2 years ago")],where=("s4","阶段 4 · 节点 6"),
  f="帖子全文已读，只有两行加节目链接。",o="“以前我自己做 → 现在一支队伍”，一句讲完成长。",
  h="回复里多人围绕“自己做 → 交给团队”这一跳发问；但只读 18 条。",b="回复 18 条，其中有 Lenny 自己的回复。",k="用一句“以前/现在”概括你的变化。"),
 dict(id="w3",t="播客：把方法一次讲透",links=[TR,L("2117277733273366891","Lenny 的要点帖")],where=("s3","阶段 3–4"),
  f="全文对照页：从自然 UGC 转付费 UGC、smart retainer、招人、营销人“对 AI 过敏”等章节。",
  s="“There's no better way to learn as a creator than just turning on the camera and posting.”",
  o="大量具体数字和操作，但都是口述。",h="大号主持人的平台把他从公司员工推到行业视野；推断。",b="音频没逐句核；公司数据未审计。",k="对外讲方法时给具体机制（谁、做多少、付多少）。"),
 dict(id="w4",t="短观点：观众为什么看",links=[X("2118162134647570494","X：selfish reasons"),X("2105386008850448418","X：value + trust + entertain")],where=("s5","阶段 5"),
  f="两帖全文已读：“people only watch content for selfish reasons… stop making it about yourself”；“give value + build trust + entertain = a channel people actually watch”。",
  o="公式化、一两行。",h="适合被截图转发；没有数据。",b="回复没读。",k="把你的方法压成一个公式。"),
 dict(id="w5",t="招聘帖：内容团队怎么搭",links=[X("2117351027930542178","X：招主持人"),X("2118120968396906559","X：内容形式说明")],where=("s5","阶段 5 · 节点 9"),
  f="两帖全文已读：列出主持人条件，补充说明 “content will be challenges and behind the scenes content not a podcast”。",
  o="招聘帖本身也在说明频道定位。",h="借节目热度招人；推断。",b="—",k="用招聘帖顺便讲清你要做什么内容。")],
aud=[
 ("做增长和营销的从业者（B2B SaaS 为主）","可照搬的付费 UGC 机制","保底补差、素材组合等做法",'<a href="#w3">卡 3</a>',C+"“Running so ugc myself for 3 years but was mostly in my own bubble”；“yo you do any consulting?”","读者现在：未知<br>内容指向：营销方法，AI 使用层级不适用"),
 ("对他早期职业经历感兴趣的人","19 岁入行的经过","个人故事",'<a href="#w1">卡 1</a>',C+"“Wish I had your hustle at 19.”","读者现在：未知<br>内容指向：职业故事，层级不适用"),
 ("做短视频的创作者","观众心理和内容公式","短观点",'<a href="#w4">卡 4</a>',A+"短观点帖面向创作者","读者现在：未知<br>内容指向：内容方法，层级不适用"),
 ("想找工作机会的创作者","加入他的团队","招聘信息",'<a href="#w5">卡 5</a>',A+"招聘帖要求直接回复或私信","读者现在：未知<br>内容指向：不适用")],
why=[S+"“2 years ago i was making every single ad myself”（<a href=\"#w2\">卡 2</a>）。"+A+"他以自述的大量广告制作经历支撑方法介绍；是否因此获得信任未验证。",
 A+"Lenny 节目和官方要点帖让他的方法被大量转述（本轮搜到多条第三方总结）。"+B+"个人号增长原因未知。",
 S+"他说观众只为自己看内容（<a href=\"#w4\">卡 4</a>）。"+A+"他的帖子也几乎都在给读者东西：方法、机会、故事。",
 C+"节目帖回复多为称赞、要咨询、问怎么选创作者。"+B+"只读 18 条。"],
cmp=[("开头","前后对比或一个公式（<a href=\"#w2\">卡 2</a>、<a href=\"#w4\">卡 4</a>）","@某人的一句回复"),
 ("个人经历","家庭、足球、做广告的经历","喝水改善皮肤"),
 ("读者能拿走什么","机制、公式、工作机会","一句玩笑"),
 ("形式","全小写短句，分行","全小写短回复")],
cmp_note="普通内容一列来自同期 X 帖原文："+X("2118193953866731873","喝水和皮肤")+" · "+X("2118131021644431735","回复玩笑")+" · "+X("2118416311261053255","一句回复")+"（2026-11-05～11-06，全文已读）。",
voice=[F+"几乎全用小写、短句、分行，口语化（“bro”“goat”）。",
 F+"大量回复别人，原创帖少；本轮 25 条里多数是回复。",
 A+"观点帖压成一两行公式。",
 A+"个人故事帖情绪很重，和方法帖反差大。"],
tpl="【一句】以前我怎么做 → 现在怎么做\n【公式】A + B + C = 结果\n【故事】一件逼我做决定的事\n【邀请】我在招人 / 回复我",
limits=["<b>身份</b>：已用主持人标注、本人简介和本人引用三方核对；仍只代表 X 账号对应关系。",
 "<b>他不是独立博主</b>：本轮主要核到公司内容工作和节目相关帖子；个人号增长原因未知，没有增长曲线数据。",
 "<b>数据</b>：营收倍数、播放、订阅、创作者收入都是口述或第三方转述，没审计；第三方总结帖不当证据。",
 "<b>原文</b>：播客音频没逐句核，以全文对照页为准。","<b>评论</b>：只读 18 条回复。"],
take=["用“以前自己做 → 现在交给团队”讲一次自己的工作变化。","把方法压成一句公式。","讲方法时写清具体机制。","Ocean 作为大厂 PM，可以像他一样讲“替公司做事”的过程，而不只讲个人。"],
skip=["靠一档头部播客带来的曝光。","全小写、大量互动回复的英文 X 风格。","付费广告预算和创作者团队。"],
cov=[("X","资料（API）+ 2026-11-02～11-06 帖 25 条 + 2026-09～10 帖 18 条 + Lenny 标注帖","2024–2026-08 的帖子"),
 ("小红书","无","未核；不标双发"),
 ("评论","节目引用帖回复 18 条（API 返回范围）","其他帖评论；YouTube 评论"),
 ("作品原文","播客全文对照（站内）；X 帖全文","Wispr Flow YouTube 频道视频；他做的广告本身")],
status="X 本人帖和播客全文已补一手资料；身份已核。小红书未核：不据此判断效果，也不标双发。",
src_extra=["身份核对记录：/workspace/creator-growth-20261108/hector/identity.md（仓库外）。"],
todo="2024–2025 的个人帖；Wispr Flow YouTube 频道；他做的广告样本；个人号关注者增长时间点。")
render(c)
