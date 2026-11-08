import html, re
src=open('/workspace/xhs-ui-20261108/src-backup/zhangzala.before.html').read().split('\n')
L=lambda a,b:'\n'.join(src[a-1:b])
head='\n'.join(src[:83]).replace('<title>张咋啦成长深拆 · 起号复盘 + 爆款逐拆 · 给 Ocean</title>','<title>张咋啦成长深拆 · 五阶段时间线 + 证据分层 · 给 Ocean</title>')
extra_css='''<style>
.stage{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:1rem 1.15rem;margin:0 0 1.2rem;box-shadow:var(--shadow)}
.stage h3{margin:.1rem 0 .3rem}.stage .q{margin:.2rem 0 .7rem;color:var(--ink-2)}
.tw{overflow-x:auto;max-width:100%}
.tw table{width:100%;border-collapse:collapse;font-size:.88rem;min-width:44rem}
.tw th,.tw td{border-top:1px solid var(--line);padding:.45rem .5rem;vertical-align:top;text-align:left}
.tw th{font-size:.74rem;color:var(--mut);font-weight:650;background:var(--hi-soft)}
.lv{display:inline-block;font-size:.7rem;font-weight:650;padding:.05rem .4rem;border-radius:999px;border:1px solid var(--line);margin-right:.25rem}
.lv.f{background:#e8f3ec}.lv.s{background:var(--hi-soft)}.lv.a{background:#eef0f4}.lv.b{background:#fbe9e7}
details.arch>summary{cursor:pointer;font-weight:700;padding:.6rem 0}
@media(max-width:900px) and (min-width:701px){.tw table{min-width:36rem}}
@media(max-width:700px){
.stage .tw{overflow:visible}
.stage .tw table,.stage .tw tbody,.stage .tw tr,.stage .tw td{display:block;width:100%;min-width:0}
.stage .tw thead{display:none}
.stage .tw tr{border:1px solid var(--line);border-radius:12px;padding:.55rem .7rem;margin:0 0 .7rem;background:#fff}
.stage .tw td{border:0;padding:.22rem 0;overflow-wrap:anywhere}
.stage .tw td::before{content:attr(data-l);display:block;font-size:.7rem;font-weight:650;color:var(--mut)}
.stage .tw td[data-l="#"]{font-weight:700}
}
</style>
</head>'''
head=head.replace('</head>',extra_css,1) if '</head>' in head else head
A=lambda u,t:f'<a href="{html.escape(u,True)}" target="_blank" rel="noopener">{t}</a>'
XU='https://x.com/zarazhangrui/status/'
def row(n,date,act,fact,said,ana,edge):
    c=lambda s:s or '—'
    return (f'<tr><td data-l="#">{n}</td><td data-l="日期">{date}</td><td data-l="动作与作品">{act}</td>'
            f'<td data-l="事实">{c(fact)}</td><td data-l="自述">{c(said)}</td><td data-l="分析">{c(ana)}</td><td data-l="边界">{c(edge)}</td></tr>')
TH='<div class="tw"><table><thead><tr><th>#</th><th>日期（UTC+8）</th><th>当时动作 → 作品</th><th><span class="lv f">事实</span>可直接核到</th><th><span class="lv s">自述</span>本人说法</th><th><span class="lv a">分析</span>研究者推断</th><th><span class="lv b">边界</span></th></tr></thead><tbody>'
def stage(id_,title,q,rows,after=''):
    return f'<section id="{id_}" class="stage"><h3>{title}</h3><p class="q"><b>当时的问题：</b>{q}</p>{TH}{"".join(rows)}</tbody></table></div>{after}</section>'
