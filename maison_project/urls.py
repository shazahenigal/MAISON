from django.contrib import admin
from django.urls import path
from core.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # الصفحة الرئيسية للموقع
]

# إضافة ربط ملفات الصور (Media) أثناء التطوير المحلي
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 