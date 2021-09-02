from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, is_active=True, password=None ):
        if not email:
            raise ValueError('کابران باید یک ایمیل داشته باشند')
        user = self.model(is_active=is_active,username=username, email=self.normalize_email(email) )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, is_active=True, password=None):
        user = self.create_user(username, email, is_active=is_active, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(verbose_name='نام کاربری', max_length=300, validators=[
        RegexValidator(regex=USERNAME_REGEX, message='نام کاربری باید شامل حروف الفبا و یا اعداد باشد',
                       code='invalid_username')], unique=True)

    email = models.EmailField(verbose_name='آدرس ایمیل', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='نام', max_length=300, blank=True, null=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=300, blank=True, null=True)
    is_admin = models.BooleanField(verbose_name='مدیر سایت', default=False, blank=True)
    is_staff = models.BooleanField(verbose_name='کارمند', default=False, blank=True)
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def get_short_name(self):
        """
        کاربر با ایمیل خود شناسایی می شود
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True


# مشتری
class Customer(CustomUser):
    is_admin = False
    is_staff = False

    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'


# کارمند
class Staff(CustomUser):
    is_staff = True
    is_admin = False

    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'


# مدیرسایت
class AdminSite(CustomUser):
    is_staff = True
    is_admin = True

    class Meta:
        proxy = True
        verbose_name = 'مدیر سایت'
        verbose_name_plural = 'مدیر سایت'


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