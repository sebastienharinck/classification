# Generated by Django 2.0.2 on 2018-04-19 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0009_auto_20180419_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
