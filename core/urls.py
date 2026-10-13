from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('validate-promo/', views.validate_promo, name='validate_promo'),
    path('checkout/', views.checkout_view, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 