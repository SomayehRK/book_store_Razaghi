# Generated by Django 3.2.6 on 2021-09-02 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='عنوان کتاب')),
                ('author', models.CharField(max_length=100, verbose_name='نویسنده')),
                ('image', models.ImageField(blank=True, upload_to='img_book/')),
                ('slug', models.SlugField(max_length=200)),
                ('price', models.IntegerField(verbose_name='قیمت کتاب')),
                ('quantity', models.IntegerField(verbose_name='موجودی انبار')),
                ('available', models.BooleanField(default=True, verbose_name='موجود در انبار')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
            ],
            options={
                'verbose_name_plural': 'کتاب ها',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='دسته')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ایجاد کننده')),
            ],
            options={
                'verbose_name_plural': 'گروه ها',
                'ordering': ('name',),
            },
        ),
    ]
