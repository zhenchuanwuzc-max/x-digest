"""Opportunity copy pinned to the 2026-11-06 06:18 Beijing digest snapshot.

Numbers below are either that snapshot, a GitHub API sample from the same
calendar day, or a sentence read on an official page that returned HTTP 200.
They are not user counts.
"""

TITLES = [
    ("what", "产品是什么"),
    ("who", "给谁"),
    ("flow", "工作流程与场景"),
    ("price", "价格、开放与权限"),
    ("signal", "真实使用信号"),
    ("cn", "国内替代"),
    ("wedge", "可做的窄切口"),
    ("mvp", "最小版与不做的范围"),
    ("check", "验证办法与建议的成功和停止条件"),
    ("money", "流量和付费"),
    ("risk", "风险"),
    ("sources", "来源"),
]


def blocks(mapping):
    out = []
    for sid, title in TITLES:
        out.append(
            {
                "id": sid,
                "title": title,
                "paragraphs": [{"kind": kind, "text": text} for kind, text in mapping[sid]],
            }
        )
    return out


def backs(anchor, label):
    return [
        (f"../../index.html#{anchor}", f"返回 {label}"),
        (f"../../2026-11-06.html#{anchor}", "返回 2026-11-06 快照同一栏"),
    ]


BOARD = "[[2026-11-06 情报站|https://zhenchuanwuzc-max.github.io/x-digest/2026-11-06.html]]"
GH = "https://api.github.com/repos/{repo}"

DATA = {
    "snapshot_id": "2026-11-06",
    "marker": "更新于 2026-11-06 06:18（北京时间）",
    "entries": [],
}


def entry(**kwargs):
    DATA["entries"].append(kwargs)


entry(
    slug="impeccable",
    panel="jm-ghw",
    rank="01",
    href="https://github.com/pbakaus/impeccable",
    name="pbakaus/impeccable",
    board_line="GitHub 热榜 · 本周涨星 · 显示序 1 · 快照写本周 +10,921 星，总星 103,844",
    banner="我们没有安装这个技能，也没有跑检测。下面的命令和规则数来自官方 README。星数是关注度，不是安装人数或付费人数。",
    meta="快照 2026-11-06 06:18 北京时间 · 显示序 1 · 本周 +10,921 星 · 未实测 · 星不是用户数",
    backs=backs("jm-ghw", "GitHub 热榜 · 本周涨星"),
    summary=[
        {"angle": "cn", "text": "国内已有中文设计技能 huashu-design，2026-11-06 的 GitHub API 抽样为 28,818 星，自述覆盖网页、PPTX 和 84 个风格，机会不是再做一个英文命令合集。"},
        {"angle": "min", "text": "最小可做的是一套中文页面禁令，只查紫渐变、假数据和过小字号，再配三张改前改后图给 Cursor 用。"},
        {"angle": "go", "text": "对比图适合做成短视频，但 Apache-2.0 仓库的本周新增星不能当成安装人数，模型变强后固定规则会失效。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[README|https://github.com/pbakaus/impeccable]] 称它是编程 Agent 的设计词汇。用 polish、bolder 改已有界面，用 critique、audit 做评审，并用 62 条确定性规则抓模板化设计。这些规则不调用模型，也不要 API key。"),
            ("事实", "GitHub API 在 2026-11-06 返回许可 Apache-2.0，语言栏为 Rust，主页指向 [[impeccable.style|https://impeccable.style/docs/]]。情报站快照把它放在本周涨星第 1，本周 +10,921，总星 103,844。同日 API 的公开星是 104,087。两个数字都不是安装人数。"),
        ],
        "who": [
            ("官方自述", "README 列出 Claude Code、Cursor、Codex、Copilot、Devin、Gemini CLI、OpenCode、DeepSeek Harness 等。对象是已经在用这些工具改界面的人。"),
            ("官方自述", "README 写它最强的地方是改已经存在的界面。从零做新站也可以，但作者把那叫更难的模式。"),
        ],
        "flow": [
            ("官方自述", "在项目根执行 npx impeccable install，然后在 Agent 里跑 init。init 追问它推断不出的受众和约束，写出 PRODUCT.md。之后的命令读这个文件。document 会另写 DESIGN.md。"),
            ("官方自述", "命令分成改调性、评审、收尾、浏览器里挑选变体、以及规划。live 模式在本地开发服务器上选中元素并换变体。README 写明 live 只改本地仓库，并警告不要为了它去放宽线上站点的 CSP。"),
            ("事实", "检测可以在 Agent 钩子、命令行或 Chrome 扩展里跑。扫源码只有模式规则。对比度和过小字号要扫渲染后的 URL。我们没有跑其中任何一种。"),
        ],
        "price": [
            ("事实", "API 与 README 都是 Apache-2.0。README 没有 SaaS 价目。"),
            ("官方自述", "新设计开始时会向 impeccable.style 拉一组视觉方向。关掉遥测后，项目名、文件和 PRODUCT.md 仍按 README 所说不会上传，但拉目录的请求还在。隐私页我们这次没有逐项复读，遥测字段以 [[隐私页|https://impeccable.style/docs/]] 同站文档为准，细节待核。"),
            ("官方自述", "live 的 Apply 在没有聊天会话轮询时，可能调用本机 codex 或 claude，并带上绕过审批的参数。这是 README 写明的权限行为。不熟悉的仓库里要先看它。"),
        ],
        "signal": [
            ("事实", f"{BOARD} 的本周涨星序和第 1 名热度是这次报告的榜单位置。API 公开星、6167 个 fork、65 个 open issue、219 个 watcher 是 2026-11-06 的仓库元数据，[[API|https://api.github.com/repos/pbakaus/impeccable]]。watcher 不是日活。"),
            ("待核", "第三方站点上的「实测」我们没有复现，不采信。留存、付费和检测误报率都没有。"),
        ],
        "cn": [
            ("事实", "[[huashu-design|https://github.com/alchaincyf/huashu-design]] 的 API 描述写的是在 Agent 里一句话拿到网页、App 原型、可编辑 PPTX、动画和信息图，六个候选里挑三个方向，84 个带样张的风格，外加外观账本和设计体检。许可 MIT。2026-11-06 抽样星数 28,818。"),
            ("事实", "[[aiku123 的 2026-10-28 对比|https://aiku123.com/articles/ai-design-skills-compare]] 把 hallmark、impeccable、ai-design-skills、huashu-design 放在一起。那篇文章自己的星数是 10 月 28 日口径，不能拿来当今天的星数。它能证明的是中文盘点已经存在。"),
            ("假设", "空隙更像中文交易页的检测规则，而不是再翻译 24 个英文命令。这个判断还没被用户验证。"),
        ],
        "wedge": [
            ("建议", "只做电商详情和活动页。规则写成中文例子。检测结果输出改哪一段，而不是再提供一套视觉主题。"),
        ],
        "mvp": [
            ("建议", "十条约定加三张对比图，装成一个 Cursor skill。约定只覆盖渐变、假数字、英文占位和过小字号。"),
            ("不做", "不宣称全面超过 impeccable。不把 Apache-2.0 仓库整份搬进闭源包。不在没跑过的情况下展示「62 条全通过」。"),
        ],
        "check": [
            ("建议", "找 8 个正在用 Cursor 改中文活动页的人。成功是其中 5 人愿意把检测留在仓库里超过 7 天，并且能指出一条规则改了他们的页面。"),
            ("建议", "停止条件是 7 天里没人留下 skill，或对比图播放高但没人要规则文件。流量不能代替留下。"),
        ],
        "money": [
            ("事实", "官方没有标出的 SaaS 价格。仓库是开源技能。"),
            ("假设", "收入更可能来自定制规则或录屏课，而不是星本身。这是猜测。"),
            ("建议", "先用同一提示词的两张截图做一条短视频。付费实验要等有人留下 skill 再做。"),
        ],
        "risk": [
            ("风险", "同题仓库已经很多。hallmark 的 README 也把 impeccable 列为参照。规则会过时。live 模式的绕过审批参数是安装者自己的权限风险。"),
        ],
        "sources": [
            ("事实", "页面均在 2026-11-06 打开且 HTTP 200。[[仓库 README|https://github.com/pbakaus/impeccable]]，[[文档|https://impeccable.style/docs/]]，[[GitHub API|https://api.github.com/repos/pbakaus/impeccable]]，[[huashu-design|https://github.com/alchaincyf/huashu-design]]，[[aiku123 对比|https://aiku123.com/articles/ai-design-skills-compare]]，" + BOARD + "。Product Hunt 页面这次返回 403，不作为来源。"),
        ],
    }),
)

