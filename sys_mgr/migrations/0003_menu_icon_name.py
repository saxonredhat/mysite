# Generated by Django 3.0.4 on 2020-04-19 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_mgr', '0002_auto_20200401_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='icon_name',
            field=models.CharField(default='circle', max_length=32),
        ),
    ]
