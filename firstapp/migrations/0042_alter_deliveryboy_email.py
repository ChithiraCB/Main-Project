# Generated by Django 4.2.5 on 2024-03-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0041_deliveryboy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryboy',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]