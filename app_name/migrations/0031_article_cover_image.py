# Generated by Django 3.2.18 on 2023-04-25 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0030_remove_article_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(default='static/covers/default.png', upload_to='static/covers/'),
        ),
    ]
