# Generated by Django 4.0.4 on 2022-04-25 07:06

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0015_rename_parent_id_menu_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='short_description',
            field=models.CharField(blank=True, help_text='Краткое описание содержимого меню', max_length=100, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
