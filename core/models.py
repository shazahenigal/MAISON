from django.db import models
from django.utils import timezone

class BannerImage(models.Model):
    title = models.CharField(max_length=100, default="Main Brand Banner")
    image = models.ImageField(upload_to='banner_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class FashionEventTicket(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='Runway Ticket')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10, help_text="Total available stock. Decreases automatically with orders.")
    event_date = models.CharField(max_length=100, blank=True, null=True)
    event_location = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='tickets_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.price} EGP"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"

class PaymentSettings(models.Model):
    merchant_name = models.CharField(max_length=100, default="MAISON Fashion House")
    bank_account_number = models.CharField(max_length=100, blank=True, null=True, help_text="أدخلي رقم الحساب أو بيانات التحويل الخاصة بك هنا لاحقاً")
    is_live_gateway = models.BooleanField(default=False, help_text="تفعيل بوابة الدفع الحقيقية مستقبلاً")

    def __str__(self):
        return "Payment & Bank Account Settings"

class Order(models.Model):
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, default='')
    email = models.EmailField()
    
    ticket = models.ForeignKey(FashionEventTicket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code_used = models.CharField(max_length=50, blank=True, null=True)
    
    # بيانات الفيزا المبسطة لتجربة العميل
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.ticket.title})" 