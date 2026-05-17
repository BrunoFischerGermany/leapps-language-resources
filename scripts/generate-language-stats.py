#!/usr/bin/env python3
"""
Generate UI translation stats: SVG bar chart and docs/stats.md.

Run from repository root:

    python scripts/generate-language-stats.py

If `python` is not available, use `python3` instead.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path
from datetime import datetime


REPO_ROOT = Path(__file__).resolve().parent.parent
LOCALES_DIR = REPO_ROOT / "locales"
SOURCE_LANG = "en"
SOURCE_FILE = LOCALES_DIR / SOURCE_LANG / f"translation_{SOURCE_LANG}.json"
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
SVG_PATH = ASSETS_DIR / "translation-progress.svg"
STATS_MD_PATH = DOCS_DIR / "stats.md"

# English name and autonym for SVG labels: "English / Autonym (code)".
LANGUAGE_NAMES: dict[str, tuple[str, str]] = {
    "en": ("English", "English"),
    "es": ("Spanish", "Español"),
    "fr": ("French", "Français"),
    "de": ("German", "Deutsch"),
}


@dataclass(frozen=True)
class LangStats:
    code: str
    translated: int
    missing: int
    empty: int
    total: int

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return 100.0 * self.translated / self.total


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def _load_translation_json(path: Path) -> dict[str, object]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        _fail(f"cannot read {path}: {exc}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        _fail(f"expected JSON object at root in {path}")
    # Normalize keys to str (JSON object keys are always str).
    return {str(k): v for k, v in data.items()}


def _is_nonempty_translation_value(value: object) -> bool:
    if not isinstance(value, str):
        return False
    return bool(value.strip())


def _discover_target_language_codes() -> list[str]:
    if not LOCALES_DIR.is_dir():
        _fail(f"missing locales directory: {LOCALES_DIR}")
    codes: list[str] = []
    for entry in sorted(LOCALES_DIR.iterdir(), key=lambda p: p.name):
        if not entry.is_dir():
            continue
        code = entry.name
        if code == SOURCE_LANG or code == "_template":
            continue
        trans_path = entry / f"translation_{code}.json"
        if not trans_path.is_file():
            _fail(f"missing translation file for language {code!r}: {trans_path}")
        codes.append(code)
    return sorted(codes)


def _compute_counts(source: dict[str, object], target: dict[str, object]) -> tuple[int, int, int, int]:
    source_keys = list(source.keys())
    total = len(source_keys)
    translated = missing = empty = 0
    for key in source_keys:
        if key not in target:
            missing += 1
            continue
        if _is_nonempty_translation_value(target[key]):
            translated += 1
        else:
            empty += 1
    return translated, missing, empty, total


def _analyze_language(code: str, source: dict[str, object]) -> LangStats:
    path = LOCALES_DIR / code / f"translation_{code}.json"
    target = _load_translation_json(path)
    translated, missing, empty, total = _compute_counts(source, target)
    return LangStats(code=code, translated=translated, missing=missing, empty=empty, total=total)


def _bar_color(percent: float) -> str:
    if percent == 100.0:
        return "#16a34a"  # green
    if percent >= 70.0:
        return "#ca8a04"  # yellow / amber
    return "#dc2626"  # red


def _language_row_label(code: str) -> str:
    pair = LANGUAGE_NAMES.get(code)
    if pair:
        english, native = pair
        return f"{native} / {english} ({code})"
    return f"{code} / {code} ({code})"


def _codes_missing_from_language_names(non_english_codes: list[str]) -> list[str]:
    """Locale folders with translation files but no LANGUAGE_NAMES entry."""
    return sorted(c for c in non_english_codes if c not in LANGUAGE_NAMES)


def _build_svg(title: str, source_key_count: int, rows: list[LangStats]) -> str:
    width = 720
    margin_top = 44
    row_height = 36
    bar_x = 230
    bar_width = 380
    bar_h = 18
    bg_fill = "#a3a3a3"  # medium grey canvas
    text_black = "#000000"
    footer_lines = 4
    footer_gap = 28
    footer_h = 14 * footer_lines + footer_gap
    height = margin_top + len(rows) * row_height + footer_h

    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
    )
    parts.append(
        f'  <rect x="0" y="0" width="{width}" height="{height}" fill="{bg_fill}"/>'
    )
    parts.append(
        f'  <text x="12" y="26" font-family="system-ui, -apple-system, Segoe UI, sans-serif" '
        f'font-size="18" font-weight="600" fill="{text_black}">{escape(title)}</text>'
    )

    for i, st in enumerate(rows):
        y_row = margin_top + i * row_height
        y_mid = y_row + row_height // 2 + 5
        y_bar = y_row + (row_height - bar_h) // 2
        pct = st.percent
        fill_w = int(round(bar_width * (pct / 100.0)))
        fill_w = max(0, min(bar_width, fill_w))
        color = _bar_color(pct)

        label = _language_row_label(st.code)
        parts.append(
            f'  <text x="12" y="{y_mid}" font-family="system-ui, -apple-system, Segoe UI, sans-serif" '
            f'font-size="13" fill="{text_black}">{escape(label)}</text>'
        )
        parts.append(
            f'  <rect x="{bar_x}" y="{y_bar}" width="{bar_width}" height="{bar_h}" '
            f'rx="4" ry="4" fill="#e5e7eb"/>'
        )
        if fill_w > 0:
            parts.append(
                f'  <rect x="{bar_x}" y="{y_bar}" width="{fill_w}" height="{bar_h}" '
                f'rx="4" ry="4" fill="{color}"/>'
            )
        pct_text = f"{pct:.1f}%"
        parts.append(
            f'  <text x="{bar_x + bar_width + 10}" y="{y_mid}" '
            f'font-family="system-ui, -apple-system, Segoe UI, sans-serif" '
            f'font-size="13" fill="{text_black}">{escape(pct_text)}</text>'
        )

    footer_y = margin_top + len(rows) * row_height + 18
    footer = [
        f"Source key file: locales/{SOURCE_LANG}/translation_{SOURCE_LANG}.json",
        f"Total source keys: {source_key_count}",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "Generated by: python scripts/generate-language-stats.py",
    ]
    for j, line in enumerate(footer):
        parts.append(
            f'  <text x="12" y="{footer_y + j * 14}" '
            f'font-family="system-ui, -apple-system, Segoe UI, sans-serif" '
            f'font-size="11" fill="#6b7280">{escape(line)}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _write_stats_md(unlisted_locale_codes: list[str]) -> str:
    lines = [
        "# Translation Stats",
        "",
        "These numbers are generated from the **UI** `translation_xx.json` files under the `/locales/` directory. ",
        "Empty or whitespace-only values in a locale file count as **untranslated**.",
        "",
        "![UI Translation Progress](./assets/translation-progress.svg)",
        "",
    ]
    if unlisted_locale_codes:
        codes_fmt = ", ".join(f"`{c}`" for c in unlisted_locale_codes)
        lines.extend(
            [
                "**Note:** The following translation locale(s) exist under `locales/` but are not yet "
                "listed in `LANGUAGE_NAMES` in "
                "[`scripts/generate-language-stats.py`](../scripts/generate-language-stats.py): \n"
                f"{codes_fmt} \n"
                "Add an English name and autonym tuple for each so the chart labels stay correct.",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    if not SOURCE_FILE.is_file():
        _fail(f"missing English source file: {SOURCE_FILE}")

    source = _load_translation_json(SOURCE_FILE)
    total_keys = len(source)
    if total_keys == 0:
        _fail(f"source file has no keys: {SOURCE_FILE}")

    codes = _discover_target_language_codes()
    if not codes:
        _fail("no non-English language folders with translation files found under locales/")

    en_row = LangStats(
        code="en",
        translated=total_keys,
        missing=0,
        empty=0,
        total=total_keys,
    )
    rows = sorted(
        [en_row] + [_analyze_language(code, source) for code in codes],
        key=lambda s: s.code,
    )

    unlisted = _codes_missing_from_language_names(codes)
    if unlisted:
        listed = ", ".join(unlisted)
        print(
            f"warning: locale(s) present but missing from LANGUAGE_NAMES: {listed}",
            file=sys.stderr,
        )

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    svg = _build_svg("LEAPPs UI Translation Progress", total_keys, rows)
    SVG_PATH.write_text(svg, encoding="utf-8")
    STATS_MD_PATH.write_text(_write_stats_md(unlisted), encoding="utf-8")

    print("UI translation stats (translation namespace, English as source)")
    print(f"Source: {SOURCE_FILE}")
    print(f"Total source keys: {total_keys}")
    print()
    for st in rows:
        pct = st.percent
        print(
            f"  {st.code}: translated={st.translated}/{st.total} "
            f"({pct:.1f}%), missing={st.missing}, empty={st.empty}"
        )
    print()
    print(f"Wrote {SVG_PATH}")
    print(f"Wrote {STATS_MD_PATH}")


if __name__ == "__main__":
    main()
