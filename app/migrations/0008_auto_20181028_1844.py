# Generated by Django 2.0.7 on 2018-10-28 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20181028_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='name', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='shirt_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('Goalkeeper', 'Goalkeeper'), ('Defender', 'Defender'), ('Midfielder', 'Midfielder'), ('Attacker', 'Attacker')], max_length=50),
        ),
    ]
