from django.contrib import admin
from .models import BannerImage, FashionEventTicket, PromoCode, Order, PaymentSettings

@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(FashionEventTicket)
class FashionEventTicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'event_date')
    search_fields = ('title', 'category')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'valid_from', 'valid_to', 'active')
    list_filter = ('active',)

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    list_display = ('merchant_name', 'bank_account_number', 'is_live_gateway')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'email', 'ticket', 'quantity', 'total_price', 'card_last_four', 'created_at')
    search_fields = ('full_name', 'phone_number', 'email', 'ticket__title') 