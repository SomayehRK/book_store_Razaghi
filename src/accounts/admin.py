from django.contrib import admin
from .models import *


@admin.register(AdminSite)
class AdminSite(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای مدیر فروشگاه
    """
    list_display = ('username', 'email',)

    def get_queryset(self, request):
        return CustomUser.objects.filter(user_type=1)


@admin.register(Staff)
class AdminStaff(admin.ModelAdmin):
    """
        کاستوم کردن پنل ادمین برای کارمندان فروشگاه
    """
    list_display = ('username', 'email',)

    def get_queryset(self, request):
        return CustomUser.objects.filter(user_type=2)


@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    """
        کاستوم کردن پنل ادمین برای مشتریان فروشگاه
    """
    list_display = ('username', 'email',)

    def get_queryset(self, request):
        return CustomUser.objects.filter(user_type=3)


admin.site.register(Address)