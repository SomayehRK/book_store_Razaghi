from django.urls import path
from .views import order_create, discount_code_apply

app_name = 'order'
urlpatterns = [
    # ایجاد سفارش از روی سبد خرید
    path('create/', order_create, name='order_create'),

    # اعمال تخفیف روی سب خرید
    path('apply/', discount_code_apply, name='discount_apply'),
]