entry(
    slug="claude-mem",
    panel="jm-ghw",
    rank="02",
    href="https://github.com/thedotmack/claude-mem",
    name="thedotmack/claude-mem",
    board_line="GitHub 热榜 · 本周涨星 · 显示序 2 · 快照写本周 +8,822 星，总星 113,500",
    banner="我们没有安装，也没有登录 cmem.ai。试用和月费是官网页面上的句子。星数不是留存。",
    meta="快照 2026-11-06 06:18 北京时间 · 显示序 2 · 本周 +8,822 星 · 未实测 · 星不是用户数",
    backs=backs("jm-ghw", "GitHub 热榜 · 本周涨星"),
    summary=[
        {"angle": "cn", "text": "可对照的本地方案是 PyPI 上的 silo-memory 0.3.5，它写明记忆留在本机的 SQLite，不把原文送到外部服务，因此没必要先做另一个托管记忆云。"},
        {"angle": "min", "text": "最小验证是一个仓库在会话结束时写一份 markdown，下次会话先读它，看隔天是否少解释一遍项目。"},
        {"angle": "go", "text": "「Agent 失忆」适合做内容，但官方安装会引导浏览器登录，cmem.ai 写试用后 CMEM Pro 每月 30 美元，密钥进记忆库才是付费前要过的关。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[README|https://github.com/thedotmack/claude-mem]] 说它捕获会话里的工具使用，生成摘要，再注入以后的会话。描述里点名 Claude Code、OpenClaw、Codex、Gemini、Hermes、Copilot、OpenCode。"),
            ("事实", "2026-11-06 的 [[GitHub API|https://api.github.com/repos/thedotmack/claude-mem]] 返回 Apache-2.0，公开星 113,635，fork 9,855，open issue 130。情报站快照是本周 +8,822、总星 113,500。两边都不是用户数。"),
        ],
        "who": [
            ("官方自述", "给跨会话、跨工具继续同一个项目的人。README 也单列团队功能 TeamBrain，每个人选择分享什么。"),
            ("事实", "中文模式写在 README 里。CLAUDE_MEM_MODE 设为 code--zh 时，观察和摘要用中文。这是配置说明，我们没有跑。"),
        ],
        "flow": [
            ("官方自述", "生命周期钩子覆盖 SessionStart、UserPromptSubmit、PreToolUse、PostToolUse、Stop、SessionEnd。本地 worker 提供 HTTP API 和查看页。存储是 SQLite。检索一层是 mem-search，另一层 README 写了 Chroma 向量库。"),
            ("官方自述", "默认安装 npx claude-mem install 会在浏览器里用邮件链接登录，领取 memory key，并打开 30 天试用。README 写试用期内记忆不走你的 Anthropic 套餐。试用结束若未订阅，就退回你的套餐。加 --provider、或设置 CLAUDE_MEM_ONLINE_OPTIN=false，可以跳过登录。"),
            ("官方自述", "截图默认关闭。只有同时打开 Cloud Sync 和图像推理才会上传或送给观察模型。排除敏感内容用标签，具体标签写法以文档为准，这里不复述。"),
        ],
        "price": [
            ("官方自述", "2026-11-06 打开的 [[cmem.ai|https://cmem.ai/]] 写 30 天免费试用，之后 CMEM Pro 每月 30 美元。引擎页面同时写开源。我们没有下单，也没有看到税费和席位表。"),
            ("事实", "仓库许可是 Apache-2.0。README 另写商业边界文档，这次没有逐页打开 [[docs.claude-mem.ai|https://docs.claude-mem.ai/introduction]] 里的许可专页，边界条款待核。"),
        ],
        "signal": [
            ("事实", "热度来自情报站周榜和 API 星数。README 没有公布付费订阅数。"),
            ("待核", "30 美元是否对所有地区一致、试用是否要绑卡，这次只看到「no card required」写在安装说明里。结账页没有打开。"),
        ],
        "cn": [
            ("事实", "[[silo-memory 0.3.5|https://pypi.org/project/silo-memory/]] 的摘要是给编程 Agent 的本地长期记忆，SQLite FTS5 加关键词图，技能覆盖 Claude Code、Codex、OpenCode、Cursor、Grok。正文写原文和索引都在本机，不发送到外部服务。仓库 [[flynn-eye/silo-memory|https://github.com/flynn-eye/silo-memory]] 同日可打开。"),
            ("假设", "和 claude-mem 的差别在托管观察者、跨工具云同步和团队共享。若只需要单机回忆，Silo 的描述已经覆盖「开始时召回、结束时沉淀」。我们没有并排安装。"),
        ],
        "wedge": [
            ("建议", "只做中文项目的会话结束摘要，文件留在仓库里，不上传。不要做账号、向量库和团队空间。"),
        ],
        "mvp": [
            ("建议", "一个 hook。会话结束写 markdown。下次把该文件放进上下文。只服务一个自己的仓库。"),
            ("不做", "不做托管记忆、不做截图同步、不对比「省了多少 token」。官方写约 10 倍 token 节省，那是 README 的检索流程说明，不是我们测到的数。"),
        ],
        "check": [
            ("建议", "连续 5 个工作日用同一仓库。成功是第 5 天不用重新解释目录约定，且摘要文件里没有出现密钥。"),
            ("建议", "停止条件是摘要每天都要手改，或一次把令牌写进了文件。"),
        ],
        "money": [
            ("事实", "开源引擎加上官网写出的 30 美元 Pro。星数不能换成订阅。"),
            ("建议", "内容可以讲失忆。收费要等本地摘要真的被第二天用上，再决定要不要做同步。"),
        ],
        "risk": [
            ("风险", "记忆里会有命令、路径和密钥。云同步把这个库交给第三方。官方记忆功能若变强，插件的理由会变薄。安装器默认要登录，和「纯本地」不是一回事。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[README|https://github.com/thedotmack/claude-mem]]，[[API|https://api.github.com/repos/thedotmack/claude-mem]]，[[cmem.ai|https://cmem.ai/]]，[[文档|https://docs.claude-mem.ai/introduction]]，[[silo-memory|https://pypi.org/project/silo-memory/]]，[[Silo 仓库|https://github.com/flynn-eye/silo-memory]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="hallmark",
    panel="jm-ghw",
    rank="03",
    href="https://github.com/Nutlope/hallmark",
    name="Nutlope/hallmark",
    board_line="GitHub 热榜 · 本周涨星 · 显示序 3 · 快照写本周 +7,622 星，总星 48,695",
    banner="我们没有安装 Hallmark，也没有跑它的浏览器 lint。主题数和门禁名称来自 README。",
    meta="快照 2026-11-06 06:18 北京时间 · 显示序 3 · 本周 +7,622 星 · 未实测 · 星不是用户数",
    backs=backs("jm-ghw", "GitHub 热榜 · 本周涨星"),
    summary=[
        {"angle": "cn", "text": "它和 impeccable 同在设计技能赛道，但 Hallmark 先发 50 个主题再过 Floor、Reflex、Finish 三道门，impeccable 是 24 个命令加 62 条确定性规则。"},
        {"angle": "min", "text": "最小可做的是中文交易页禁令，只拦紫渐变和编造的数据，并给出一张 lint 前后图，而不是翻译它的英文主题。"},
        {"angle": "go", "text": "官网用同一提示词的左右对比做演示，这种素材容易带来播放，MIT 星数仍然不是付费，主题同质化也已经发生。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[README|https://github.com/Nutlope/hallmark]] 写它由 Together AI 制作，是 Claude Code、Codex、Cursor、OpenCode 的设计技能。目录有 50 个主题。每个主题是材质，不是页面提纲。"),
            ("事实", "2026-11-06 [[API|https://api.github.com/repos/Nutlope/hallmark]] 返回 MIT，公开星 48,903，fork 2,591。情报站快照是本周 +7,622、总星 48,695。"),
        ],
        "who": [
            ("官方自述", "给要 Agent 出页面、又不想要模板腔的人。redesign 保留内容和接线，audit 只出报告。"),
        ],
        "flow": [
            ("官方自述", "预检读字体、色板和是否已有锁住的 design.md，并要求照片、截图和真实数字，声明不编造。theme.mjs 先给三个主题。英雄区单独做完并冷审，再做页面其余部分。sloplint --render 在八个宽度检查，然后换一个新上下文的评审收尾。"),
            ("官方自述", "Floor 不过就不发布，例子包括对比度、焦点、减少动效、编造事实、手机布局坏掉。Reflex 是模型的默认习惯，有理由可以记录后推翻。Finish 不挡发布。"),
            ("事实", "浏览器检查需要 puppeteer-core 和 Chrome。没有它们时 README 说静态检查仍能跑。我们两种都没跑。"),
        ],
        "price": [
            ("事实", "许可 MIT。README 写 custom on request，没有标出定制价格。这次打开的 [[usehallmark.com|https://www.usehallmark.com]] 也是安装命令和演示，没有价目表。"),
        ],
        "signal": [
            ("事实", "榜单热度加上 API 星数。官网演示写 Without 26 issues、With Hallmark 0 issues，并注明数字来自它自己的 linter。那是官网自述，不是独立复测。"),
            ("待核", "50 个主题是否都可用、定制是否收费，没有逐个打开主题文件。"),
        ],
        "cn": [
            ("事实", "README 的参照列表里已经写了 [[huashu-design|https://github.com/alchaincyf/huashu-design]] 和 impeccable。中文对比文见 [[aiku123|https://aiku123.com/articles/ai-design-skills-compare]]。huashu 的差异是中文流程、PPTX 和 84 个风格。Hallmark 的差异是主题抽取加浏览器门禁。"),
            ("假设", "把英文主题译成中文不会形成差别。差别只会出现在中文交易页特有的失败模式。"),
        ],
        "wedge": [
            ("建议", "做「禁止编造销量和倒计时」这一类中文活动页规则。输出是失败清单，不是新的视觉主题。"),
        ],
        "mvp": [
            ("建议", "五条规则，一张活动页，改前改后各一张图。规则文件放进 Cursor skill。"),
            ("不做", "不克隆 50 个主题。不使用 README 点名的图库许可问题去再分发照片。照片库条款以仓库为准，我们没有逐张核对。"),
        ],
        "check": [
            ("建议", "拿 6 个真实中文活动页跑规则。成功是每个页面至少一条规则被作者接受，且没有把真实价格判成假数据。"),
            ("建议", "停止条件是规则只会报 Inter 字体和紫渐变，作者改完仍觉得没有用。"),
        ],
        "money": [
            ("事实", "没有官价。播放可以来自对比图。"),
            ("建议", "先发对比，不设付费。有人把规则要进自己的仓库，再谈按站定制。"),
        ],
        "risk": [
            ("风险", "和 impeccable、huashu-design 挤在同一周的关注里。浏览器 lint 依赖本机 Chrome。主题文件若直接再分发，要单独看 MIT 以外的照片许可。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[README|https://github.com/Nutlope/hallmark]]，[[API|https://api.github.com/repos/Nutlope/hallmark]]，[[usehallmark.com|https://www.usehallmark.com]]，[[huashu-design|https://github.com/alchaincyf/huashu-design]]，[[aiku123|https://aiku123.com/articles/ai-design-skills-compare]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="security-audit-skill",
    panel="jm-ghw",
    rank="04",
    href="https://github.com/cloudflare/security-audit-skill",
    name="cloudflare/security-audit-skill",
    board_line="GitHub 热榜 · 本周涨星 · 显示序 4 · 快照写本周 +7,528 星，总星 61,317",
    banner="我们没有对任何仓库跑这份审计技能，也没有漏洞数可以报。",
    meta="快照 2026-11-06 06:18 北京时间 · 显示序 4 · 本周 +7,528 星 · 未实测 · 星不是漏洞数",
    backs=backs("jm-ghw", "GitHub 热榜 · 本周涨星"),
    summary=[
        {"angle": "cn", "text": "这是 Cloudflare 给编程 Agent 的六阶段审计技能，结论只有 confirmed、needs_validation、rejected，适合要审自己代码的团队，不是面向消费者的 App。"},
        {"angle": "min", "text": "最小可做的是把自己的鉴权和租户隔离写成狩猎清单，对一个玩具仓库跑通 findings.json 能否被它自带的校验脚本读过。"},
        {"angle": "go", "text": "安全选题能带来阅读，但星数不是发现率，误报和把攻击细节写进工单才是能不能拿去卖服务的关。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[README|https://github.com/cloudflare/security-audit-skill]] 说它把 Agent 编排成分阶段审计。六个阶段是侦察、按覆盖率狩猎、候选人否证、结构化输出、独立复核记录、以及与目标无关的报告。"),
            ("官方自述", "它是 Cloudflare 漏洞发现流程的单仓库起点。博文是 [[Build your own vulnerability harness|https://blog.cloudflare.com/build-your-own-vulnerability-harness]]。博文讲的是他们后来的集群系统，这个仓库是起点，不是那套集群本身。"),
        ],
        "who": [
            ("官方自述", "给已经有代码库、并让编程 Agent 做审计的人。安装用 npx skills add。触发语包括安全审计和找漏洞。没有沙箱时，README 要求把需要执行目标代码的线索留在 needs_validation，而不是直接跑。"),
        ],
        "flow": [
            ("官方自述", "侦察写 architecture.md 和 coverage-ledger.json。狩猎按账本分配互不复用结论的猎人。每个候选人交给一个新的验证者去推翻。findings.json 里的三种结论用 report-schema.json 校验。发现者不能当自己发现的验证者。"),
            ("官方自述", "confirmed 要有完整的源码追溯和有边界的观察结果。needs_validation 只有一个未解决事实，不写严重度。rejected 记录被推翻的候选人。多次跑是叠加，旧结论不能当成已经覆盖。"),
            ("事实", "校验脚本是仓库里的零依赖 Node 脚本。我们没有执行它。"),
        ],
        "price": [
            ("事实", "2026-11-06 [[API|https://api.github.com/repos/cloudflare/security-audit-skill]] 返回 MIT，公开星 61,903，fork 4,016，open issue 116。没有价格页。情报站快照是本周 +7,528、总星 61,317。"),
            ("待核", "Cloudflare 是否另卖托管审计，这个仓库没有写。不把缺席当成免费企业服务。"),
        ],
        "signal": [
            ("官方自述", "README 写他们自己的测试里，单次运行大约找到多次运行合计漏洞的一半。这是作者对内部测试的说法，没有附公开漏洞清单，我们不当成基准。"),
            ("事实", "没有可以引用的 CVE 计数。星和 fork 只说明仓库被关注。"),
        ],
        "cn": [
            ("假设", "国内团队缺的通常不是另一份通用英文技能，而是本公司的鉴权、租户隔离和导出接口清单。这次没有打开某一家国内安全产品的价目，所以不点名比较报价。"),
            ("建议", "若要对照，对照的是流程差别。这里有独立否证和三种结论。一份只给「高中低」而不写未决事实的清单，不是同一件东西。"),
        ],
        "wedge": [
            ("建议", "把本公司 20 条必查项写成狩猎附加清单。输出沿用 confirmed、needs_validation、rejected，而不是新发明等级。"),
        ],
        "mvp": [
            ("建议", "选一个自己的玩具仓库。只跑到写出 findings.json，并用仓库里的校验脚本看它是否合格。不对外发布找到的问题。"),
            ("不做", "不把这份技能包装成可以绕过目标系统的工具。不在没有沙箱时执行不可信代码。不承诺发现率。"),
        ],
        "check": [
            ("建议", "成功是校验脚本接受这份 findings.json，并且每个 needs_validation 都写了一个可以继续查的事实。"),
            ("建议", "停止条件是结论无法被人复核，或一次就把利用步骤发到了公开频道。"),
        ],
        "money": [
            ("事实", "仓库免费、MIT。"),
            ("假设", "能收费的是带本公司规范的审计服务，不是再发一个星标仓库。销售周期是团队采购，不是短视频成交。"),
        ],
        "risk": [
            ("风险", "误报会消耗工程时间。把可利用细节写进工单或公开报告有合规问题。没有沙箱就执行目标构建，README 自己把它视为不够格的确认。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[README|https://github.com/cloudflare/security-audit-skill]]，[[API|https://api.github.com/repos/cloudflare/security-audit-skill]]，[[Cloudflare 博文|https://blog.cloudflare.com/build-your-own-vulnerability-harness]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="dsh-purge",
    panel="jm-ghw",
    rank="05",
    href="https://github.com/HunYiSage/dsh-purge",
    name="HunYiSage/dsh-purge",
    board_line="GitHub 热榜 · 本周涨星 · 显示序 5 · 快照写本周 +6,079 星，总星 19,096",
    banner="我们没有下载、执行或引用这个仓库里的提示词。下面只根据 GitHub API 的描述、许可、topic 和情报站快照做中立说明。",
    meta="快照 2026-11-06 06:18 北京时间 · 显示序 5 · 本周 +6,079 星 · 未执行 · 星不是使用成功次数",
    backs=backs("jm-ghw", "GitHub 热榜 · 本周涨星"),
    summary=[
        {"angle": "cn", "text": "仓库自述是可换模型的破甲提示词包，这类产品和绕过模型安全策略绑在一起，不适合做成要卖给国内用户的同类工具。"},
        {"angle": "min", "text": "若只取相邻的合法需求，最小版本是书面授权下、只针对自有模型的回归评测集，里面不放绕过文本。"},
        {"angle": "go", "text": "星数说明有人点了 Star，不能当成越狱成功或付费，传播绕过内容还有平台封禁和违法风险，本页不提供做法。"},
    ],
    sections=blocks({
        "what": [
            ("事实", "2026-11-06 的 [[GitHub API|https://api.github.com/repos/HunYiSage/dsh-purge]] 描述把它称为面向 DeepSeek Harness 的破甲提示词包，并写可以按模型更换提示词。topic 包含 deepseek-harness、harness-jailbreak、jailbreak、llm-jailbreak。"),
            ("事实", "情报站卡片的简介与这段 API 描述一致，位置是本周涨星显示序 5，本周 +6,079，总星 19,096。同日 API 公开星 19,343，fork 4,550。这些都不是成功次数。"),
            ("不做", "本报告不引用提示词，不描述绕过步骤，也不链到仓库里的提示词文件。项目页链接只用于核对仓库身份。"),
        ],
        "who": [
            ("事实", "按 API 描述，它面向要在 DeepSeek Harness 里更换提示词的人。我们没有阅读二开说明的正文。"),
        ],
        "flow": [
            ("待核", "安装方式、提示词如何被 Harness 加载、默认面向哪一个模型，都写在我们故意没有打开的文件里。因此这里没有工作流程。"),
            ("事实", "能确认的只有元数据。它是一个公开 JavaScript 仓库，默认分支 master，创建于 API 返回的 2026-08-19。"),
        ],
        "price": [
            ("事实", "API 返回的许可是 Apache-2.0。描述另要求二开先看署名部分。署名正文这次没有打开，条款待核，不能把 Apache-2.0 理解成没有额外署名要求。"),
            ("事实", "没有价格页。API 描述里有求 Star 的句子。Star 不是订单。"),
        ],
        "signal": [
            ("事实", "信号只有公开星、fork、12 个 open issue 和 33 个 watcher。没有成功率、留存或付费。我们未使用。"),
        ],
        "cn": [
            ("建议", "不要做国内版的同类提示词包。功能差异不是「换一套中文提示词」，而是目的不同。合法的相邻物是自有模型的回归评测，或普通的 Harness 生产力技能。"),
            ("待核", "具体哪一家国内评测平台提供授权红队环境，这次没有打开他们的合同页，不点名报价。"),
        ],
        "wedge": [
            ("建议", "只做一件窄事。给自己的模型维护一组拒绝应当发生的请求类型清单，记录模型是否拒绝，不保存能让别人复现绕过的文本。"),
        ],
        "mvp": [
            ("建议", "一张表格。列是请求类型、期望是拒绝、实际是否拒绝、日期。样本来自公开、无害的政策边界问题，不来自这个仓库。"),
            ("不做", "不转发、不改写、不翻译该仓库的提示词。不把它当成可卖的「破甲服务」。不在未读署名条款时做二开。"),
        ],
        "check": [
            ("建议", "成功是表格能被安全负责人读懂，并且仓库和文档里检索不到从 dsh-purge 复制的文本。"),
            ("建议", "停止条件是任何一步需要打开或粘贴绕过提示词。到那一步就停。"),
        ],
        "money": [
            ("事实", "没有官价。热度是 Star。"),
            ("建议", "不要用这个主题做流量。播放绕过演示本身就是不该做的分发。"),
        ],
        "risk": [
            ("风险", "可能违反模型提供方的条款，也可能涉及违法内容。平台可以封号。署名条款未读。高 fork 数只说明复制容易，不说明使用合法。"),
        ],
        "sources": [
            ("事实", "2026-11-06 读取且 HTTP 200 的只有元数据，没有提示词文件。[[GitHub API|https://api.github.com/repos/HunYiSage/dsh-purge]]，[[仓库主页|https://github.com/HunYiSage/dsh-purge]]，" + BOARD + "。主页能核对身份。不要从主页继续打开提示词文件来补充本报告。"),
        ],
    }),
)

entry(
    slug="glasshand",
    panel="jm-phd",
    rank="01",
    href="https://www.producthunt.com/products/glasshand",
    name="Glasshand",
    board_line="AI 产品榜单 · 日 · 显示序 1 · 快照票数 293 · 范围 2026-11-05 · 这是情报站分组后的显示序，不是 Product Hunt 全站绝对名次",
    banner="我们没有租设备，也没有登录。价格来自 2026-11-06 打开的官网定价页。Product Hunt 产品页这次返回 403，不引用那里的句子。",
    meta="快照 2026-11-06 06:18 北京时间 · 日榜显示序 1 · 293 票 · 未租用 · 票不是续租人数",
    backs=backs("jm-phd", "AI 产品榜单 · 日"),
    summary=[
        {"angle": "cn", "text": "官网卖的是独占的真机 iPhone 或 Mac，国内扣子文档卖的是按 CU·天计费的云电脑和云手机，UBox 卖的是按时长调度的 Android、iOS、HarmonyOS 真机池，都不是同一件账单。"},
        {"angle": "min", "text": "最小可做的不是自建机房，而是用一台自己的闲置安卓加现成投屏，先证明有人愿意为「Agent 能点真机」付钱。"},
        {"angle": "go", "text": "真机录屏很容易带来播放，但账号、短信和释放后是否真的擦除都没有被我们验证，293 票也不是续租人数。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[glasshand.com|https://glasshand.com]] 写给 Agent 一台真的 iPhone 或 Mac，通过 API 接 Claude Code、Codex、Cursor 或其他 Agent。他们提供设备和操作。"),
            ("事实", "情报站日榜把 Glasshand 放在编程分组的显示序 1，票数 293，并链到 Product Hunt。Product Hunt 页面本次 403，名次以情报站显示序为准。"),
        ],
        "who": [
            ("官方自述", "定价页的用途是安装 App、登录自己的账号、用 eSIM 收验证短信，以及在 Mac 上用 Xcode 测应用。对象是需要苹果真机、而不是模拟器的 Agent 流程。"),
        ],
        "flow": [
            ("官方自述", "定价页写先租设备，再把一段提示贴进 Agent。Agent 看屏幕、点击和输入。我们没有走完这一步，所以看不到控制通道的权限模型。"),
            ("官方自述", "释放设备时，页面写会擦除数据并重置。取消后设备保留到当前账期结束。这是页面句子，不是我们观察到的擦除结果。"),
        ],
        "price": [
            ("官方自述", "[[定价页|https://glasshand.com/pricing/]] 在 2026-11-06 写 iPhone 每月 60 美元，Mac 每月 90 美元，美元价另加税，按月，可取消。"),
            ("待核", "有没有免费额度、企业合同和国内支付，定价页这次没写。不把第三方转载价再写一遍。"),
        ],
        "signal": [
            ("事实", "能核对的是官网可打开，以及情报站上的 293 票。没有续租人数、设备在线率或退款率。"),
        ],
        "cn": [
            ("事实", "[[扣子云设备费用|https://docs.coze.cn/coze_pro_cloud_device_fee]] 写云电脑和云手机按规格折成 CU，云电脑 12 积分每 CU 每天或 0.3 元每 CU 每天，云手机另有快速和经济模式。文档举例 2C4G 云电脑运行 1 天是 24 积分。这是虚拟规格，不是一台固定的苹果手机。"),
            ("事实", "[[UBox|https://utest.21kunpeng.com/home/ubox]] 写用云真机 Skill 把 Android、iOS、HarmonyOS 真机接入 Agent，按使用时长结算，并记录画面和日志。页面没有给出和 60 美元对得上的单价。它是设备池，不是月租一台专用 iPhone。"),
            ("事实", "[[Devicebase|https://www.devicebase.cn/]] 写统一 API 操作手机、浏览器和电脑，注册送 500 积分，并称 10k+ 活跃开发者。活跃开发者是厂商首页句子，我们没有核对。它也没有写苹果真机独占月租。"),
        ],
        "wedge": [
            ("建议", "只做安卓投屏教程或小范围代管，明确不提供苹果账号、短信和 iCloud。差异要写在第一屏，避免被理解成 Glasshand 的国内版。"),
        ],
        "mvp": [
            ("建议", "一台自己的闲置安卓，投屏给一个本地 Agent，完成「打开设置并截图」这一条任务。记录失败在哪一步。"),
            ("不做", "不采购 iPhone 库存。不帮用户养号。不承诺擦除达到厂商声称的程度。"),
        ],
        "check": [
            ("建议", "成功是 5 个开发者愿意为这台安卓的一周代管支付一笔能覆盖流量和电费的钱，并且没有人要求登录别人的账号。"),
            ("建议", "停止条件是需求立刻滑向批量账号或短信验证。"),
        ],
        "money": [
            ("事实", "官网是月租美元价。情报站是 293 票。"),
            ("建议", "录屏可以做内容。收款要先有单台设备的真实任务，再谈包月。"),
        ],
        "risk": [
            ("风险", "登录用户自己的社交或支付账号有封号和隐私风险。eSIM 短信可能被用在验证滥用上。硬件损耗、海关和支付我们都没核。苹果对自动化的限制也不会因为换了出租方就消失。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[glasshand.com|https://glasshand.com]]，[[定价页|https://glasshand.com/pricing/]]，[[扣子云设备|https://docs.coze.cn/coze_pro_cloud_device_fee]]，[[UBox|https://utest.21kunpeng.com/home/ubox]]，[[Devicebase|https://www.devicebase.cn/]]，" + BOARD + "。Product Hunt 产品页 403，不采用。"),
        ],
    }),
)

entry(
    slug="pushary",
    panel="jm-phd",
    rank="02",
    href="https://www.producthunt.com/products/pushary",
    name="Pushary for Teams",
    board_line="AI 产品榜单 · 日 · 显示序 2 · 快照票数 158 · 范围 2026-11-05",
    banner="我们没有开通工作区。价格来自官网团队页、定价页和团队文档，三处在 2026-11-06 都能打开。",
    meta="快照 2026-11-06 06:18 北京时间 · 日榜显示序 2 · 158 票 · 未开通 · 票不是付费席位",
    backs=backs("jm-phd", "AI 产品榜单 · 日"),
    summary=[
        {"angle": "cn", "text": "官网把编码 Agent 的提问送到手机或 Mac，并留下谁点了同意，这次没有打开飞书或企微的审批文档，所以不能把它们写成已经核实的同类账本。"},
        {"angle": "min", "text": "最小可做的是一个只拦截 git push 和对外发信的机器人，把同意记进一张表，先给一个五人小组用。"},
        {"angle": "go", "text": "团队页写 5 人每月 59 美元、多一人每月 12 美元，演示短、好讲，但国内能否用人民币结账仍待核，158 票也不是席位数。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[团队页|https://pushary.com/teams]] 写把 Agent 的批准从手机完成，并留下团队记录。[[定价页|https://pushary.com/pricing]] 写一个人也可以用，手机 App 和 Mac App 包含在内。"),
            ("事实", "情报站显示序 2，158 票。原链接是 Product Hunt。该页本次 403。"),
        ],
        "who": [
            ("官方自述", "团队文档写给需要知道谁点了同意的人。提问可以到个人，也可以到你指定步骤的负责人。个人方案写给跑很多 Agent 的一个人。"),
        ],
        "flow": [
            ("官方自述", "[[团队文档|https://pushary.com/docs/agents/team]] 写价格，并说明团队记录可以导出 CSV 和 JSON，记录保留 365 天。定价页的个人档写批准、拒绝或从手机回答，并包含权限策略、MCP 和 API。"),
            ("待核", "文档后半提到有的渠道作答是否记名。这次摘到的正文没有把每个渠道的记名差异列全，记名范围待核，不把「所有渠道都有实名」写成事实。"),
        ],
        "price": [
            ("官方自述", "三处页面一致写出团队价。5 人每月 59 美元，额外一人每月 12 美元，新工作区 3 天免费，试用期内取消不收费。"),
            ("官方自述", "定价页另有个人档每月 9.99 美元、每月 5,000 条通知，以及 19.99 美元的不限通知档。合作方档写着每月 99、299、799 美元，按终端用户规模分。我们没有结账。"),
            ("官方自述", "团队页写美国以外结账可能把同样的数字收成欧元或英镑。页面没有写人民币。国内发票和 App 上架待核。"),
        ],
        "signal": [
            ("事实", "158 票来自情报站。官网没有公开付费团队数。"),
        ],
        "cn": [
            ("待核", "飞书、钉钉、企微都有审批产品，但这次没有打开它们的文档，不能写它们是否能拦住 Cursor 或 Claude Code 的一次 git push。"),
            ("假设", "若国内缺口存在，它在「编码工具的权限提问」而不在「请假审批」。这个缺口仍是假设。"),
        ],
        "wedge": [
            ("建议", "只做两类拦截。git push，以及向外部发信。同意写进一张共享表，字段是谁、何时、哪条命令。"),
        ],
        "mvp": [
            ("建议", "一个飞书或邮件机器人。先不覆盖所有 Agent。服务一个自己的五人小组两周。"),
            ("不做", "不做 Mac 灵动岛客户端。不做全量 MCP 代理。不宣称和 Pushary 功能对等。"),
        ],
        "check": [
            ("建议", "成功是两周内真实拦截至少 20 次，复盘时能指出责任人，并且没有一次误拦导致大家关掉它。"),
            ("建议", "停止条件是小组改回在聊天里口头说「可以推」。"),
        ],
        "money": [
            ("事实", "官网团队价是 59 美元 5 人。票数是 158。"),
            ("建议", "可以用 20 秒演示讲清楚。收费要等那 20 次真实拦截出现。"),
        ],
        "risk": [
            ("风险", "批准记录本身是敏感日志。漏记一次同意会在事故后无法追责。国内支付未核。若机器人能看到命令全文，密钥可能进日志。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[团队页|https://pushary.com/teams]]，[[定价页|https://pushary.com/pricing]]，[[团队文档|https://pushary.com/docs/agents/team]]，" + BOARD + "。Product Hunt 403，不采用。"),
        ],
    }),
)

entry(
    slug="maritime",
    panel="jm-phd",
    rank="03",
    href="https://www.producthunt.com/products/maritime",
    name="Maritime",
    board_line="AI 产品榜单 · 日 · 显示序 3 · 快照票数 156 · 范围 2026-11-05 · 官网是 maritime.sh",
    banner="我们没有开机器。单价来自 2026-11-06 的官网定价页。没有把首页示例命令当成用量。",
    meta="快照 2026-11-06 06:18 北京时间 · 日榜显示序 3 · 156 票 · 未开机器 · 票不是并发用量",
    backs=backs("jm-phd", "AI 产品榜单 · 日"),
    summary=[
        {"angle": "cn", "text": "官网按秒卖沙箱和云桌面，扣子按 CU·天卖云电脑和云手机，两边都能跑 Agent，但账单单位和能不能拿到 Windows 桌面并不一样。"},
        {"angle": "min", "text": "个人最小动作是用一家现成云的一次性沙箱跑完一个生成脚本，而不是自建机房或转售 Maritime。"},
        {"angle": "go", "text": "云电脑演示能做视频，156 票不是用量，滥用、许可和毛利会先于播放变成成本。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[maritime.sh|https://maritime.sh]] 把 Agent 电脑分成会睡眠的 agent box、跑完即删的 sandbox、可看屏幕的 Linux 或 Windows 桌面，以及 Android 手机。"),
            ("事实", "情报站显示序 3，156 票，原链是 Product Hunt。该页 403。不要把 maritime.ai 当成这个产品，这次没有使用那个域名。"),
        ],
        "who": [
            ("官方自述", "定价页用问题区分。要在对话之间留文件，用 agent box。任务结束就丢，用 sandbox。需要屏幕或 Windows，用按需电脑。对象是把环境交给 Agent 的开发者，不是自己远程办公的个人桌面用户。"),
        ],
        "flow": [
            ("官方自述", "sandbox 在任务结束时连磁盘一起删。agent box 空闲睡眠，大约一秒唤醒。桌面允许人接管。这些是定价页和首页的描述，我们没有创建过实例。"),
        ],
        "price": [
            ("官方自述", "[[定价页|https://maritime.sh/pricing]] 2026-11-06 写 agent box 每 2 GB 每月 1 美元，含 5 GB 磁盘，超出每 GB 每月 0.08 美元。sandbox 每 vCPU 和 2 GB 每小时 0.011 美元，按秒、无最低时长。Linux 桌面醒着每小时 0.12 美元。Windows 桌面每小时 0.18 美元且含许可，Growth 及以上。Android 每小时 0.15 美元。"),
            ("官方自述", "Starter 每月 20 美元，含 20 美元用量，7 天试用最高 20 美元用量，同时 5 台醒着。Growth 每月 100 美元、25 台。Scale 每月 500 美元、60 台。Dedicated 每月 5,000 美元、500 台。我们没有注册。"),
        ],
        "signal": [
            ("事实", "156 票是情报站数字。官网没有公开并发台数或收入。"),
            ("待核", "有的转述称它是 YC 项目。这次打开的定价页和首页摘录里没有看到 YC 句子，所以不写。"),
        ],
        "cn": [
            ("事实", "扣子云电脑按 CU·天，文档给出 2C4G 为 2 CU、每天 12 积分每 CU。Maritime 的 sandbox 按秒，并且单列 Windows 许可。一个适合放进现有扣子订阅，一个适合按任务秒数结算。"),
            ("事实", "UBox 和 Devicebase 解决的是手机或浏览器控制，不是 Maritime 定价页上的 Windows 桌面和大规模 sandbox。"),
        ],
        "wedge": [
            ("建议", "不要重做云。只做一个很窄的封装。把「跑完这条生成脚本就销毁」写成对某一家已有云的一页说明。"),
        ],
        "mvp": [
            ("建议", "用现成云跑 10 次一次性任务，记下每次从发起到销毁的分钟数和费用。"),
            ("不做", "不买服务器。不承诺 Windows 许可。不把 Maritime 的价目翻译成人民币价后当成自己的报价。"),
        ],
        "check": [
            ("建议", "成功是这 10 次的费用能在一张表里对上云账单，并且有第二个项目愿意按同样方式跑。"),
            ("建议", "停止条件是支持时间超过写脚本的时间，或出现挖矿和违法用途。"),
        ],
        "money": [
            ("事实", "官网是套餐加按量。156 票不是用量。"),
            ("假设", "个人转售算力的毛利通常盖不住值班。这是判断，不是测算。"),
        ],
        "risk": [
            ("风险", "生成代码可能挖矿或攻击外部。桌面许可和地区可用性未核。按秒计费在循环失控时会变成账单。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[maritime.sh|https://maritime.sh]]，[[定价页|https://maritime.sh/pricing]]，[[扣子云设备|https://docs.coze.cn/coze_pro_cloud_device_fee]]，[[UBox|https://utest.21kunpeng.com/home/ubox]]，[[Devicebase|https://www.devicebase.cn/]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="clocknext",
    panel="jm-phd",
    rank="04",
    href="https://www.producthunt.com/products/clocknext",
    name="Clocknext",
    board_line="AI 产品榜单 · 日 · 显示序 4 · 快照票数 134 · 范围 2026-11-05",
    banner="我们没有创建 Clocknext 账号。价目只采用定价页。首页上的发票金额看起来是界面示例，不当成客户实价。",
    meta="快照 2026-11-06 06:18 北京时间 · 日榜显示序 4 · 134 票 · 未接入 · 票不是计费收入",
    backs=backs("jm-phd", "AI 产品榜单 · 日"),
    summary=[
        {"angle": "cn", "text": "定价页按你向外开出的账单收入分档，国内支付和发票这次没有逐家打开，所以不能写国内没有计费工具。"},
        {"angle": "min", "text": "最小版本是给自己的一个 Agent 产品做每周一张表，左边模型成本，右边客户套餐，先不要做发票和钱包。"},
        {"angle": "go", "text": "创业者内容能带来阅读，成交却要接进别人的账单系统，134 票不能当成年经常性收入。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[clocknext.com|https://www.clocknext.com/]] 写给 AI Agent 的用量计费。功能名包括额度钱包、用量计量、按结果计价、定价实验、组合项目、毛利和发票。"),
            ("事实", "情报站显示序 4，134 票。"),
        ],
        "who": [
            ("官方自述", "给已经有 AI 产品、需要把用量变成可计费项目的团队。定价页的档位按「向外开出的账单收入」划分，不是按席位。"),
        ],
        "flow": [
            ("官方自述", "首页描述从信号到发票。可以混合 credits、outcomes 和 units。价格可以不重新部署就改。这些是产品说明。"),
            ("事实", "首页示例里有 Acme Inc. 等发票数字。它们出现在产品示意图里。本报告不把 0.45 美元每次或 46,000 美元已收当成 Clocknext 或某客户的真实账单。"),
        ],
        "price": [
            ("官方自述", "[[定价页|https://www.clocknext.com/pricing]] 2026-11-06 写年账单收入 10 万美元以内永久免费。Pro 每月 300 美元，对应 25 万美元以内。Business 每月 500 美元，对应 50 万美元以内。Premium 每月 900 美元，对应 100 万美元以内。年付节省 20%。"),
            ("待核", "超出档位后怎么计价，摘录里没有写全。国内主体能否签约未核。"),
        ],
        "signal": [
            ("事实", "134 票是榜单热度。定价页没有客户数。"),
        ],
        "cn": [
            ("待核", "Stripe、国内支付服务商和若干 AI 计费产品都存在。这次没有打开它们的价目，不并列名单充数。"),
            ("假设", "还能做的窄事是「一次 Agent 任务对应一笔客户费用」的周报，而不是再做一个发票产品。"),
        ],
        "wedge": [
            ("建议", "只服务一个自己的 Agent。定义一个 outcome，例如成功生成一份报告。每周对比模型发票和向用户收取的套餐。"),
        ],
        "mvp": [
            ("建议", "一张表，四周数据。列是调用次数、供应商费用、向客户收取的金额、毛利。"),
            ("不做", "不做支付牌照范围内的事。不抄首页示例数字当案例。不在没有第二家客户时做通用计费平台。"),
        ],
        "check": [
            ("建议", "成功是这张表连续四周和供应商发票对得上，误差来源能指出来，并且有一个外部团队要同样的表。"),
            ("建议", "停止条件是四周后仍然只有自己的产品在用，或者对账每周超过半天。"),
        ],
        "money": [
            ("事实", "官网用账单收入分档，入门是 0 美元直到 10 万美元。134 票不是收入。"),
            ("建议", "内容可以讲一张毛利表。付费要等外部团队愿意把供应商发票交给你。"),
        ],
        "risk": [
            ("风险", "计费错误会直接多收费或少收费。用量日志含客户数据。年付 20% 是定价页句子，和别处转述的折扣不要混用。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[首页|https://www.clocknext.com/]]，[[定价页|https://www.clocknext.com/pricing]]，" + BOARD + "。Product Hunt 403，不采用。"),
        ],
    }),
)

entry(
    slug="rerun",
    panel="jm-phd",
    rank="05",
    href="https://www.producthunt.com/products/rerun-2",
    name="Rerun",
    board_line="AI 产品榜单 · 日 · 显示序 5 · 快照票数 190 · 分组后的显示序，不是按票数的全榜第 5",
    banner="我们没有部署，也没有开始试用。29 美元是 2026-11-06 这一次未登录打开定价页时看到的数字，响应里同时有价格实验 cookie。",
    meta="快照 2026-11-06 06:18 北京时间 · 日榜显示序 5 · 190 票 · 分组显示序 · 未部署 · 票不是留存",
    backs=backs("jm-phd", "AI 产品榜单 · 日"),
    summary=[
        {"angle": "cn", "text": "它把已有的 ChatGPT 或 Claude 订阅排成步骤可见、敏感操作要人点头的同事，扣子则是在扣子里另建 Agent 和按 CU 计费的云设备。"},
        {"angle": "min", "text": "最小可做的是一条定时任务加一次人工确认，例如每天整理邮箱草稿，用现成的自动化工具而不是自研一整套同事平台。"},
        {"angle": "go", "text": "官网写 2,000 多用户，190 票却因分组显示在第 5，这次定价页还带 price1:29 实验 cookie，都不能当成已核实的付费留存。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[rerun.build|https://rerun.build]] 写把已经购买的 ChatGPT、Claude、Grok 或 OpenRouter 模型接成会干活的 Coworker，而不是只回答的聊天机器人。首页写步骤可见，并列出销售、社群、支持和助理等角色。"),
            ("事实", "情报站在效率分组里把它显示为第 5，票数 190。190 高于同页显示序 2 的 158、序 3 的 156 和序 4 的 134。页面说明日榜按类别分组。因此 190 票不是「官方绝对第 5」。"),
        ],
        "who": [
            ("官方自述", "给已经有模型订阅、想把重复工作交给可排班流程的人。首页引用了两位使用者的话。那是官网选登的引言，我们没有联系他们。"),
        ],
        "flow": [
            ("官方自述", "定价页写先 5 天试用，再按 Coworker 数量选择。Coworker 使用你已有的模型。敏感操作需要人回答。具体工具列表我们没有在登录后核对。"),
            ("官方自述", "首页和定价页都写现在以 AGPL-3.0 开源。我们没有克隆仓库，开源范围以他们给出的仓库为准，仓库地址这次没有从定价页正文里单独摘出，待核。"),
        ],
        "price": [
            ("事实", "2026-11-06 未登录请求 [[定价页|https://rerun.build/pricing]] 返回 200。正文写 5 天 0 美元试用，取消则不收费。随后看到 5 个 Coworker 每月 29 美元、席位不按人加价、每月 500 credits。同一次响应设置 cookie rerun-ab=price1:29。"),
            ("假设", "这个 cookie 像价格实验。其他访客可能看到别的数字。不能把 29 美元写成唯一官价。"),
            ("待核", "加 5 个 Coworker 是否另加 10 美元、credits 加购是否 10 美元，摘录里有这些句子，但是否随实验变化没有第二组对照。我们没有付款。"),
        ],
        "signal": [
            ("官方自述", "首页写 2,000+ users trust Rerun。这是营销句。"),
            ("事实", "情报站给出 190 票。没有独立留存、试用转付费或自托管部署数。"),
        ],
        "cn": [
            ("事实", "扣子的云设备和任务跑在扣子的计费里，文档按 CU·天结算。Rerun 的首页强调接上你已经付费的 ChatGPT 或 Claude 订阅。一个要换到对方的 Agent 运行时，一个声称留在你现有的模型账单上。我们没有两边各跑同一条任务。"),
            ("待核", "影刀一类 RPA 是否已有「人工点头再继续」的模板，这次没有打开他们的文档，不写功能对等。"),
        ],
        "wedge": [
            ("建议", "只包一条已经有人每周手工做的流程。定时运行，遇到发信或付款就停下来等人点。不做 3,000 个集成。首页写 3,000+ integrations，那是官网数字，我们没有点数。"),
        ],
        "mvp": [
            ("建议", "用现成自动化工具做「每天收集邮箱草稿，生成一封待发信，人点头才发送」。记录一周里点头几次、拒绝几次。"),
            ("不做", "不自托管一套 AGPL 平台当代工，除非先读完许可并确认能公开修改。不把 29 美元印成自己的价目。"),
        ],
        "check": [
            ("建议", "成功是同一个五人小组连续两周使用，并且至少三次拒绝了不该发出的信。"),
            ("建议", "停止条件是大家仍然回到聊天窗口里复制粘贴，定时任务每周被关掉。"),
        ],
        "money": [
            ("事实", "这次看到的云价格是试用后每月 29 美元起，且可能只是实验臂。开源许可是页面上的 AGPL-3.0。190 票高于若干排在它前面的产品。"),
            ("建议", "内容可以讲「订阅还在、步骤看得见」。收费要等两周的点头记录，而不是等票数。"),
        ],
        "risk": [
            ("风险", "AGPL 的网络服务义务要以许可原文为准，我们没有做法务结论。Coworker 能操作的工具越多，误发和误删的面越大。价格实验使对外报价容易抄错。官网用户数不可直接引用为留存。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[rerun.build|https://rerun.build]]，[[定价页|https://rerun.build/pricing]]，[[扣子云设备|https://docs.coze.cn/coze_pro_cloud_device_fee]]，" + BOARD + "。Product Hunt 403，不采用。价格实验只记录了这一次响应的 cookie。"),
        ],
    }),
)

