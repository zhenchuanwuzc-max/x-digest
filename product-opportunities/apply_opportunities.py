#!/usr/bin/env python3
"""Inject the 2026-11-06 product-board opportunity notes and write their pages.

The daily publisher is not in this repo. Run this after a publisher writes HTML.
A page without this snapshot's marker is left unchanged, so a later ranking
cannot inherit these notes.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from snapshot_2026_11_06 import DATA  # noqa: E402

ROOT = HERE.parents[0]
REPORT_DIR = HERE / "reports"
RESEARCH_DIR = HERE / "research"
DATE_RE = re.compile(r"更新于 (\d{4}-\d{2}-\d{2})")
TOP_RANKS = {"01", "02", "03", "04", "05", "1", "2", "3", "4", "5"}
CSS_START = "/* product-opportunities:start */"
CSS_END = "/* product-opportunities:end */"
LINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")
REQUIRED = [
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
CARD_CSS = f"""{CSS_START}
.opp{{grid-column:1 / -1;margin-top:10px;padding-top:8px;border-top:1px dashed var(--line);font-size:13.5px;line-height:1.65;color:var(--ink-2);overflow-wrap:anywhere;word-break:break-word}}
.opp p{{margin:0 0 6px}}
.opp-meta{{font-size:12px;color:var(--ink-4);margin:0 0 4px}}
.opp-more{{color:var(--accent-ink);font-weight:650}}
{CSS_END}"""
REPORT_CSS = """
:root{
  --bg:#faf9f6;--surface:#fff;--ink:#202a30;--ink-2:#303c42;--ink-3:#59656b;--ink-4:#657176;
  --line:#dfe4e1;--accent:#176b75;--accent-ink:#145f68;--accent-soft:rgba(23,107,117,.08);
  --amber:#7c5a24;--amber-soft:rgba(184,135,58,.12);--hot:#b3402a;
  --font:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.7}
