# backend/equipment/models.py
from django.db import models

class Equipment(models.Model):
    equipment_id = models.IntegerField(default=0)           # integer default
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Unknown')
    location = models.CharField(max_length=100, default='Unknown')
    purchase_year = models.IntegerField(default=0)         # integer default
    condition = models.CharField(max_length=50, default='Unknown')

    def __str__(self):
        return f"{self.name} ({self.type})"
