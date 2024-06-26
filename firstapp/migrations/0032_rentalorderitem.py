# Generated by Django 4.2.5 on 2024-02-27 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0031_rentalorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.rentalorder')),
                ('rental_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.rentalproduct')),
            ],
        ),
    ]
