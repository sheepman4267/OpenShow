# Generated by Django 5.1 on 2024-11-15 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0028_alter_mediaobject_media_type_alter_mediaobject_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='advance_in_loop',
            field=models.BooleanField(default=False),
        ),
    ]
