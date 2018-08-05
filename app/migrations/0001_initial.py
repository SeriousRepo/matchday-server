# Generated by Django 2.0.7 on 2018-08-05 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('league', 'league'), ('tournament', 'tournament')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EventInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_time', models.TimeField()),
                ('match_minute', models.IntegerField()),
                ('rank_points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, null=True)),
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
            name='MatchEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('event_type', models.CharField(max_length=100)),
                ('event_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.EventInfo')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Match')),
            ],
        ),
        migrations.CreateModel(
            name='MatchTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='RedCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, null=True)),
                ('substituted_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stadium', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TeamEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.EventInfo')),
                ('match_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MatchTeam')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('join_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='YellowCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50, null=True)),
                ('team_event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.TeamEvent')),
            ],
        ),
        migrations.AddField(
            model_name='substitution',
            name='team_event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.TeamEvent'),
        ),
        migrations.AddField(
            model_name='redcard',
            name='team_event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.TeamEvent'),
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
        migrations.AddField(
            model_name='goal',
            name='team_event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.TeamEvent'),
        ),
        migrations.AddField(
            model_name='eventinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AddField(
            model_name='assist',
            name='assisted_to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Player'),
        ),
        migrations.AddField(
            model_name='assist',
            name='team_event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.TeamEvent'),
        ),
    ]
