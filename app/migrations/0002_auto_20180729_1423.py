# Generated by Django 2.0.7 on 2018-07-29 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='main_referee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(choices=[('coach', 'coach'), ('player', 'player'), ('referee', 'referee')], max_length=10),
        ),
    ]
