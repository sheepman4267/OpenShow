# Generated by Django 4.1.5 on 2023-08-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0009_show_advance_between_decks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='advance_between_decks',
            new_name='advance_between_segments',
        ),
    ]
