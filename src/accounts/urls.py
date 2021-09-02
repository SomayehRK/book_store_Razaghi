from django.urls import path
from .views import *
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [

    path('register/', register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    # ویرایش اطلاعات کاربر
    path('profile/', EditProfile.as_view(), name='edit_profile'),
    path('profile/address/', list_address, name='list_address'),
    path('profile/address/add', add_address, name='add_address'),
    path('profile/orders', history_order, name='order_list'),
    path('profile/<int:order_id>', order_detail, name='order_detail'),

    # عملیات کارمند
    path('panel/', staff_panel, name='staff_panel'),
    path('staff/create/book/', CreateBookView.as_view(), name='create_book'),
    path('staff/create/category/', CreateCategoryView.as_view(), name='create_category'),
    path('staff/create/cashoff/', CreateCashOffView.as_view(), name='create_cash_off'),
    path('staff/create/percentoff/', CreatePercentOffView.as_view(), name='create_percent_off'),
    path('staff/create/discountcode/', CreateDiscountCodeView.as_view(), name='create_discount_code'),
]