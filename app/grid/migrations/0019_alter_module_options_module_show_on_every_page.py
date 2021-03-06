# Generated by Django 4.0.4 on 2022-06-09 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0018_remove_column_published_remove_column_published_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['column'], 'verbose_name': 'Модуль', 'verbose_name_plural': 'Модули'},
        ),
        migrations.AddField(
            model_name='module',
            name='show_on_every_page',
            field=models.BooleanField(default=False, help_text='Если выбрано - значения из поля "меню" будут проигнорированы.', verbose_name='Отображать на всех страницах сайта'),
        ),
    ]
