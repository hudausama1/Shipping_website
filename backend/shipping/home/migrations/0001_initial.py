# Generated by Django 5.2.1 on 2025-05-22 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField()),
                ('contact_email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('features', models.TextField()),
                ('price_note', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('feedback', models.TextField()),
                ('company', models.CharField(blank=True, max_length=100)),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
