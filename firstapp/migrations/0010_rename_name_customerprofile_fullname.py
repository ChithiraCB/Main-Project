# Generated by Django 4.2.5 on 2023-10-05 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0009_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerprofile',
            old_name='name',
            new_name='fullName',
        ),
    ]