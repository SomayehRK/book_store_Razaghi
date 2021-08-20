from django.db import models
from django.conf import settings
from book.models import Book, Category
from accounts.models import CustomUser, Address
from django.contrib.auth import get_user_model
import string
import random
from django.core.validators import MinValueValidator, MaxValueValidator


# تعریف تخفیف ها --------------------------
class PercentageOff(models.Model):
    """
    جدول تخفیف های درصدی
    name: نام
    value: مقداری تخفف اعمال شده
    created_by:این تخفیف توسط چه کسی ایجاد شده است
    created_time: زمان ایجاد تخفیف
    expired_time: زمان انقضای تخفیف
    active : وضعیت اعتبار
    """
    name = models.CharField(verbose_name='نوع تخفیف', max_length=50)
    value = models.IntegerField(verbose_name='میزان تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_by = models.ForeignKey(get_user_model(), verbose_name='ایجاد کننده', on_delete=models.CASCADE,)
    created_time = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    expired_time = models.DateTimeField(verbose_name='تاریخ انقضا')
    active = models.BooleanField(verbose_name='وضعیت اعتبار', default=False)

    class Meta:
        verbose_name_plural = 'تخفیف های درصدی'
        """
        براساس زمان انقضا مرتب میشوند
        """
        ordering = ['expired_time']

    def __str__(self):
        return str(self.name)


class CashOff(models.Model):
    """
    جدول تخفیف های نقدی
    name:نام
    value: مقدار تخفیف اعمال شده
    created_by: این تخفیف توسط چه کسی ایجاد شده است
    created_time: زمان ایجاد
    expired_time: زمان انقضای تخفیف
    active: وضعیت اعتبار
    """
    name = models.CharField(verbose_name='نوع تخفیف', max_length=50)
    value = models.DecimalField(verbose_name='مقدار تخیف', max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(get_user_model(), verbose_name='ایجاد کننده', on_delete=models.CASCADE,)
    created_time = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    expired_time = models.DateTimeField(verbose_name='تاریخ انقضا')
    active = models.BooleanField(verbose_name='وضعیت اعتبار', default=False)

    class Meta:
        verbose_name_plural = 'تخفیف های نقدی'
        """
        براساس زمان انقضا مرتب می شوند
        """
        ordering = ['expired_time']

    def __str__(self):
        return str(self.name)


class DiscountCode(models.Model):
    """
    جدول شامل کدهای تخفیف مربوطبه تخفیفات امتیازی و مقدار آنها
    discount_code: کد تخفیف
    value: درصد تخفیف که بصورت یک عدد بین 0 تا 100 دریافت می شود
    created_by:این تخفیف توسط چه کسی ایجاد شده است
    valid_from: از چه زمانی این کد تخفیف فال است
    valid_to: زمان انقضای این تخفیف
    active:آیا این کد فعال است یا خیر
    """
    discount_code = models.CharField(verbose_name='کد تخفیف', max_length=6, unique=True)
    value = models.IntegerField(verbose_name='مقدار تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_by = models.ForeignKey(get_user_model(), verbose_name='ایجاد کننده',
                                   on_delete=models.CASCADE, blank=True, null=True
                                   )
    valid_from = models.DateTimeField(verbose_name='تاریخ شروع تخفیف')
    valid_to = models.DateTimeField(verbose_name='تاریخ انقضا')
    active = models.BooleanField(verbose_name='وضعیت اعتبار', default=False)

    class Meta:
        verbose_name_plural = 'تخیف های امتیازی'
        """
        براساس زمان انقضا مرتب می شوند
        """
        ordering = ['valid_to']

    def __str__(self):
        return self.discount_code


# ------------------ > customer orders
class Order(models.Model):
    """
    جدول ثبت سفارشات
    customer: مشتری
    order_date: تاریخ سفارش
    discount: کد تخفیف امتیازی
    province: استان
    city: شهر
    postal_code: کد پستی
    full_address: آدرس کامل
    status: وضعیت سفارش
    """
    customer = models.ForeignKey(CustomUser,
                                 verbose_name='مشتری',
                                 on_delete=models.CASCADE,
                                 related_name='customer')
    order_date = models.DateTimeField(verbose_name='تاریخ ثبت سفارش', auto_now_add=True)
    discount = models.IntegerField(verbose_name='کد تخفیف', blank=True, null=True, default=None)
    province = models.CharField(verbose_name='استان', max_length=50, blank=True, null=True)
    city = models.CharField(verbose_name='شهر', max_length=50, blank=True, null=True)
    postal_code = models.BigIntegerField(verbose_name='کد پستی', blank=True, null=True)
    full_address = models.TextField(verbose_name='آدرس کامل', blank=True, null=True)
    STATUS = [
        ('ordered', 'سفارش'),
        ('record', 'ثبت')
    ]
    status = models.CharField(verbose_name='وضعیت سفارش', max_length=7, choices=STATUS, default='ordered')

    class Meta:
        verbose_name_plural = 'سفارش ها'
        ordering = ['order_date']

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        """
        :return: این متود براساس میزان تخفیف این سبد قیمت نهایی آن را محاسبه می کند
        """
        total_price = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total_price
            return int(total_price - discount_price)
        return total_price


class OrderItems(models.Model):
    """
    جزئیات سفارشهای موجود در سبد خرید
    order: کد سفارش
    book:  کتاب سفارش داده شده
    book_price: قیمت فروش کتاب
    book_quantity: تعداد خریداری شده
    """

    order = models.ForeignKey(Order, verbose_name='کد سفارش', related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='کتاب', null=True, on_delete=models.SET_NULL)
    book_price = models.FloatField(verbose_name='قیمت کتاب')
    book_quantity = models.PositiveSmallIntegerField(verbose_name='نعداد', default=1)

    class Meta:
        verbose_name_plural = 'جزئیات سفارش'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """
        محاسبه قیمت این ردیف از سفارشات براساس تعدادآن
        """
        return self.book_price * self.book_quantity






