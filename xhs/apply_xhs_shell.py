#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
HUB_NAV = (
    '<details class="navg" open><summary>今天</summary>'
    '<a href="#top" data-s="top">今天一句话</a>'
    '<a href="#xhs" data-s="xhs">热词最高赞</a>'
    '<a href="#feed" data-s="feed">本日最热兴趣</a>'
    "</details>"
    '<details class="navg" open><summary>选题</summary>'
    '<a href="#picks" data-s="picks">汇总建议选题</a>'
    '<a href="#insp" data-s="insp">Ocean 灵感</a>'
    '<a href="#xdiff" data-s="xdiff">X 热帖差异化</a>'
    '<a href="#tingji" data-s="tingji">听记选题</a>'
    "</details>"
    '<details class="navg"><summary>素材与对标</summary>'
    '<a href="#lenny" data-s="lenny">Lenny</a>'
    '<a href="#deep" data-s="deep">细看</a>'
    '<a href="#raw" data-s="raw">原始数据</a>'
    '<a href="#bench" data-s="bench">对标动态</a>'
    '<a href="#profiles" data-s="profiles">对标档案</a>'
    '<a href="#growth" data-s="growth">起号与变现</a>'
    "</details>"
    '<details class="navg"><summary>库与计划</summary>'
    '<a href="#tools" data-s="tools">长驻工具</a>'
    '<a href="curriculum.html" data-s="curriculum">课表</a>'
    '<a href="#drafts" data-s="drafts">已成稿</a>'
    '<a href="#pos" data-s="pos">定位</a>'
    '<a href="#plan" data-s="plan">发布计划</a>'
    '<a href="#main" data-s="main">主线系列</a>'
    '<a href="#side" data-s="side">辅线「我学 AI」</a>'
    '<a href="#log" data-s="log">更新记录</a>'
    "</details>"
    '<div class="sec">完整页</div>'
    '<a href="growth/">成长记录专属入口 →</a>'
    '<a href="day/">往期日页归档 →</a>'
)
FLAT_NAV = re.compile(r'<div class="sec">今天</div>.*?(?=</aside>)', re.S)
LINK = re.compile(r'<link rel="stylesheet" href="[^"]+" data-xhs-shell>')


def pages():
    found = [ROOT / "index.html", ROOT / "day" / "index.html"]
    found.extend(sorted((ROOT / "day").glob("2026-*.html")))
    return found


def href_for(page):
    return "xhs-shell.css" if page.parent == ROOT else "../xhs-shell.css"


def stamp_link(html, href):
    html = LINK.sub("", html)
    needle = f'<link rel="stylesheet" href="{href}" data-xhs-shell>'
    if "</head>" not in html:
        raise SystemExit("missing </head>")
    return html.replace("</head>", needle + "</head>", 1)


def stamp_hub_nav(html):
    matches = FLAT_NAV.findall(html)
    if not matches:
        if 'details class="navg"' not in html:
            raise SystemExit("hub nav is neither flat nor grouped")
        return html
    if len(matches) != 1:
        raise SystemExit(f"expected one flat hub nav, found {len(matches)}")
    return FLAT_NAV.sub(HUB_NAV, html, count=1)


def stamp(page):
    html = page.read_text(encoding="utf-8")
    updated = stamp_link(html, href_for(page))
    if page.name == "index.html" and page.parent == ROOT:
        updated = stamp_hub_nav(updated)
    if updated != html:
        page.write_text(updated, encoding="utf-8")
        return True
    return False


def main():
    changed = [str(page.relative_to(ROOT.parent)) for page in pages() if stamp(page)]
    print("updated" if changed else "unchanged", *changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