XHS5='https://www.xiaohongshu.com/explore/68ccbc56000000000e022358?xsec_token=ABUcpaYJnXAnMYht_N_HshQcD3ZgE-cUBYTX9jI9X7_Xw=&xsec_source=pc_user'
XHSB='https://www.xiaohongshu.com/explore/6a1018060000000007027155?xsec_token=AB-QSO3EIltr0KEwJqPLsYnuD1Ptzjx8K3plXk1eA5-dA=&xsec_source=pc_user'
XHSG='https://www.xiaohongshu.com/explore/6a2761520000000008032277?xsec_token=ABV4nTHPpFrx7LlpI92U9NtGNxdKD1Xd8K5PORPmqpf5E=&xsec_source=pc_user'
XHSX='https://www.xiaohongshu.com/explore/6a31edc300000000200387f4?xsec_token=ABQSKYmEqpZfsugCKX7VlrlMwEK09rjxlMv-UP-lMOuLs=&xsec_source=pc_user'
XHSC='https://www.xiaohongshu.com/explore/6a66b57e000000001302c44a?xsec_token=AB6Ae3oL5kee0o1xqGiecxfmnOwkze_DGliK3UyCdDwdI=&xsec_source=pc_user'
HX='https://www.huxiu.com/article/4824449.html'
FS='https://www.feishu.cn/content/article/7647408304896953549'
s1=stage('s1','阶段 1 · 2017 长期写作底子','毕业、刚入行，怎么把学到的东西说清楚。',[
 row(1,'2017-05-27','个人博客复盘大学四年 → '+A('https://zarazhang.wordpress.com/2017/05/27/so-what-did-i-learn-at-harvard/','So What Did I Learn at Harvard?'),'发文日 2017-05-27','“biggest takeaway from four years at Harvard”','AI 热潮前已有长期表达习惯','只读到索引摘要，未读全文；不推算早期受众'),
 row(2,'2017-11-27','把朋友的重复问题整理成资源帖 → '+A('https://zarazhang.wordpress.com/2017/11/27/resources-for-those-interested-in-vc/','Resources for those interested in VC'),'发文日 2017-11-27','“I’m obviously still new to the field”','新手也能输出：先讲清边界再给资源','发文日不等于入职日')],
 '<p class="muted">反馈与下一步：本批没有这一阶段的读者反馈证据，标未知。</p>')
s2=stage('s2','阶段 2 · 2019–2023 职业选择','留在观察行业，还是去做实操；要不要创业。',[
 row(3,'<b>2019-05（月份推定）</b>','GGV 转字节，2020-01-09 公开复盘 → '+A('https://zarazhang.wordpress.com/2020/01/09/why-i-joined-bytedance/','Why I joined ByteDance'),'文章日期 2020-01-09','文中写“this May”、已入职 7 个月','双语跨文化与长期主题相连','2019-05 由文中推定，不是精确入职日'),
 row(4,'2023-08-18','公开反思创业门槛 → '+A('https://zarazhang.wordpress.com/2023/08/18/why-i-dont-want-to-be-a-founder/','Why I don’t want to be a founder'),'发文日 2023-08-18','“Instead of entrepreneurship, think apprenticeship.”','做作品不等于融资创业，不写成裸辞神话','2023 年观点，不代表现在立场')],
 '<p class="muted">下一次变化：本批证据未说明她何时开始小红书，开始时间标未知。</p>')
s3=stage('s3','阶段 3 · 小红书持续更新与读者反馈（截至 2025-09-18 回顾，起点未知）','业余时间做内容，靠什么持续更新。',[
 row('5a','<b>2025-09-18</b>（编辑日）',A(XHS5,'《2年400篇笔记，12万粉丝：做小红书的一些感想》'),'页面显示编辑于 2025-09-18；标题文字如上','“这是我的第415篇帖子”；两年平均约 1.7 天一篇；内容是业余爱好，动力来自正反馈；不接广告/推广；“谦虚的学生、learn in public”','持续更新靠读者反馈，不靠粉丝 KPI','标题里的“12万粉丝”是当时自述，不是审计值；“2年”的起点日期未知'),
 row('5b','2025-09-18','同帖：读者行动反馈','—','作者自述：每天至少 3 位粉丝发帖 @ 她，说看内容后采取了行动（做出第一个 vibe-code 产品、看完 Karpathy 大模型教程、开始 learn in public、录第一个分享视频）','“内容 → 读者行动 → 作者继续写”的反馈链','作者口述的频次，无法独立核实'),
 row('5c','2025-09-18','同帖评论区','评论与作者回复在页面可见','<b>评论者自述（不是作者）</b>：“狗牯仔的人间喜剧”看完大模型视频，用 Cursor 和 Trea 尝试做小程序；“芒果.beta”受启发做出第一个视频。作者回复“用技术把想法变成现实的感觉特别好”“赞～”','读者把内容变成了自己的第一个作品','评论者说法只代表评论者；快照中未见“置顶”标记'),
 row(6,'日期未知（采访回顾）','起号约定：唯一目标是“连续日更半年”，定位“非技术视角学 AI” → '+A(HX,'虎嗅采访'),'—','“连续日更半年”；当场把“每天 1.5 篇”更正为“约 1.5 天一篇”','先定过程目标，再看题材反馈','虎嗅正文抓取超时，只读到搜索索引摘录；“近 500 篇”“约 2 万→18 万”都是索引摘录里的口述，不作硬事实；三者窗口不同，不合并成“半年 500 篇”')],
 '<p class="muted">两个口径并存：“约 1.5 天一篇”（采访口述）与“约 1.7 天一篇”（2025-09-18 原帖）来自不同时间点，本页不合并、不换算。</p>')
