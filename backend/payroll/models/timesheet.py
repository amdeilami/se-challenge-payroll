from django.db import models
from .uploaded_timesheet_file import UploadedTimesheetFile
from .employee import Employee
from .jobgroup import JobGroup


class TimesheetEntry(models.Model):
    file = models.ForeignKey(
        UploadedTimesheetFile, on_delete=models.PROTECT, related_name="rows"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="entries"
    )
    job_group = models.ForeignKey(
        JobGroup, on_delete=models.PROTECT, related_name="entries"
    )

    date = models.DateField()
    hours = models.DecimalField(max_digits=8, decimal_places=2)

    # Snapshot of the rate used for this entry so historical totals never change
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["employee", "date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["file", "employee", "date", "job_group", "hours"],
                name="unique_timesheet_entry_row_per_file",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.hourly_rate:  # auto-snapshot from current group
            self.hourly_rate = self.job_group.hourly_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.employee} {self.date} {self.hours}hrs job_group: {self.job_group}"
        )
