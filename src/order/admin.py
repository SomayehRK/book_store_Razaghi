from django.contrib import admin
from .models import *


class PercentageOffAdmin(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای نمایش ایتم های موجود در جدول تخفیفات درصدی
    """
    list_display = ['name', 'value', 'expired_time',]


class CashOffAdmin(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای نمایش ایتم های موجود در جدول تخفیفات نقدی
    """
    list_display = ['name', 'value', 'expired_time', ]


class OrderItemInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ['book']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'order_date', 'discount']
    list_filter = ['status', 'order_date', 'discount']
    inlines = [OrderItemInline]


class DiscountCodeAdmin(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای نمایش ایتم های موجود در جدول تخفیفات امتیازی
    """
    list_display = ['discount_code', 'value', 'valid_to', 'active',]


# admin.site.register(ShoppingBasket)
admin.site.register(OrderItems)
# admin.site.register(Order)
admin.site.register(CashOff, CashOffAdmin)
admin.site.register(PercentageOff, PercentageOffAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)

