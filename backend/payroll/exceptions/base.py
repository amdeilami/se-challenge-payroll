class PayrollError(Exception):
    """Base class for domain-level errors in the payroll app."""

    pass


class ConflictError(PayrollError):
    """409-style conflicts (duplicates, already processed, etc.)."""


class NotFoundError(PayrollError):
    """404-style lookups that failed."""


class ValidationError(PayrollError):
    """400/422-style invalid inputs."""


class DuplicateUploadError(ConflictError):
    """Raised when a CSV with the same source_id was already imported."""

    def __init__(self, source_id: int):
        super().__init__(f"Upload {source_id} already exists")
        self.source_id = source_id


class InvalidCSVFormatError(ValidationError):
    """Raised when the CSV headers/rows are malformed."""

    def __init__(self, reason: str):
        super().__init__(f"Invalid CSV: {reason}")
        self.reason = reason


class UnknownEmployeeError(NotFoundError):
    def __init__(self, employee_id: str):
        super().__init__(f"Employee '{employee_id}' not found")
        self.employee_id = employee_id


class UnknownJobGroupError(NotFoundError):
    def __init__(self, code: str):
        super().__init__(f"Job group '{code}' not found")
        self.code = code


class DuplicateTimesheetRowError(ConflictError):
    """Raised when a row duplicates an existing one within the same file."""

    pass


class PeriodClosedError(ConflictError):
    """Raised when trying to write to a finalized pay period."""

    pass
