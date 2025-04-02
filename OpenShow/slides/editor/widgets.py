from django.forms.widgets import Select

class SelectByThumbnailWidget(Select):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context(self, name, value, attrs):
        context = super(self.__class__, self).get_context(name, value, attrs)
        return context
    template_name = 'editor/widgets/select_by_thumbnail.html'
    option_template_name = 'editor/widgets/select_by_thumbnail_option.html'
