# Generated by Django 3.2 on 2021-05-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210503_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='pvpseason',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
