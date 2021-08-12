from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Category(models.Model):
    """
    مدل مربوط به دسته بندی های کتابها
    name: نام دسته
    created_by: توسط چه کسی ایجاد شده است
    create_time: زمان ایجاد این آیتم
    update_time: زمان بروزرسانی این آیتم
    """
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
        )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'گروه ها'
        """
        براساس نام گروه مرتب می شوند
        """
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    مدل مربوط به کتابهای فروشگاه
    title: عنوان کتاب
    author: نویسنده کتاب
    category: دسته ای که این کتاب به آن تعلق دارد
    price: فیمت اصلی کتاب
    created_by: این آیتم توسط چه کسی ایجاد شده است
    quantity: موجودی کتاب
    created_time: زمان ایجاد این آیتم
    update_time: زمان بروزرسانی این آیتم
    """
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.ManyToManyField(
        Category,
        related_name='category'
    )
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()
    created_by = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
        )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'کتاب ها'
        """
        براساس زمان ایجاد مرتب میشوند
        """
        ordering = ['create_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
