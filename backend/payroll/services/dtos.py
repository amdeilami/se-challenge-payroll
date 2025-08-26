from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class TimesheetRow:
    day: date
    hours: Decimal
    employee_id: str
    job_group_code: str


@dataclass(frozen=True)
class ImportResult:
    file_id: int
    rows_inserted: int


@dataclass(frozen=True)
class PayrollLine:
    employee_id: str
    period_start: date
    period_end: date
    amount: Decimal
