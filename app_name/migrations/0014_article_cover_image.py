# Generated by Django 3.2.18 on 2023-04-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0013_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(default='article_covers/default.png', upload_to='article_covers/'),
        ),
    ]