# Generated by Django 3.2.18 on 2023-04-25 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0026_article_cover_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cover_image',
        ),
    ]
