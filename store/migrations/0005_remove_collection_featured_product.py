# Generated by Django 5.0.4 on 2024-05-16 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_collection_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='featured_product',
        ),
    ]
