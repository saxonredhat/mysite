# Generated by Django 3.0.4 on 2020-05-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0009_auto_20200514_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobplan',
            name='type',
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='jobplan',
            name='job_type',
            field=models.SmallIntegerField(blank=True, choices=[(1, '手动发布'), (2, '自动发布')], default=0, verbose_name='发布方式'),
        ),
        migrations.AlterField(
            model_name='jobplan',
            name='created_type',
            field=models.SmallIntegerField(blank=True, choices=[(1, '手动创建'), (2, '工单创建')], default=0, verbose_name='创建类型'),
        ),
    ]
