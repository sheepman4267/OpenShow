# Generated by Django 4.2.6 on 2023-11-04 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0016_alter_slide_options_slide_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='script',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='slide',
            name='cue',
            field=models.TextField(blank=True, null=True),
        ),
    ]