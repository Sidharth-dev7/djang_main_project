# Generated by Django 5.1.5 on 2025-03-23 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_delete_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerecord',
            name='invoice_pdf',
            field=models.FileField(blank=True, null=True, upload_to='invoices/'),
        ),
    ]
