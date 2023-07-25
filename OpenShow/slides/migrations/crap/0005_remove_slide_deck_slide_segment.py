# Generated by Django 4.1.5 on 2023-02-07 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0004_remove_slide_elements_remove_slide_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='deck',
        ),
        migrations.AddField(
            model_name='slide',
            name='segment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='slides.segment'),
        ),
    ]