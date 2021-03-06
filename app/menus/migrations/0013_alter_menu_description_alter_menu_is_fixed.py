# Generated by Django 4.0.4 on 2022-04-23 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0012_alter_menu_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.CharField(blank=True, help_text='Краткое описание содержимого меню', max_length=100, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_fixed',
            field=models.BooleanField(default=False, help_text='Если отмечено - дочерние пункты меню не будут раскрываться, если не отмечено -  будут.', verbose_name='Зафиксировать дочерние пункты меню?'),
        ),
    ]
