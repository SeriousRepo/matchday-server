# Generated by Django 2.0.7 on 2018-10-28 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_team_crest_uri'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='crest_uri',
            new_name='crest_url',
        ),
    ]