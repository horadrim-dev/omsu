# Generated by Django 4.0.4 on 2022-05-27 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_feed_updated_at_post_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='date_publish',
            new_name='published_at',
        ),
    ]
