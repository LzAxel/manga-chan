# Generated by Django 4.0.4 on 2022-05-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0004_manga_original_name_alter_manga_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='pages',
            field=models.IntegerField(blank=True, default='0', verbose_name='Кол-во страниц'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='views',
            field=models.IntegerField(blank=True, default=0, verbose_name='Просмотры'),
        ),
    ]