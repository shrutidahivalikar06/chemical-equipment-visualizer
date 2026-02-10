from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Count
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Equipment


# CSV Upload API
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES['file']

    if not file.name.endswith('.csv'):
        return Response({"error": "Only CSV files are allowed"}, status=400)

    try:
        df = pd.read_csv(file)

        required_columns = [
            "equipment_id",
            "equipment_name",
            "equipment_type",
            "status",
            "location",
            "purchase_year",
            "condition"
        ]

        if not all(col in df.columns for col in required_columns):
            return Response(
                {"error": "CSV columns do not match required format"},
                status=400
            )

        # Clear old data to avoid duplicates
        Equipment.objects.all().delete()

        # Save data
        for _, row in df.iterrows():
            Equipment.objects.create(
                equipment_id=int(row["equipment_id"]),
                name=str(row["equipment_name"]),
                type=str(row["equipment_type"]),
                status=str(row["status"]),
                location=str(row["location"]),
                purchase_year=int(row["purchase_year"]),
                condition=str(row["condition"])
            )

        # Return first 10 rows for frontend preview
        data_preview = df.head(10).to_dict(orient="records")

        return Response({
            "message": "File uploaded successfully",
            "rows": len(df),
            "data_preview": data_preview
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# Summary API
@api_view(['GET'])
@permission_classes([AllowAny])
def summary_view(request):
    summary = {
        "total_equipment": Equipment.objects.count(),
        "avg_purchase_year": round(
            Equipment.objects.aggregate(Avg("purchase_year"))["purchase_year__avg"] or 0, 2
        ),
        "type_distribution": dict(
            Equipment.objects
            .values("type")
            .annotate(count=Count("type"))
            .values_list("type", "count")
        )
    }

    return JsonResponse(summary)


# PDF Report API
@api_view(['GET'])
@permission_classes([AllowAny])
def pdf_report_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Equipment Report")

    p.setFont("Helvetica", 12)
    y -= 40

    total = Equipment.objects.count()
    avg_year = Equipment.objects.aggregate(Avg('purchase_year'))['purchase_year__avg'] or 0

    p.drawString(50, y, f"Total Equipment: {total}")
    y -= 20
    p.drawString(50, y, f"Average Purchase Year: {round(avg_year, 2)}")

    y -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Equipment Type Distribution")

    y -= 30
    p.setFont("Helvetica", 12)

    distribution = Equipment.objects.values('type').annotate(count=Count('type'))
    for item in distribution:
        p.drawString(60, y, f"{item['type']}: {item['count']}")
        y -= 20

    p.showPage()
    p.save()

    return response
