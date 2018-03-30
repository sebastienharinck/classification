# Generated by Django 2.0.2 on 2018-03-23 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0018_auto_20180323_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='choice',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vote',
            name='label',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.DO_NOTHING, to='buckets.Label'),
            preserve_default=False,
        ),
    ]
