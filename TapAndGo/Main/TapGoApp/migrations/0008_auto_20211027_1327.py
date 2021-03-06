# Generated by Django 3.2.7 on 2021-10-27 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TapGoApp', '0007_auto_20211027_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('online', 'online'), ('pending', 'pending'), ('blocked', 'blocked')], default='pending', max_length=7),
        ),
        migrations.AlterField(
            model_name='cash',
            name='balance',
            field=models.FloatField(default='0.0'),
        ),
        migrations.AlterField(
            model_name='healthreport',
            name='report',
            field=models.CharField(choices=[('Vaccinated', 'Vaccinated'), ('Positive', 'Positive'), ('Unvaccinated', 'Unvaccinated')], default='Not reported', max_length=12),
        ),
        migrations.AlterField(
            model_name='nationalid',
            name='id_num',
            field=models.SlugField(default='85a7e5b4'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='typeUser',
            field=models.CharField(choices=[('Agent', 'Agent'), ('Admin', 'Admin'), ('Driver', 'Driver'), ('Passenger', 'Passenger')], default='Passenger', max_length=9),
        ),
    ]
