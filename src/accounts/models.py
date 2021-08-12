from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    مدل مربوط به کارمندان شامل کارمندان ساده و ادمین
    """
    class Meta:
        verbose_name_plural = 'کارمندان'


class Customer(models.Model):
    """
    مدل مربوط به مشتری ها
    username: نام کاربری مشتری
    first_name: نام کوچک مشتری
    last_name: نام خانوادگی مشتری
    email: ایمیل مشتری
    password: رمز عبور مشتری
    """
    username = models.CharField('نام کاربری', max_length=50)
    first_name = models.CharField('نام', max_length=50)
    last_name = models.CharField('نام خانوادگی', max_length=50)
    email = models.EmailField('ایمیل')
    password = models.CharField(max_length=50, default=None)

    class Meta:
        verbose_name_plural = 'مشتری ها'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name


class Address(models.Model):
    """
    مدل مربوط به آدرس های هر مشتری
    customer: مشتری
    province: استان محل سکونت
    city: شهر محل سکونت
    postal_code: کد پستی محل سکونت
    full_address: آدرس کامل
    """
    customer = models.ForeignKey(Customer, related_name='customer_id', on_delete=models.CASCADE)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.BigIntegerField()
    full_address = models.TextField()

    class Meta:
        verbose_name_plural = 'آدرس ها'
        ordering = ['customer']
