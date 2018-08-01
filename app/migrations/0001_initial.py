# Generated by Django 2.0.7 on 2018-08-01 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('league', 'league'), ('tournament', 'tournament')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='MatchTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals_amount', models.IntegerField()),
                ('is_host', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('coach', 'coach'), ('player', 'player'), ('referee', 'referee')], max_length=10)),
                ('birth_date', models.DateField(null=True)),
                ('nationality', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('goalkeeper', 'GK'), ('left-back', 'LB'), ('centre-back', 'CB'), ('right-back', 'RB'), ('left-midfield', 'LM'), ('centre-midfield', 'CM'), ('right-midfield', 'RM'), ('centre-forward', 'CF')], max_length=3)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('points', models.IntegerField()),
                ('goals_scored', models.IntegerField()),
                ('goals_conceded', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('hash_password', models.CharField(max_length=250)),
                ('join_date', models.DateField()),
                ('rank_points', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team'),
        ),
        migrations.AddField(
            model_name='matchteam',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
        migrations.AddField(
            model_name='matchteam',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Match'),
        ),
        migrations.AddField(
            model_name='matchteam',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='main_referee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
    ]
