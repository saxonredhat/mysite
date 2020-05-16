# Generated by Django 3.0.4 on 2020-05-08 05:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='audit_description',
            field=models.TextField(blank=True, null=True, verbose_name='审核说明'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='audited_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核时间'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='execute_description',
            field=models.TextField(blank=True, null=True, verbose_name='执行说明'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='executed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='执行时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='test_description',
            field=models.TextField(blank=True, null=True, verbose_name='测试说明'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tested_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='测试时间'),
        ),
    ]
