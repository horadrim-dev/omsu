# Generated by Django 4.0.4 on 2022-05-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_remove_feed_alias_remove_feed_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='alias',
            field=models.SlugField(blank=True, default='', help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.", max_length=1000),
        ),
        migrations.AddField(
            model_name='feed',
            name='title',
            field=models.CharField(default='', max_length=1000, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='post',
            name='alias',
            field=models.SlugField(blank=True, default='', help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.", max_length=1000),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=1000, verbose_name='Заголовок'),
        ),
    ]