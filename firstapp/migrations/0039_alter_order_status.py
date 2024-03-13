# Generated by Django 4.2.5 on 2024-03-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0038_thread_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Order Confirmed', max_length=20),
        ),
    ]