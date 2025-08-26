from typing import Optional, Iterable
from ..models import JobGroup


def get_jobgroup(code: str) -> Optional[JobGroup]:
    try:
        return JobGroup.objects.get(code=code)
    except JobGroup.DoesNotExist:
        return None


def list_jobgroups() -> Iterable[JobGroup]:
    return JobGroup.objects.all().order_by("code")
