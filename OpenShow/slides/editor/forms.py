from django.forms import Form, ModelForm, IntegerField, ChoiceField, Select
from django.urls import reverse_lazy
from ..models import Show, Theme, SlideElement


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
