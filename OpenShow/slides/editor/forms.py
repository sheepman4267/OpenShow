from django.forms import Form, ModelForm, IntegerField, ChoiceField, Select, ClearableFileInput, FileField, CharField
from django.urls import reverse_lazy
from ..models import Show, Theme, SlideElement, Deck


# class SimpleShowForm(ModelForm):
#     class Meta:
#         model = Show
#         fields = [
#             'name'
#         ]


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