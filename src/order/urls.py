from django.urls import path
from .views import order_create, order_detail, discount_code_apply

app_name = 'order'
urlpatterns = [
    #ایجاد سفارش از روی سبد خرید
    path('create/', order_create, name='order_create'),

    # مشاهده سفارش
    path('<int:order_id>/', order_detail, name='order_detail'),

    # اعمال تخفیف روی سب خرید
    path('apply/', discount_code_apply, name='discount_apply'),
]




