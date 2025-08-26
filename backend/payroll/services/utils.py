from decimal import Decimal, InvalidOperation
import re
from datetime import datetime, date

_FILE_ID = re.compile(r"^time-report-(\d+)\.csv$")


def parse_file_id(filename: str) -> int:
    m = _FILE_ID.match(filename)
    if not m:
        raise ValueError("Filename must look like 'time-report-<id>.csv'")
    return int(m.group(1))


def parse_ddmmyyyy(value: str) -> date:
    return datetime.strptime(value.strip(), "%d/%m/%Y").date()


def parse_hours(value: str) -> Decimal:
    try:
        h = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError("Hours must be a number")
    if h <= 0:
        raise ValueError("Hours must be > 0")
    return h


def normalize_group(code: str) -> str:
    c = (code or "").strip().upper()
    if c not in {"A", "B"}:
        raise ValueError("Unknown job group")
    return c
