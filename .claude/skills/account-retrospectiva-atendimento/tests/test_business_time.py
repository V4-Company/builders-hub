#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "business_time.py"
SPEC = importlib.util.spec_from_file_location("business_time", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


SCHEDULE = {
    "0": [["09:00", "18:00"]],
    "1": [["09:00", "18:00"]],
    "2": [["09:00", "18:00"]],
    "3": [["09:00", "18:00"]],
    "4": [["09:00", "18:00"]],
}


def main() -> int:
    tz = ZoneInfo("America/Sao_Paulo")
    saturday = datetime.fromisoformat("2026-10-03T10:00:00").replace(tzinfo=tz)
    monday = datetime.fromisoformat("2026-10-05T14:00:00").replace(tzinfo=tz)
    assert MODULE.business_minutes(saturday, monday, SCHEDULE, set()) == 300

    holiday_start = datetime.fromisoformat("2026-10-12T09:00:00").replace(tzinfo=tz)
    holiday_end = datetime.fromisoformat("2026-10-13T10:00:00").replace(tzinfo=tz)
    assert MODULE.business_minutes(holiday_start, holiday_end, SCHEDULE, {date(2026, 10, 12)}) == 60

    print("OK: sábado não penaliza; feriado é ignorado; segunda conta apenas tempo útil")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
