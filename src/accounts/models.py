from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        ایجاد کاربر
        """
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now, joined_at=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        ایجاد کاربر سوپر یوزر
        """
        user = self.create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    username:نام کاربری
    email: ایمبل
    first_name : نام
    last_name : نام خانوادگی
    is_superuser : مدیر سایت
    is_staff : کارمند
    is_active : فعال
    last_login : آخرین ورود
    joined_at : تاریخ ثبت نام
    """
    username = models.CharField(verbose_name='نام کاربری', max_length=300, unique=True)
    email = models.EmailField(verbose_name='ایمیل', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='نام', max_length=300, blank=True, null=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=300, blank=True, null=True)
    is_superuser = models.BooleanField(verbose_name='مدیر سایت', default=False)
    is_staff = models.BooleanField(verbose_name='کارمند', default=False)
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    last_login = models.DateTimeField(verbose_name='آخرین ورود', blank=True, null=True)
    joined_at = models.DateTimeField(verbose_name='تاریخ ثبت نام', auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class AdminSite(CustomUser):
    """
    مدل مدیر فروشگاه
    """
    is_staff = True
    is_superuser = True

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
    is_staff = True
    is_superuser = False

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
    is_staff = False
    is_superuser = False

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
    customer = models.ForeignKey(get_user_model(), verbose_name='مشتری', on_delete=models.CASCADE, blank=True, null=True)
    province = models.CharField(verbose_name='استان', max_length=50)
    city = models.CharField(verbose_name='شهر', max_length=50)
    postal_code = models.CharField(verbose_name='کد پستی', max_length=12)
    full_address = models.TextField(verbose_name='آدرس کامل')

    class Meta:
        verbose_name_plural = 'آدرس ها'
        ordering = ['customer']

    def __str__(self):
        return self.full_address