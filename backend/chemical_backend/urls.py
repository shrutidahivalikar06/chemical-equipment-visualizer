# chemical_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('equipment.urls')),  # <-- include your app URLs under /api/
]
