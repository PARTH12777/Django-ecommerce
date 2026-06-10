from decimal import Decimal
from django.conf import settings
from products.models import Product
from .models import Cart, CartItem


class SessionCart:
    """Session-based cart for guest users."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.current_price)}
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.remove(product)
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        for product in products:
            item = self.cart[str(product.id)]
            item['product'] = product
            item['quantity'] = int(item['quantity'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    @property
    def subtotal(self):
        return sum(
            Decimal(item['price']) * int(item['quantity'])
            for item in self.cart.values()
        )

    def get_items(self):
        return list(self)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def merge_session_cart_to_db(request, user):
    """Merge session cart into database cart on login."""
    session_cart = SessionCart(request)
    if not session_cart.cart:
        return

    db_cart = get_user_cart(user)
    for item in session_cart:
        cart_item, created = CartItem.objects.get_or_create(
            cart=db_cart, product=item['product'],
            defaults={'quantity': item['quantity']}
        )
        if not created:
            cart_item.quantity += item['quantity']
            cart_item.save()

    session_cart.clear()


def get_cart_for_request(request):
    """Return unified cart interface for template context."""
    if request.user.is_authenticated:
        db_cart = get_user_cart(request.user)
        items = []
        for item in db_cart.items.select_related('product').all():
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.current_price,
                'total_price': item.total_price,
            })
        return {
            'items': items,
            'total_items': db_cart.total_items,
            'subtotal': db_cart.subtotal,
            'is_authenticated': True,
        }
    else:
        session_cart = SessionCart(request)
        items = list(session_cart)
        return {
            'items': items,
            'total_items': len(session_cart),
            'subtotal': session_cart.subtotal,
            'is_authenticated': False,
        }
