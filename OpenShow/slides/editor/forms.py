from django.forms import Form, ModelForm, IntegerField
from ..models import Show


# class SimpleShowForm(ModelForm):
#     class Meta:
#         model = Show
#         fields = [
#             'name'
#         ]


class DeleteSlideElementForm(Form):
    slide_pk = IntegerField()