from django.urls import path
from .views import upload_csv, summary_view, pdf_report_view

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('summary/', summary_view, name='summary'),
    path("report/pdf/", pdf_report_view, name="pdf_report"),
]
