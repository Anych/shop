from cart.models import Cart, CartItem
from cart.views import _cart_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user__email=request.user.email)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)


# def cart(request, total=0, quantity=0, cart_items=None):
#
#     try:
#         delivery = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         if total > 50000:
#             delivery = 0
#         if total == 0:
#             delivery = 0
#         grand_total = delivery + total
#     except ObjectDoesNotExist:
#         pass
#
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'delivery': delivery,
#         'grand_total': grand_total,
#     }
#     return context

