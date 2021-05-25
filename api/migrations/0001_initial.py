# Generated by Django 3.2 on 2021-05-01 14:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('aid', models.IntegerField()),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('is_account_wide', models.BooleanField()),
                ('points', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/achievement')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('gender', models.CharField(max_length=264)),
                ('cid', models.IntegerField()),
                ('guild', models.CharField(blank=True, default=None, max_length=528, null=True)),
                ('level', models.IntegerField()),
                ('active_title', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('covenant_rank', models.IntegerField(blank=True, default=None, null=True)),
                ('item_level', models.IntegerField()),
                ('media', models.ImageField(upload_to='static/img/character')),
                ('avatar', models.ImageField(upload_to='static/img/character/avatar')),
                ('achievement_points', models.IntegerField()),
                ('alters', models.CharField(blank=True, default=None, max_length=5000, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_search', models.DateTimeField(default=django.utils.timezone.now)),
                ('checked', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='WowClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('cid', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/class')),
                ('power_type', models.CharField(max_length=264)),
            ],
        ),
        migrations.CreateModel(
            name='Conduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('cid', models.IntegerField()),
                ('ranks', jsonfield.fields.JSONField()),
                ('type', models.CharField(max_length=264)),
                ('icon', models.ImageField(upload_to='static/img/conduit')),
            ],
        ),
        migrations.CreateModel(
            name='Covenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('cid', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/covenant')),
            ],
        ),
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('icon', models.ImageField(upload_to='static/img/faction')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('code', models.CharField(max_length=128)),
                ('icon', models.ImageField(upload_to='static/img/language')),
            ],
        ),
        migrations.CreateModel(
            name='PvpBracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pvp_type', models.CharField(max_length=264)),
                ('bid', models.IntegerField()),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='PvpBracketStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('won', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('played', models.IntegerField()),
                ('winratio', models.IntegerField()),
                ('bracket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pvpbracket')),
            ],
        ),
        migrations.CreateModel(
            name='PvpEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.character')),
                ('pvp_bracket_statistics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pvpbracketstatistics')),
            ],
        ),
        migrations.CreateModel(
            name='PvpLeaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('bracket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pvpbracket')),
                ('entries', models.ManyToManyField(blank=True, default=None, to='api.PvpEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.ImageField(upload_to='static/img/region')),
            ],
        ),
        migrations.CreateModel(
            name='Soulbind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('sid', models.IntegerField()),
                ('covenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.covenant')),
            ],
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('sid', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/spec')),
                ('role', models.CharField(max_length=264)),
                ('talents', jsonfield.fields.JSONField()),
                ('pvp_talents', jsonfield.fields.JSONField()),
                ('wow_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.class')),
            ],
        ),
        migrations.CreateModel(
            name='Talent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('spell_id', models.IntegerField()),
                ('talent_id', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/talent')),
                ('tier_index', models.IntegerField()),
                ('column_index', models.IntegerField()),
                ('level', models.IntegerField()),
                ('spec', models.ManyToManyField(to='api.Spec')),
                ('wow_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.class')),
            ],
        ),
        migrations.CreateModel(
            name='SoulbindTrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('sid', models.IntegerField()),
                ('spell_id', models.IntegerField()),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('icon', models.ImageField(upload_to='static/img/soulbind_trait')),
                ('soulbind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.soulbind')),
            ],
        ),
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('slug', models.CharField(max_length=264)),
                ('rid', models.IntegerField()),
                ('category', models.CharField(max_length=264)),
                ('locale', models.CharField(max_length=128)),
                ('timezone', models.CharField(max_length=264)),
                ('rtype', models.CharField(max_length=264)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.region')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('rid', models.IntegerField()),
                ('is_allied_race', models.BooleanField()),
                ('icon_male', models.ImageField(upload_to='static/img/race')),
                ('icon_female', models.ImageField(upload_to='static/img/race')),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.faction')),
            ],
        ),
        migrations.CreateModel(
            name='PvpTalent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('name_es', models.CharField(max_length=264)),
                ('description', models.CharField(max_length=5000)),
                ('description_es', models.CharField(max_length=5000)),
                ('spell_id', models.IntegerField()),
                ('talent_id', models.IntegerField()),
                ('icon', models.ImageField(upload_to='static/img/pvp_talent')),
                ('level', models.IntegerField()),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.spec')),
                ('wow_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.class')),
            ],
        ),
        migrations.CreateModel(
            name='PvpSeasonReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cutoff', models.IntegerField(blank=True, default=None, null=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.achievement')),
                ('bracket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pvpbracket')),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.faction')),
            ],
        ),
        migrations.CreateModel(
            name='PvpSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField()),
                ('season_start_timestamp', models.DateTimeField()),
                ('season_end_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('leaderboards', models.ManyToManyField(blank=True, default=None, to='api.PvpLeaderboard')),
                ('rewards', models.ManyToManyField(blank=True, default=None, to='api.PvpSeasonReward')),
            ],
        ),
        migrations.AddField(
            model_name='pvpleaderboard',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.region'),
        ),
        migrations.AddField(
            model_name='class',
            name='races',
            field=models.ManyToManyField(to='api.Race'),
        ),
        migrations.CreateModel(
            name='CharacterConduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('conduit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.conduit')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_completed', models.DateTimeField()),
                ('achievement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.achievement')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='achievements',
            field=models.ManyToManyField(blank=True, default=None, to='api.CharacterAchievement'),
        ),
        migrations.AddField(
            model_name='character',
            name='conduits',
            field=models.ManyToManyField(blank=True, default=None, to='api.CharacterConduit'),
        ),
        migrations.AddField(
            model_name='character',
            name='covenant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.covenant'),
        ),
        migrations.AddField(
            model_name='character',
            name='faction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.faction'),
        ),
        migrations.AddField(
            model_name='character',
            name='pvp_talents',
            field=models.ManyToManyField(blank=True, default=None, to='api.PvpTalent'),
        ),
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.race'),
        ),
        migrations.AddField(
            model_name='character',
            name='ratings',
            field=models.ManyToManyField(blank=True, default=None, to='api.PvpBracketStatistics'),
        ),
        migrations.AddField(
            model_name='character',
            name='realm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.realm'),
        ),
        migrations.AddField(
            model_name='character',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.region'),
        ),
        migrations.AddField(
            model_name='character',
            name='soulbind',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.soulbind'),
        ),
        migrations.AddField(
            model_name='character',
            name='soulbind_abilities',
            field=models.ManyToManyField(blank=True, default=None, to='api.SoulbindTrait'),
        ),
        migrations.AddField(
            model_name='character',
            name='spec',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.spec'),
        ),
        migrations.AddField(
            model_name='character',
            name='talents',
            field=models.ManyToManyField(blank=True, default=None, to='api.Talent'),
        ),
        migrations.AddField(
            model_name='character',
            name='wow_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.class'),
        ),
    ]