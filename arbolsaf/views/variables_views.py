from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import json
from ..models import VariableModel, SpeciesModel, VariableTypeModel, VariableTypeOption, ReferenceModel
from ..forms import SpeciesForm, VariableO2MForm, VariableSpeciesForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

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
        if 'tipo' in self.kwargs:
            context['id_diligenciar'] = self.kwargs['tipo']
            nombre_variable_diligenciar = VariableTypeModel.objects.get(id=int(self.kwargs['tipo'])).variable
            context['nombre_variable_diligenciar'] = nombre_variable_diligenciar
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
        if specie.tipo_variable.tipo_variables == 'cualitativo':
            specie.valor_general = specie.valor_cualitativo.nombre
        elif specie.tipo_variable.tipo_variables == 'numerico': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'texto': 
            specie.valor_general = specie.valor_texto
        elif specie.tipo_variable.tipo_variables == 'rango': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'boolean': 
            specie.valor_general = "Verdadero" if specie.valor_boolean else "Falso"
         
        specie.save()
        return super(VariableO2MCreateView, self).form_valid(form)


class VariableO2MUpdateView(LoginRequiredMixin, UpdateView):
    model = VariableModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_o2m_form.html'
    form_class = VariableO2MForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        if self.object.chequeo:
            raise PermissionDenied()
             
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        context['specie_pk'] = self.object.especie.id
        redireccion = reverse_lazy("arbolsaf:species_detail", kwargs={"pk":self.object.especie.id})   
        context['species_url'] =  redireccion+'#variablessection'

        context['id_diligenciar'] = self.object.tipo_variable.id
        nombre_variable_diligenciar = VariableTypeModel.objects.get(id=int(self.object.tipo_variable.id)).variable
        context['nombre_variable_diligenciar'] = nombre_variable_diligenciar
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

        if specie.tipo_variable.tipo_variables == 'cualitativo':
            specie.valor_general = specie.valor_cualitativo.nombre
        elif specie.tipo_variable.tipo_variables == 'numerico': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'texto': 
            specie.valor_general = specie.valor_texto
        elif specie.tipo_variable.tipo_variables == 'rango': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'boolean': 
            specie.valor_general = "Verdadero" if specie.valor_boolean else "Falso"
         
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



