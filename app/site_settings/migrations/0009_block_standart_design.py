# Generated by Django 4.0.4 on 2022-06-07 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0008_section_indents_alter_block_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='standart_design',
            field=models.BooleanField(default=True, verbose_name='Оформление по умолчанию'),
        ),
    ]
