# Generated by Django 4.2.5 on 2023-11-12 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0010_alter_category1_name_alter_subcategory1_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='customer',
        ),
    ]