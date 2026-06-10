def wishlist_context(request):
    if request.user.is_authenticated:
        count = request.user.wishlist_items.count()
    else:
        count = 0
    return {'wishlist_count': count}
