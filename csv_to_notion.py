#!/usr/bin/env python3
"""Convert expenses CSV to a Notion-pasteable markdown table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ALIASES = {
    "date": ("date", "dated", "transaction_date"),
    "merchant": ("merchant", "vendor", "payee", "name"),
    "description": ("description", "memo", "note", "notes"),
    "amount": ("amount", "total", "value"),
    "currency": ("currency", "curr", "ccy"),
    "category": ("category", "cat", "label"),
}

DEFAULT_ORDER = ["date", "merchant", "description", "amount", "currency", "category"]


def map_headers(fieldnames: list[str]) -> dict[str, str]:
    lower = {f.lower().strip(): f for f in fieldnames}
    mapping: dict[str, str] = {}
    for canonical, aliases in ALIASES.items():
        for a in aliases:
            if a in lower:
                mapping[canonical] = lower[a]
                break
    return mapping


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def to_markdown(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(c.title() for c in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(c, "")) for c in columns) + " |")
    return "\n".join(lines) + "\n"


def convert(path: Path, limit: int | None = None) -> str:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit("CSV has no header row")
        mapping = map_headers(list(reader.fieldnames))
        columns = [c for c in DEFAULT_ORDER if c in mapping]
        if not columns:
            columns = [h.lower() for h in reader.fieldnames]
            normalized_rows = []
            for i, raw in enumerate(reader):
                if limit is not None and i >= limit:
                    break
                normalized_rows.append({k.lower(): (v or "") for k, v in raw.items()})
            return to_markdown(normalized_rows, columns)

        rows: list[dict[str, str]] = []
        for i, raw in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append({c: (raw.get(mapping[c], "") or "") for c in columns})
    return to_markdown(rows, columns)


def main() -> None:
    p = argparse.ArgumentParser(description="CSV expenses → Notion markdown table")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, help="Write markdown to file")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    md = convert(args.csv_path, args.limit)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(md, end="")


if __name__ == "__main__":
    main()
