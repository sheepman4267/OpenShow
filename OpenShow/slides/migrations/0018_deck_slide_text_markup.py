# Generated by Django 4.2.6 on 2023-12-07 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0017_deck_script_slide_cue'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='slide_text_markup',
            field=models.TextField(blank=True, null=True),
        ),
    ]
