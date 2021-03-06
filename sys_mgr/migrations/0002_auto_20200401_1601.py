# Generated by Django 3.0.4 on 2020-04-01 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sys_mgr', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': '菜单', 'verbose_name_plural': '菜单'},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': '权限', 'verbose_name_plural': '权限'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': '角色', 'verbose_name_plural': '角色'},
        ),
        migrations.AlterModelOptions(
            name='space',
            options={'verbose_name': '空间', 'verbose_name_plural': '空间'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.RemoveField(
            model_name='menu',
            name='is_top',
        ),
        migrations.AddField(
            model_name='menu',
            name='parent_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sys_mgr.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='seq',
            field=models.IntegerField(),
        ),
    ]
