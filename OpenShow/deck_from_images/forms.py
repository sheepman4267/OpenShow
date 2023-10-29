from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        print('cleaning')
        print(data)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
            print('many')
        else:
            result = single_file_clean(data, initial)
            print('single')
        print('hi!')
        return result


class DeckFromImagesForm(forms.Form):
    name = forms.CharField(max_length=100)
    files = MultipleFileField()
    transition_pk = forms.IntegerField()  # this is horrible and should be replaced with a civilized selection system.
    image_css_class = forms.CharField(max_length=1000)
