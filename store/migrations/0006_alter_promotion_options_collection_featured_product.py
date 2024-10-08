# Generated by Django 5.0.4 on 2024-05-16 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_collection_featured_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['description']},
        ),
        migrations.AddField(
            model_name='collection',
            name='featured_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='store.product'),
        ),
    ]
