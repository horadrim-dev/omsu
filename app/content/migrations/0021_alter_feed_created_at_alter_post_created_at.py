# Generated by Django 4.0.4 on 2022-05-25 08:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_feed_published_at_post_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='created_at',
            field=models.DateField(default=datetime.date.today, editable=False, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateField(default=datetime.date.today, editable=False, verbose_name='Дата создания'),
        ),
    ]
