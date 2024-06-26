# Generated by Django 5.0.1 on 2024-01-13 14:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(10, message='Name must contain at list 10 characters')])),
                ('is_available', models.BooleanField(default=True)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateField(auto_now=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images')),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, message='The rating must be above 0'), django.core.validators.MaxValueValidator(5, message='max rating value is 5')])),
                ('n_votes', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0, message='votes recived can not be lower than 0')])),
                ('total_score', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0, message='total score can not be lower than 0')])),
                ('slug', models.SlugField(blank=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElectronicProduct',
            fields=[
                ('baseproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store_management.baseproduct')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0, message='price lower than 0 is not allowed'), django.core.validators.MaxValueValidator(999, message='Price is over the current limit of 999€')])),
            ],
            options={
                'abstract': False,
            },
            bases=('store_management.baseproduct',),
        ),
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('baseproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store_management.baseproduct')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0, message='price lower than 0 is not allowed'), django.core.validators.MaxValueValidator(999, message='Price is over the current limit of 999€')])),
                ('is_local', models.BooleanField(default=True)),
                ('exp_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('store_management.baseproduct',),
        ),
        migrations.CreateModel(
            name='FornitureProduct',
            fields=[
                ('baseproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store_management.baseproduct')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0, message='price lower than 0 is not allowed'), django.core.validators.MaxValueValidator(999, message='Price is over the current limit of 999€')])),
            ],
            options={
                'abstract': False,
            },
            bases=('store_management.baseproduct',),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_seller', to='store_management.seller'),
        ),
        migrations.CreateModel(
            name='StoreUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_seller', models.BooleanField(default=False)),
                ('card_number', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='store_users', related_query_name='store_user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='store_users_permissions', related_query_name='store_user_permission', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='seller',
            name='store_user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='store_management.storeuser'),
        ),
    ]
