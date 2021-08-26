from django.contrib import admin
from .models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش دسته های موجود در پنل ادمین
    """
    list_display = ['name', 'slug']
    empty_value_display = '-empty-'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    کاستوم کردن نمایش کتاب های موجود در پنل ادمین
    """
    list_display = ['title', 'author','slug', 'price', 'quantity',
                    'available', 'create_time', 'update_time']
    empty_value_display = '-empty-'
    list_filter = ['available', 'create_time', 'update_time']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}