# Generated by Django 5.2 on 2025-06-04 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_productorder_reservasi_productorder_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('billing_name', models.CharField(max_length=255)),
                ('billing_email', models.EmailField(max_length=254)),
                ('billing_address', models.TextField()),
                ('payment_method', models.CharField(max_length=50)),
                ('card_last_digits', models.CharField(blank=True, max_length=4, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.websiteuser')),
            ],
        ),
    ]
