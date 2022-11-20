from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render



class TempateView404(TemplateView):
    template_name = 'apps/templates/home/page-404.html.html'



def render_404_view(request):
    context = {}
    return render(request, 'apps/templates/home/page-404.html.html', context)