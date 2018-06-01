# Generated by Django 2.0.2 on 2018-04-19 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0026_auto_20180406_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='bucket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.Bucket'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.Label'),
        ),
    ]