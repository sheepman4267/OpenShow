from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from neapolitan.views import CRUDView, Role

from slides.editor.forms import MediaObjectUploadToElementForm
from slides.models import MediaObject, Image, SlideElement


class MediaObjectCRUDView(CRUDView):
    model = MediaObject
    fields = [
        'title',
        'media_type',
        'raw_file',
        'embed_url',
        'needs_transcode',
        #'autoplay',  # Uncomment this once it will be useful for something
    ]

    def form_valid(self, form):
        success_url = super(MediaObjectCRUDView, self).form_valid(form)
        if 'raw_file' in form.changed_data:
            self.object.needs_transcode = True
            self.object.save()
        return success_url


    def get_success_url(self):
        if self.role is Role.DELETE:
            success_url = reverse('slides-index')
        else:
            success_url = super(self.__class__, self).get_success_url()
        return success_url

    def detail(self, request, *args, **kwargs):
        """GET handler for the detail view."""
        self.object = self.get_object()
        context = self.get_context_data()
        context['previous_page'] = 'slides-index'
        return self.render_to_response(context)

    def get_template_names(self):
        """
        Returns a list of template names to use when rendering the response.

        If `.template_name` is not specified, uses the
        "{app_label}/{model_name}{template_name_suffix}.html" model template
        pattern, with the fallback to the
        "neapolitan/object{template_name_suffix}.html" default templates.
        """
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            return [
                f"editor/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"neapolitan/object{self.template_name_suffix}.html",
            ]
        msg = (
            "'%s' must either define 'template_name' or 'model' and "
            "'template_name_suffix', or override 'get_template_names()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)


class MediaObjectUploadToElementView(CreateView):
    model = MediaObject
    form_class = MediaObjectUploadToElementForm
    template_name = "editor/element_media_object_upload.html"

    def form_valid(self, form):
        element = SlideElement.objects.get(pk=form.cleaned_data['element_pk'])
        self.success_url = element.get_absolute_url()
        return super(self.__class__, self).form_valid(form)
