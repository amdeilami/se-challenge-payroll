from django.test import TestCase
from io import StringIO
from payroll.services import import_timesheet, payroll_for_range
from datetime import date
from decimal import Decimal
from pathlib import Path

# CSV = """14/11/2023,7.5,1,A
# 9/11/2023,4,2,B
# 10/11/2023,4,2,B
# """


class PayrollReportTests(TestCase):
    def setUp(self):
        here = Path(__file__).resolve().parent
        f = (here / "time-report-99.csv").open(mode="r", encoding="utf-8")
        import_timesheet(f, "time-report-99.csv")

    def test_half_month_grouping_and_amounts(self):
        rows = payroll_for_range(start_date(2023, 11, 1), start_date(2023, 11, 30))
        # helper for readability
        by_period = {
            (
                r["employee_id"],
                date.fromisoformat(r["pay_period"]["start"]),
                date.fromisoformat(r["pay_period"]["end"]),
            ): Decimal(r["amount_paid"])
            for r in rows
        }

        # Nov 1–15: 7.5h @ $20 = 150.00
        # The calculation above is based on the current test-99.csv file, I should update it whenever I change test files
        self.assertEqual(
            by_period[("1", date(2023, 11, 1), date(2023, 11, 15))], decimal("150.00")
        )
        # Nov 1–15: 8.0h @ $30 = 240.00
        self.assertEqual(
            by_period[("2", date(2023, 11, 1), date(2023, 11, 15))], decimal("240.00")
        )


def start_date(y, m, d):
    return date(y, m, d)


def decimal(s):
    return Decimal(s)
