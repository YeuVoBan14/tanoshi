# Generated by Django 3.2 on 2024-12-03 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_order_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='size',
        ),
        migrations.AddField(
            model_name='order',
            name='note_size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]