
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
import json
from ..models import SynonymousModel, SpeciesModel
from ..forms import SynonymousForm




@login_required(login_url='/login/')
def sinonimo_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id= query['id']
    print(id)
    sinonimo = SynonymousModel.objects.get(pk=id)
    try:
        sinonimo.delete()
    except RestrictedError as e:
        resp['mensaje']= 'restricted'
        resp['error'] = "{} {}".format(e.args[0], str(e.args[1]))
        return  JsonResponse(resp, status=500)
    except Exception as e:
        resp['mensaje']= 'error'
        resp['error'] = json.dumps(e)
        return  JsonResponse(resp, status=500)
    
    resp['mensaje']= 'deleted'
    print(resp)
    return  JsonResponse(resp, status=200)




class Synonymous2MCreateView(LoginRequiredMixin, CreateView):
    model = SynonymousModel
    context_object_name = 'sinonimo'
    template_name = 'arbolsaf/synonimous/synonimous_o2m_form.html'
    form_class = SynonymousForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        if 'pk' in self.kwargs:
            specie_id = get_object_or_404(SpeciesModel, pk=self.kwargs['pk'])
            context['specie'] =specie_id
            context['specie_pk'] = self.kwargs['pk']
            redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.kwargs['pk']})   
            context['species_url'] =  redireccion+'#sinonimosection'
        return context

    def get_success_url(self):
        if 'pk' in self.kwargs:
            redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.kwargs['pk']})   
            return redireccion+'#sinonimosection'
        #else:
        #    return reverse_lazy("ganaclima:period_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        specie = form.save(commit=False)
        #User = get_user_model()

        specie.created_by = self.request.user # use your own profile here
        #farm.active=True
        specie.save()
        return super(Synonymous2MCreateView, self).form_valid(form)


@login_required(login_url='/login/')
def create_sinonimo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SynonymousForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_sinonimo = form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":request.POST['especie']})
            redireccion = redireccion+'#sinonimosection'
           
            return HttpResponseRedirect(redireccion)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SynonymousForm()

    #return render(request, 'name.html', {'form': form})
