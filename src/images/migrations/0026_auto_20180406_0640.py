# Generated by Django 2.0.2 on 2018-04-06 06:40

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0025_auto_20180405_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(max_length=133, upload_to=images.models.upload_to),
        ),
    ]
