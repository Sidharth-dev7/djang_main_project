# Generated by Django 5.1.5 on 2025-03-10 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_customer_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='last_login',
        ),
    ]
