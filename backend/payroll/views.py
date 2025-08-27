import io
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dataclasses import asdict

from .services import import_timesheet, payroll_for_range
from .exceptions import (
    DuplicateUploadError,
    InvalidCSVFormatError,
    UnknownJobGroupError,
    DuplicateTimesheetRowError,
)


def _bad_request(msg: str, status: int = 400):
    return JsonResponse({"error": msg}, status=status)


@csrf_exempt
@require_http_methods(["POST"])
def upload_timesheet(request):
    """
    POST /api/timesheets/upload
    form-data: file=@time-report-42.csv
    """
    f = request.FILES.get("file")
    if not f:
        return _bad_request("Missing file (form field name: 'file')")
    try:
        # decode bytes to text for csv.reader
        with io.TextIOWrapper(f.file, encoding="utf-8") as text:
            result = import_timesheet(text, f.name)
    except DuplicateUploadError as e:
        return _bad_request(str(e), status=409)
    except InvalidCSVFormatError as e:
        return _bad_request(str(e), status=400)
    except UnknownJobGroupError as e:
        return _bad_request(str(e), status=400)
    except DuplicateTimesheetRowError as e:
        return _bad_request(str(e), status=409)
    except ValueError as e:
        # catch stray ValueErrors from parsing if any slipped through
        return _bad_request(str(e), status=400)

    return JsonResponse(asdict(result), status=201)


@require_http_methods(["GET"])
def payroll(request):
    """
    GET /api/payroll?start=YYYY-MM-DD&end=YYYY-MM-DD
    Returns half-month aggregated lines.
    """
    start_s = request.GET.get("start")
    end_s = request.GET.get("end")
    if not start_s or not end_s:
        return _bad_request("Query params 'start' and 'end' are required (YYYY-MM-DD)")
    try:
        start = date.fromisoformat(start_s)
        end = date.fromisoformat(end_s)
    except ValueError:
        return _bad_request("Dates must be YYYY-MM-DD")

    data = payroll_for_range(start, end)
    return JsonResponse({"results": data}, status=200)
