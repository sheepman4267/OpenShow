# Generated by Django 4.1.5 on 2023-08-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0006_alter_deck_options_alter_segment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transitionkeyframe',
            name='out',
            field=models.BooleanField(default=False),
        ),
    ]