@login_required(login_url='/login/')
def variable_tipo_get(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id= query['id']
    print(id)
    
    try:
        variable  = get_object_or_404(VariableTypeModel, pk=id)
        resp['tipo_variable']= variable.tipo_variables or 'desconocido'

    except Exception as e:
        resp['mensaje']= 'error'
        resp['error'] = json.dumps(e)
        return  JsonResponse(resp, status=404)
    
    
    print(resp)
    return  JsonResponse(resp, status=200)


@login_required(login_url='/login/')
def variable_get_opciones(request):
    resp = {}
    variable = int(request.GET.get('variable_id', 0)) if request.GET.get('variable_id', '0') !='' else 0 
  
    opciones = VariableTypeOption.objects.filter(tipo_variable__id=variable)
    lista_opciones= [{"id":opcion.id, "nombre":opcion.nombre} for opcion in opciones ]
    

    
    resp['mensaje'] = 'ok'
    resp['opciones'] = lista_opciones
    return JsonResponse(resp, status=200)


class VariableSpeciesListView(LoginRequiredMixin, ListView):
    model = VariableModel
    template_name = 'arbolsaf/variable/variable_species_list.html'
    context_object_name = 'variables_species'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(VariableSpeciesListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf', 'variable-species']
        context['active_menu'] = 'arbolsaf'

        context['value_nombre_comun'] = self.request.GET.get('nombre_comun', '')
        context['value_nombre_cientifico'] = self.request.GET.get('nombre_cientifico', '')
        context['value_tipo_variable'] = self.request.GET.get('tipo_variable', '')
        context['value_referencia'] = self.request.GET.get('referencia', '')

        filtrado = context['value_nombre_comun'] + context['value_nombre_cientifico'] + \
                   context['value_tipo_variable'] + context['value_referencia']

        print(len(filtrado))

        context['ordenar_por'] = self.request.GET.get('ordenar_por', 'nombre_comun')

        context['has_filters'] = False

        if len(filtrado) > 0:
            context['has_filters'] = True

        especies = SpeciesModel.objects.all()

        nombre_comun_values = list()
        for especie in especies.order_by('nombre_comun'):
            nombre_comun_values.append(especie.nombre_comun)

        context['nombre_comun_values'] = nombre_comun_values

        nombre_cientifico_values = list()
        for especie in especies.order_by('nombre_cientifico'):
            nombre_cientifico_values.append(especie.nombre_cientifico)

        context['nombre_cientifico_values'] = nombre_cientifico_values

        variables = VariableTypeModel.objects.order_by('variable')
        context['variables'] = variables

        referencias = ReferenceModel.objects.order_by('fuente_final')
        context['referencias'] = referencias

        if context['is_paginated']:
            list_pages = []

            first_range = self.request.GET.get('page', '1')
            actual_rows = round(int(first_range) * self.paginate_by)
            total_rows = len(VariableSpeciesListView.get_queryset(self))

            context['count_actual_rows'] = total_rows if actual_rows > total_rows else actual_rows
            context['total_rows'] = total_rows

            if 'nombre_comun' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:

                if len(VariableSpeciesListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(VariableSpeciesListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(VariableSpeciesListView.get_queryset(self)) / self.paginate_by) + 1

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
            'nombre_comun': self.request.GET.get('nombre_comun', None),
            'nombre_cientifico': self.request.GET.get('nombre_cientifico', None),
            'tipo_variable': self.request.GET.get('tipo_variable', None),
            'referencia': self.request.GET.get('referencia', None),
        }
        tipos_de_orden = {
            'nombre_comun': 'especie__nombre_comun',
            'nombre_comun_dec': '-especie__nombre_comun',
            'nombre_cientifico': 'especie__nombre_cientifico',
            'nombre_cientifico_dec': '-especie__nombre_cientifico',
            'tipo_variable': 'tipo_variable__tipo_variables',
            'tipo_variable_dec': '-tipo_variable__tipo_variables',
            'referencia': 'referencia__fuente_final',
            'referencia_dec': '-referencia__fuente_final',
            'valor': 'valor_general',
            'valor_dec': '-valor_general'

        }
        orden = self.request.GET.get('ordenar_por', 'nombre_comun')

        query_result = VariableModel.objects

        if query['nombre_comun'] and query['nombre_comun'] != '':
            query_result = query_result.filter(especie__nombre_comun__icontains=query['nombre_comun'])
        if query['nombre_cientifico'] and query['nombre_cientifico'] != '':
            query_result = query_result.filter(especie__nombre_cientifico__icontains=query['nombre_cientifico'])

        if query['tipo_variable'] and query['tipo_variable'] != '':
            tipo_variable = VariableTypeModel.objects.get(pk=int(query['tipo_variable']))
            query_result = query_result.filter(tipo_variable=tipo_variable)

        if query['referencia'] and query['referencia'] != '':
            referencia = ReferenceModel.objects.get(pk=int(query['referencia']))
            query_result = query_result.filter(referencia=referencia)

        if orden in tipos_de_orden:
            query_result = query_result.order_by(tipos_de_orden[orden])
        else:
            query_result = query_result.order_by(tipos_de_orden['nombre_comun'])

        return query_result


class VariableSpeciesDetailView(LoginRequiredMixin, DetailView):
    model = VariableModel
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_species_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable-species']
        context['active_menu'] ='arbolsaf'
        return context
    
class VariableSpeciesCreateView(LoginRequiredMixin, CreateView):
    model = VariableModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_species_form.html'
    form_class = VariableSpeciesForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable-species']
        context['active_menu'] ='arbolsaf'

        return context

    def get_success_url(self):
        return reverse_lazy("arbolsaf:variable_species_detail", kwargs={"pk":self.object.id})   
        #else:
        #   return reverse_lazy("ganaclima:period_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        specie = form.save(commit=False)
        #User = get_user_model()

        specie.created_by = self.request.user # use your own profile here
        if specie.tipo_variable.tipo_variables == 'cualitativo':
            specie.valor_general = specie.valor_cualitativo.nombre
        elif specie.tipo_variable.tipo_variables == 'numerico': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'texto': 
            specie.valor_general = specie.valor_texto
        elif specie.tipo_variable.tipo_variables == 'rango': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'boolean': 
            specie.valor_general = "Verdadero" if specie.valor_boolean else "Falso"
         
        specie.save()
        return super(VariableSpeciesCreateView, self).form_valid(form)
    



class VariableSpeciesUpdateView(LoginRequiredMixin, UpdateView):
    model = VariableModel
    context_object_name = 'variable'
    template_name = 'arbolsaf/variable/variable_species_form.html'
    form_class = VariableSpeciesForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','variable-species']
        context['active_menu'] ='arbolsaf'

        context['nombre_especie']  = self.object.especie
        context['nombre_variable']  = self.object.tipo_variable

        return context

    def get_success_url(self):
        return reverse_lazy("arbolsaf:variable_species_detail", kwargs={"pk":self.object.id})   
        #else:
        #    return reverse_lazy("ganaclima:period_detail", kwargs={"pk":self.object.id})   
    
    def form_valid(self, form):
        specie = form.save(commit=False)
        #User = get_user_model()

        specie.modified_by = self.request.user # use your own profile here
        #farm.active=True

        if specie.tipo_variable.tipo_variables == 'cualitativo':
            specie.valor_general = specie.valor_cualitativo.nombre
        elif specie.tipo_variable.tipo_variables == 'numerico': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'texto': 
            specie.valor_general = specie.valor_texto
        elif specie.tipo_variable.tipo_variables == 'rango': 
            specie.valor_general = f"{specie.rango_inferior}:{specie.rango_superior}"
        elif specie.tipo_variable.tipo_variables == 'boolean': 
            specie.valor_general = "Verdadero" if specie.valor_boolean else "Falso"
         
        specie.save()
        return super(VariableSpeciesUpdateView, self).form_valid(form)