# Generated by Django 5.1 on 2024-11-20 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0034_replace_image_with_image_object"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="slideelement",
            name="image",
        ),
    ]
