# Generated by Django 4.0.5 on 2022-07-21 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0043_rename_feed_modulecontent_feed_content_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modulecontent',
            old_name='feed_content',
            new_name='content_feed',
        ),
        migrations.RenameField(
            model_name='modulecontent',
            old_name='menu_content',
            new_name='content_menu',
        ),
        migrations.RenameField(
            model_name='modulecontent',
            old_name='post_content',
            new_name='content_post',
        ),
    ]
