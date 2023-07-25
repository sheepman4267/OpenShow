# Generated by Django 4.1.5 on 2023-02-07 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0003_alter_segment_included_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='elements',
        ),
        migrations.RemoveField(
            model_name='slide',
            name='name',
        ),
        migrations.AddField(
            model_name='slideelement',
            name='slide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='slides.slide'),
        ),
    ]