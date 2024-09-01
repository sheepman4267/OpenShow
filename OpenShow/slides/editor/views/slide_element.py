from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse
from slides.models import SlideElement
from slides.editor.forms import DeleteSlideElementForm, EditSlideElementTextForm


class SlideElementCreateView(CreateView):
    model = SlideElement
    fields = ['css_class', 'body', 'order', 'image', 'video', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'new'}


class SlideElementUpdateView(UpdateView):
    model = SlideElement
    fields = ['css_class', 'body', 'order', 'image','video', 'slide']
    template_name = 'editor/edit_element.html'
    extra_context = {'action': 'edit'}


class SlideElementDeleteView(DeleteView):
    model = SlideElement
    template_name = 'editor/delete_element.html'
    form_class = DeleteSlideElementForm

    def form_valid(self, form):
        self.success_url = reverse('edit-slide', kwargs={"pk": form.cleaned_data["slide_pk"]})
        return super().form_valid(form)


class SlideElementUpdateTextView(UpdateView):
    form_class = EditSlideElementTextForm
    model = SlideElement
    # fields = ['body',]
    template_name = 'editor/element_text_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class SlideElementUpdateCSSClassView(UpdateView):
    model = SlideElement
    fields = ['css_class']
    template_name = 'editor/element_css_class_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class SlideElementUpdateImageView(UpdateView):
    model = SlideElement
    fields = ['image']
    template_name = 'editor/element_image_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class SlideElementUpdateVideoView(UpdateView):
    model = SlideElement
    fields = ['video']
    template_name = 'editor/element_video_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()
