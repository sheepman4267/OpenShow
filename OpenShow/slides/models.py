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
    current_theme = models.ForeignKey(
        to='Theme',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    segments = models.ManyToManyField(
        to='Segment',
        blank=True,
    )

    def __str__(self):
        return self.name


class Deck(models.Model):  # A Reusable set of slides, which can be included in a Show Segment
    name = models.CharField(max_length=100)
    default_transition_duration = models.FloatField(
        default=1,
    )
    default_transition = models.ForeignKey(
        to='Transition',
        unique=False,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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
    advance_between_segments = models.BooleanField(default=False, null=False)

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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
        ordering = ["order"]

    def __str__(self):
        return self.name

    def next_with_slides(self, direction):
        siblings = self.show.segments.all()
        if direction == 'reverse':
            siblings = siblings.reverse()
        for idx, segment in enumerate(siblings):
            if segment == self:
                try:
                    next_segment =  siblings[idx + 1]
                except IndexError:
                    return None
                if next_segment.slides.first() or next_segment.included_deck:
                    return next_segment
                else:
                    pass

    def get_first_slide(self):
        if self.included_deck:
            return self.included_deck.slides.first()
        elif self.slides.first():
            return self.slides.first()
        else:
            return None

    def get_last_slide(self):
        if self.slides.last():
            return self.slides.last()
        elif self.included_deck:
            return self.included_deck.slides.last()
        else:
            return None

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
    video = models.FileField(
        blank=True,
        null=True,
        upload_to='element_videos/'
    )

    def get_absolute_url(self):
        return reverse('edit-slide', kwargs={'pk': self.slide.pk})

    def __str__(self):
        if self.slide.segment:
            return f'Show "{self.slide.segment.show.name}"/Segment "{self.slide.segment.name}"/Slide ID {self.slide.pk}/Segment ID {self.pk}'
        elif self.slide.deck:
            return f'Deck "{self.slide.deck.name}"/Slide ID {self.slide.pk}/Segment ID {self.pk}'
        else:
            raise RuntimeError('A slide must be part of something... something has gone very wrong.')

    class Meta:
        ordering = ["-order"]


class QRCodeElement(SlideElement):
    link = models.TextField()


class Slide(models.Model):
    transition_duration = models.FloatField(default=1)
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
            return reverse('edit-show', kwargs={'pk': self.segment.show.pk})
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
            slide_theme = self.get_theme()
            display.current_slide = self
            if display.current_theme != slide_theme:
                display.current_theme = slide_theme
                display.save()
                send_event('test', f'display-{display.pk}-theme', f'sending theme {slide_theme.pk} to display {display.pk}')
            else:
                display.save()
                send_event('test', f'display-{display.pk}-slide', f'sending slide {self.pk} to display {display.pk}')

    def get_theme(self):
        """
        :return:
        Returns the correct Theme object to use when displaying this slide.
        This can be either the deck/show theme (whichever exists in context), or the slide's theme selection.
        The slide theme will override the show/deck theme, if it is set.
        """
        theme = None
        if self.deck:
            if self.deck.theme:
                theme = self.deck.theme
        elif self.segment:
            if self.segment.show.theme:
                theme = self.segment.show.theme
        else:
            theme = self.theme
        return theme

    def get_elements(self):
        return self.elements.all().order_by('order')

    def __str__(self):
        if self.segment:
            return f'Show "{self.segment.show.name}"/Segment "{self.segment.name}"/Slide ID {self.pk}'
        elif self.deck:
            return f'Deck "{self.deck.name}"/Slide ID {self.pk}'
        else:
            raise RuntimeError('A slide must be part of something... something has gone very wrong.')

    def next(self, direction):
        if self.deck:
            siblings = list(self.deck.slides.all())
        elif self.segment:
            siblings = list(self.segment.slides.all())
        else:
            raise RuntimeError('A slide must be part of something... something has gone very wrong.')
        if direction == 'reverse':
            siblings.reverse()
        for idx, slide in enumerate(siblings):
            if slide == self:
                try:
                    return siblings[idx + 1]
                except IndexError:
                    return None
        # or, if there are no more (say, we're at the beginning/end...)
        return self  # TODO: Make this mess better - add a toggle for "continue past end of deck" on the show control sidebar

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.deck:
                if self.deck.default_transition:
                    self.transition = self.deck.default_transition
                if self.deck.default_transition_duration:
                    self.transition_duration = self.deck.default_transition_duration
        super(Slide, self).save(*args, **kwargs)


class Transition(models.Model):
    name = models.CharField(max_length=30)
    default_time = models.FloatField(help_text="Default total time for transition, in seconds", default=1)

    def get_keyframes_in(self):
        return self.keyframes.filter(out=False)

    def get_keyframes_out(self):
        return self.keyframes.filter(out=True)

    def get_safe_name(self):
        """
        :return:
        Returns the name of the transition, with all whitespace removed. This makes it safe for CSS.
        """
        return "".join(self.name.split())

    def get_absolute_url(self):
        return reverse('edit-transition', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


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
    out = models.BooleanField(default=False)

    class Meta:
        ordering = ('marker',)

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


