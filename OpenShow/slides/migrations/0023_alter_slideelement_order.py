# Generated by Django 5.1 on 2024-09-03 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0022_themerule_themevariant_themevariantrule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slideelement",
            name="order",
            field=models.FloatField(),
        ),
    ]