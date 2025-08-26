from django.db import models


class JobGroup(models.Model):
    code = models.CharField(max_length=8, unique=True, db_index=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.code}  (${self.hourly_rate}/hr)"
