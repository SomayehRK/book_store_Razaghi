from django import forms
from .models import Order
from django.contrib.auth import get_user_model
from accounts.models import CustomUser, Address


class DiscountForm(forms.Form):
	"""
	فرم وارد کردن کد تخفیف
	"""
	code = forms.CharField(label='کد تخفیف')


class OrderCreateForm(forms.Form):
	"""
	فرم گرفتن آدرس ارسال سفارش
	"""
	default_address = forms.ModelChoiceField(label="آدرس های موجود", queryset=Address.objects.all(),
											 required=False, widget=forms.Select())

	def __init__(self, customer, *args, **kwargs):
		super(OrderCreateForm, self).__init__(*args, **kwargs)
		self.fields['default_address'].queryset = customer.address_set.all()

	province = forms.CharField(label='استان', max_length=50, required=False)
	city = forms.CharField(label='شهر', max_length=50, required=False)
	postal_code = forms.IntegerField(label='کد پستی', required=False)
	full_address = forms.CharField(label='آدرس کامل', widget=forms.Textarea, required=False)

