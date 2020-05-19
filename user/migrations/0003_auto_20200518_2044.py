# Generated by Django 2.2 on 2020-05-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200512_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(default=None, max_length=256, verbose_name='个人形象'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(default=None, max_length=128, verbose_name='长居地'),
            preserve_default=False,
        ),
    ]
