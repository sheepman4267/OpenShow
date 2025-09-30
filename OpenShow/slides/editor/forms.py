from django.forms import Form, ModelForm, IntegerField, ChoiceField, Select, ClearableFileInput, FileField, CharField, ModelChoiceField
from django.forms.models import ModelChoiceIterator
from django.urls import reverse_lazy
from ..models import Show, Theme, SlideElement, Deck, Segment, Image, MediaObject
from .widgets import SelectByThumbnailWidget
from natsort import natsorted


# class SimpleShowForm(ModelForm):
#     class Meta:
#         model = Show
#         fields = [
#             'name'
#         ]


class NatsortedChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        choices = natsorted(list(queryset), key=lambda deck: deck.name)
        for obj in choices:
            yield self.choice(obj)


class NatsortedModelChoiceField(ModelChoiceField):
    iterator = NatsortedChoiceIterator


class DeleteSlideElementForm(Form):
    slide_pk = IntegerField()


class SetThemeForm(ModelForm):
    show_pk = IntegerField()
    class Meta:
        model = Show
        fields = (
            'theme',
            'show_pk',
        )
        widgets = {
            'theme': Select(
                    attrs={
                        'hx-post': reverse_lazy('check-theme-compatibility'),
                        'hx-swap': 'afterend',
                        'hx-trigger': 'change',
                    }
                ),
        }


class ChangeSlideOrderForm(Form):
    deck_or_segment_pk = IntegerField()
    moved_slide_pk = IntegerField()
    next_slide_pk = IntegerField(required=False)


class ChangeSlideElementOrderForm(Form):
    moved_element_pk = IntegerField()
    next_element_pk = IntegerField(required=False)


class EditSlideElementTextForm(ModelForm):
    class Meta:
        model = SlideElement
        fields = ['body',]

    def save(self, commit=True):
        self.instance.body = self.cleaned_data['body'].replace('\n', '<br>')
        return super(EditSlideElementTextForm, self).save()


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DeckFromImagesForm(ModelForm):
    class Meta:
        model = Deck
        fields = [
            'name',
            'default_transition',
            'default_transition_duration',
            'default_auto_advance',
            'default_auto_advance_duration',
            'advance_in_loop',
            'theme',
        ]
    files = MultipleFileField()
    image_css_class = CharField()


class ImportImagesForm(Form):
    OVERWRITE = 'OVERWRITE'
    APPEND = 'APPEND'
    IMPORT_MODE_CHOICES = [
        (APPEND, 'Append'),
        (OVERWRITE, 'Overwrite (DANGER!! Will permanently erase all slides in this deck!)'),
    ]
    files = MultipleFileField()
    image_css_class = CharField()
    mode = ChoiceField(
        choices=IMPORT_MODE_CHOICES,
    )


class UpdateSegmentForm(ModelForm):
    included_deck = NatsortedModelChoiceField(queryset=Deck.objects.all(), required=False)
    class Meta:
        model = Segment
        fields = [
            'name',
            'order',
            'included_deck',
            'details',
        ]


class SlideElementUpdateImageObjectForm(ModelForm):
    class Meta:
        model = SlideElement
        fields = [
            'image_object',
        ]
        widgets = {
            'image_object': SelectByThumbnailWidget(),
        }


class SlideElementUpdateMediaObjectForm(ModelForm):
    class Meta:
        model = SlideElement
        fields = [
            'media_object',
        ]
        widgets = {
            'media_object': SelectByThumbnailWidget(),
        }


class ImageUploadToElementForm(ModelForm):
    element_pk = IntegerField()
    class Meta:
        model = Image
        fields = [
            'file',
        ]

    def save(self, commit=True):
        image = super(self.__class__, self).save(commit)
        element = SlideElement.objects.get(pk=self.cleaned_data["element_pk"])
        element.image_object = image
        element.save()
        return image

class MediaObjectUploadToElementForm(ModelForm):
    element_pk = IntegerField()

    class Meta:
        model = MediaObject
        fields = [
            'title',
            'media_type',
            'raw_file',
            'embed_url',
        ]

    def save(self, commit=True):
        media_object = super(self.__class__, self).save(commit)
        element = SlideElement.objects.get(pk=self.cleaned_data["element_pk"])
        element.media_object = media_object
        element.save()
        return media_object


class ShowRemoteImportForm(Form):
    url = ChoiceField()


class ShowJSONImportForm(Form):
    name_prefix = CharField()
    json_string = CharField()
