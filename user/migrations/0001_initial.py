# Generated by Django 2.2 on 2020-05-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.IntegerField(max_length=20, unique=True, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=64, unique=True, verbose_name='昵称')),
                ('gender', models.CharField(max_length=8, verbose_name='性别')),
                ('birthday', models.DateTimeField(verbose_name='出生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象')),
                ('location', models.CharField(max_length=128, verbose_name='长居地')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
