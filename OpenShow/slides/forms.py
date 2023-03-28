from django.forms import Form
from django.forms.fields import IntegerField


class SlideDisplayForm(Form):
    show_pk = IntegerField()
    slide_pk = IntegerField()

    class Meta:
        fields = [
            'show_pk',
            'slide_pk',
        ]
