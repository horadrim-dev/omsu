# Generated by Django 4.0.6 on 2022-08-07 08:50

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Если оставить равным 0 - добавится в конец.', null=True, verbose_name='Порядок')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('alias', models.SlugField(blank=True, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.", max_length=100, unique=True)),
                ('list_order', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('level', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('url', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('megamenu', models.BooleanField(default=False, help_text='Если отмечено, меню будет выпадать шириной во весь экран', verbose_name='Мегаменю')),
                ('icon', models.CharField(blank=True, default='', help_text="Необязательно. Названия брать <a href='https://icons.getbootstrap.com/' target='_blank'>отсюда.</a>", max_length=32, verbose_name='Иконка')),
                ('short_description', models.CharField(blank=True, help_text='Краткое описание содержимого меню', max_length=100, verbose_name='Краткое описание')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Описание')),
                ('debug_info', models.TextField(blank=True, default='', null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.menu', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ['list_order'],
            },
        ),
    ]
