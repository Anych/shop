from django.urls import path

from orders import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('order/<int:order_number>', views.orders, name='order'),

    path('payments/', views.payments, name='payments'),
]