entry(
    slug="beacon",
    panel="jm-ph",
    rank="01",
    href="https://www.producthunt.com/products/asymptotelabs",
    name="beacon.sh",
    board_line="AI 产品榜单 · 周 · 显示序 1 · 快照本周票 429 · 范围 2026-11-02～2026-11-05 · 这是周榜合并后的显示序，不是日榜名次",
    banner="我们没有安装 Beacon，也没有登录 beacon.sh。下面的免费档和月费是 2026-11-06 定价页静态文本里的句子。",
    meta="快照 2026-11-06 06:18 北京时间 · 周榜显示序 1 · 本周票 429 · 未实测 · 票不是付费席位",
    backs=[
        ("../../index.html#jm-ph", "返回 AI 产品周榜"),
        ("../../2026-11-06.html#jm-ph", "返回 2026-11-06 快照的周榜"),
    ],
    summary=[
        {"angle": "cn", "text": "它跨 Claude Code、Cursor、Codex 等工具收会话并收成可复用技能，和只留在本机 SQLite 的 silo-memory 不是同一条安装路径。"},
        {"angle": "min", "text": "最小可做的是一个仓库在会话结束时写 markdown，下一次换工具先读这份文件，先不做云端技能市场。"},
        {"angle": "go", "text": "定价页写可以 0 美元开始，失忆对比容易做成演示，周榜 429 票和 GitHub 上 3,314 星都不是付费人数。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[beacon.sh|https://beacon.sh/]] 写把 Claude Code、Cursor、Codex、OpenCode 等 20 多种工具的会话变成可累积的知识，让下一个 Agent 不用从头学。"),
            ("事实", "情报站周榜显示序 1，本周票 429。原链是 Product Hunt 的 asymptotelabs。该页本次不作为正文来源。仓库是 [[Asymptote-Labs/agent-beacon|https://github.com/Asymptote-Labs/agent-beacon]]。"),
        ],
        "who": [
            ("官方自述", "给同时用多款编程 Agent、希望纠正和调试路径能跨工具留下的人。README 写一个 Agent 解决过的问题不必让另一个从头再学。"),
        ],
        "flow": [
            ("官方自述", "首页把流程写成三步。先留下提示、工具调用、修改和结果。再从成功会话里抽出可复用技能。人看过之后，以后的 Agent 用 MCP 或 Agent Skills 取回。"),
            ("事实", "2026-11-06 的 [[GitHub API|https://api.github.com/repos/Asymptote-Labs/agent-beacon]] 返回 MIT，公开星 3,314，fork 292，语言 Go。星不是安装数。"),
        ],
        "price": [
            ("官方自述", "[[定价页|https://beacon.sh/pricing]] 的静态文本写开始是 0 美元。Beacon Cloud Pro 按年计费写着每月 20 美元，并写省 25%。团队档写着每席每月 30 美元，同样注明按年计费。页面上还有 Loading 字样，结账时数字可能不同。我们没有下单。"),
            ("待核", "本地安装是否完全不要账号，以 README 的安装段为准。这次没有逐步点完安装器。"),
        ],
        "signal": [
            ("事实", "周榜 429 票来自情报站，范围是 2026-11-02 到 2026-11-05 的最高日榜票，不是我们数出来的一周用户。API 星数是同日抽样。"),
        ],
        "cn": [
            ("事实", "[[silo-memory|https://pypi.org/project/silo-memory/]] 写记忆留在本机，用 SQLite 做检索，不把原文送到外部服务。它没有 Beacon 这种跨工具抽技能再放回 MCP 的描述。"),
            ("事实", "claude-mem 的安装说明会引导浏览器登录，并有 30 天试用。Beacon 的差异写在跨工具会话和技能复用。我们没有并排安装。"),
        ],
        "wedge": [
            ("建议", "只做中文项目的一份会话结束摘要，文件留在仓库里。下一次无论用 Cursor 还是 Claude Code，都先读这份文件。"),
        ],
        "mvp": [
            ("建议", "一个仓库，五天，每天一份 markdown。内容只保留决定和踩坑，不上传。"),
            ("不做", "不做托管技能市场，不宣称比 Beacon 更懂全部工具，不把 429 票写成用户数。"),
        ],
        "check": [
            ("建议", "成功是换了一款编程工具之后，仍能靠那份 markdown 少解释一遍目录约定，并且文件里没有密钥。"),
            ("建议", "停止条件是每天都要手改摘要，或者一次把令牌写进了文件。"),
        ],
        "money": [
            ("事实", "页面写 0 美元可以开始。Pro 的 20 美元是年付价目上的静态文本。429 票不是席位。"),
            ("建议", "可以做一条「两个工具共享一份项目记忆」的演示。收费要等有人连续五天留下文件。"),
        ],
        "risk": [
            ("风险", "会话里有命令和密钥。云档把记录交给对方。定价页的 Loading 说明标价可能还没定死。和 claude-mem、Silo 挤在同一类需求里。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[beacon.sh|https://beacon.sh/]]，[[定价页|https://beacon.sh/pricing]]，[[仓库|https://github.com/Asymptote-Labs/agent-beacon]]，[[API|https://api.github.com/repos/Asymptote-Labs/agent-beacon]]，[[silo-memory|https://pypi.org/project/silo-memory/]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="wanaka",
    panel="jm-ph",
    rank="02",
    href="https://www.producthunt.com/products/wanaka-studio",
    name="Wanaka Studio",
    board_line="AI 产品榜单 · 周 · 显示序 2 · 快照本周票 421 · 范围 2026-11-02～2026-11-05",
    banner="我们没有打开 Wanaka 的工作室，也没有发布游戏。定价页能打开，但这次读到的 HTML 里没有具体月费数字。",
    meta="快照 2026-11-06 06:18 北京时间 · 周榜显示序 2 · 本周票 421 · 未实测 · 票不是玩家数",
    backs=[
        ("../../index.html#jm-ph", "返回 AI 产品周榜"),
        ("../../2026-11-06.html#jm-ph", "返回 2026-11-06 快照的周榜"),
    ],
    summary=[
        {"angle": "cn", "text": "扣子编程文档写可以用对话做网页应用，例子里包括网页版互动游戏并按访问的算力和流量收费，Wanaka 首页写的则是浏览器里可玩的 3D，并一键给出链接。"},
        {"angle": "min", "text": "最小可做的是用现成网页模板改一个玩法再发出链接，不自研 3D 引擎，也不承诺自动绑骨。"},
        {"angle": "go", "text": "游戏演示很容易带来播放，定价页只写了可以免费开始和年付送两个月，具体月费这次没有读到，421 票也不是留存。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[wanaka.app|https://wanaka.app/]] 写用一句话做可玩的 3D 游戏，在浏览器里打开链接就能玩，不要求会写代码。FAQ 写描述需求后由创作 Agent 一起做，也可以自己改。"),
            ("事实", "情报站周榜显示序 2，本周票 421。卡片原链是 Product Hunt。情报站简介还写了可视化编辑器、自动绑骨、多人联机和一键发布。这些句子在情报站卡片上，Wanaka 首页这次读到的是角色、动画、界面和分享链接，自动绑骨没有在首页摘录里再次出现，所以绑骨能力待核。"),
        ],
        "who": [
            ("官方自述", "给想做赛车、射击、平台、塔防、多人竞技或城市建造，但不写代码的人。作品在现代浏览器里玩。"),
        ],
        "flow": [
            ("官方自述", "描述想法，Agent 分步做出可玩版本，然后用链接分享。[[eval.wanaka.app|https://eval.wanaka.app/]] 把角色分成三块。人定风格和手感，Agent 拆步骤并改逻辑，引擎负责实时预览、物理和发布。我们没有走完一条创作。"),
        ],
        "price": [
            ("官方自述", "[[定价页|https://wanaka.app/pricing]] 2026-11-06 返回 200。读到的文字是可以免费开始做游戏，月付和年付切换，年付写着送两个月。具体每一档多少钱没有出现在这次抓到的 HTML 里。"),
            ("待核", "不把缺失的数字补成价格。结账页没有打开。"),
        ],
        "signal": [
            ("事实", "421 票是情报站周榜上的最高日榜票，范围 2026-11-02 到 2026-11-05。没有公开的付费创作者数或次日仍在玩的人数。"),
        ],
        "cn": [
            ("事实", "[[扣子编程的网页应用文档|https://docs.coze.cn/guides_vibe_coding_web_app]] 写在网页里对话完成应用，例子包含网页版互动游戏，然后部署成线上地址。费用是编程对话积分，加上 [[托管费|https://docs.coze.cn/coze_pro_service_hosting_fee]]。托管按算力秒数和流量计，算力写着 0.0072 积分每 CU 每秒，或 0.00018 元每 CU 每秒。没人访问不计托管费。"),
            ("假设", "差别在 3D 引擎和浏览器即玩，而不在「国内没有人用 AI 做游戏」。这个判断还没被玩家验证。"),
        ],
        "wedge": [
            ("建议", "只做一个浏览器里能点的小玩法，用现成网页托管发出链接。第一屏写清楚这不是 3D 引擎。"),
        ],
        "mvp": [
            ("建议", "一个周末做完的网页小游戏，加一段 30 秒屏幕录像。"),
            ("不做", "不自研物理和多人同步。不引用我们没在首页读到的「省 80% token」一类对比。"),
        ],
        "check": [
            ("建议", "成功是 10 个朋友能打开链接玩完一局，并且其中 3 人第二天还打开。"),
            ("建议", "停止条件是链接打不开，或大家只看录像、不玩。"),
        ],
        "money": [
            ("事实", "能确认的只有免费开始和年付送两个月。421 票不是收入。"),
            ("建议", "录像可以发。收费要等有人玩到第二天，再决定要不要做素材包。"),
        ],
        "risk": [
            ("风险", "3D 和多人是重资产。生成内容有版权和适龄问题。价格没读到就不能对外报价。扣子的网页游戏和它不是同一套引擎，不能说成已经覆盖。"),
        ],
        "sources": [
            ("事实", "2026-11-06 HTTP 200。[[wanaka.app|https://wanaka.app/]]，[[定价页|https://wanaka.app/pricing]]，[[eval.wanaka.app|https://eval.wanaka.app/]]，[[扣子网页应用|https://docs.coze.cn/guides_vibe_coding_web_app]]，[[扣子托管费|https://docs.coze.cn/coze_pro_service_hosting_fee]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="floot",
    panel="jm-ph",
    rank="03",
    href="https://www.producthunt.com/products/floot",
    name="Floot Payments",
    board_line="AI 产品榜单 · 周 · 显示序 3 · 快照本周票 319 · 范围 2026-11-02～2026-11-05 · 卡片简介写的是不离开 ChatGPT 就能做并发布应用",
    banner="我们没有连接 Floot，也没有用测试卡付款。抽成来自 2026-11-06 能打开的支付文档。月费数字没有读到。",
    meta="快照 2026-11-06 06:18 北京时间 · 周榜显示序 3 · 本周票 319 · 未开通 · 票不是成交额",
    backs=[
        ("../../index.html#jm-ph", "返回 AI 产品周榜"),
        ("../../2026-11-06.html#jm-ph", "返回 2026-11-06 快照的周榜"),
    ],
    summary=[
        {"angle": "cn", "text": "支付文档写在 ChatGPT 或 Claude 里做应用，预览用测试卡，真正收款要 Pro 或 Power 且 Pro 对每笔抽 1%，扣子编程则是在自己的网页里做应用再按 CU·秒托管。"},
        {"angle": "min", "text": "最小可做的是给一个自己的页面接一笔测试收款并记到表里，先不要做整套应用托管。"},
        {"angle": "go", "text": "不离开聊天就发布，演示很短，319 票不是流水，月费这次没在定价页正文里读到，不能把 1% 说成订阅价。"},
    ],
    sections=blocks({
        "what": [
            ("官方自述", "[[floot.com|https://floot.com/]] 写把 Floot 加到 Claude、ChatGPT 或 Cursor，用对话做出带后端、数据库和托管的应用，然后发布。情报站卡片的名字是 Floot Payments，简介是不离开 ChatGPT 就能做并发布真实 App。"),
            ("事实", "周榜显示序 3，本周票 319。原链是 Product Hunt 的 floot。"),
        ],
        "who": [
            ("官方自述", "给已经在用 Claude 或 ChatGPT、想让聊天结果变成一个带登录和收款的线上应用的人。文档写构建跑在 Floot 的服务器上，本机没有 CLI，也没有要克隆的仓库。"),
        ],
        "flow": [
            ("官方自述", "[[支付文档|https://floot.com/docs/integrations/payments]] 写让助手加上结账。预览用 Stripe 测试卡 4242，不发生真钱，任何档包括 Free 都可以试。发布后的真收款进入你自己的 Stripe。只有项目所有者能接 Stripe。"),
            ("官方自述", "[[从聊天构建的文档|https://floot.com/docs/integrations/build-from-claude-and-chatgpt]] 写 ChatGPT 默认每次动作都要批准，构建会因此频繁停下，可以改成允许全部动作。这是权限选择，我们没有打开那个开关。"),
        ],
        "price": [
            ("官方自述", "支付文档的表写 Free 只能测试、不能真收款，抽成没有。Pro 可以真收款，Floot 抽每笔 1%。Power 可以真收款，Floot 抽成 0%。Stripe 自己的手续费另计。抽成在订阅开始时定下。"),
            ("待核", "https://floot.com/pricing 这次打开后几乎没有正文，月费没有读到。不把 1% 写成月费。首页写 Backed by Y Combinator 的字样在抓取里被截成 Y Combi，批次待核。"),
        ],
        "signal": [
            ("事实", "319 票是情报站周榜数字。没有公开的 Pro 订阅数或支付流水。"),
        ],
        "cn": [
            ("事实", "[[扣子编程网页应用|https://docs.coze.cn/guides_vibe_coding_web_app]] 写在扣子网页里对话完成应用并部署。[[托管费|https://docs.coze.cn/coze_pro_service_hosting_fee]] 按访问时长的算力和流量结算，算力 0.0072 积分每 CU 每秒。它不写停在 ChatGPT 里、用你的 Claude 订阅来构建，也不写对 Stripe 每笔抽 1%。"),
            ("假设", "若要做国内切口，更像给已有页面加一笔国内支付的测试单，而不是再做一个聊天里的全栈托管。"),
        ],
        "wedge": [
            ("建议", "只服务一个自己的报名页。测试环境记下一笔收款，字段是谁、金额、时间。"),
        ],
        "mvp": [
            ("建议", "一张表加一个测试支付。不发布到应用商店。"),
            ("不做", "不代接别人的 Stripe 密钥。不承诺和 Floot 一样能在聊天里生成数据库。不做支付牌照范围内的资金池。"),
        ],
        "check": [
            ("建议", "成功是测试支付能在表里对上，并且有第二个自己的页面愿意用同一条路。"),
            ("建议", "停止条件是对账对不上，或需求变成代收别人的钱。"),
        ],
        "money": [
            ("事实", "能确认的价格是真收款时 Pro 抽 1%、Power 抽 0%，外加 Stripe 手续费。319 票不是流水。月费待核。"),
            ("建议", "演示可以是一次从聊天到测试卡的录屏。收费要等第二张自己的页面接上。"),
        ],
        "risk": [
            ("风险", "真收款涉及主体、结算和退款。文档写允许全部动作会让聊天里的工具少一次确认。国内支付和微信、支付宝这次没有在 Floot 文档里读到，不能写成已经支持。"),
        ],
        "sources": [
            ("事实", "2026-11-06 用浏览器标头打开为 HTTP 200。[[floot.com|https://floot.com/]]，[[支付文档|https://floot.com/docs/integrations/payments]]，[[从聊天构建|https://floot.com/docs/integrations/build-from-claude-and-chatgpt]]，[[扣子网页应用|https://docs.coze.cn/guides_vibe_coding_web_app]]，[[扣子托管费|https://docs.coze.cn/coze_pro_service_hosting_fee]]，" + BOARD + "。"),
        ],
    }),
)

entry(
    slug="glasshand",
    panel="jm-ph",
    rank="04",
    href="https://www.producthunt.com/products/glasshand",
    name="Glasshand",
    board_line="AI 产品榜单 · 周 · 显示序 4 · 快照本周票 293 · 范围 2026-11-02～2026-11-05 · 与日榜 293 是同一笔最高日票，不是另一套计数",
    meta="快照 2026-11-06 06:18 北京时间 · 周榜显示序 4 · 本周票 293 · 与日榜同一笔最高日票 · 未租用 · 票不是续租人数",
    backs=[
        ("../../index.html#jm-ph", "返回 AI 产品周榜"),
        ("../../2026-11-06.html#jm-ph", "返回 2026-11-06 快照的周榜"),
    ],
    summary=[
        {"angle": "cn", "text": "周榜这张仍是独占 iPhone 或 Mac 的月租，和扣子按 CU·天的云手机、UBox 按时长调度的真机池不是同一张账单。"},
        {"angle": "min", "text": "最小可做的还是一台自己的闲置安卓加投屏，不因为周榜更靠前就去采购苹果库存。"},
        {"angle": "go", "text": "这里的显示序是 4，本周票 293，和日榜第 1 名的 293 是同一笔最高日票，录屏仍容易带来播放，擦除是否彻底没有验证。"},
    ],
)

entry(
    slug="pushary",
    panel="jm-ph",
    rank="05",
    href="https://www.producthunt.com/products/pushary",
    name="Pushary for Teams",
    board_line="AI 产品榜单 · 周 · 显示序 5 · 快照本周票 158 · 范围 2026-11-02～2026-11-05 · 与日榜 158 是同一笔最高日票。同页第 6 名 AgentKit 票数更高，因为周榜按类别分组",
    meta="快照 2026-11-06 06:18 北京时间 · 周榜显示序 5 · 本周票 158 · 与日榜同一笔最高日票 · 未开通 · 票不是付费席位",
    backs=[
        ("../../index.html#jm-ph", "返回 AI 产品周榜"),
        ("../../2026-11-06.html#jm-ph", "返回 2026-11-06 快照的周榜"),
    ],
    summary=[
        {"angle": "cn", "text": "周榜这张仍是把编码 Agent 的提问送到手机或 Mac 并留下谁点了同意，飞书和企微的审批文档这次依然没打开，不能写成已经核实的同类账本。"},
        {"angle": "min", "text": "最小可做的仍是只拦截 git push 和对外发信，把同意写进一张表，给一个五人小组用两周。"},
        {"angle": "go", "text": "显示序是 5，本周票 158，和日榜第 2 名是同一笔最高日票，官网团队价仍是 5 人每月 59 美元，演示短，人民币结账待核。"},
    ],
)
