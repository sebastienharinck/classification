# Generated by Django 2.0.2 on 2018-03-09 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0002_auto_20180309_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='labels',
        ),
        migrations.AddField(
            model_name='label',
            name='bucket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='buckets.Bucket'),
        ),
    ]
