# Generated by Django 4.0.4 on 2022-04-28 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0021_menu_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(default='', help_text="Необязательно. Названия брать <a href='https://icons.getbootstrap.com/' target='_blank'>отсюда.</a>", max_length=32, verbose_name='Иконка'),
        ),
    ]
