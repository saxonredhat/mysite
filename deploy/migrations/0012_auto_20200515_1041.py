# Generated by Django 3.0.4 on 2020-05-15 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0011_job_create_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobplan',
            options={'verbose_name': '发布计划', 'verbose_name_plural': '发布计划'},
        ),
        migrations.RemoveField(
            model_name='jobplan',
            name='description',
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='发布描述'),
        ),
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(default='', max_length=256, verbose_name='发布名'),
        ),
        migrations.AlterField(
            model_name='jobplan',
            name='detail_description',
            field=models.TextField(blank=True, null=True, verbose_name='发布计划详情'),
        ),
        migrations.AlterField(
            model_name='jobplan',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_tasks', to='deploy.Job', verbose_name='发布'),
        ),
        migrations.AlterField(
            model_name='jobplan',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='发布计划名'),
        ),
        migrations.AlterField(
            model_name='jobplan',
            name='number',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='发布计划编号'),
        ),
    ]