s4=stage('s4','阶段 4 · 2025 从看 AI 到动手','只看不做，学不进去；怎么筛选输入。',[
 row(7,'2025 全年（年底回顾）','先做再带问题学；转岗产品，发业余产品 LongCut → '+A(HX,'虎嗅'),'—','“2025对我来说是行动的一年”','输入 → 实践 → 带问题再输入','只读到搜索摘录；LongCut 首发日期与用户反馈未知'),
 row(8,'2025-05-07 16:21','X 公开学习方法 → '+A(XU+'1920031101239607353','原帖'),'帖子存在','“Discover widely / Use deeply / Follow the builders / Watch their interviews”','—','正文可能被 API 截断'),
 row(9,'2025-05-14 08:47','记录写 AI 数月后的订阅进展 → '+A(XU+'1922453757465338210','原帖'),'帖子存在','Substack 达到 1k 订阅','—','发帖时自述，不是当前值'),
 row(10,'2025-05-21 09:43','输入筛选标准 → '+A(XU+'1925004608830898247','原帖'),'帖子存在','“follow builders, not influencers”','—','正文可能截断'),
 row(11,'2025-05-21 22:51','把自己的标签页过载写成产品请求 → '+A(XU+'1925202887107662256','原帖'),'帖子存在','想要能把浏览器标签页整理成待办的 agent','从自己的高频摩擦出发','这是请求，不是她做出的产品')])
s5=stage('s5','阶段 5 · 2026 作品、分发与维护','做出来之后，怎么让人用、怎么撑住维护。',[
 row(12,'2026-05-18 06:00','反思“做出来”和“获得注意力”的差距 → '+A(XU+'2056132881630826952','原帖'),'帖子存在','低估了赢得注意力的难度','—','—'),
 row(13,'2026-05-19 08:08','公开贴 Claude Code 报错求解 → '+A(XU+'2056527354772722127','原帖'),'帖子存在','“socket connection closed” 报错，问是否只有她遇到','公开失败也是内容','—'),
 row(14,'05-22（年份未知）','小红书 '+A(XHSB,'《把Claude Code接入飞书，太爽了！教程+演示》'),'页面可见日期 05-22；正文：“用这个开源项目，可以把Claude Code无缝接入飞书…手机上也可以！”','—','—','正文没有项目名或仓库名；视频未播放、评论未载入，不写视频步骤；与下面的 GitHub 仓库是否同一项目未知'),
 row(15,'2026-05-27 02:20','Frontend Slides 接入自有 HTML 模板库 → '+A(XU+'2059338915023393161','原帖'),'帖子存在','当时 19k stars','—','stars 是发帖时自述，不是当前值'),
 row(16,'2026-06-04（官方整理页日期）','飞书官方整理她的桥接实践 → '+A(FS,'飞书文章'),'文中写“飞书同学 Zara（小红书博主‘张咋啦’）的实践分享”','—','可复制的是协作闭环，不是一段终端命令','页面日期不等于功能首次上线；X 首发帖未找到'),
 row('16b','06-16 编辑 / 06-17 编辑 / 07-27 页面显示日期（年份均未知）','小红书 '+A(XHSX,'《如何一年在Twitter涨粉7万》')+' · '+A(XHSG,'《我在GitHub上有超过3万星（虽然并不会写代码》')+' · '+A(XHSC,'《用coding agent辅助内容创作的几个实践》'),'页面可见标题与日期','涨粉帖正文自述“视频的动画和剪辑都是 Claude Code 做的”；GitHub 帖正文“AI时代我们应该做有观点的产品”','—','标题里的数字是自述；视频未播放、评论未载入；与桥接项目关系未知；07-27 帖无可读正文'),
 row(17,'2026-10-20 21:04','受众用于验证 idea、找早期用户 → '+A(XU+'2112530473994072225','原帖'),'帖子存在','Signals > distribution','—','点赞不等于留存或付费'),
 row(18,'2026-10-22 14:02','“Your personal website is the new resume” → '+A(XU+'2113148949842534482','原帖'),'帖子存在','—','—','—'),
 row(19,'2026-10-25 15:19','主张每天露出的系统，而非一次昂贵发布 → '+A(XU+'2114255477907570865','原帖'),'帖子存在','—','—','是评论别人访谈时的观点'),
 row(20,'2026-11-05 07:18','公开问社区群聊工具 → '+A(XU+'2118120795780370768','原帖'),'帖子存在','Discord / WhatsApp / iMessage / Slack 各有摩擦','社区运营仍是未解问题','—')])
