# Generated by Django 3.0.4 on 2020-05-14 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0005_auto_20200514_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='repository',
        ),
        migrations.AddField(
            model_name='project',
            name='repository',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='deploy.Repository', verbose_name='版本仓库'),
        ),
    ]