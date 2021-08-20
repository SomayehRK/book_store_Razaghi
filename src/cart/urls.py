from django.urls import path
from .views import cart_add, cart_remove, cart_detail

app_name = 'cart'
urlpatterns = [
    # مشاهده جزئیات سبد خرید
    path('', cart_detail, name='cart_detail'),

    # افزودن به سبد خرید
    path('add/<int:book_id>/', cart_add, name='cart_add'),

    # حذف از سبد خرید
    path('remove/<int:book_id>/', cart_remove, name='cart_remove'),
]