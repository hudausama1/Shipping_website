# Generated by Django 5.2.1 on 2025-05-22 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='document',
        ),
    ]
