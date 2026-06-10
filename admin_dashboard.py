from django.contrib import admin
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from products.models import Product, Review
from django.contrib.auth.models import User


def get_admin_stats():
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    return {
        'total_orders': Order.objects.count(),
        'total_revenue': Order.objects.exclude(status='cancelled').aggregate(Sum('total'))['total__sum'] or 0,
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_users': User.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'recent_orders': Order.objects.filter(created_at__date__gte=month_ago).count(),
        'total_reviews': Review.objects.count(),
    }


original_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context['stats'] = get_admin_stats()
    extra_context['recent_orders'] = Order.objects.select_related('user').order_by('-created_at')[:10]
    return original_index(request, extra_context)


admin.site.index = custom_admin_index
