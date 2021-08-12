from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای نمایش ایتم های موجود در جدول مشتری ها
    """
    list_display = ('full_name', 'email')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomUser)
admin.site.register(Address)