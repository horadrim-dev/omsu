# Generated by Django 4.0.4 on 2022-05-19 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_post_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='url',
        ),
    ]
