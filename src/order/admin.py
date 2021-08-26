from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(PercentageOff)
class PercentageOffAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش تخفیف های درصدی در پنل ادمین
    """
    list_display = ['name', 'created_time', 'expired_time', 'value', 'active']
    empty_value_display = '-empty-'
    list_filter = ['active', 'expired_time']
    search_fields = ['name']


@admin.register(CashOff)
class CashOffAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش تخفیف های نقدی در پنل ادمین
    """
    list_display = ['name', 'created_time', 'expired_time', 'value', 'active']
    empty_value_display = '-empty-'
    list_filter = ['active', 'expired_time']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    """
    نمایش لیست کتاب های موجود در یک سفارش
    """
    model = OrderItems
    raw_id_fields = ['book']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش سفارشات در پنل ادمین
    """
    list_display = ['id', 'customer', 'status', 'order_date', 'discount', 'total_price']
    empty_value_display = '-empty-'
    list_filter = ['status', 'order_date',]
    inlines = [OrderItemInline]

    @admin.display()
    def total_price(self, obj):
        return obj.get_total_price()


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش تخفیف های امتیازی در پنل ادمین
    """
    list_display = ['discount_code', 'valid_from', 'valid_to', 'value', 'active']
    empty_value_display = '-empty-'
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['discount_code']


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش جزئیات هر سفارش در پنل ادمین
    """
    list_display = ['order', 'book', 'book_quantity', 'total_price']
    empty_value_display = '-empty-'
    list_filter = ['order', 'book',]

    @admin.display()
    def total_price(self, obj):
        return obj.get_cost()

