# Generated by Django 5.1 on 2024-11-20 20:26

from django.db import migrations
from django.core.files.base import ContentFile
import os
import hashlib


def get_file_hash(file):
    hash_func = hashlib.new('sha256')
    with open(file, 'rb') as file:
        while chunk := file.read(65536):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def forwards_func(apps, schema_editor):
    slide_element_model = apps.get_model('slides', 'SlideElement')
    image_model = apps.get_model('slides', 'Image')
    for element in slide_element_model.objects.all():
        if element.image:
            image_object = image_model(file=ContentFile(element.image.read(), name=os.path.basename(element.image.name)))
            image_object.file_hash = get_file_hash(element.image.file.name)
            image_object.save()
            element.image_object = image_object
            element.image = None
            element.save()


def reverse_func(apps, schema_editor):
    slide_element_model = apps.get_model('slides', 'SlideElement')
    for element in slide_element_model.objects.all():
        if element.image_object:
            element.image = ContentFile(element.image_object.file.read(), name=os.path.basename(element.image_object.file.name))
            element.save()
            element.image_object.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("slides", "0033_slideelement_image_object"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]