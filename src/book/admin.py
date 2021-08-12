from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    """
    کاستوم کردن پنل ادمین برای نمایش ایتم های موجود در جدول کتاب ها
    """
    list_display = ("title", "author", "price",)


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
