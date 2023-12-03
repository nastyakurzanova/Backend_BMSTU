# Generated by Django 4.2.4 on 2023-12-02 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_booking_date_alter_booking_date_complete_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingaudiences',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 2, 12, 34, 40, 713203, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 34, 40, 713203, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 34, 40, 713203, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 34, 40, 713203, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]
