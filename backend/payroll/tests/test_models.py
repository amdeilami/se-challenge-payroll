from django.test import TestCase
from payroll.models import JobGroup, Employee, UploadedTimesheetFile, TimesheetEntry
from datetime import date
from decimal import Decimal


class ModelsSmokeTest(TestCase):
    def test_seeded_jobgroups_exist(self):
        self.assertTrue(JobGroup.objects.filter(code="A").exists())
        self.assertTrue(JobGroup.objects.filter(code="B").exists())

    def test_create_basic_entry(self):
        a = JobGroup.objects.get(code="A")
        emp = Employee.objects.create(employee_id="1")
        up = UploadedTimesheetFile.objects.create(file_id=42)
        TimesheetEntry.objects.create(
            file=up,
            employee=emp,
            job_group=a,
            date=date(2023, 1, 14),
            hours=Decimal("7.5"),
            hourly_rate=a.hourly_rate,
        )
        self.assertEqual(TimesheetEntry.objects.count(), 1)
