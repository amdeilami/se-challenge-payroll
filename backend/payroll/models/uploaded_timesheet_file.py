from django.db import models


class UploadedTimesheetFile(models.Model):
    file_id = models.PositiveIntegerField(unique=True, db_index=True)

    def __str__(self):
        return f"CSV File {self.file_id}"
