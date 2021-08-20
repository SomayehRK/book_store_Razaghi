from decimal import Decimal
from django.conf import settings
from book.models import Book
from order.models import DiscountCode


class Cart(object):
    def __init__(self, request):
        """
        مقدار دهی اولیه به سبد خرید براساس سیشن
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # ذخیره یک سبد خرید خالی در سیشن
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # ذخیره سازی کد تخفیف اعمال شده
        self.coupon_id = self.session.get('coupon_id')

    def add(self, book, quantity=1, override_quantity=False):
        """
        افزودن کتاب به سبد خرید و یا بروزرسانی تعداد خریداری شده
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.final_price)}
        if override_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        # مشخص کردن وضعیت تغییر کرده جهت ذخیره سازی سیشن
        self.session.modified = True

    def remove(self, book):
        """
        حذف کتاب از سبد خرید
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """
        پیمایش روی آیتم های سبد خرید ودریافت اطلاعات از دیتا بیس
        """
        book_ids = self.cart.keys()
        # دریافت آبجکت های کتاب و افزودن آنها به سبد خرید
        books = Book.objects.filter(id__in=book_ids)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        تعداد آیتم های موجود در سبد خرید
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # حذف سبد خرید از سیشن
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        # بررسی کد تخفیف
        if self.coupon_id:
            try:
                return DiscountCode.objects.get(id=self.coupon_id)
            except DiscountCode.DoesNotExist:
                pass
        return None

    def get_discount(self):
        # محاسبه میزان تخفیف
        if self.coupon:
            return (self.coupon.value / Decimal(100)) \
                   * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        # محاسبه قیمت نهایی پس از اعمال تخفیف
        return self.get_total_price() - self.get_discount()