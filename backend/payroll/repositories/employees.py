from typing import Optional
from ..models import Employee


def get_employee(employee_id: str) -> Optional[Employee]:
    try:
        return Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return None


def get_or_create_employee(employee_id: str) -> Employee:
    obj, _ = Employee.objects.get_or_create(employee_id=employee_id)
    return obj
