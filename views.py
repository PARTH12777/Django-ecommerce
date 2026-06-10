from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import WishlistItem


@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'items': items})


@login_required
def add_to_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    _, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'"{product.name}" added to wishlist.')
    else:
        messages.info(request, f'"{product.name}" is already in your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))


@login_required
def remove_from_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'"{product.name}" removed from wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))
