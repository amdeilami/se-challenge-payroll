import calendar
from datetime import date as d, date
from dataclasses import dataclass


@dataclass(frozen=True)
class PayPeriod:
    start: date
    end: date


def period_for(day: date) -> PayPeriod:
    if day.day <= 15:
        return PayPeriod(d(day.year, day.month, 1), d(day.year, day.month, 15))
    last = calendar.monthrange(day.year, day.month)[1]
    return PayPeriod(d(day.year, day.month, 16), d(day.year, day.month, last))
