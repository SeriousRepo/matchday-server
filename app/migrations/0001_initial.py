# Generated by Django 2.0.7 on 2018-10-26 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('league', 'league'), ('tournament', 'tournament')], max_length=10)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_time', models.TimeField()),
                ('match_minute', models.IntegerField()),
                ('description', models.CharField(max_length=50, null=True)),
                ('rank_points', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('event_type', models.CharField(choices=[('first whistle', 'first whistle'), ('last whistle', 'last whistle'), ('end of first half', 'end of first half'), ('begin of second half', 'begin of second half'), ('end of second half', 'end of second half'), ('begin of extra time', 'begin of extra time'), ('begin of extra time second half', 'begin of extra time second half'), ('end of extra time first half', 'end of extra time first half'), ('end of extra time second half', 'end of extra time second half'), ('begin of penalty shoots', 'begin of penalty shoots')], max_length=100)),
                ('event_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.EventInfo')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('role', models.CharField(choices=[('coach', 'coach'), ('player', 'player'), ('referee', 'referee')], max_length=10)),
                ('birth_date', models.DateField(null=True)),
                ('nationality', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('GK', 'goalkeeper'), ('LB', 'left-back'), ('CB', 'centre-back'), ('RB', 'right-back'), ('LM', 'left-midfield'), ('CM', 'centre-midfield'), ('RM', 'right-midfield'), ('CF', 'centre-forward')], max_length=3)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stadium', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('yellow_card', 'yellow_card'), ('red_card', 'red_card'), ('goal', 'goal'), ('substitution', 'substitution')], max_length=20)),
                ('event_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.EventInfo')),
                ('event_participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='app.Player')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
            ],
        ),
        migrations.CreateModel(
            name='TeamInMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_host', models.BooleanField()),
                ('coach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Person')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team')),
            ],
        ),
        migrations.AddField(
            model_name='teamevent',
            name='team_in_match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TeamInMatch'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='main_referee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Person'),
        ),
    ]
