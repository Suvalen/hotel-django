# Generated by Django 5.2 on 2025-05-29 00:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_payment_paid_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
