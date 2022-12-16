from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db import connection
import json
from ..models import SpeciesModel, VariableTypeModel, ReferenceModel, VariableTypeFamilyModel
from ..forms import VariableTypeForm




class VariableTypeListView(LoginRequiredMixin, ListView):
    model = VariableTypeModel
    template_name = 'arbolsaf/variable_type/variable_type_list.html'
    context_object_name = 'variables'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(VariableTypeListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf','variable_type']
        context['active_menu'] ='arbolsaf'



        familias =  VariableTypeFamilyModel.objects.order_by('nombre')
        context['familias']=familias

        if 'variable' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True



        context['value_cod_var'] = self.request.GET.get('cod_var', '')
        context['value_variable'] = self.request.GET.get('variable', '')

        context['value_tipo_variables'] = self.request.GET.get('tipo_variables', '')
        context['value_familia'] = self.request.GET.get('familia', '')




        #context['value_taxonid_wfo'] = self.request.GET.get('taxonid_wfo', '')
        #context['value_nombre_comun'] = self.request.GET.get('nombre_comun', '')
        #context['value_nombre_cientifico'] = self.request.GET.get('nombre_cientifico', '')
        #context['value_tipo_variable'] = self.request.GET.get('tipo_variable', '')
        #context['value_referencia'] = self.request.GET.get('referencia', '')

        if context['is_paginated']:
            list_pages = []

            if 'nombre_comun' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(VariableTypeListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(VariableTypeListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(VariableTypeListView.get_queryset(self)) / self.paginate_by) + 1

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

        query = {
            'cod_var': self.request.GET.get('cod_var', None),
            'variable': self.request.GET.get('variable', None),
            'tipo_variables': self.request.GET.get('tipo_variables', None),
            'familia': self.request.GET.get('familia', None),
            }


        query_result =  VariableTypeModel.objects.order_by('cod_var')

        if query['cod_var'] and query['cod_var'] != '':
            query_result = query_result.filter(cod_var__icontains=query['cod_var'])

        if query['variable'] and query['variable'] != '':
            query_result = query_result.filter(variable__icontains=query['variable'])

        if query['tipo_variables'] and query['tipo_variables'] != '':
            query_result = query_result.filter(tipo_variables=query['tipo_variables'])

        if query['familia'] and query['familia'] != '':
            query_result = query_result.filter(familia__id=int(query['familia']))

        

        return query_result


class VariableTypeDetailView(LoginRequiredMixin, DetailView):
    model = VariableTypeModel
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable_type/variable_type_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable_type']
        context['active_menu'] ='arbolsaf'
        return context


class VariableTypeCreateView(LoginRequiredMixin, CreateView):
    model = VariableTypeModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable_type/variable_type_form.html'
    form_class = VariableTypeForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable_type']
        context['active_menu'] ='arbolsaf'

        return context

    def get_success_url(self):
        return reverse_lazy("arbolsaf:variable_type_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.created_by = self.request.user 
        farm.active=True
        farm.save()
        return super(VariableTypeCreateView, self).form_valid(form)
        #return HttpResponseRedirect(self.get_success_url())
    

class VariableTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = VariableTypeModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable_type/variable_type_form.html'
    form_class = VariableTypeForm
    
    def get_success_url(self):
        return reverse_lazy("arbolsaf:variable_type_detail", kwargs={"pk":self.object.id})   
    

    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.modified_by = self.request.user # use your own profile here
        farm.active=True
        farm.save()
        return super(VariableTypeUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable_type']
        context['active_menu'] ='arbolsaf'
        return context



@login_required(login_url='/login/')
def species_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id= query['id']
    print(id)
    period = SpeciesModel.objects.get(pk=id)
    try:
        period.delete()
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


