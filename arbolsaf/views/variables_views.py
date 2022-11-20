from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import json
from ..models import VariableModel, SpeciesModel
from ..forms import SpeciesForm, VariableO2MForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError, HttpResponseBadRequest

"""
class SpeciesListView(LoginRequiredMixin, ListView):
    model = SpeciesModel
    template_name = 'arbolsaf/species/species_list.html'
    context_object_name = 'species'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(SpeciesListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'

        context['value_name'] = self.request.GET.get('name', '')

        if 'name' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True
        
        self.request.session['page_from'] = ""
        self.request.session['referer'] = {}

        if context['is_paginated']:
            list_pages = []

            if 'name' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(SpeciesListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(SpeciesListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(SpeciesListView.get_queryset(self)) / self.paginate_by) + 1

                if paginated > 1:
                    for i in range(int(first_range), int(first_range) + 5):
                        if i <= paginated:
                            list_pages.append(i)

                    context['total_pages'] = paginated
                    context['has_more_pages'] = True if int(first_range) < paginated else False
                    context['next_page'] = int(first_range) + 1 if int(first_range) < paginated else '0'
                    context['has_previous_pages'] = True if int(first_range) > 1 else False
                    context['previous_page'] = int(first_range) - 1 if int(first_range) > 1 else '0'
                    context['actual_page'] = int(first_range)

            context['paginator_rows'] = list_pages

        return context

    def get_queryset(self):

        query = {'name': self.request.GET.get('name', None)}


        query_result =  SpeciesModel.objects.order_by('cod_esp')

        if query['name'] and query['name'] != '':
            query_result = query_result.filter(name__icontains=query['name'])

        return query_result

class SpeciesDetailView(LoginRequiredMixin, DetailView):
    model = SpeciesModel
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'specie'
    template_name = 'arbolsaf/species/species_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        return context

class SpeciesCreateView(LoginRequiredMixin, CreateView):
    model = SpeciesModel
    context_object_name = 'specie'
    template_name = 'arbolsaf/species/species_form.html'
    form_class = SpeciesForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        #if 'pk' in self.kwargs:
        #    context['farm_pk'] = self.kwargs['pk']
        #    redireccion = reverse_lazy("ganaclima:farm_detail", kwargs={"pk":self.kwargs['pk']})   
        #    context['farm_url'] =  redireccion+'#periodos'
        return context

    def get_success_url(self):
        return reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.created_by = self.request.user 
        farm.active=True
        farm.save()
        return super(SpeciesCreateView, self).form_valid(form)
        #return HttpResponseRedirect(self.get_success_url()) 


class SpeciesUpdateView(LoginRequiredMixin, UpdateView):
    model = SpeciesModel
    context_object_name = 'specie'
    template_name = 'arbolsaf/species/species_form.html'
    form_class = SpeciesForm
    
    def get_success_url(self):
        return reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.id})   

    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.modified_by = self.request.user # use your own profile here
        farm.active=True
        farm.save()
        return super(SpeciesUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        return context
"""

class Variable2MDetailView(LoginRequiredMixin, DetailView):
    model = VariableModel
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_o2m_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        context['specie_pk'] = self.object.especie.id
        redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.especie.id})   
        context['species_url'] =  redireccion+'#variablessection'
        return context

class VariableO2MCreateView(LoginRequiredMixin, CreateView):
    model = VariableModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_o2m_form.html'
    form_class = VariableO2MForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        if 'pk' in self.kwargs:
            specie_id = get_object_or_404(SpeciesModel, pk=self.kwargs['pk'])
            context['specie'] =specie_id
            context['specie_pk'] = self.kwargs['pk']
            redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.kwargs['pk']})   
            context['species_url'] =  redireccion+'#variablessection'
        return context

    def get_success_url(self):
        if 'pk' in self.kwargs:
            redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.kwargs['pk']})   
            return redireccion+'#variablessection'
        #else:
        #    return reverse_lazy("ganaclima:period_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        specie = form.save(commit=False)
        #User = get_user_model()

        specie.created_by = self.request.user # use your own profile here
        #farm.active=True
        specie.save()
        return super(VariableO2MCreateView, self).form_valid(form)


class VariableO2MUpdateView(LoginRequiredMixin, UpdateView):
    model = VariableModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_o2m_form.html'
    form_class = VariableO2MForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        context['specie_pk'] = self.object.especie.id
        redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.especie.id})   
        context['species_url'] =  redireccion+'#variablessection'
        #if 'pk' in self.kwargs:
        #    context['specie_pk'] = self.kwargs['pk']
        #    redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.kwargs['pk']})   
        #    context['species_url'] =  redireccion+'#variablessection'
        return context

    def get_success_url(self):

        redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.especie.id})   
        return redireccion+'#variablessection'
        #else:
        #    return reverse_lazy("ganaclima:period_detail", kwargs={"pk":self.object.id})   
    
    def form_valid(self, form):
        specie = form.save(commit=False)
        #User = get_user_model()

        specie.modified_by = self.request.user # use your own profile here
        #farm.active=True
        specie.save()
        return super(VariableO2MUpdateView, self).form_valid(form)


@login_required(login_url='/login/')
def variable_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id= query['id']
    print(id)
    variable = VariableModel.objects.get(pk=id)
    try:
        variable.delete()
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



