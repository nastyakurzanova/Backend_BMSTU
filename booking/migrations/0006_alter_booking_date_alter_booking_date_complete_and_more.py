# Generated by Django 4.2.4 on 2023-12-02 12:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_remove_booking_audincess_alter_booking_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 2, 12, 33, 48, 611773, tzinfo=datetime.timezone.utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 33, 48, 611773, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 33, 48, 611773, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 2, 12, 33, 48, 611773, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
        migrations.CreateModel(
            name='BookingAudiences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audience', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.audiences')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='audincess',
            field=models.ManyToManyField(through='booking.BookingAudiences', to='booking.audiences'),
        ),
    ]
