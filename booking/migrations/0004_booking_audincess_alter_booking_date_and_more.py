# Generated by Django 4.2.4 on 2023-12-02 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_audiences_image_alter_booking_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='audincess',
            field=models.ManyToManyField(to='booking.audiences'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 2, 12, 17, 22, 850056, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 17, 22, 850056, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 17, 22, 850056, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 17, 22, 850056, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]
