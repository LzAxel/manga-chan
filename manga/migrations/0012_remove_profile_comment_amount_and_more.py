# Generated by Django 4.0.4 on 2022-06-11 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0011_alter_like_manga_alter_like_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='comment_amount',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='upload_amount',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Фотография профиля'),
        ),
    ]