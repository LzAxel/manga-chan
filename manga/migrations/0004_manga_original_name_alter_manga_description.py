# Generated by Django 4.0.4 on 2022-05-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0003_alter_manga_upload_date_alter_user_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='original_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Оригинальное Название'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
    ]
