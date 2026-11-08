#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
HUB_GROUPS = (
    ("今天", True, ("top", "xhs", "feed")),
    ("选题", True, ("newsmall", "picks", "insp", "xdiff", "tingji")),
    ("素材与对标", False, ("lenny", "deep", "raw", "bench", "profiles", "growth")),
    ("库与计划", False, ("tools", "curriculum", "drafts", "pos", "plan", "main", "side", "log")),
)
HUB_TAIL = (
    '<div class="sec">完整页</div>'
    '<a href="growth/">成长记录专属入口 →</a>'
    '<a href="day/">往期日页归档 →</a>'
)


def shell_link(href):
    return f'<link rel="stylesheet" href="{href}" data-xhs-shell>'


def group_hub_links(items):
    known = {}
    order = {}
    n = 0
    for name, _open, ids in HUB_GROUPS:
        for i in ids:
            known[i] = name
            order[i] = n
            n += 1
    buckets = {name: [] for name, _open, _ids in HUB_GROUPS}
    unknown = []
    for item in items:
        group = known.get(item[0])
        if group is None:
            unknown.append(item)
        else:
            buckets[group].append(item)
    buckets["今天"].extend(unknown)
    parts = []
    for name, is_open, _ids in HUB_GROUPS:
        rows = sorted(buckets[name], key=lambda it: (order.get(it[0], n), it[0]))
        if not rows:
            continue
        body = "".join(
            f'<a href="{href}" data-s="{i}">{label}</a>' for i, label, href in rows
        )
        opened = " open" if is_open else ""
        parts.append(f'<details class="navg"{opened}><summary>{name}</summary>{body}</details>')
    return "".join(parts)


def _shipped_entries():
    return [
        ("top", "今天一句话", "#top"),
        ("xhs", "热词最高赞", "#xhs"),
        ("feed", "本日最热兴趣", "#feed"),
        ("picks", "汇总建议选题", "#picks"),
        ("insp", "Ocean 灵感", "#insp"),
        ("xdiff", "X 热帖差异化", "#xdiff"),
        ("tingji", "听记选题", "#tingji"),
        ("lenny", "Lenny", "#lenny"),
        ("deep", "细看", "#deep"),
        ("raw", "原始数据", "#raw"),
        ("bench", "对标动态", "#bench"),
        ("profiles", "对标档案", "#profiles"),
        ("growth", "起号与变现", "#growth"),
        ("tools", "长驻工具", "#tools"),
        ("curriculum", "课表", "curriculum.html"),
        ("drafts", "已成稿", "#drafts"),
        ("pos", "定位", "#pos"),
        ("plan", "发布计划", "#plan"),
        ("main", "主线系列", "#main"),
        ("side", "辅线「我学 AI」", "#side"),
        ("log", "更新记录", "#log"),
    ]


HUB_NAV = group_hub_links(_shipped_entries()) + HUB_TAIL
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
    if "</head>" not in html:
        raise SystemExit("missing </head>")
    return html.replace("</head>", shell_link(href) + "</head>", 1)


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
