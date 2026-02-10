# backend/equipment/admin.py
from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'equipment_id',
        'name',
        'type',
        'status',
        'location',
        'purchase_year',
        'condition'
    )
