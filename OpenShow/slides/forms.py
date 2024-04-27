from django.forms import Form, ModelForm
from django.forms.fields import IntegerField, CharField
from .models import Show


class SlideDisplayForm(Form):
    show_pk = IntegerField(required=False)
    slide_pk = IntegerField(required=False)
    direction = CharField(required=False)
    display_pk_multiple = CharField(required=False)

    class Meta:
        fields = [
            'show_pk',
            'slide_pk',
            'direction',
            'display_pk_multiple',
        ]


class ShowDisplaySelectorForm(ModelForm):
    class Meta:
        model = Show
        fields = ['displays',]
