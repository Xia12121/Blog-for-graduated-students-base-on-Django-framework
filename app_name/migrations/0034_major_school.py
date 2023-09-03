# Generated by Django 3.2.18 on 2023-04-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0033_userloginrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('majors', models.ManyToManyField(to='app_name.Major')),
            ],
        ),
    ]
