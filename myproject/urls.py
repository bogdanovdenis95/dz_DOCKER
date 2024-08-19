from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),  # Убедитесь, что путь к 'lms.urls' правильный
    path('api/', include('users.urls')),  # Добавлено для маршрутизации к приложению users
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