limits='''<section id="limits"><h2>失败、权限与维护边界（桥接项目）</h2><div class="card"><ul>
<li><b>名称不统一，关系未知</b>：研究文按飞书官方教程称 <code>zarazhangrui/lark-coding-agent-bridge</code>；采集的 README（<code>research/zhangzhala-growth-2026-11-08-evidence/bridge-readme.md</code>）标题是 <code>lark-channel-bridge</code>；旧名 feishu-claude-code-bridge 是否重定向未证实；小红书 05-22 帖没写项目名。本页保留各来源的称呼，不断定是改名。</li>
<li><b>权限</b>：当前 README 新配置默认 <code>full</code>（Claude <code>bypassPermissions</code>、Codex <code>danger-full-access</code>）；工作目录不是文件系统沙箱。同一 README 列出可收紧为 <code>workspace</code> 或 <code>read-only</code>；照搬前要按所用版本核对后收紧。</li>
<li><b>触发面</b>：聊天默认仅 owner；开放群后群成员可触发；能在文档评论里 @ 机器人的人也能触发，需要审计。</li>
<li><b>运行</b>：本机须在线、CLI 登录有效；官方示例建议 Mac 不休眠。</li>
<li><b>安装</b>：官方旧教程给的是一行 <code>npx</code>；当前 README 要求后台服务先全局安装再 start，因为 npx 临时缓存被清理后服务会坏。旧教程不能当永久部署方案。</li>
<li><b>维护</b>：README 记有旧版图片去重 bug；无响应 watchdog（README：agent 连续 N 分钟无输出即终止）默认关闭。不是零故障产品。</li>
</ul></div></section>'''
borrow='''<section id="for-ocean"><h2>给 Ocean（「AI具身牛马」）的借鉴</h2><p class="muted"><span class="lv a">分析</span>以下是研究者建议，不是成功公式；没有收入或涨粉承诺。</p><div class="grid2">
<div class="card"><h3>可借鉴</h3><ol>
<li>定过程目标（连续发满 N 期），代替粉丝 KPI。</li>
<li>每帖给一件能拿走的东西，并写清一个限制。</li>
<li>从自己的一条高频摩擦做起（例：钉钉 → Codex），录前后对比，附仓库、教程、故障入口。</li>
<li>把读者的“我做了第一个 X”当作反馈信号，高频问题变下一篇。</li>
<li>把“丝滑”拆成可验收场景：状态回执、一群一项目、可停止/排队、断线恢复。（未在钉钉实测）</li></ol></div>
<div class="card"><h3>不适用</h3><ul>
<li>她的产能（两年约 415 篇）是长期积累，不是可复制的起号速度。</li>
<li>哈佛、双语、公司渠道、海外人脉照搬不了。</li>
<li>飞书 API 换成钉钉不会自动同样好用。</li>
<li>点赞高不等于方法有效：旧爆款表只有标题与点赞，没有同曝光对照，不作因果。</li></ul></div></div></section>'''
gaps='''<section id="sources"><h2>来源与待核</h2><ul class="plain">
<li>研究文件：<code>research/zhangzhala-growth-2026-11-08.md/.json</code>、<code>research/zhangzala-xhs-20261108.md</code>（2026-11-08 采集，UTC+8）。</li>
<li>主页：'''+A('https://www.xiaohongshu.com/user/profile/59757acd50c4b45e6e9a90df?channel_type=web_note_detail_r10&parent_page_channel_type=web_profile_board&xsec_token=ABYrQlTr-QxtSHq2UD_FtC65qbj6rmyfaMwp-ID99k6FA=&xsec_source=pc_user','小红书主页（2026-11-08）')+' · '+A('https://www.xiaohongshu.com/user/profile/59757acd50c4b45e6e9a90df?xsec_token=ABhSjy7kfB8CQrcwVQ8ISLTADnVqGJt8LPmx3IG6C6tFw%3D&xsec_source=pc_search','小红书主页（2026-11-01 链接）')+' · '+A('https://x.com/zarazhangrui','X @zarazhangrui')+' · '+A('https://zarazhang.com/about/','zarazhang.com/about')+'</li><li>采访与复盘：'+A(HX,'虎嗅 4824449')+' · '+A('https://www.xiaoyuzhoufm.com/episode/695af1289b7892496e9811cb','小宇宙')+' · '+A('https://www.woshipm.com/share/6230525.html','人人都是产品经理复盘')+' · '+A(XU+'2079395028485488707','X 80k 帖')+'''</li></ul>
<p><span class="tag warn">待核</span>：小红书 5 篇视频均未播放；前 4 篇评论未载入，第 5 篇（2025-09-18）已读到正文和部分评论、未见置顶标记；05-22、06-16、06-17、07-27 的年份；虎嗅正文全文；LongCut 首发与反馈；桥接 X 首发帖；早期职业起止日期；桥接项目名称关系；小红书开始时间。</p></section>'''
overview=f'''<section id="overview"><h2>账号概况（快照，不是增长史）</h2><div class="grid2">
<div class="card stat"><span class="tag">小红书</span><strong>主页</strong><p style="margin:.35rem 0 0">旧版主页计数（粉丝、获赞与收藏、笔记数等）：旧采集数据未复核，暂不展示。</p><p class="sub">'''+A('https://www.xiaohongshu.com/user/profile/59757acd50c4b45e6e9a90df?xsec_token=ABhSjy7kfB8CQrcwVQ8ISLTADnVqGJt8LPmx3IG6C6tFw%3D&xsec_source=pc_search','打开主页')+'''</p></div>
<div class="card stat"><span class="tag">X</span><strong>@zarazhangrui</strong><p style="margin:.35rem 0 0">旧版粉丝读数与帖子采样：旧采集数据未复核，暂不展示。</p><p class="sub">'''+A('https://x.com/zarazhangrui','打开 X')+'''</p></div>
<div class="card stat"><span class="tag">产出 · 作者原帖自述</span><strong>第 415 篇 · 约 1.7 天一篇</strong><p class="muted" style="margin:.4rem 0 0">2025-09-18 '''+A(XHS5,'《2年400篇笔记，12万粉丝》')+'''，两年平均；起点日期未知。</p></div>
<div class="card stat"><span class="tag">定位 · 作者自述</span><strong>learn in public · 谦虚的学生</strong><p class="muted" style="margin:.4rem 0 0">“不制造焦虑…不包装自己”；称不接广告/推广（2025-09-18 原帖）</p></div>
</div><p class="muted">快照数字只代表采集当天；不同时期的粉丝数不连成增长曲线。</p></section>'''
nav='''<aside class="nav" aria-label="目录">
  <p class="brand">张咋啦深拆</p>
  <p class="meta">私密 · 写给 Ocean<br>采集 2026-11-01 · 重写 2026-11-08（UTC+8）<br>事实 / 自述 / 分析分栏 · 未知不凑</p>
  <a href="growth/">← 人物成长研究</a>
  <div class="sec">本页</div>
  <a href="#overview">账号概况</a>
  <a href="#timeline">五阶段时间线</a>
  <a href="#s1">1 · 2017 写作底子</a>
  <a href="#s2">2 · 职业选择</a>
  <a href="#s3">3 · 小红书与反馈</a>
  <a href="#s4">4 · 2025 动手</a>
  <a href="#s5">5 · 2026 作品与维护</a>
  <a href="#limits">失败与边界</a>
  <a href="#for-ocean">给 Ocean</a>
  <a href="#sources">来源与待核</a>
  <a href="#archive">旧版留档</a>
</aside>
<main class="main">
<nav class="mob-nav" aria-label="移动目录">
  <a href="growth/">← 人物成长研究</a>
  <a href="#overview">概况</a>
  <a href="#timeline">时间线</a>
  <a href="#limits">边界</a>
  <a href="#for-ocean">借鉴</a>
  <a href="#archive">留档</a>
</nav>
<header>
  <h1>张咋啦（Zara Zhang）成长深拆</h1>
  <p class="muted">对象：小红书「张咋啦」· X '''+A('https://x.com/zarazhangrui','@zarazhangrui')+''' · '''+A('https://zarazhang.com/about/','zarazhang.com/about')+'''。按“阶段 → 当时的问题 → 动作 → 作品 → 反馈 → 下一步变化”排，每条附原始链接。<span class="lv f">事实</span>可从原始页核到；<span class="lv s">自述</span>是本人说法，不是审计；<span class="lv a">分析</span>是研究者推断；<span class="lv b">边界</span>写不能怎么用。时间统一 UTC+8，查不到写未知。</p>
</header>'''
tl='<section id="timeline"><h2>五阶段时间线</h2>'+s1+s2+s3+s4+s5+'</section>'
arch_body=L(173,333)+'\n'+L(356,366)
arch_body=arch_body.replace('id="milestones"','id="old-milestones"').replace('id="breakout"','id="old-breakout"').replace('id="pieces"','id="pieces"')

