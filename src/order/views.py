from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItems, DiscountCode
from book.models import Book
from cart.cart import Cart
from .forms import *
from django.views.decorators.http import require_POST
from accounts.models import Address


@login_required
def order_detail(request, order_id):
    """
    مشاهده سفارش
    """
    order = get_object_or_404(Order, id=order_id)
    form = DiscountForm()
    return render(request, 'orders/order.html', {'order': order, 'form': form})


@login_required
def order_create(request):
    """
    ایجاد سفارش از روی سبد خرید
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['default_address']:
                addr = Address.objects.filter(customer=request.user)[0]
                order = Order.objects.create(customer=request.user, province=addr.province,
                                             city=addr.city, postal_code=addr.postal_code,
                                             full_address=addr.full_address)
                for item in cart:
                    OrderItems.objects.create(order=order,
                                              book=item['book'],
                                              book_price=item['price'],
                                              book_quantity=item['quantity']
                                              )
                    book = Book.objects.get(title=item['book'])
                    book.quantity = book.quantity - item['quantity']
                    order.status = 'record'
                    book.save()
                    order.save()
                cart.clear()
                return render(request, 'orders/complete_order.html', {'order': order})
            else:
                order = Order.objects.create(customer=request.user, province=data['province'],
                                             city=data['city'], postal_code=data['postal_code'],
                                             full_address=data['full_address'])
                for item in cart:
                    OrderItems.objects.create(order=order,
                                              book=item['book'],
                                              book_price=item['price'],
                                              book_quantity=item['quantity']
                                              )
                    book = Book.objects.get(title=item['book'])
                    book.quantity = book.quantity - item['quantity']
                    order.status = 'record'
                    book.save()
                    order.save()
                cart.clear()
                return render(request, 'orders/order_create.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


@require_POST
def discount_code_apply(request):
    """
    اعمال تخفیف روی سبد خرید
    """
    now = timezone.now()
    form = DiscountForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = DiscountCode.objects.get(discount_code__iexact=code,
                                              valid_from__lte=now,
                                              valid_to__gte=now,
                                              active=True
                                              )
            request.session['coupon_id'] = coupon.id
        except DiscountCode.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'This coupon does not exist', 'danger')
        return redirect('cart:cart_detail')