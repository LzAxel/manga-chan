# Generated by Django 4.0.4 on 2022-05-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0002_alter_manga_uploader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки'),
        ),
        migrations.AlterField(
            model_name='user',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации'),
        ),
    ]
