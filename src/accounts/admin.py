from django.contrib import admin
from .models import AdminSite, Staff, Customer, Address
from django.contrib.auth import get_user_model


@admin.register(AdminSite)
class AdminSite(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای مدیر فروشگاه
    """
    list_display = ('username', 'email',)
    empty_value_display = '-empty-'

    def get_queryset(self, request):
        return get_user_model().objects.filter(is_superuser=True, is_staff=True)


@admin.register(Staff)
class AdminStaff(admin.ModelAdmin):
    """
        کاستوم کردن پنل ادمین برای کارمندان فروشگاه
    """
    list_display = ('username', 'email',)
    empty_value_display = '-empty-'

    def get_queryset(self, request):
        return get_user_model().objects.filter(is_superuser=False, is_staff=True)


@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    """
        کاستوم کردن پنل ادمین برای مشتریان فروشگاه
    """
    list_display = ('username', 'email',)
    empty_value_display = '-empty-'

    def get_queryset(self, request):
        return get_user_model().objects.filter(is_superuser=False, is_staff=False)


admin.site.register(Address)