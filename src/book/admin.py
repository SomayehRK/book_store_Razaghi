from django.contrib import admin
from .models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','slug', 'price', 'quantity',
                    'available', 'create_time', 'update_time']
    list_filter = ['available', 'create_time', 'update_time']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}