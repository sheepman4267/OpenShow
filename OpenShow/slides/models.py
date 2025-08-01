import hashlib
from django.db import models
from django_eventstream import send_event
from django.templatetags.static import static
from collections.abc import Iterable
from django.shortcuts import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from django_q.models import Schedule
import yaml
import os

import tinycss2

from tinycss2.ast import IdentToken, QualifiedRule


class InvalidArgumentException(Exception):
    pass


class NotSupportedException(Exception):
    pass


class Display(models.Model):  # A set of characteristics used to modify slide appearance for different displays
    name = models.CharField(max_length=100)
    pixel_width = models.IntegerField(default=1920)
    pixel_height = models.IntegerField(default=1080)
    custom_css = models.TextField(null=True, blank=True)
    slide_changed_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False, help_text='Activate this display for any newly created shows')
    current_show = models.ForeignKey(
        to='Show',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    current_slide = models.ForeignKey(
        to='Slide',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    previous_slide = models.ForeignKey(
        to='Slide',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    current_theme = models.ForeignKey(
        to='Theme',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    current_deck = models.ForeignKey(
        to='Deck',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='current_displays'
    )
    segments = models.ManyToManyField(
        to='Segment',
        blank=True,
    )  # TODO: What the heck is this for?

    def advance_slide(self, direction):
        if self.current_deck:
            self._advance_slide_in_deck(direction)
        elif self.current_show:
            self._advance_slide_in_show(direction)

    def _advance_slide_in_deck(self, direction):
        if self.previous_slide and self.current_slide.auto_advance:
            if timezone.now() - \
                    self.slide_changed_at < \
                    timedelta(seconds=self.current_slide.auto_advance_duration):
                # Abort and continue silently if we're getting a "next slide" directive and
                # the previous slide's auto_advance_duration has not passed
                # Manually selecting a different slide will override this.
                return 1
        slide = self.current_slide.next(direction)
        if not slide:
            if self.current_slide.deck.advance_in_loop:
                slide = self.current_slide.deck.slides.first()
            else:
                slide = self.current_slide
        slide.send_to_display([self, ])

    def _advance_slide_in_show(self, direction):
        if self.previous_slide and self.current_slide.auto_advance:
            if timezone.now() - \
                    self.slide_changed_at < \
                    timedelta(seconds=self.current_slide.auto_advance_duration):
                # Abort and continue silently if we're getting a "next slide" directive and
                # the previous slide's auto_advance_duration has not passed
                # Manually selecting a different slide will override this.
                return 1
        slide = self.current_slide.next(direction)
        next_segment = None
        if not slide:
            if self.current_show.advance_between_segments:
                try:  # TODO: review this horrible try/except block
                    if self.current_slide.deck:
                        # If we're out of room to iterate through a deck...
                        current_segment = self.current_show.segments.filter(included_deck=self.current_slide.deck).first()
                        if current_segment.slides.first() and direction == 'forward':
                            slide = current_segment.slides.first()
                        elif direction == 'reverse':
                            slide = current_segment.next_with_slides(direction).get_last_slide()
                        elif direction == 'forward':
                            slide = current_segment.next_with_slides(direction).get_first_slide()
                    else:  # ..if current_slide.segment
                        current_segment = self.current_slide.segment
                        if direction == 'reverse' and current_segment.included_deck:
                            slide = current_segment.included_deck.slides.last()
                        elif direction == 'reverse':
                            slide = current_segment.next_with_slides(direction).get_last_slide()
                        elif direction == 'forward':
                            slide = current_segment.next_with_slides(direction).get_first_slide()
                except AttributeError:
                    slide = self.current_slide
            elif self.current_show.advance_loop:
                if direction == 'reverse':
                    if self.current_slide.deck:
                        slide = self.current_slide.deck.slides.last()
                    else:
                        slide = self.current_slide.segment.slides.last()
                elif direction == 'forward':
                    if self.current_slide.deck:
                        slide = self.current_slide.deck.slides.first()
                    else:
                        slide = self.current_slide.segment.slides.first()
            else:
                slide = self.current_slide
        slide.send_to_display([self, ], self.current_show)
        return 0

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Untitled Display"
    # TODO: Make it possible to pause auto-advance on displays, configurable in the show view.
    # TODO: Make auto-advance pausing triggerable per segment
    # TODO: The Display should probably know the current segment, as well as the current show.
    # auto_advance_paused = models.BooleanField(default=False, null=False)

    def get_absolute_url(self):
        return reverse('display-detail', kwargs={'pk': self.pk})


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
    default_auto_advance = models.BooleanField(default=False, null=False)
    advance_in_loop = models.BooleanField(default=False, null=False)
    default_auto_advance_duration = models.FloatField(default=10)
    slide_text_markup = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('edit-deck', kwargs={'pk': self.pk})

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Untitled Deck"

    def recompute_order(self):
        # TODO: recompute slide order occasionally
        pass

    def pull_aoml(self):
        aoml_str = ''
        for slide in self.slides.all():
            aoml_str += slide.pull_aoml()
            if slide != self.slides.last():
                aoml_str += '~~\r'
        return aoml_str

    def save(self, *args, **kwargs):
        if not self.theme:
            self.theme = Theme.get_default()
        if not self.default_transition:
            self.default_transition = Transition.get_default()
        super(Deck, self).save(*args, **kwargs)

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
    advance_loop = models.BooleanField(default=False, null=False)

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
        theme_classes = theme.get_css_classes()
        for css_class in show_classes:
            if css_class not in theme_classes:
                missing.append(css_class)
        return missing

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Untitled Show"

    def save(self, *args, **kwargs):
        if not self.pk:
            set_defaults = True
        else:
            set_defaults = False
        self.theme = Theme.get_default()
        super(self.__class__, self).save(*args, **kwargs)
        if set_defaults:
            for display in Display.objects.filter(default=True):
                self.displays.add(display.pk)
            self.save()


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
        if self.name:
            return self.name
        else:
            return "Untitled Segment"
    def next_with_slides(self, direction):
        siblings = self.show.segments.all()
        future_segments = []
        if direction == 'reverse':
            siblings = siblings.reverse()
        for idx, segment in enumerate(siblings):
            if segment == self:
                future_segments = siblings[idx + 1:]
        for segment in future_segments:
            if segment.slides.first() or segment.included_deck:
                return segment

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
    css_class = models.CharField(max_length=100, verbose_name="CSS Class")
    body = models.TextField(null=True, blank=True, default="")
    order = models.FloatField()
    slide = models.ForeignKey(
        to='Slide',
        unique=False,
        null=False,
        blank=False,
        related_name='elements',
        on_delete=models.CASCADE,
    )
    image_object = models.ForeignKey(
        to='Image',
        blank=True,
        null=True,
        related_name='elements',
        on_delete=models.SET_NULL,
    )
    missing_image_object = models.BooleanField(default=False)
    video = models.FileField(
        blank=True,
        null=True,
        upload_to='element_videos/'
    )
    missing_media_object = models.BooleanField(default=False)
    media_object = models.ForeignKey(
        to='MediaObject',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='elements',
    )

    def get_absolute_url(self):
        return reverse('slide-wysiwyg', kwargs={'pk': self.slide.pk})

    def __str__(self):
        if self.slide.segment:
            return f'Show "{self.slide.segment.show.name}"/Segment "{self.slide.segment.name}"/Slide ID {self.slide.pk}/Segment ID {self.pk}'
        elif self.slide.deck:
            return f'Deck "{self.slide.deck.name}"/Slide ID {self.slide.pk}/Segment ID {self.pk}'
        else:
            raise RuntimeError('A slide must be part of something... something has gone very wrong.')

    class Meta:
        ordering = ["-order"]

    def save(self, *args, **kwargs):
        if self.missing_image_object and self.image_object:
            self.missing_image_object = False
        if self.missing_media_object and self.media_object:
            self.missing_media_object = False
        if not self.pk:
            if self.slide.elements.last():
                self.order = self.slide.elements.last().order + 10
            else:
                self.order = 1
        super(SlideElement, self).save(*args, **kwargs)

    def get_editable_text(self):
        if self.body:
            self.body = self.body.replace('<br>', '\n')
        return self.body

    def pull_aoml(self):
        aoml_str = f'>>{self.css_class}||\r'
        if self.image_object:
            aoml_str += f'image:{self.image_object.file_hash}||\r'
        if self.media_object:
            aoml_str += f'media:{self.media_object.file_hash}||\r'
        aoml_str += f'{self.body}\r'.replace('<br>', '\\')

        return aoml_str


class QRCodeElement(SlideElement):
    link = models.TextField()


class Slide(models.Model):
    auto_advance = models.BooleanField(default=False, null=False)
    auto_advance_duration = models.FloatField(default=10)
    transition_duration = models.FloatField(default=1)
    order = models.FloatField(null=True)
    cue = models.TextField(null=True, blank=True)
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

    class Meta:
        ordering=['order', 'pk']

    def get_absolute_url(self):
        # if self.segment:
        #     return reverse('edit-show', kwargs={'pk': self.segment.show.pk})
        # elif self.deck:
        #     return reverse('edit-deck', kwargs={'pk': self.deck.pk})
        # else:
        #     raise RuntimeError('A slide must be part of something... something has gone very wrong.')
        return reverse('edit-slide', kwargs={'pk': self.pk})

    def send_to_display(self, displays:Iterable, show:None or Show = None) -> None:
        """
        :param displays:
        An iterable (probably a QuerySet) of Display objects to display the slide on
        :param show:
        The Show object which this slide is being displayed from currently. If this is set to None or not supplied,
        we assume that the slide is being displayed directly from a deck rather than a show.
        :return:
        This method always returns None.
        """
        for display in displays:
            slide_theme = self.get_theme()
            display.previous_slide = display.current_slide  # do the slide shuffle
            display.current_slide = self
            display.current_show = show
            if show is None:
                display.current_deck = self.deck
            else:
                display.current_deck = None
            if display.current_theme != slide_theme and slide_theme is not None:
                # TODO: Add a UI warning to make it more obvious when a show has no theme set
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

    def deck_or_segment(self):
        if self.deck:
            return self.deck
        else:
            return self.segment

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
        # TODO: Not going to pull a chesterton's fence here while working on something else, but let's revisit whether the above return ever gets executed. I don't think it does.

    def save(self, *args, **kwargs):
        if not self.pk:
            self.transition = Transition.get_default()
            # Getting the system-wide default transition first ensures that deck defaults will be used instead if they
            # are set.
            if self.deck:
                if self.deck.default_transition:
                    self.transition = self.deck.default_transition
                if self.deck.default_transition_duration:
                    self.transition_duration = self.deck.default_transition_duration
                if self.deck.default_auto_advance:
                    self.auto_advance = self.deck.default_auto_advance
                if self.deck.default_auto_advance_duration:
                    self.auto_advance_duration = self.deck.default_auto_advance_duration
                if self.deck.slides.last() and not self.order:
                    self.order = self.deck.slides.last().order + 10
                else:
                    self.order = 1
            else:  # as in, if self.segment:
                if self.segment.slides.last() and not self.order:
                    self.order = self.segment.slides.last().order + 10
                else:
                    self.order = 1
        super(Slide, self).save(*args, **kwargs)

    def has_video(self):
        result = False
        for element in self.elements.all():
            if element.video:
                result = True
        return result

    def has_mediaobject(self):
        result = False
        for element in self.elements.all():
            if element.media_object:
                result = True
        return result

    def pull_aoml(self):
        metadata = yaml.safe_dump(
            {
                'cue': self.cue,
            }
        )
        aoml_str = f'{metadata}##\n'
        for element in self.elements.all().order_by('order'):
            aoml_str += element.pull_aoml()
        return aoml_str


class Transition(models.Model):
    name = models.CharField(max_length=30)
    default_time = models.FloatField(help_text="Default total time for transition, in seconds", default=1)
    default = models.BooleanField(default=False)

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
        if self.name:
            return self.name
        else:
            return "Untitled Transition"

    def save(self, *args, **kwargs):
        if self.default:
            for transition in Transition.objects.filter(default=True):
                transition.default = False
                transition.save()
        super(Transition, self).save(*args, **kwargs)

    @staticmethod
    def get_default():
        return Transition.objects.filter(default=True).first()


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
    default = models.BooleanField(default=False)

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
                classes.append(class_string)
        return classes

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Untitled Theme"

    def save(self, *args, **kwargs):
        if self.default:
            for theme in Theme.objects.filter(default=True):
                theme.default = False
                theme.save()
        super(Theme, self).save(*args, **kwargs)

    @staticmethod
    def get_default():
        return Theme.objects.filter(default=True).first()


class ThemeRule(models.Model):
    css_selector = models.CharField(max_length=100, help_text="CSS Selector")
    properties = models.TextField()
    base_rule = models.BooleanField(default=False)
    theme = models.ForeignKey(
        to=Theme,
        on_delete=models.CASCADE,
        related_name='rules',
    )


class ThemeVariant(models.Model):
    name = models.CharField(max_length=100)
    theme = models.ForeignKey(
        to=Theme,
        on_delete=models.CASCADE,
        related_name='variants',
    )


class ThemeVariantRule(models.Model):
    rule = models.ForeignKey(
        to=ThemeRule,
        on_delete=models.CASCADE,
        related_name='variants',
    )
    properties = models.TextField()
    variant = models.ForeignKey(
        to=ThemeVariant,
        on_delete=models.CASCADE,
        related_name='rules',
    )


VIMEO_LIVE_EMBED = 'VIMEO_LIVE_EMBED'
VIDEO = 'VIDEO'
AUDIO = 'AUDIO'


class MediaObject(models.Model):
    title = models.CharField(max_length=100, unique=True)
    media_type = models.CharField(
        max_length=100,
        choices=[
            (VIMEO_LIVE_EMBED, 'Vimeo Live Embed'),
            (VIDEO, 'Video'),
            (AUDIO, 'Audio'),
        ],
        default=VIDEO,
    )
    # We'll use the same field regardless of what file type is uploaded - the FileField does no validation, so there's
    # no particular benefit to adding more fields here.
    raw_file = models.FileField(
        blank=True,
        null=True,
        upload_to='media_intake/'
    )
    # We'll use the same field regardless of what file type is uploaded - the FileField does no validation, so there's
    # no particular benefit to adding more fields here.
    final_file = models.FileField(
        blank=True,
        null=True,
        upload_to='media_final/'
    )
    thumbnail_image = models.FileField(
        blank=True,
        null=True,
        upload_to='media_final/thumbnail/'
    )
    embed_url = models.URLField(
        blank=True,
        null=True,
    )
    autoplay = models.BooleanField(
        default=True,
        # Currently, there would be no mechanism to manually start a non-autoplaying media object, so this will just sit
        # until more features are implemented, but let's leave the bones of it here for the future.
    )
    needs_transcode = models.BooleanField(
        default=True,
        blank=True,
        verbose_name='Transcode this Media Object',
    )
    file_hash = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.embed_url:
            self.file_hash = hashlib.sha256(self.embed_url.encode("utf-8")).hexdigest()
        if self.media_type == VIDEO and self.needs_transcode:
            super().save(*args, **kwargs)
            Schedule.objects.create(
                func='slides.editor.tasks.transcode_video',
                args=self.pk,
                schedule_type=Schedule.ONCE,
                next_run=datetime.utcnow(),
            )
            Schedule.objects.create(
                func='slides.editor.tasks.thumbnail_video',
                args=self.pk,
                schedule_type=Schedule.ONCE,
                next_run=datetime.utcnow(),
            )
            self.needs_transcode = False
        elif self.media_type == AUDIO and self.needs_transcode:
            super().save(*args, **kwargs)
            Schedule.objects.create(
                func='slides.editor.tasks.transcode_audio',
                args=self.pk,
                schedule_type=Schedule.ONCE,
                next_run=datetime.utcnow(),
            )
            self.needs_transcode = False
        super().save(*args, **kwargs)

    def get_slide_element_template(self):
        template_name = None
        match self.media_type:
            case 'VIDEO':
                template_name = 'slides/media/video.html'
            case 'AUDIO':
                template_name = 'slides/media/audio.html'
            case 'VIMEO_LIVE_EMBED':
                template_name = 'slides/media/vimeo_live_embed.html'
        return template_name

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Untitled Media Object"

    def thumbnail(self):
        thumbnail = None
        match self.media_type:
            case 'VIDEO':
                if self.thumbnail_image:
                    thumbnail = self.thumbnail_image.url
                else:
                    thumbnail = static('media_object_thumbnails/video-thumbnail-error.png')
            case 'AUDIO':
                thumbnail = static('media_object_thumbnails/audio-mediaobject-thumbnail.png')
            case 'VIMEO_LIVE_EMBED':
                thumbnail = static('media_object_thumbnails/vimeo-live-embed-thumbnail.png')
        return thumbnail

    class Meta:
        ordering = ('-pk', )


class Image(models.Model):
    file = models.ImageField(
        blank=False,
        null=False,
        upload_to='images/',
    )
    file_hash = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(self.__class__, self).save(*args, **kwargs)
        hash_func = hashlib.new('sha256')
        with open(self.file.path, 'rb') as file:
            while chunk := file.read(65536):
                hash_func.update(chunk)
        self.file_hash = hash_func.hexdigest()
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.file.name)

    def thumbnail(self):
        return self.file.url

    class Meta:
        ordering = ('-pk', )
