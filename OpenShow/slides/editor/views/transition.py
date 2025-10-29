from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from slides.models import Transition, TransitionKeyframe

class TransitionEditorView(UpdateView):
    model = Transition
    template_name = 'editor/transition/transition_editor.html'
    fields = ["name", "default"]
    extra_context = {
        'transition_list': Transition.objects.all,
        'previous_page': 'slides-index',
    }


class TransitionCreateView(CreateView):
    model = Transition
    fields = ["name"]
    template_name = 'editor/snippets/hx-simple_create_form.html'
    extra_context = {
        'action': 'new-transition',
        'object_type': 'Transition',
    }


class TransitionDeleteView(DeleteView):
    model = Transition
    success_url = reverse_lazy('slides-index')
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-transition',
    }


class TransitionPreviewCSSView(DetailView):
    model = Transition
    template_name = 'editor/transition/transition.css'

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        print(object.get_safe_name())
        context = {
            'transition': self.get_object(),
            'transition_duration': 1,
        }
        return TemplateResponse(request, self.template_name, context, content_type='text/css')


class TransitionDemoView(DetailView):
    model = Transition
    template_name = 'editor/transition/transition_demo.html'


class TransitionKeyframeCreateView(CreateView):
    model = TransitionKeyframe
    fields = ["transition", "marker", "css", "out"]
    template_name = "editor/transition/edit_keyframe.html"
    extra_context = {
        'action': 'new-keyframe',
    }


class TransitionKeyframeUpdateView(UpdateView):
    model = TransitionKeyframe
    fields = ["marker", "css"]
    template_name = "editor/transition/edit_keyframe.html"
    extra_context = {
        'action': 'edit-keyframe',
    }


class TransitionKeyframeDeleteView(DeleteView):
    model = TransitionKeyframe
    success_url = reverse_lazy('slides-index')
    template_name = 'editor/generic_confirm_delete.html'
    extra_context = {
        'action': 'delete-keyframe',
    }
