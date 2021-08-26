from django.urls import path
from .views import *
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    # ورود و ثبت نام کاربران
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # تغییر و ریست پسورد
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ویرایش اطلاعات کاربر
    path('profile/', EditProfile.as_view(), name='edit_profile'),
    path('profile/address/', list_address, name='list_address'),
    path('profile/address/add', add_address, name='add_address'),
    # path('profile/orders', ListOrder.as_view(), name='order_list'),
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