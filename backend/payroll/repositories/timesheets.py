from datetime import date
from decimal import Decimal
from typing import Iterable, List
from django.db.models import QuerySet
from ..models import TimesheetEntry, UploadedTimesheetFile, Employee, JobGroup


def create_entry(
    *,
    file: UploadedTimesheetFile,
    employee: Employee,
    job_group: JobGroup,
    day: date,
    hours: Decimal,
    hourly_rate: Decimal,
) -> TimesheetEntry:
    """
    Insert a single entry. Assumes inputs are validated by logic layer.
    Requires explicit hourly_rate (no computation here).
    May raise IntegrityError if it violates the unique constraint.
    """
    entry = TimesheetEntry(
        file=file,
        employee=employee,
        job_group=job_group,
        date=day,
        hours=hours,
        hourly_rate=hourly_rate,  # snapshot provided by logic
    )
    entry.save()
    return entry


def bulk_create_entries(
    entries: Iterable[TimesheetEntry], batch_size: int = 1000
) -> List[TimesheetEntry]:
    """
    Persist many pre-constructed TimesheetEntry instances.
    Caller must set hourly_rate on each entry beforehand.
    """
    return TimesheetEntry.objects.bulk_create(list(entries), batch_size=batch_size)


def list_entries_for_file(upload: UploadedTimesheetFile) -> QuerySet[TimesheetEntry]:
    return (
        TimesheetEntry.objects.select_related("employee", "job_group")
        .filter(file=upload)
        .order_by("date", "id")
    )


def list_entries_for_employee_between(
    emp: Employee, start: date, end: date
) -> QuerySet[TimesheetEntry]:
    return (
        TimesheetEntry.objects.select_related("employee", "job_group")
        .filter(employee=emp, date__range=(start, end))
        .order_by("date", "id")
    )


def list_entries_between(start: date, end: date) -> QuerySet[TimesheetEntry]:
    return (
        TimesheetEntry.objects.select_related("employee", "job_group")
        .filter(date__range=(start, end))
        .order_by("employee__employee_id", "date", "id")
    )
