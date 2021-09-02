from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import Customer, Address
from book.models import Book, Category
from order.models import DiscountCode, CashOff, PercentageOff
from django.contrib.auth import get_user_model
from django.db.models import Q
from django import forms
from accounts.models import Address
User = get_user_model()


class CustomerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("پسورد اشتباست")
        return password2

    def save(self, commit=True):
        user = super(CustomerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='گذر واژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید گذر واژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['password', 'last_login']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("پسورد اشتباست")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(label='ایمیل')
    password = forms.CharField(label='گذر واژه', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("اعتبار نامعتبر کاربری وجود ندارد")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("اعتبارنامه اشتباست")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


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


