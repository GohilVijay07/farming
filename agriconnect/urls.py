"""
URL configuration for agriconnect project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('farming.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Admin Site Headers
admin.site.site_header = "AgriConnect Administration"
admin.site.site_title = "AgriConnect Admin Portal"
admin.site.index_title = "Welcome to AgriConnect Farming Management Portal"
