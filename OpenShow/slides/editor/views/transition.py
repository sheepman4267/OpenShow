from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from slides.models import Transition, TransitionKeyframe


class TransitionEditorIndexView(ListView):
    queryset = Transition.objects.all()
    template_name = 'editor/transition_editor.html'
    extra_context = {
        'transition_list': Transition.objects.all()
    }


class TransitionEditorView(UpdateView):
    model = Transition
    template_name = 'editor/transition_editor.html'
    fields = ["name", "default"]
    extra_context = {
        'transition_list': Transition.objects.all
    }


class TransitionCreateView(CreateView):
    model = Transition
    fields = ["name"]
    template_name = 'editor/snippets/hx-simple_create_form.html'
    extra_context = {
        'action': 'new-transition',
        'object_type': 'Transition',
    }


class TransitionKeyframeCreateView(CreateView):
    model = TransitionKeyframe
    fields = ["transition", "marker", "css", "out"]
    template_name = "editor/edit_keyframe.html"
    extra_context = {
        'action': 'new-keyframe',
    }


class TransitionKeyframeUpdateView(UpdateView):
    model = TransitionKeyframe
    fields = ["marker", "css"]
    template_name = "editor/edit_keyframe.html"
    extra_context = {
        'action': 'edit-keyframe',
    }
