# Generated by Django 3.2.7 on 2021-10-26 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TapGoApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='heath',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='nationalid',
        ),
        migrations.AddField(
            model_name='nationalid',
            name='id_num',
            field=models.SlugField(default='202012345'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='health',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='health_account', to='TapGoApp.healthreport'),
        ),
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('online', 'online'), ('blocked', 'blocked'), ('pending', 'pending')], default='pending', max_length=7),
        ),
        migrations.AlterField(
            model_name='healthreport',
            name='citizen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cit_health', to='TapGoApp.nationalid'),
        ),
        migrations.AlterField(
            model_name='healthreport',
            name='report',
            field=models.CharField(choices=[('Positive', 'Positive'), ('Vaccinated', 'Vaccinated'), ('Unvaccinated', 'Unvaccinated')], default='Not reported', max_length=12),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cardNum',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='card_account', to='TapGoApp.card'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='typeUser',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Agent', 'Agent'), ('Passenger', 'Passenger'), ('Admin', 'Admin')], default='Passenger', max_length=9),
        ),
        migrations.AlterField(
            model_name='road',
            name='roadNum',
            field=models.CharField(choices=[('311', '311'), ('301', '301'), ('303', '303'), ('313', '313')], default='301', max_length=5),
        ),
    ]