body{overflow-x:hidden}
a{color:var(--accent-ink)}
.page{max-width:1120px;margin:0 auto;padding:20px 16px 72px}
.back{display:inline-block;margin:0 16px 8px 0;font-weight:650;text-decoration:none}
.back:hover{text-decoration:underline}
.kicker{color:var(--ink-3);font-size:13px;margin:8px 0}
h1{font-size:28px;line-height:1.3;margin:8px 0 8px}
.banner{background:var(--amber-soft);border:1px solid #e4d3ae;border-radius:12px;padding:10px 14px;margin:12px 0 18px}
.shell{display:block}
.toc{margin:0 0 18px;padding:0}
.toc strong{display:block;font-size:13px;letter-spacing:.04em;color:var(--ink-4);margin-bottom:6px}
.toc a{display:block;padding:3px 0;text-decoration:none;overflow-wrap:anywhere}
.toc a:hover{text-decoration:underline}
main{min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:8px 18px 28px}
section{scroll-margin-top:16px;padding-top:8px;border-top:1px solid var(--line)}
section:first-child{border-top:0}
h2{font-size:18px;margin:16px 0 8px}
p{margin:0 0 10px;overflow-wrap:anywhere;word-break:break-word}
.kind{display:inline-block;font-size:12px;font-weight:700;color:var(--accent-ink);background:var(--accent-soft);border-radius:999px;padding:0 8px;margin-right:6px;vertical-align:1px}
.kind.warn{color:var(--amber);background:var(--amber-soft)}
.kind.stop{color:var(--hot);background:rgba(179,64,42,.08)}
@media (min-width:960px){
  .shell{display:grid;grid-template-columns:220px minmax(0,720px);gap:28px;align-items:start;justify-content:center}
  .toc{position:sticky;top:16px}
  main{padding:8px 28px 36px}
}
"""


def render_text(text: str, blank_external: bool = True) -> str:
    parts = []
    pos = 0
    for match in LINK_RE.finditer(text):
        parts.append(html.escape(text[pos : match.start()]))
        label, url = match.group(1), match.group(2)
        if not (url.startswith("https://") or url.startswith("../../") or url.startswith("#")):
            raise ValueError(f"refused url {url}")
        attrs = ' target="_blank" rel="noopener"' if blank_external and url.startswith("https://") else ""
        parts.append(f'<a href="{html.escape(url, quote=True)}"{attrs}>{html.escape(label)}</a>')
        pos = match.end()
    parts.append(html.escape(text[pos:]))
    return "".join(parts)


def kind_class(kind: str) -> str:
    if kind in {"假设", "建议", "待核"}:
        return "kind warn"
    if kind in {"不做", "风险"}:
        return "kind stop"
    return "kind"


def groups(entries):
    grouped = {}
    for entry in entries:
        grouped.setdefault(entry["slug"], []).append(entry)
    return grouped


def validate(data: dict) -> None:
    ids = [item[0] for item in REQUIRED]
    grouped = groups(data["entries"])
    seen = set()
    for entry in data["entries"]:
        key = (entry["panel"], entry["rank"], entry["href"])
        if key in seen:
            raise SystemExit(f"duplicate card {key}")
        seen.add(key)
        sentences = entry["summary"]
        if not 2 <= len(sentences) <= 4:
            raise SystemExit(f"{entry['slug']} summary must be 2 to 4 sentences")
        angles = {item["angle"] for item in sentences}
        if not {"cn", "min", "go"} <= angles:
            raise SystemExit(f"{entry['slug']} summary is missing an angle")
        for sentence in sentences:
            if sentence["text"].count("。") != 1 or not sentence["text"].endswith("。"):
                raise SystemExit(f"{entry['slug']} sentence must be exactly one sentence")
    for slug, group in grouped.items():
        bodies = [entry for entry in group if entry.get("sections")]
        if len(bodies) != 1:
            raise SystemExit(f"{slug} needs exactly one report body")
        got = [block["id"] for block in bodies[0]["sections"]]
        if got != ids:
            raise SystemExit(f"{slug} sections are {got}")
        for block in bodies[0]["sections"]:
            if not block["paragraphs"]:
                raise SystemExit(f"{slug} {block['id']} is empty")


def ordered_group(group):
    priority = {"jm-ph": 0, "jm-ghw": 1, "jm-phd": 2}
    return sorted(group, key=lambda entry: priority.get(entry["panel"], 9))


def report_html(entry: dict, group=None) -> str:
    group = ordered_group(group or [entry])
    toc = "\n".join(
        f'<a href="#{section_id}">{html.escape(title)}</a>' for section_id, title in REQUIRED
    )
    body = []
    for block in entry["sections"]:
        chunks = [f'<section id="{block["id"]}"><h2>{html.escape(block["title"])}</h2>']
        for paragraph in block["paragraphs"]:
            chunks.append(
                f'<p><span class="{kind_class(paragraph["kind"])}">{html.escape(paragraph["kind"])}</span>{render_text(paragraph["text"])}</p>'
            )
        chunks.append("</section>")
        body.append("".join(chunks))
    banner = entry["banner"] if "未实测" in entry["banner"] else "未实测。" + entry["banner"]
    backs = []
    seen_hrefs = set()
    for item in group:
        for href, label in item["backs"]:
            if href in seen_hrefs:
                continue
            seen_hrefs.add(href)
            backs.append(f'<a class="back" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
    board_line = " ".join(item["board_line"] for item in group)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(entry["name"])} · 机会报告 · 2026-11-06</title>
<style>{REPORT_CSS}</style>
</head>
<body>
<div class="page">
<p class="kicker">X 情报 · 产品榜单机会报告 · 快照 2026-11-06 06:18 北京时间</p>
{''.join(backs)}
<h1>{html.escape(entry["name"])}</h1>
<p class="kicker">{html.escape(board_line)}</p>
<div class="banner">{html.escape(banner)}</div>
<div class="shell">
<nav class="toc" aria-label="目录"><strong>目录</strong>{toc}</nav>
<main>
{''.join(body)}
</main>
</div>
</div>
</body>
</html>
"""


def card_block(item: dict, page_date: str) -> str:
    summary = "".join(html.escape(sentence) for sentence in item["summary"])
    meta = item.get("meta") or ""
    verified = item.get("verified_on") or ""
    if item["status"] == "reuse" and verified and verified != page_date and verified not in meta:
        meta = f"核验于 {verified}，不是 {page_date} 的新核验。{meta}"
    link = ""
    report_name = item.get("report") or ""
    report_ok = report_name.endswith(".html") and "/" not in report_name and (REPORT_DIR / report_name).is_file()
    if item["status"] in {"ready", "reuse"} and report_ok:
        link = f'<a class="opp-more" href="product-opportunities/reports/{html.escape(report_name, quote=True)}">详细报告</a>'
    elif item["status"] in {"ready", "reuse"}:
        if "报告未挂上" not in meta:
            meta = (meta + " 报告文件不在这次发布里，没有链接。").strip()
    return (
        f'<div class="opp" data-opp="{html.escape(item["product"], quote=True)}" '
        f'data-snapshot="{html.escape(page_date, quote=True)}">'
        f"<p>{summary}</p>"
        f'<p class="opp-meta">{html.escape(meta)}</p>'
        f"{link}"
        f"</div>"
    )


def pending_block(page_date: str) -> str:
    return (
        f'<div class="opp" data-opp="pending" data-snapshot="{html.escape(page_date, quote=True)}">'
        f"<p>这张卡片在 {html.escape(page_date)} 的研究里还没有核验。待研究。</p>"
        f'<p class="opp-meta">未核验 · 没有详细报告</p>'
        f"</div>"
    )


def upsert_css(page: str) -> str:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.S)
    if pattern.search(page):
        return pattern.sub(CARD_CSS, page, count=1)
    marker = "</style>"
    at = page.find(marker)
    if at < 0:
        raise ValueError("page has no style block")
    return page[:at] + CARD_CSS + page[at:]


