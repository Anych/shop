from django.shortcuts import redirect, render
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderProduct
from store.models import Product, Size
from store.utils import order_email


def payments(request):
    return render(request, 'orders/payments.html')


def order_complete(request):
    return render(request, 'orders/order_complete.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    delivery = 2000
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    if total > 50000:
        delivery = 0
    grand_total = delivery + total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.delivery = delivery
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Код без оплаты, оформление заказа
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

            payment = Payment(
                user=request.user,
                payment_id=order.id,
                payment_method='Оплата курьеру',
                amount_paid=grand_total,
                status='В заказе',
            )
            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.save()

            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order.payment = payment
                order_product.user_id = request.user.id
                order_product.size = item.size
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.product_price = item.product.price
                order_product.ordered = True
                order_product.save()

                # уменьшение колличества товара
                size = Size.objects.get(product=item.product_id, size=item.size)
                size.stock -= item.quantity
                size.save()

            # очистка корзины
            CartItem.objects.filter(user=request.user).delete()

            # отправка письма
            mail_subject = 'Спасибо за покупку!'
            message = render_to_string('orders/order_received_email.html', {
                'user': current_user,
                'order': order,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            order_email(order.id)
            return redirect('order_complete')
        else:
            return redirect('checkout')


@login_required(login_url='login')
def orders(request, order_number):

    order = Order.objects.get(order_number=order_number)
    order_products = order.orderproduct_set.all()
    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'orders/order.html', context)
