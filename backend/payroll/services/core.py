import csv
from decimal import Decimal
from typing import TextIO, List
from collections import defaultdict

from django.db import transaction, IntegrityError
from .utils import parse_hours, normalize_group, parse_file_id, parse_ddmmyyyy
from .pay_periods import period_for
from .dtos import TimesheetRow, ImportResult, PayrollLine
from ..exceptions import (
    DuplicateUploadError,
    InvalidCSVFormatError,
    UnknownJobGroupError,
    DuplicateTimesheetRowError,
)
from ..repositories import (
    create_upload,
    get_employee,
    get_or_create_employee,
    get_jobgroup,
    bulk_create_entries,
    list_entries_between,
)
from ..models import TimesheetEntry  # only to create instances for bulk_create


def _read_rows(f: TextIO, filename: str) -> tuple[int, list[TimesheetRow]]:
    reader = csv.reader(f)
    _header = next(reader)

    out: list[TimesheetRow] = []
    for row in reader:
        """
        I can have an enumerate here to iterate and have line numbers too
        in case if any line has an issue, I can report it more specifically
        if len(row) != 4:
            raise InvalidCSVFormatError(
                f"Line {lineno}: expected 4 columns, got {len(row)}"
            )
        """

        raw_date, raw_hours, raw_emp, raw_group = [c.strip() for c in row]

        day = parse_ddmmyyyy(raw_date)
        hours = parse_hours(raw_hours)
        emp = raw_emp.strip()
        group = normalize_group(raw_group)

        out.append(
            TimesheetRow(day=day, hours=hours, employee_id=emp, job_group_code=group)
        )

    file_id = parse_file_id(filename)
    return file_id, out


@transaction.atomic
def import_timesheet(f: TextIO, filename: str) -> ImportResult:
    """
    Pure business flow:
      - parse/validate CSV
      - create upload (DB enforces duplicate file_id)
      - upsert employees, fetch job groups
      - build entries and bulk insert (repositories handle DB I/O)
    Raises domain exceptions on error.
    """
    file_id, rows = _read_rows(f, filename)

    # Create upload (IntegrityError -> DuplicateUploadError)
    try:
        upload = create_upload(file_id=file_id)
    except IntegrityError:
        raise DuplicateUploadError(file_id)

    # Preload job groups for speed
    group_map = {"A": get_jobgroup("A"), "B": get_jobgroup("B")}
    if not group_map["A"] or not group_map["B"]:
        raise UnknownJobGroupError("A/B not seeded")

    # Prepare model instances without saving (no DB in services except upload)
    seen = set()
    to_create: list[TimesheetEntry] = []

    for r in rows:
        key = (r.employee_id, r.day, r.job_group_code, str(r.hours))
        if key in seen:
            # duplicate row within the same file before hitting DB
            raise DuplicateTimesheetRowError(f"Duplicate row for {key}")
        seen.add(key)

        emp = get_employee(r.employee_id) or get_or_create_employee(r.employee_id)
        grp = group_map.get(r.job_group_code)
        if not grp:
            raise UnknownJobGroupError(r.job_group_code)

        to_create.append(
            TimesheetEntry(
                file=upload,
                employee=emp,
                job_group=grp,
                date=r.day,
                hours=r.hours,
                hourly_rate=grp.hourly_rate,
            )
        )

    try:
        bulk_create_entries(to_create, batch_size=1000)
    except IntegrityError as e:
        # DB-level unique constraint guard
        raise DuplicateTimesheetRowError(str(e))

    return ImportResult(file_id=file_id, rows_inserted=len(to_create))


def payroll_for_range(start, end) -> List[PayrollLine]:
    totals = defaultdict(Decimal)
    entries = list_entries_between(start, end)
    for e in entries:
        p = period_for(e.date)
        key = (e.employee.employee_id, p.start, p.end)
        totals[key] += e.hours * e.hourly_rate
    return [
        PayrollLine(
            employee_id=k[0],
            period_start=k[1],
            period_end=k[2],
            amount=v.quantize(Decimal("0.01")),
        )
        for k, v in sorted(totals.items())
    ]
