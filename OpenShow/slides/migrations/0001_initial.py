# Generated by Django 4.1.5 on 2023-07-10 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pixel_width', models.IntegerField(default=1920)),
                ('pixel_height', models.IntegerField(default=1080)),
                ('custom_css', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('included_deck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slides.deck')),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='slides.deck')),
                ('segment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='slides.segment')),
            ],
        ),
        migrations.CreateModel(
            name='SlideElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('css_class', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('order', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='element_images/')),
                ('slide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='slides.slide')),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('css', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TransitionKeyframe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marker', models.CharField(help_text='CSS Keyframe Marker (from, 2%, 50%, to, etc.)', max_length=30)),
                ('css', models.TextField(help_text='CSS to apply at this keyframe marker')),
            ],
        ),
        migrations.CreateModel(
            name='QRCodeElement',
            fields=[
                ('slideelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='slides.slideelement')),
                ('link', models.TextField()),
            ],
            bases=('slides.slideelement',),
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('default_time', models.FloatField(default=1, help_text='Default total time for transition, in seconds')),
                ('keyframes', models.ManyToManyField(null=True, to='slides.transitionkeyframe')),
            ],
        ),
        migrations.AddField(
            model_name='slide',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slides', to='slides.theme'),
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('displays', models.ManyToManyField(blank=True, to='slides.display')),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shows', to='slides.theme')),
            ],
        ),
        migrations.AddField(
            model_name='segment',
            name='local_slides_post',
            field=models.ManyToManyField(blank=True, related_name='post_slides', to='slides.slide'),
        ),
        migrations.AddField(
            model_name='segment',
            name='local_slides_pre',
            field=models.ManyToManyField(blank=True, related_name='pre_slides', to='slides.slide'),
        ),
        migrations.AddField(
            model_name='segment',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='slides.show'),
        ),
        migrations.AddField(
            model_name='display',
            name='current_slide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='slides.slide'),
        ),
        migrations.AddField(
            model_name='display',
            name='segments',
            field=models.ManyToManyField(blank=True, to='slides.segment'),
        ),
        migrations.AddField(
            model_name='deck',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decks', to='slides.theme'),
        ),
    ]
