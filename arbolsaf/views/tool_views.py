from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ToolView(LoginRequiredMixin, TemplateView):
    template_name = "arbolsaf/tool/tool.html"