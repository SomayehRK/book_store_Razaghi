from django.urls import path
from .views import book_list, book_detail


app_name = 'book'
urlpatterns = [
    # مشاهده لیست کتاب ها
    path('', book_list, name='book_list'),

    # مشاهده کتاب های مرتبط به یک دسته
    path('<slug:category_slug>/', book_list, name='book_list_by_category'),

    # مشاهده جزئیات هر کتاب
    path('<int:id>/<slug:slug>/', book_detail, name='book_detail'),
]
