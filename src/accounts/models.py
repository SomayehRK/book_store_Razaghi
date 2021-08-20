from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    """
    user_type: نقش کاربر
    """
    USER_TYPE = (
        (1, 'مدیر سایت'),
        (2, 'کارمند'),
        (3, 'مشتری'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=1)


class AdminSite(CustomUser):
    """
    مدل مدیر فروشگاه
    """
    class Meta:
        proxy = True
        verbose_name = 'مدیر سایت'
        verbose_name_plural = 'مدیر سایت'

    def __str__(self):
        return self.email


class Staff(CustomUser):
    """
    مدل کارمند فروشگاه
    """
    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'

    def __str__(self):
        return self.email


class Customer(CustomUser):
    """
    مدل مشتری
    """
    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'

    def __str__(self):
        return self.email


class Address(models.Model):
    """
    مدل مربوط به آدرس های هر مشتری
    customer: مشتری
    province: استان محل سکونت
    city: شهر محل سکونت
    postal_code: کد پستی محل سکونت
    full_address: آدرس کامل
    """
    customer = models.ForeignKey(get_user_model(), verbose_name='مشتری', on_delete=models.CASCADE)
    province = models.CharField(verbose_name='استان', max_length=50)
    city = models.CharField(verbose_name='شهر', max_length=50)
    postal_code = models.BigIntegerField(verbose_name='کد پستی')
    full_address = models.TextField(verbose_name='آدرس کامل')

    class Meta:
        verbose_name_plural = 'آدرس ها'
        ordering = ['customer']

    def __str__(self):
        return self.full_address
