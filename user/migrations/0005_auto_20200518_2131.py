# Generated by Django 2.2 on 2020-05-18 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200518_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phonenum',
            field=models.CharField(max_length=50, unique=True, verbose_name='手机号'),
        ),
    ]
