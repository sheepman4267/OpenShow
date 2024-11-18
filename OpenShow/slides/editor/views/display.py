from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from slides.models import Display


class DisplayDetailView(DetailView):
    model = Display
    template_name = 'editor/display/detail.html'
    extra_context = {
        'previous_page': 'slides-index',
    }


class DisplayCreateView(CreateView):
    model = Display
    fields = [
        'name',
    ]
    template_name = 'editor/display/create.html'


class DisplayUpdateView(UpdateView):
    model = Display
    fields = [
        'name',
        # 'pixel_width',
        # 'pixel_height',
        # Changing these will break things right now; non-1080p resolutions are not supported. See #22.
        'custom_css',
        'default',
        # Display.custom_css might go away to be replaced by theme display variants.
    ]
    template_name = 'editor/display/update.html'


class DisplayDeleteView(DeleteView):
    model = Display
    template_name = 'editor/display/delete.html'