from django.views.generic import CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse
from slides.models import SlideElement, Slide
from slides.editor.forms import DeleteSlideElementForm, EditSlideElementTextForm
from slides.editor.forms import ChangeSlideElementOrderForm


class SlideElementCreateView(CreateView):
    model = SlideElement
    fields = ['css_class', 'slide']
    template_name = 'editor/element_create.html'


class SlideElementDeleteView(DeleteView):
    model = SlideElement
    template_name = 'editor/delete_element.html'
    form_class = DeleteSlideElementForm

    def form_valid(self, form):
        self.success_url = reverse('slide-wysiwyg', kwargs={"pk": form.cleaned_data["slide_pk"]})
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

    def form_invalid(self, form):
        print(form.errors)
        return(super().form_invalid(form))

    def get_success_url(self):
        print('SUCCESS')
        return self.object.get_absolute_url()


class SlideElementUpdateMediaObjectView(UpdateView):
    model = SlideElement
    fields = ['media_object']
    template_name = 'editor/element_media_object_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

class SlideElementUpdateImageObjectView(UpdateView):
    model = SlideElement
    fields = ['image_object']
    template_name = 'editor/element_image_object_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

class ChangeSlideElementOrderView(FormView):
    form_class = ChangeSlideElementOrderForm

    def __init__(self):
        self.moved_slide = None
        super().__init__()

    def form_valid(self, form):
        self.moved_element = SlideElement.objects.get(pk=form.cleaned_data['moved_element_pk'])
        if form.cleaned_data['next_element_pk']:
            next_element = SlideElement.objects.get(pk=form.cleaned_data['next_element_pk'])
            previous_element = SlideElement.objects.filter(
                slide=self.moved_element.slide,
                order__lt=next_element.order,
            ).last()
            if previous_element:
                order_difference = next_element.order - previous_element.order
                self.moved_element.order = next_element.order - (order_difference / 2)
                self.moved_element.save()
            else:
                self.moved_element.order = next_element.order - 1
                self.moved_element.save()
        else:
            self.moved_element.order = self.moved_element.slide.elements.last().order + 10
            self.moved_element.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.moved_element.slide.get_absolute_url()
