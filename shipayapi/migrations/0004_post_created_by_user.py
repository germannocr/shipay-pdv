# Generated by Django 3.1 on 2020-08-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipayapi', '0003_remove_post_created_by_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_by_user',
            field=models.IntegerField(default=int),
            preserve_default=False,
        ),
    ]
