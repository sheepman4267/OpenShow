# Generated by Django 5.1 on 2025-02-07 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0040_alter_slide_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="image",
            options={"ordering": ("-pk",)},
        ),
        migrations.AlterModelOptions(
            name="mediaobject",
            options={"ordering": ("-pk",)},
        ),
    ]
