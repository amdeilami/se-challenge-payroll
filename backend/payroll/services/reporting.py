import calendar
from datetime import date as d, date
from .dtos import PayrollLine, PayPeriod
from decimal import Decimal
from typing import List
from ..repositories import list_entries_between
from collections import defaultdict


def period_for(day: date) -> PayPeriod:
    if day.day <= 15:
        return PayPeriod(d(day.year, day.month, 1), d(day.year, day.month, 15))
    last = calendar.monthrange(day.year, day.month)[1]
    return PayPeriod(d(day.year, day.month, 16), d(day.year, day.month, last))


def payroll_for_range(start: date, end: date):
    totals = defaultdict(Decimal)
    entries = list_entries_between(start, end)
    for e in entries:
        p = period_for(e.date)
        key = (e.employee.employee_id, p.start, p.end)
        totals[key] += e.hours * e.hourly_rate
    lines = [
        PayrollLine(
            employee_id=k[0],
            period_start=k[1],
            period_end=k[2],
            amount=v.quantize(Decimal("0.01")),
        )
        for k, v in sorted(totals.items())
    ]

    data = [
        {
            "employee_id": r.employee_id,
            "pay_period": {
                "start": r.period_start.isoformat(),
                "end": r.period_end.isoformat(),
            },
            "amount_paid": f"{r.amount:.2f}",
        }
        for r in lines
    ]
    return data
