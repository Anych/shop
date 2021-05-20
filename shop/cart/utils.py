from cart.models import Cart, CartItem


def _cart_id(request):
    """
    Cart_id for not authorized users
    """
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def move_cart_when_authenticate(request, user):
    """
    Move cart items into cart when user is logining
    """
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(cart=cart)
        for item in cart_item:
            item.user = user
            item.save()
    except:
        pass
