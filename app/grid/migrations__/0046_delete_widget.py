# Generated by Django 4.0.5 on 2022-07-23 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0045_rename_feed_count_objects_modulecontent_feed_count_items_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Widget',
        ),
    ]