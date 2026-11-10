#!/usr/bin/env python3
"""小红书热帖互动门槛（单源）。

规则（Ocean 2026-11-10）：
- 近 7 天发布：赞 ≥ 200 或 藏 ≥ 300
- 8 到 30 天发布：赞 ≥ 500 或 藏 ≥ 800
- 小号只是达标后的加分，不是入选条件
- 不够门槛的不当热帖；可进页底「观察中（未达标）」
"""
from __future__ import annotations
import re
from typing import Optional

RULE_TEXT = (
    "热帖门槛：近7天赞≥200或藏≥300；8到30天赞≥500或藏≥800。"
    "小号只是达标后的加分，不是入选条件。"
)

NEAR7_LIKES, NEAR7_COLLECTS = 200, 300
MID_LIKES, MID_COLLECTS = 500, 800

_COUNTS_RE = re.compile(
    r"赞\s*([0-9]+|未显示)[^\d藏]{0,12}藏\s*([0-9]+|未显示)"
)
_DAYS_RE = re.compile(r"(\d+)\s*天前")


def parse_int_maybe(raw: str | int | None) -> Optional[int]:
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw
    s = str(raw).strip().replace(",", "")
    if not s or s in ("未显示", "—", "-", "n/a", "N/A"):
        return None
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None


def parse_counts_text(text: str | None) -> tuple[Optional[int], Optional[int]]:
    """从「赞 12 / 藏 34 / 评 …」类原文取赞、藏；取不到则 (None, None)。"""
    if not text:
        return None, None
    m = _COUNTS_RE.search(text)
    if not m:
        return None, None
    return parse_int_maybe(m.group(1)), parse_int_maybe(m.group(2))


def age_days_from_relative(text: str | None) -> Optional[int]:
    """相对发布时间 → 天数。昨天=1；N天前=N；无法判断返回 None。"""
    if not text:
        return None
    if "昨天" in text or "昨日" in text:
        return 1
    if "今天" in text or "刚刚" in text or "小时前" in text or "分钟前" in text:
        return 0
    m = _DAYS_RE.search(text)
    if m:
        return int(m.group(1))
    return None


def meets_hot_threshold(
    likes: Optional[int],
    collects: Optional[int],
    age_days: Optional[int],
) -> bool:
    """互动门槛。年龄或两边互动都未知 → 不达标（不当热帖）。"""
    if age_days is None:
        return False
    if age_days < 0:
        return False
    lk = likes or 0
    cl = collects or 0
    if likes is None and collects is None:
        return False
    if age_days <= 7:
        return lk >= NEAR7_LIKES or cl >= NEAR7_COLLECTS
    if age_days <= 30:
        return lk >= MID_LIKES or cl >= MID_COLLECTS
    return False


def sample_meets_hot(sample: dict, *, date_fallback: str | None = None) -> bool:
    """new-small 样本：从 counts + date 字段判断是否达标热帖。"""
    likes, collects = parse_counts_text(sample.get("counts") or "")
    age = age_days_from_relative(sample.get("date") or date_fallback or "")
    return meets_hot_threshold(likes, collects, age)


def empty_hot_html() -> str:
    return (
        '<div class="card verdict">'
        '<p class="lead"><b>今天没有达标热帖。</b>'
        "本窗口读到的帖子都没过互动门槛，不当热帖，也不从它们出选题。"
        "未达标样本如需留档，只放页底「观察中（未达标）」。</p>"
        "</div>"
    )


def rule_p() -> str:
    return f'<p class="muted" id="hot-rule">{RULE_TEXT}</p>'


def wrap_watch(inner_html: str) -> str:
    if not (inner_html or "").strip():
        return ""
    return (
        '<details class="rawfold" id="watch">'
        "<summary>观察中（未达标）</summary>"
        f"{inner_html}"
        "</details>"
    )
