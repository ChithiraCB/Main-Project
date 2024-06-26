# Generated by Django 4.2.5 on 2024-02-19 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0028_rentalcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalcart',
            name='rental_products',
            field=models.ManyToManyField(through='firstapp.RentalCartItem', to='firstapp.rentalproduct'),
        ),
        migrations.AddField(
            model_name='rentalcartitem',
            name='cart',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='firstapp.rentalcart'),
            preserve_default=False,
        ),
    ]
