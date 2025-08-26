from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(max_length=16, unique=True, db_index=True)

    def __str__(self):
        return self.employee_id
