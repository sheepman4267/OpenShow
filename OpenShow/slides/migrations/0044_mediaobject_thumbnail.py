# Generated by Django 5.1 on 2025-04-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0043_theme_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediaobject",
            name="thumbnail",
            field=models.FileField(
                blank=True, null=True, upload_to="media_final/thumbnail/"
            ),
        ),
    ]
