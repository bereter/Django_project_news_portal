# Generated by Django 4.1.6 on 2023-04-20 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_remove_author_subscribers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authorcategory',
            old_name='author',
            new_name='user',
        ),
    ]
