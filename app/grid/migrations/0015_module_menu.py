# Generated by Django 4.0.4 on 2022-06-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0036_delete_col_delete_row'),
        ('grid', '0014_module_alter_column_options_delete_block_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='menu',
            field=models.ManyToManyField(to='menus.menu', verbose_name='Привязка к меню'),
        ),
    ]
