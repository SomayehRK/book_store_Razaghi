from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from book.models import Book
from .cart import Cart
from .forms import CartAddBookForm
from order.forms import DiscountForm
from django.contrib import messages


@require_POST
def cart_add(request, book_id):
    """
    افزودن کتاب براساس تعداد مورد تقاضا به سبد خرید و بررسی موجودی انبار
    """
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if data['quantity'] <= book.quantity:
            cart.add(book=book, quantity=data['quantity'], override_quantity=data['override'])
        else:
            messages.error(request, 'موجودی انبار کافی نیست!', 'danger')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, book_id):
    """
    حذف کتاب از سبد خرید
    """
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    مشاهده جزئیات سبد خرید
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(initial={'quantity': item['quantity'], 'override': True})
    coupon_apply_form = DiscountForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
