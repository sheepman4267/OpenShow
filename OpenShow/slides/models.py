from django.db import models
from django_eventstream import send_event
from collections.abc import Iterable
from django.shortcuts import reverse


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
    custom_css = models.TextField(null=True, blank=True)


class Show(models.Model):  # The main driver of the "presentation interface". A collection of segments, which could either have their own slides or include them from a Deck
    name = models.CharField(max_length=200)
    displays = models.ManyToManyField(
        to=Display,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('edit-show', kwargs={'pk': self.pk})

    def next_segment_order(self):
        return max([0, ] + [segment.order for segment in self.segments.all()]) + 1


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
    name = models.CharField(max_length=100)
    css_class = models.CharField(max_length=100)
    body = models.TextField()
    order = models.IntegerField()
    slide = models.ForeignKey(
        to='Slide',
        unique=False,
        null=False,
        blank=False,
        related_name='elements',
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse('edit-slide', kwargs={'pk': self.slide.pk})

    class Meta:
        ordering = ["-order"]


class Slide(models.Model):
    segment = models.ForeignKey(
        to=Segment,
        unique=False,
        related_name='slides',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

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
    default_time = models.FloatField(help_text="Default total time for transition, in seconds")
    keyframes = models.ManyToManyField("TransitionKeyframe")


class TransitionKeyframe(models.Model):
    marker = models.CharField(max_length=30, help_text="CSS Keyframe Marker (from, 2%, 50%, to, etc.)")
    css = models.TextField(help_text="CSS to apply at this keyframe marker")

