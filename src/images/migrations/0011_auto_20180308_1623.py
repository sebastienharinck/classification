# Generated by Django 2.0.2 on 2018-03-08 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0010_bucket_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bucket',
        ),
    ]