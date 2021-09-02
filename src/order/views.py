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
def order_create(request):
    """
    ایجاد سفارش از روی سبد خرید
    """
    cart = Cart(request)
    try:
        order = Order.objects.get(customer=request.user, status='ordered')
    except Order.DoesNotExist:
        order = Order.objects.create(customer=request.user)
    if request.method == 'POST' and request.user:

        form = OrderCreateForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['default_address']:
                order.customer_address = data['default_address']
                # order = Order.objects.create(customer=request.user, customer_address=data['default_address'], status='ordered')
                for item in cart:
                    OrderItems.objects.create(order=order,
                                              book=item['book'],
                                              book_price=item['price'],
                                              book_quantity=item['quantity']
                                              )
                    book = Book.objects.get(title=item['book'])
                    book.quantity = book.quantity - item['quantity']
                    book.save()
                if cart.coupon:
                    order.discount = cart.coupon.value
                order.status = 'record'
                order.save()
                cart.clear()
                return render(request, 'orders/complete_order.html', {'order': order})
            else:
                user_new_addrr = Address.objects.create(customer=request.user,
                                                        province=data['province'],
                                                        city=data['city'],
                                                        postal_code=data['postal_code'],
                                                        full_address=data['full_address'])
                user_new_addrr.save()
                order.customer_address = user_new_addrr
                # order = Order.objects.create(customer=request.user, customer_address=user_new_addrr)
                for item in cart:
                    OrderItems.objects.create(order=order,
                                              book=item['book'],
                                              book_price=item['price'],
                                              book_quantity=item['quantity']
                                              )
                    book = Book.objects.get(title=item['book'])
                    book.quantity = book.quantity - item['quantity']
                    book.save()
                if cart.coupon:
                    order.discount = cart.coupon.value
                order.status = 'record'
                order.save()
                cart.clear()
                return render(request, 'orders/complete_order.html', {'order': order})
    else:
        form = OrderCreateForm(request.user)
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