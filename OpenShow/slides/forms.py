from django.forms import Form
from django.forms.fields import IntegerField, CharField


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
