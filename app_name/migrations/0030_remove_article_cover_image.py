# Generated by Django 3.2.18 on 2023-04-25 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0029_alter_article_cover_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cover_image',
        ),
    ]