def panel_window(page: str, panel: str) -> tuple[int, int]:
    token = f'id="{panel}"'
    start = page.find(token)
    if start < 0:
        raise ValueError(f"missing panel {panel}")
    end = page.find('id="', start + len(token))
    if end < 0:
        end = len(page)
    return start, end


def split_cards(page: str, panel: str):
    start, end = panel_window(page, panel)
    needle = '<li class="mc">'
    pieces = page[start:end].split(needle)
    cards = []
    for index, piece in enumerate(pieces[1:], start=1):
        card, sep, rest = piece.partition("</li>")
        if sep != "</li>":
            continue
        href_match = re.search(r'<h3><a href="([^"]+)"', card)
        rank_match = re.search(r'<span class="hk">(\d+)', card)
        cards.append(
            {
                "index": index,
                "card": card,
                "rest": rest,
                "href": href_match.group(1) if href_match else "",
                "rank": rank_match.group(1) if rank_match else "",
            }
        )
    return start, end, needle, pieces, cards


def join_cards(pieces, cards) -> str:
    needle = '<li class="mc">'
    by_index = {card["index"]: card for card in cards}
    rebuilt = [pieces[0]]
    for index, piece in enumerate(pieces[1:], start=1):
        card = by_index.get(index)
        if card is None:
            rebuilt.append(piece)
            continue
        rebuilt.append(card["card"] + "</li>" + card["rest"])
    return needle.join(rebuilt)


def strip_opp(card: str) -> str:
    return re.sub(r'<div class="opp" data-opp="[^"]*" data-snapshot="[^"]*">.*?</div>', "", card, flags=re.S)


def apply_research(page: str, research: dict) -> tuple[str, list[str]]:
    page_date = research["date"]
    notes = []
    covered = {panel: set() for panel in research["boards"]}
    updated = page
    for item in research["items"]:
        panel = item["panel"]
        if f'id="{panel}"' not in updated:
            notes.append(f"skip missing-panel {item['product']} {panel}")
            continue
        start, end, needle, pieces, cards = split_cards(updated, panel)
        matched = [card for card in cards if card["href"] == item["match_href"]]
        if not matched:
            notes.append(f"skip missing-link {item['product']} {panel}")
            continue
        for card in matched:
            card["card"] = strip_opp(card["card"]) + card_block(item, page_date)
            covered.setdefault(panel, set()).add(card["href"])
        updated = updated[:start] + join_cards(pieces, cards) + updated[end:]
    for panel in research["boards"]:
        if f'id="{panel}"' not in updated:
            continue
        start, end, needle, pieces, cards = split_cards(updated, panel)
        known = covered.get(panel, set())
        for card in cards:
            if card["rank"] not in TOP_RANKS or card["href"] in known or not card["href"]:
                continue
            if 'class="opp"' in card["card"]:
                continue
            card["card"] = card["card"] + pending_block(page_date)
            notes.append(f"pending {panel} {card['href']}")
        updated = updated[:start] + join_cards(pieces, cards) + updated[end:]
    return updated, notes


