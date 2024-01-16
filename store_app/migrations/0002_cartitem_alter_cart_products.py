# Generated by Django 5.0.1 on 2024-01-16 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0001_initial'),
        ('store_management', '0002_myupdateview_alter_seller_store_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_cost', models.PositiveIntegerField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_management.baseproduct')),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart_items', to='store_app.cartitem'),
        ),
    ]
