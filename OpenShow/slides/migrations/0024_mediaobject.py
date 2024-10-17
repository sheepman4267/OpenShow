# Generated by Django 5.1 on 2024-09-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0023_alter_slideelement_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "media_type",
                    models.CharField(
                        choices=[
                            ("VIMEO_EMBED", "Vimeo Embed"),
                            ("VIDEO", "Video"),
                            ("AUDIO", "Audio"),
                        ],
                        default="VIDEO",
                        max_length=100,
                    ),
                ),
                (
                    "raw_file",
                    models.FileField(blank=True, null=True, upload_to="media_intake/"),
                ),
                (
                    "final_file",
                    models.FileField(blank=True, null=True, upload_to="media_final/"),
                ),
                ("embed_url", models.URLField(blank=True, null=True)),
                ("autoplay", models.BooleanField(default=True)),
            ],
        ),
    ]
