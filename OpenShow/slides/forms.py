from django.forms import Form, ModelForm
from django.forms.fields import IntegerField, CharField
from .models import Show


class SlideDisplayForm(Form):
    show_pk = IntegerField()
    slide_pk = IntegerField(required=False)
    direction = CharField(required=False)

    class Meta:
        fields = [
            'show_pk',
            'slide_pk',
            'direction',
        ]


class ShowDisplaySelectorForm(ModelForm):
    class Meta:
        model = Show
        fields = ['displays',]
