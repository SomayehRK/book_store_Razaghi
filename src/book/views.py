from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from cart.forms import CartAddBookForm
from django.utils import timezone
from order.models import CashOff
from django.db.models import Q
from django.contrib import messages


def book_list(request, category_slug=None):
    """
    مشاهده لیست کتاب ها و همچنین نایج جستجو
    """
    category = None
    categories = Category.objects.all()
    search_book = request.GET.get('search')
    if search_book:
        books = Book.objects.filter(Q(title__icontains=search_book) | Q(author__icontains=search_book), available=True)
    else:
        books = Book.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)
    return render(request,
                  'book/book_list.html',
                  {'category': category, 'categories': categories, 'books': books}
                  )


def book_detail(request, id, slug):
    """
    مشاهده اطلاعات مربوط به کتاب مورد ظر
    """
    book = get_object_or_404(Book, id=id, slug=slug, available=True)
    cart_book_form = CartAddBookForm
    return render(request,
                  'book/book_detail.html',
                  {'book': book, 'cart_book_form': cart_book_form}
                  )



