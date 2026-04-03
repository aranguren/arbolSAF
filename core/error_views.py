from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

class TempateView404(TemplateView):
    template_name = 'apps/templates/home/page-404.html.html'




def render_404_view(request, *args, **argv):
    #return render(request, '500.html', status=500)
    #return render(request, 'homa/page-404.html', {})
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render({}, request))

def render_403_view(request, *args, **argv):
    #return render(request, '500.html', status=500)
    #return render(request, 'homa/page-404.html', {})
    html_template = loader.get_template('home/page-403.html')
    return HttpResponse(html_template.render({}, request))   

def render_500_view(request, *args, **argv):
    #return render(request, '500.html', status=500)
    #return render(request, 'homa/page-404.html', {})
    html_template = loader.get_template('home/page-500.html')
    return HttpResponse(html_template.render({}, request))   

def render_400_view(request, *args, **argv):
    #return render(request, '500.html', status=500)
    #return render(request, 'homa/page-404.html', {})
    html_template = loader.get_template('home/page-400.html')
    return HttpResponse(html_template.render({}, request))   
    #return render(request, 'arbolsaf/errors/page-404.html', {}, status=404)
"""
def render_404_view(request):
    context = {}
    return render(request, 'apps/templates/home/page-404.html.html', context)
"""
