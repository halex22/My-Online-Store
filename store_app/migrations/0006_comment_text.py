# Generated by Django 5.0.1 on 2024-01-18 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_rating_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
