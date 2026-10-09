from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from slides.editor.forms import ThemeRuleCreateForm
from slides.models import Theme, ThemeFont, ThemeRule, ThemeVariant, ThemeVariantRule


class ThemeCreateView(CreateView):
    model = Theme
    template_name = "editor/snippets/hx-simple_create_form.html"
    fields = ["name"]
    extra_context = {
        "action": "theme-create",
        "object_type": "Theme",
    }


class ThemeDeleteView(DeleteView):
    model = Theme
    success_url = reverse_lazy("slides-index")
    template_name = "editor/generic_confirm_delete.html"
    extra_context = {
        "action": "theme-delete",
    }


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = "editor/theme/theme_edit.html"
    fields = ["name", "default", "css"]
    extra_context = {
        "previous_page": "slides-index",
    }
    # TODO: Send a theme refresh event to all displays when saving


class ThemeRuleCreateView(CreateView):
    form_class = ThemeRuleCreateForm
    template_name = "editor/theme/rule_create.html"

    def form_valid(self, form):
        form.save()
        if form.instance.base_rule:
            success_url = form.instance.get_absolute_url()
        else:
            success_url = ThemeRule.objects.get(pk=form.cleaned_data["parent_rule_pk"]).get_absolute_url()
        return HttpResponseRedirect(success_url)


class ThemeRuleUpdateView(UpdateView):
    model = ThemeRule
    template_name = "editor/theme/rule_edit.html"
    fields = ["css_selector", "properties", "base_rule", "description"]


class ThemeRuleDeleteView(DeleteView):
    model = ThemeRule
    template_name = "editor/generic_confirm_delete.html"
    extra_context = {
        "action": "theme-rule-delete",
    }

    def get_success_url(self):
        success_url = reverse_lazy("theme-edit", kwargs={"pk": self.object.theme.pk})
        return success_url


class ThemeVariantCreateView(CreateView):
    model = ThemeVariant
    template_name = "editor/theme/variant_create.html"
    fields = ["name", "description", "theme"]


class ThemeVariantUpdateView(UpdateView):
    model = ThemeVariant
    template_name = "editor/theme/variant_edit.html"
    fields = ["name", "description"]


class ThemeVariantDeleteView(DeleteView):
    model = ThemeVariant
    template_name = "editor/generic_confirm_delete.html"
    extra_context = {
        "action": "theme-variant-delete",
    }

    def get_success_url(self):
        success_url = reverse_lazy("theme-edit", kwargs={"pk": self.object.theme.pk})
        return success_url


class ThemeVariantRuleCreateView(CreateView):
    model = ThemeVariantRule
    template_name = "editor/theme/variant_rule_create.html"
    fields = ["name", "description", "theme"]


class ThemeVariantRuleUpdateView(UpdateView):
    model = ThemeVariantRule
    template_name = "editor/theme/variant_rule_edit.html"
    fields = ["name", "description"]


class ThemeVariantRuleDeleteView(DeleteView):
    model = ThemeVariantRule
    template_name = "editor/generic_confirm_delete.html"
    extra_context = {
        "action": "theme-variant-rule-delete",
    }

    def get_success_url(self):
        success_url = reverse_lazy(
            "theme-variant-edit", kwargs={"pk": self.object.variant.pk}
        )
        return success_url


class ThemeFontCreateView(CreateView):
    model = ThemeFont
    template_name = "editor/theme/font_create.html"
    fields = ["name", "properties", "font_file", "theme"]


class ThemeFontUpdateView(UpdateView):
    model = ThemeFont
    template_name = "editor/theme/font_edit.html"
    fields = ["name", "properties", "font_file"]


class ThemeFontDeleteView(DeleteView):
    model = ThemeFont
    template_name = "editor/generic_confirm_delete.html"
    extra_context = {
        "action": "theme-font-delete",
    }

    def get_success_url(self):
        success_url = reverse_lazy("theme-edit", kwargs={"pk": self.object.theme.pk})
        return success_url
