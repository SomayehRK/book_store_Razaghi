from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import Customer, Address
from book.models import Book, Category
from order.models import DiscountCode, CashOff, PercentageOff


class CustomUserCreationForm(UserCreationForm):
    """
    کاستومایز کردم فرم ایجاد کاربری جهت استفاده در پروسه ثبتنام در سایت
    """
    email = forms.EmailField(label="Email")

    class Meta:
        model = get_user_model()
        fields = ("username", "email",)

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = get_user_model()
        fields = ("username", "email",)


class LoginForm(AuthenticationForm):
    """
    کاستومایز کردن فرم تایید هویت کاربران جهت استفاده در پروسه لاگین در سایت
    """
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfile(forms.ModelForm):
    """
    فرم ویرایش اطلاعات کاربری
    """
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'last_login')


class AddAddress(forms.ModelForm):
    """
    فرم افزودن آدرس جدید
    """
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('customer',)


class AddBookCategory(forms.ModelForm):
    """
    فرم افزودن دسته جدید
    """
    class Meta:
        model = Category
        fields = '__all__'


class AddBookToStore(forms.ModelForm):
    """
    فرم افزودن کتاب جدید
    """
    class Meta:
        model = Book
        fields = '__all__'


class CreateCashOff(forms.ModelForm):
    """
    فرم تعریف تخفیف نقدی
    """
    class Meta:
        model = CashOff
        fields = '__all__'


class CreatePercentOff(forms.ModelForm):
    """
    فرم تعریف تخفیف درصدی
    """
    class Meta:
        model = PercentageOff
        fields = '__all__'


class CreateDiscountCode(forms.ModelForm):
    """
    فرم تعریف تخفیف امتیازی
    """
    class Meta:
        model = DiscountCode
        fields = '__all__'


