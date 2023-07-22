from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ToolView(TemplateView):
    template_name = "arbolsaf/tool/tool.html"

class IntroToolView(TemplateView):
    template_name = "arbolsaf/tool/tool_intro.html"