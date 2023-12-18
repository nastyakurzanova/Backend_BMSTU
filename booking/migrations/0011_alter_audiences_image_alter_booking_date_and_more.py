# Generated by Django 4.2.4 on 2023-12-16 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_alter_audiences_info_alter_booking_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiences',
            name='image',
            field=models.ImageField(default='audiences/default.jpg', upload_to='', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 16, 11, 56, 25, 340155, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 56, 25, 340155, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 56, 25, 340155, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 56, 25, 340155, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]