def page_date(path: Path, text: str) -> str | None:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem):
        return path.stem
    start = text.find('id="jm-ghw"')
    if start < 0:
        return None
    end = text.find('id="', start + 10)
    found = DATE_RE.search(text[start:end if end > start else None])
    return found.group(1) if found else None


def load_research(date: str) -> dict | None:
    path = RESEARCH_DIR / f"{date}.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("date") != date:
        raise ValueError(f"{path} date field is {data.get('date')}")
    validate_research(data)
    return data


def validate_research(data: dict) -> None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("date", "")):
        raise ValueError("research date is missing")
    boards = data.get("boards") or []
    if not boards or any(board not in {"jm-ghw", "jm-ph", "jm-phd"} for board in boards):
        raise ValueError("research boards must be GitHub weekly, AI weekly, or AI daily")
    seen = set()
    for item in data.get("items") or []:
        key = (item.get("panel"), item.get("match_href"))
        if key in seen:
            raise ValueError(f"duplicate research item {key}")
        seen.add(key)
        if item.get("panel") not in boards:
            raise ValueError(f"{item.get('product')} panel is outside boards")
        if not str(item.get("match_href", "")).startswith("https://"):
            raise ValueError(f"{item.get('product')} link is not https")
        status = item.get("status")
        summary = item.get("summary") or []
        if status == "pending":
            if item.get("report"):
                raise ValueError(f"{item.get('product')} pending item cannot name a report")
            continue
        if status not in {"ready", "reuse"}:
            raise ValueError(f"{item.get('product')} status {status}")
        if not 2 <= len(summary) <= 4 or any(sentence.count("。") != 1 or not sentence.endswith("。") for sentence in summary):
            raise ValueError(f"{item.get('product')} summary must be 2 to 4 sentences")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item.get("verified_on", "")):
            raise ValueError(f"{item.get('product')} verified_on is missing")
        report = item.get("report") or ""
        if not re.fullmatch(r"[a-z0-9-]+\.html", report):
            raise ValueError(f"{item.get('product')} report name is not a local html file")
        if status == "ready" and not item.get("sources"):
            raise ValueError(f"{item.get('product')} ready item needs sources")
        for source in item.get("sources") or []:
            if not source.startswith("https://") or " " in source:
                raise ValueError(f"{item.get('product')} source is not https")
        if status == "reuse" and item["verified_on"] > data["date"]:
            raise ValueError(f"{item.get('product')} reuse date is after the page date")


def write_reports() -> list[Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for slug, group in groups(DATA["entries"]).items():
        primary = next(entry for entry in group if entry.get("sections"))
        path = REPORT_DIR / f"{slug}.html"
        text = report_html(primary, group)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def apply_page(path: Path) -> str:
    original = path.read_text(encoding="utf-8")
    date = page_date(path, original)
    if not date:
        return "skip"
    research = load_research(date)
    if research is None:
        print(f"skip no-research {date} {path}", file=sys.stderr)
        return "skip"
    updated, notes = apply_research(original, research)
    for note in notes:
        print(note, file=sys.stderr)
    updated = upsert_css(updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return "write"
    return "same"


def default_pages() -> list[Path]:
    return [ROOT / "index.html", ROOT / "2026-11-06.html"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Mount dated product research onto digest HTML.")
    parser.add_argument("pages", nargs="*", type=Path)
    parser.add_argument("--reports-only", action="store_true")
    parser.add_argument("--check-research", metavar="DATE")
    args = parser.parse_args(argv)
    if args.check_research:
        research = load_research(args.check_research)
        if research is None:
            print(f"missing {args.check_research}", file=sys.stderr)
            return 1
        print(f"ok {args.check_research} items={len(research['items'])}")
        return 0
    if args.reports_only:
        validate(DATA)
        written = write_reports()
        print(f"reports {len(written)}")
        return 0
    pages = args.pages or default_pages()
    wrote = skipped = same = 0
    for path in pages:
        if "xhs" in path.parts:
            print(f"refuse {path}", file=sys.stderr)
            return 2
        status = apply_page(path)
        print(f"{status} {path}")
        if status == "write":
            wrote += 1
        elif status == "skip":
            skipped += 1
        else:
            same += 1
    print(f"done write={wrote} same={same} skip={skipped}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except ValueError as exc:
        print(f"error {exc}", file=sys.stderr)
        raise SystemExit(1)
