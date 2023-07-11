from django.db import models
from django_eventstream import send_event
from collections.abc import Iterable
from django.shortcuts import reverse

import tinycss2

from tinycss2.ast import IdentToken, QualifiedRule


class Display(models.Model):  # A set of characteristics used to modify slide appearance for different displays
    name = models.CharField(max_length=100)
    pixel_width = models.IntegerField(default=1920)
    pixel_height = models.IntegerField(default=1080)
    custom_css = models.TextField(null=True, blank=True)
    current_slide = models.ForeignKey(
        to='Slide',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    segments = models.ManyToManyField(
        to='Segment',
        blank=True,
    )


class Deck(models.Model):  # A Reusable set of slides, which can be included in a Show Segment
    name = models.CharField(max_length=100)
    theme = models.ForeignKey(
        to='Theme',
        unique=False,
        related_name='decks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    def get_absolute_url(self):
        return reverse('edit-deck', kwargs={'pk': self.pk})


class Show(models.Model):  # The main driver of the "presentation interface". A collection of segments, which could either have their own slides or include them from a Deck
    name = models.CharField(max_length=200)
    displays = models.ManyToManyField(
        to=Display,
        blank=True,
    )
    theme = models.ForeignKey(
        to='Theme',
        unique=False,
        related_name='shows',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('edit-show', kwargs={'pk': self.pk})

    def next_segment_order(self):
        return max([0, ] + [segment.order for segment in self.segments.all()]) + 1

    def get_css_classes(self):
        css_classes = []
        for segment in self.segments.all():
            for slide in segment.slides.all():
                for element in slide.elements.all():
                    if element.css_class not in css_classes:
                        css_classes.append(element.css_class)
            if segment.included_deck:
                for slide in segment.included_deck.slides.all():
                    for element in slide.elements.all():
                        if element.css_class not in css_classes:
                            css_classes.append(element.css_class)
        return css_classes

    def check_compatibility(self, theme):
        missing = []
        show_classes = self.get_css_classes()
        print(show_classes)
        theme_classes = theme.get_css_classes()
        print(theme_classes)
        for css_class in show_classes:
            if css_class not in theme_classes:
                missing.append(css_class)
        return missing


class Segment(models.Model):  # A collection of slides which will be part of a Show
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    show = models.ForeignKey(
        to=Show,
        on_delete=models.CASCADE,
        related_name='segments'
    )
    included_deck = models.ForeignKey(
        to=Deck,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    local_slides_pre = models.ManyToManyField(
        to='Slide',
        blank=True,
        related_name='pre_slides',
    )
    local_slides_post = models.ManyToManyField(
        to='Slide',
        blank=True,
        related_name='post_slides',
    )

    def get_absolute_url(self):
        return reverse('edit-show', kwargs={'pk': self.show.pk})

    class Meta:
        ordering = ["-order"]

    # def slides(self):
    #     if self.included_deck:
    #         return self.local_slides_pre.all() | self.included_deck.slides.all() | self.local_slides_post.all()
    #     else:
    #         return self.local_slides_pre.all() | self.local_slides_post.all()


class SlideElement(models.Model):  # An individual piece of a slide (a block of text, a video, etc.). It's just HTML :)
    css_class = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    order = models.IntegerField()
    slide = models.ForeignKey(
        to='Slide',
        unique=False,
        null=False,
        blank=False,
        related_name='elements',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='element_images/'
    )

    def get_absolute_url(self):
        return reverse('edit-slide', kwargs={'pk': self.slide.pk})

    class Meta:
        ordering = ["-order"]

class QRCodeElement(SlideElement):
    link = models.TextField()


class Slide(models.Model):
    segment = models.ForeignKey(
        to=Segment,
        unique=False,
        related_name='slides',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    deck = models.ForeignKey(
        to=Deck,
        unique=False,
        related_name='slides',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    theme = models.ForeignKey(
        to='Theme',
        unique=False,
        related_name='slides',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    transition = models.ForeignKey(
        to='Transition',
        unique=False,
        related_name='slides',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        if self.segment:
            return reverse('edit-show', kwargs={'pk': self.segment.pk})
        elif self.deck:
            return reverse('edit-deck', kwargs={'pk': self.deck.pk})
        else:
            raise RuntimeError('A slide must be part of something... something has gone very wrong.')

    def send_to_display(self, displays:Iterable) -> None:
        """
        :param displays:
        An iterable (probably a QuerySet) of Display objects to display the slide on
        :return:
        This method always returns None.
        """
        for display in displays:
            display.current_slide = self
            display.save()
            send_event('test', f'display-{display.pk}', f'sending slide {self.pk} to display {display.pk}')

    def get_elements(self):
        return self.elements.all().order_by('order')


class Transition(models.Model):
    name = models.CharField(max_length=30)
    default_time = models.FloatField(help_text="Default total time for transition, in seconds", default=1)

    def get_absolute_url(self):
        return reverse('edit-transition', kwargs={'pk': self.pk})


class TransitionKeyframe(models.Model):
    transition = models.ForeignKey(
        to=Transition,
        unique=False,
        null=True,
        blank=False,
        related_name='keyframes',
        on_delete=models.CASCADE,
    )
    marker = models.CharField(max_length=30, help_text="CSS Keyframe Marker (from, 2%, 50%, to, etc.)")
    css = models.TextField(help_text="CSS to apply at this keyframe marker")

    def get_absolute_url(self):
        return reverse('edit-transition', kwargs={'pk': self.transition.pk})


class Theme(models.Model):
    name = models.CharField(max_length=50)
    css = models.TextField()

    def get_absolute_url(self):
        return reverse('edit-theme', kwargs={'pk': self.pk})

    def parse(self):
        return tinycss2.parse_stylesheet(self.css)

    def get_css_classes(self):
        classes = []
        for css_class in tinycss2.parse_stylesheet(self.css):
            if type(css_class) == QualifiedRule:
                class_list = []
                for token in css_class.prelude:
                    if type(token) == IdentToken:
                        class_list.append(token.value)
                class_string = ' '.join(class_list)
                print(class_string)
                classes.append(class_string)
        return classes

    def __str__(self):
        return self.name


