# Generated by Django 3.2 on 2021-05-03 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_date_added_character_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='alters',
        ),
        migrations.AddField(
            model_name='character',
            name='alters',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_api_character_alters_+', to='api.Character'),
        ),
    ]
