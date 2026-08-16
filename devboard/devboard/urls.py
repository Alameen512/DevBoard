"""
DevBoard project-level URL configuration.

The 'dashboard' app owns every user-facing route; this file just wires
in the Django admin and delegates everything else to dashboard.urls.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
]

# Serve user-uploaded media (profile pictures) during local development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
