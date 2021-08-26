from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import CustomUser
from decimal import Decimal


class Category(models.Model):
    """
    name: نام دسته
    created_by: ایجاد کننده
    create_time: تاریخ ایجاد دسته
    update_time : تاریخ بروزرسانی دسته
    """
    name = models.CharField(verbose_name='دسته', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_by = models.ForeignKey(get_user_model(), verbose_name='ایجاد کننده', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name_plural = 'گروه ها'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book:book_list_by_category', args=[self.slug])


class Book(models.Model):
    """
    category: دسته مربوطه
    title: عنوان کتاب
    author: نویسنده کتاب
    price: قیمت کتاب
    cash_off: تخفیف نقدی اعمال شده بر روی کتاب
    percent_off: تخفیف درصدی اعمال شده بر روی کتاب
    quantity: موجودی انبار
    available: موجود بودن در انبار
    created_by: ایجاد کننده
    create_time: تاریخ ایجاد
    update_time: تاریخ بروزرسانی
    """
    category = models.ManyToManyField(Category, verbose_name='دسته', related_name='books')
    title = models.CharField(verbose_name='عنوان کتاب', max_length=200, db_index=True)
    author = models.CharField(verbose_name='نویسنده', max_length=100)
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.IntegerField(verbose_name='قیمت کتاب')
    cash_off = models.ForeignKey('order.CashOff', verbose_name='تخفیف نقدی',
                                 on_delete=models.DO_NOTHING, blank=True, null=True
                                 )
    percent_off = models.ForeignKey('order.PercentageOff', verbose_name='تخفیف درصدی',
                                    on_delete=models.DO_NOTHING, blank=True, null=True
                                    )
    quantity = models.IntegerField(verbose_name='موجودی انبار')
    available = models.BooleanField(verbose_name='موجود در انبار', default=True)
    created_by = models.ForeignKey(get_user_model(), verbose_name='ایجاد کننده', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name_plural = 'کتاب ها'
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def list_category(self):
        """
        متودی که دسته های مربوطه به این کتاب را برمیگرداند
        """
        return self.category.all()

    @property
    def how_much_percent_off(self):
        """
        در صورت وجود تخفیف درصدی میزان تخفیف را محاسبه می کند
        """
        # self.percent_off.change_status()
        if self.percent_off is not None and self.percent_off.active:
            return (self.percent_off.value / 100) * float(self.price)
        return 0

    @property
    def final_price(self):
        """
        ابتدا بررسی می کند آیا تخفیف نقدی روی کتاب اعمال شده و سپس با توجه به نتیجه بررسی و مشخصه میزان تخفیف درصدی قیمت نهایی کتاب را برمیگرداند
        """
        if self.cash_off and self.cash_off.active:
            price_off = self.price - (self.cash_off.value + self.how_much_percent_off)
            if price_off > 0:
                return price_off
        return self.price - self.how_much_percent_off

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[self.id, self.slug])

