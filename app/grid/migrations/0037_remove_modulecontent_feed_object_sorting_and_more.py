# Generated by Django 4.0.5 on 2022-07-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0036_modulecontent_feed_object_sorting_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulecontent',
            name='feed_object_sorting',
        ),
        migrations.AddField(
            model_name='modulecontent',
            name='feeв_sort_direction',
            field=models.CharField(choices=[('horizontal', 'Построчно'), ('vertical', 'По колонкам')], default='horizontal', max_length=16, verbose_name='Направление сортировки'),
        ),
    ]
