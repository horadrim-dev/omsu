# Generated by Django 4.0.5 on 2022-07-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0050_alter_modulecontent_feed_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulecontent',
            name='content_type',
            field=models.CharField(choices=[('', '---'), ('post', 'Пост'), ('feed', 'Лента постов')], default='', max_length=64, verbose_name='Тип контента'),
        ),
    ]