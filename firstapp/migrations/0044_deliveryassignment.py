# Generated by Django 4.2.5 on 2024-04-03 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0043_alter_customuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('delivery_boy', models.ForeignKey(limit_choices_to={'user_types': 3}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.order')),
            ],
        ),
    ]
