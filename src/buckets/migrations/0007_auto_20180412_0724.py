# Generated by Django 2.0.2 on 2018-04-12 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '__first__'),
        ('buckets', '0006_auto_20180410_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
        migrations.AlterField(
            model_name='bucket',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='label',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]