# Generated by Django 4.1.5 on 2023-07-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0004_slide_transition'),
    ]

    operations = [
        migrations.AddField(
            model_name='slideelement',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='element_videos/'),
        ),
    ]
