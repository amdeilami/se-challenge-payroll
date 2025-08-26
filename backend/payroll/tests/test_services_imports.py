from django.test import TestCase
from io import StringIO
from payroll.services import import_timesheet
from payroll.exceptions import DuplicateUploadError
from payroll.models import TimesheetEntry
from pathlib import Path

# CSV_OK = """14/11/2023,7.5,1,A
# 9/11/2023,4,2,B
# 10/11/2023,4,2,B
# """


class ImportTimesheetTests(TestCase):
    def test_import_success(self):
        here = Path(__file__).resolve().parent
        f = (here / "time-report-99.csv").open(mode="r", encoding="utf-8")
        # f = StringIO(CSV_OK)
        res = import_timesheet(f, "time-report-99.csv")
        self.assertEqual(res.file_id, 99)
        self.assertEqual(res.rows_inserted, 3)
        self.assertEqual(TimesheetEntry.objects.count(), 3)

    def test_duplicate_upload_blocked(self):
        here = Path(__file__).resolve().parent
        f1 = (here / "time-report-99.csv").open(mode="r", encoding="utf-8")
        # f1 = StringIO(CSV_OK)
        import_timesheet(f1, "time-report-99.csv")
        with self.assertRaises(DuplicateUploadError):
            f2 = (here / "time-report-99.csv").open(mode="r", encoding="utf-8")
            # f2 = StringIO(CSV_OK)  # same file_id => should be rejected
            import_timesheet(f2, "time-report-99.csv")