FIXES=[
 ('<mark>收藏高于点赞</mark>是教程成功信号','收藏高于点赞（采集快照观察，不能证明成功原因）〔已纠错〕'),
 ('→ 置顶评论引粉丝群','；置顶评论未核实（2026-11-08 评论区未载入）〔已纠错〕'),
 ('比改功能列表更吸','比改功能列表可能更吸引人（待验证假设，无点击数据）〔已纠错〕'),
 ('时长写进标题降低跳出','时长写进标题（是否降低跳出未验证）〔已纠错〕'),
 ('价值在视频/模板。','价值在视频/模板。〔正文与模板数量为 11-01 旧采集，本轮未复核〕'),
 ('（分工/为何只跟一个聊/时间分配）。','（分工/为何只跟一个聊/时间分配）。〔视频结构未复核〕'),
]
for a,b in FIXES:
    assert arch_body.count(a)==1,a
    arch_body=arch_body.replace(a,b)
i=arch_body.index('差在哪</h2>')+len('差在哪</h2>')
arch_body=arch_body[:i]+'<p class="muted">〔已纠错〕下表是标题与点赞快照的对照，不是因果结论，也没有同曝光对比。</p>'+arch_body[i:]

NA='旧采集数据未复核，暂不展示'
import re as _re
# drop old milestones block (主页计数/粉丝轨迹，无可追溯原始数据)
_m0=arch_body.index('<section id="old-milestones">'); _m1=arch_body.index('</section>',_m0)+len('</section>')
arch_body=arch_body[:_m0]+'<section id="old-milestones"><h2>粉丝 / 影响力里程碑</h2><p class="muted">〔已纠错〕'+NA+'：旧版主页计数与粉丝轨迹缺可追溯原始数据，已移出公开页。</p></section>'+arch_body[_m1:]
arch_body=_re.sub(r'<td class="metrics">[^<]*</td>','<td class="metrics">—</td>',arch_body)
arch_body=_re.sub(r'\d[\d.,]*\s*万?赞(?:\s*/\s*\d[\d.,]*\s*万?藏)?(?:\s*/\s*\d[\d.,]*\s*评)?(?:（置顶）)?','〔'+NA+'〕',arch_body)
for a,b in [('按点赞；294 条采样 2026-06-18~2026-10-31 PT。正文截断 280。','〔已纠错〕互动数与采样范围为'+NA+'；仅保留帖子标题与链接（原表时间为 PT）。'),
            ('普通侧（列表中位~1.5千赞）','普通侧'),
            ('列表页点赞中位约 1.5 千；类型绝大多数 V=视频。置顶 2 条为涨粉方法 + GitHub 星叙事。','〔已纠错〕中位数、类型占比与置顶状态为'+NA+'。'),
            ('纯随感（&lt;〔'+NA+'〕）','纯随感'),
            (' · 置顶 · ',' · ')]:
    assert arch_body.count(a)==1,a
    arch_body=arch_body.replace(a,b)
archive=('<section id="archive"><h2>旧版留档（2026-11-01 采集）</h2><details class="arch"><summary>展开 2026-11-01 旧版：里程碑、作品清单、爆款逐拆、X Top10（原表时间为 PT，保持原样）</summary>'
 '<p class="muted"><span class="tag warn">注意</span>以下为旧版原文留档：点赞数是采集当天的快照，只有标题与点赞，没有同曝光对照，不能据此推断成功原因；“2万→18万”为采访索引摘录，不作硬事实。2026-11-08 已就地纠错：标〔已纠错〕处为更正；其余数字是 11-01 旧采集记录，本轮未复核。</p>'
 +arch_body+'</details></section>')
foot='<div class="foot"><p>私密 · x-digest/xhs/zhangzala.html · 2026-11-01 采集 / 2026-11-08 按研究文件重写（UTC+8）。</p></div>\n</main>'
tail='\n'.join(src[381:])
out='\n'.join([head,nav,overview,tl,limits,borrow,gaps,archive,foot,tail])
open('/workspace/digests/site-repo/xhs/zhangzala.html','w').write(out)
print(len(out))
