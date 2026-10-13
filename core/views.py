from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import BannerImage, FashionEventTicket, PromoCode, Order, PaymentSettings
import json

def home_view(request):
    query = request.GET.get('q', '')
    tickets = FashionEventTicket.objects.all()
    if query:
        tickets = tickets.filter(title__icontains=query)
    active_banner = BannerImage.objects.filter(is_active=True).first()
    
    # يمكنكِ تمرير حالة الـ Sold Out لكل تيكت أو التعامل معها مباشرة في الـ HTML
    context = {
        'tickets': tickets,
        'query': query,
        'active_banner': active_banner,
    }
    return render(request, 'index.html', context)

def validate_promo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code_text = data.get('code', '').strip()
            now = timezone.now()
            
            promo = PromoCode.objects.filter(code__iexact=code_text, active=True, valid_from__lte=now, valid_to__gte=now).first()
            if promo:
                return JsonResponse({'valid': True, 'discount': float(promo.discount_percentage)})
            else:
                return JsonResponse({'valid': False, 'message': 'Invalid or expired promo code.'})
        except Exception as e:
            return JsonResponse({'valid': False, 'message': 'Server error.'})
    return JsonResponse({'valid': False, 'message': 'Invalid request.'})

def checkout_view(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            
            ticket_id = request.POST.get('ticket_id')
            quantity = int(request.POST.get('quantity', 1))
            promo_code_used = request.POST.get('promo_code_used', '')
            
            # بيانات الفيزا من العميل
            card_number = request.POST.get('card_number', '')
            card_last_four = card_number[-4:] if len(card_number) >= 4 else '0000'
            
            ticket = get_object_or_404(FashionEventTicket, id=ticket_id)
            
            # التحقق المشدد من المخزون (منع الشراء إذا نفذت الكمية أو أصبحت صفرًا)
            if ticket.stock <= 0:
                return JsonResponse({'success': False, 'message': '❌ Sorry, this item is Sold Out!'})
            
            if ticket.stock < quantity:
                return JsonResponse({'success': False, 'message': f'❌ Sorry, only {ticket.stock} items left in stock.'})
            
            subtotal = ticket.price * quantity
            discount_amount = 0
            if promo_code_used:
                now = timezone.now()
                promo = PromoCode.objects.filter(code__iexact=promo_code_used, active=True, valid_from__lte=now, valid_to__gte=now).first()
                if promo:
                    discount_amount = subtotal * (promo.discount_percentage / 100)
            
            total_price = subtotal - discount_amount
            
            # خصم الكمية من المخزون تلقائياً
            ticket.stock -= quantity
            ticket.save()
            
            # حفظ الأوردر مع آخر أرقام الكارت
            Order.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                ticket=ticket,
                quantity=quantity,
                total_price=total_price,
                promo_code_used=promo_code_used,
                card_last_four=card_last_four
            )
            
            # إرجاع رسالة النجاح مع الإيموجي المناسب كما طلبتِ
            return JsonResponse({'success': True, 'message': '✅ Order added successfully! Thank you.'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}) 