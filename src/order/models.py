from django.db import models
from book.models import Book, Category
from accounts.models import Customer
from django.contrib.auth import get_user_model
import string, random
from django.core.validators import MinValueValidator, MaxValueValidator


class PercentageOff(models.Model):
    """
    جدول نگه داری کتابهای مشمول تخفیف درصدی
    book: کتاب
    category: کدام گروه از کتاب ها
    value: مقداری تخفف اعمال شده
    created_by:این تخفیف توسط چه کسی ایجاد شده است
    created_time: زمان ایجاد تخفیف
    expired_time: زمان انقضای تخفیف
    """
    book = models. ForeignKey(
        Book,
        related_name='book_percent_off',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name='category_percent_off',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField(auto_now_add=True)
    expired_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'تخفیف های درصدی'
        """
        براساس زمان انقضا مرتب میشوند
        """
        ordering = ['expired_time']

    def __str__(self):
        return str(self.value)


class CashOff(models.Model):
    """
    جدول مربوط به کتابهای مشمول تخفیف نقدی
    book:کتاب
    category: کدام گروه از کتاب ها
    value: مقدار تخفیف اعمال شده
    created_by: این تخفیف توسط چه کسی ایجاد شده است
    created_time: زمان ایجاد
    expired_time: زمان انقضای تخفیف
    """
    book = models.ForeignKey(
        Book,
        related_name='book_cash_of',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name='category_cash_off',
        on_delete=models.CASCADE,
        blank=True,  null=True
    )
    value = models.IntegerField(default=None)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField(auto_now_add=True)
    expired_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'تخفیف های نقدی'
        """
        براساس زمان انقضا مرتب می شوند
        """
        ordering = ['expired_time']

    def __str__(self):
        return str(self.value)


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
    discount_code = models.CharField(
        max_length=6,
        unique=True
    )
    value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_by = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
        )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'تخیف های امتیازی'
        """
        براساس زمان انقضا مرتب می شوند
        """
        ordering = ['valid_to']

    def __str__(self):
        return self.discount_code

    def create_code(self):
        """
        :return: این متود یک کد 6 کاراکتری شامل اعداد و حروف بصورت رندوم بعنوان مد تخفیف تولید می کند
        """
        self.discount_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return self.discount_code


class ShoppingBasket(models.Model):
    """
    سبد خرید مشتری
    customer: مشتری
    order_date: تاریخ سفارش
    discount: میزان تخفیف تعلق گرفته به این سبد خرید
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    order_date = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(
        blank=True,
        null=True,
        default=None)

    class Meta:
        verbose_name_plural = 'سبدهای خرید'
        ordering = ['customer']

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
    shop_basket: کدام سبد خرید
    book:  کتاب سفارش داده شده
    book_price: قیمت فروش کتاب
    book_quantity: تعداد خریداری شده
    status: وضعیت سفارش پرداخت شده یا سفارش داده شده
    """
    STATUS = [
        ('ordered', 'سفارش'),
        ('record', 'ثبت')
    ]
    shop_basket = models.ForeignKey(
        ShoppingBasket,
        related_name='basket_id',
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        null=True,
        on_delete=models.SET_NULL
    )
    book_quantity = models.PositiveSmallIntegerField(default=1)
    percent_off = models.IntegerField(
        blank=True,
        null=True,
        default=0)
    cash_off = models.IntegerField(
        blank=True,
        null=True,
        default=0)
    status = models.CharField(
        max_length=7,
        choices=STATUS,
        default='ordered'
    )

    class Meta:
        verbose_name_plural = 'جزئیات خرید'

    def __str__(self):
        return str(self.id)

    @property
    def sell_price(self):
        """
        :return: قیمت نهایی کتاب پس از اعمال تخفیف ها
        """
        final_price = (book.price - self.cash_off) - ((self.percent_off/100) * book.price)
        return final_price

    def get_cost(self):
        """
        :return: قیمت نهایی این ردیف از سبد کالا را با توجه به قیمت اصلی کتاب و تعداد خریداری شده محاسبه می کند
        """
        return self.sell_price * self.book_quantity
