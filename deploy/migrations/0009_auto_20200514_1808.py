# Generated by Django 3.0.4 on 2020-05-14 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sys_mgr', '0006_user_chinese_name'),
        ('ticket', '0015_auto_20200514_1055'),
        ('deploy', '0008_auto_20200514_1752'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JobTask',
            new_name='JobPlan',
        ),
    ]