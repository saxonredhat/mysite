# Generated by Django 3.0.4 on 2020-05-16 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0019_jobplan_console_output'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobplan',
            name='duration',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='构建时间'),
        ),
    ]
