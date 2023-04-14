from django.forms import Form, ModelForm, IntegerField, ChoiceField, Select
from django.urls import reverse_lazy
from ..models import Show, Theme


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
