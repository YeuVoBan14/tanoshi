# Generated by Django 3.2 on 2024-12-02 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_order_imgage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='imgage',
            new_name='image',
        ),
    ]
