# Generated by Django 5.1.5 on 2025-03-13 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_garage_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='reg_plate',
        ),
    ]
