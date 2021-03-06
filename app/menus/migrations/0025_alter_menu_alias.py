# Generated by Django 4.0.4 on 2022-04-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0024_alter_menu_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='alias',
            field=models.SlugField(blank=True, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.", max_length=100, unique=True),
        ),
    ]
