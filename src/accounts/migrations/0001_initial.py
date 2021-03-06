# Generated by Django 3.2.6 on 2021-09-02 10:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=300, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='نام کاربری باید شامل حروف الفبا و یا اعداد باشد', regex='^[a-zA-Z0-9.+-]*$')], verbose_name='نام کاربری')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='آدرس ایمیل')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='نام خانوادگی')),
                ('is_admin', models.BooleanField(blank=True, default=False, verbose_name='مدیر سایت')),
                ('is_staff', models.BooleanField(blank=True, default=False, verbose_name='کارمند')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50, verbose_name='استان')),
                ('city', models.CharField(max_length=50, verbose_name='شهر')),
                ('postal_code', models.CharField(max_length=12, verbose_name='کد پستی')),
                ('full_address', models.TextField(verbose_name='آدرس کامل')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name_plural': 'آدرس ها',
                'ordering': ['customer'],
            },
        ),
        migrations.CreateModel(
            name='AdminSite',
            fields=[
            ],
            options={
                'verbose_name': 'مدیر سایت',
                'verbose_name_plural': 'مدیر سایت',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.customuser',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتری ها',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.customuser',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
            ],
            options={
                'verbose_name': 'کارمند',
                'verbose_name_plural': 'کارمندان',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.customuser',),
        ),
    ]
