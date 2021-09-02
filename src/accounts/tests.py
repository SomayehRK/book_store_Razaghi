from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomerCreationForm
from .views import register
from django.urls import reverse, resolve


class SignupPageTests(TestCase):
    def setUp(self):
        url = reverse('account:signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'صفحه ثبت نام')
        self.assertNotContains(self.response, 'من نبابد در این صفحه باشم!')

    def test_signup_form(self): # new
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomerCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
