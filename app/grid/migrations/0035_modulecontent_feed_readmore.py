# Generated by Django 4.0.5 on 2022-07-13 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0034_rename_feed_count_posts_modulecontent_feed_count_objects'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulecontent',
            name='feed_readmore',
            field=models.BooleanField(default=True, verbose_name='Кнопка "Читать больше"'),
        ),
    ]
