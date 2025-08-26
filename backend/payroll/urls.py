from django.urls import path
from . import views

urlpatterns = [
    path("api/timesheets/upload", views.upload_timesheet, name="upload_timesheet"),
    path("api/payroll", views.payroll, name="payroll"),
]
