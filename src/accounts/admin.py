from django.contrib import admin
from .models import AdminSite, Staff, Customer, Address
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, CustomerCreationForm
from .models import CustomUser,Staff, Customer, AdminSite, Address


class UserAdmin(BaseUserAdmin):
    """
    کاستوم کردن نمایش کاربران در پنل ادمین جنگو
    """
    add_form = UserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    list_editable = ['first_name', 'last_name']
    list_filter = ('is_admin',)
    fieldsets = (
                (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
                    ('Permissions', {'fields': ('is_admin',)})
                    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)


# @admin.register(Customer)
# class AdminCustomer(admin.ModelAdmin):
#     """
#     کاستوم کردن نمایش کاربران در پنل ادمین جنگو
#     """
#     add_form = CustomerCreationForm
#     form = CustomerCreationForm
#     list_display = ['email', 'username', 'first_name', 'last_name']
#     list_editable = ['first_name', 'last_name']
#     search_fields = ('username', 'email')
#     ordering = ('username', 'email')
#
#     def get_queryset(self, request):
#         return get_user_model().objects.filter(is_admin=False, is_staff=False)
#
#
# @admin.register(Staff)
# class AdminStaff(admin.ModelAdmin):
#     """
#     کاستوم کردن نمایش کاربران در پنل ادمین جنگو
#     """
#     add_form = CustomerCreationForm
#     form = CustomerCreationForm
#     list_display = ['email', 'username', 'first_name', 'last_name']
#     list_editable = ['first_name', 'last_name']
#     search_fields = ('username', 'email')
#     ordering = ('username', 'email')
#
#     def get_queryset(self, request):
#         return get_user_model().objects.filter(is_admin=False, is_staff=True)
#
#
# @admin.register(AdminSite)
# class AdminSite(admin.ModelAdmin):
#     """
#     کاستوم کردن نمایش کاربران در پنل ادمین جنگو
#     """
#     add_form = CustomerCreationForm
#     form = CustomerCreationForm
#     list_display = ['email', 'username', 'first_name', 'last_name']
#     list_editable = ['first_name', 'last_name']
#     search_fields = ('username', 'email')
#     ordering = ('username', 'email')
#
#     def get_queryset(self, request):
#         return get_user_model().objects.filter(is_admin=True, is_staff=True)
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['email', 'username','first_name','last_name' ]
    add_form = UserCreationForm
    form = UserCreationForm
    list_editable = ['first_name', 'last_name']
    def get_queryset(self, request):
        return get_user_model().objects.filter(is_admin=False, is_staff=False)


@admin.register(Staff)
class AdminStaff(admin.ModelAdmin):
    list_display = ['email', 'username','first_name','last_name' ]
    add_form = UserCreationForm
    form = UserCreationForm
    list_editable = ['first_name', 'last_name']

    def get_queryset(self, request):
        return get_user_model().objects.filter(is_admin=False, is_staff=True)


@admin.register(AdminSite)
class AdminSite(admin.ModelAdmin):
    list_display = ['email', 'username','first_name','last_name' ]
    add_form = UserCreationForm
    form = UserCreationForm
    list_editable = ['first_name', 'last_name']

    def get_queryset(self, request):
        return get_user_model().objects.filter(is_admin=True, is_staff=True)


@admin.register(Address)
class AdminAddress(admin.ModelAdmin):
    """
    کاستوم کردن نمایش آدرس کاربران در پنل ادمین جنگو
    """
    list_display = ['customer', 'full_address']
    search_fields = ('customer',)
    ordering = ('customer',)

