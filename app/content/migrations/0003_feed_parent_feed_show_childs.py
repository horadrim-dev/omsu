# Generated by Django 4.0.6 on 2022-08-21 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_remove_contentlayout_feed_readmore_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.feed', verbose_name='Родитель'),
        ),
        migrations.AddField(
            model_name='feed',
            name='show_childs',
            field=models.BooleanField(default=True, verbose_name='Отображать посты из дочерних лент'),
        ),
    ]