from django.conf import settings

from onlineshop.models import Product


class Cart(object):
    """Класс корзины"""

    def __init__(self, request):
        """Инициализация корзины"""
        self.sesion = request.session
        cart = self.sesion.get(settings)
        if not cart:
            cart = self.sesion[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.sesion.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = Product.objects.filter(available=True)
