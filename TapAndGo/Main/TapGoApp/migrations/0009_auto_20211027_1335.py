# Generated by Django 3.2.7 on 2021-10-27 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TapGoApp', '0008_auto_20211027_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('online', 'online'), ('blocked', 'blocked')], default='pending', max_length=7),
        ),
        migrations.AlterField(
            model_name='cash',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='healthreport',
            name='report',
            field=models.CharField(choices=[('Vaccinated', 'Vaccinated'), ('Unvaccinated', 'Unvaccinated'), ('Positive', 'Positive')], default='Not reported', max_length=12),
        ),
        migrations.AlterField(
            model_name='nationalid',
            name='id_num',
            field=models.SlugField(default='036c21f5'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='typeUser',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Admin', 'Admin'), ('Agent', 'Agent'), ('Passenger', 'Passenger')], default='Passenger', max_length=9),
        ),
        migrations.AlterField(
            model_name='road',
            name='roadNum',
            field=models.CharField(choices=[('313', '313'), ('311', '311'), ('303', '303'), ('301', '301')], default='301', max_length=5),
        ),
    ]