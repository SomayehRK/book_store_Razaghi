from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from .models import Customer, Address, CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from order.models import *
from book.models import *
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


def user_signup(request):
    """
    ثبت نام کاربر
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'account/redirect_page.html', )
    form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form':form})


def user_login(request):
    """
    ورود کاربران
    """
    if request.method == 'POST':
        form = LoginForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff == False:
                return redirect('book:book_list')
            else:
                return render(request, 'account/staff_panel.html', )
    form = LoginForm()
    return render(request, "account/login.html", {'form': form})


def user_logout(request):
    """
    خروج کاربران
    """
    logout(request)
    return redirect('book:book_list')


def staff_panel(request):
    """
    پنل کارمندان
    """
    return render(request, 'account/staff_panel.html')


class EditProfile(UpdateView):
    """
    ویرایش اطلاعات کاربری
    """
    model = Customer
    template_name = 'account/edit_profile.html'
    form_class = EditProfile
    success_url = reverse_lazy('account:edit_profile')

    def get_object(self):
        return Customer.objects.get(pk=self.request.user.pk)


def list_address(request):
    """
    مشاهده آدرس های موجود
    """
    address = Address.objects.filter(customer=request.user)
    context = {
        'address': address
    }
    return render(request, 'account/address_list.html', context)


@login_required()
def add_address(request):
    """
    افزودن آدرس جدید
    """
    if request.method == 'POST':
        form = AddAddress(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_address = Address.objects.create(customer=request.user, province=data['province'], city=data['city'],
                                                 postal_code=data['postal_code'], full_address=data['full_address'])
            new_address.save()
    else:
        form = AddAddress()
    return render(request, 'account/add_address.html', {'form': form})


def history_order(request):
    """
    مشاهده تاریخچه سفارشات
    """
    orders = Order.objects.filter(customer=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'account/order_history.html', context)


def order_detail(request, order_id):
    """
    مشاهده جزئیات هر سفارش
    """
    order_items = OrderItems.objects.filter(order=order_id)
    context = {
        'order_items': order_items
    }
    return render(request, 'account/order_detail.html', context)


class CreateBookView(CreateView):
    """
    افزودن کتاب جدید
    """
    model = Book
    form_class = AddBookToStore
    template_name = 'account/create_book.html'
    success_url = reverse_lazy('book:book_list')


class CreateCategoryView(CreateView):
    """
    ایجاد دسته جدید
    """
    model = Category
    form_class = AddBookCategory
    template_name = 'account/create_category.html'
    success_url = reverse_lazy('book:book_list')


class CreateCashOffView(CreateView):
    """
    تعریف تخفیف نقدی
    """
    model = CashOff
    form_class = CreateCashOff
    template_name = 'account/create_cash_off.html'
    success_url = reverse_lazy('account:create_cash_off')


class CreatePercentOffView(CreateView):
    """
    تعریف تخفیف درصدی
    """
    model = PercentageOff
    form_class = CreatePercentOff
    template_name = 'account/create_percent_off.html'
    success_url = reverse_lazy('account:create_percent_off')


class CreateDiscountCodeView(CreateView):
    """
    تعریف کد تخفیف
    """
    model = DiscountCode
    form_class = CreateDiscountCode
    template_name = 'account/create_discount_code.html'
    success_url = reverse_lazy('account:create_discount_code')