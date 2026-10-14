#!/usr/bin/env python3
"""Calcula minutos corridos e úteis conforme calendário operacional do cliente."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


def parse_datetime(value: str, timezone: ZoneInfo) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone)
    return parsed.astimezone(timezone)


def parse_clock(value: str) -> time:
    hour, minute = (int(part) for part in value.split(":"))
    return time(hour, minute)


def overlap_minutes(start: datetime, end: datetime, left: datetime, right: datetime) -> int:
    overlap_start = max(start, left)
    overlap_end = min(end, right)
    if overlap_end <= overlap_start:
        return 0
    return int((overlap_end - overlap_start).total_seconds() // 60)


def business_minutes(
    start: datetime,
    end: datetime,
    schedule: dict[str, list[list[str]]],
    holidays: set[date],
) -> int:
    if end < start:
        raise ValueError("end anterior a start")
    timezone = start.tzinfo
    if timezone is None or end.tzinfo is None:
        raise ValueError("timestamps precisam de fuso")

    total = 0
    current = start.date()
    while current <= end.date():
        if current not in holidays:
            intervals = schedule.get(str(current.weekday()), [])
            for opening, closing in intervals:
                left = datetime.combine(current, parse_clock(opening), tzinfo=timezone)
                right = datetime.combine(current, parse_clock(closing), tzinfo=timezone)
                total += overlap_minutes(start, end, left, right)
        current += timedelta(days=1)
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--timezone", default="America/Sao_Paulo")
    parser.add_argument("--schedule", type=Path, required=True)
    parser.add_argument("--holidays", type=Path)
    args = parser.parse_args()

    timezone = ZoneInfo(args.timezone)
    start = parse_datetime(args.start, timezone)
    end = parse_datetime(args.end, timezone)
    schedule = json.loads(args.schedule.read_text(encoding="utf-8"))
    holiday_values = [] if not args.holidays else json.loads(args.holidays.read_text(encoding="utf-8"))
    holidays = {date.fromisoformat(value) for value in holiday_values}

    elapsed = int((end - start).total_seconds() // 60)
    useful = business_minutes(start, end, schedule, holidays)
    print("# Cálculo de tempo de atendimento\n")
    print("| Campo | Valor |")
    print("|---|---:|")
    print(f"| Início | {start.isoformat()} |")
    print(f"| Fim | {end.isoformat()} |")
    print(f"| Minutos corridos | {elapsed} |")
    print(f"| Minutos úteis | {useful} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
