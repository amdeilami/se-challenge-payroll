from typing import Optional
from django.db import IntegrityError
from ..models import UploadedTimesheetFile


def get_upload(file_id: int) -> Optional[UploadedTimesheetFile]:
    try:
        return UploadedTimesheetFile.objects.get(file_id=file_id)
    except UploadedTimesheetFile.DoesNotExist:
        return None


def create_upload(file_id: int) -> UploadedTimesheetFile:
    """
    Create the upload record. This relies on the DB unique constraint.
    - On duplicate, this will raise django.db.IntegrityError (let logic layer translate it).
    """
    upload = UploadedTimesheetFile(file_id=file_id)
    try:
        upload.save()
    except IntegrityError:
        # Let the logic layer catch and convert to a domain exception if desired
        raise
    return upload
