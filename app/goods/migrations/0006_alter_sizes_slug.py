# Generated by Django 5.1.1 on 2024-11-24 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_sizes_products_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sizes',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
