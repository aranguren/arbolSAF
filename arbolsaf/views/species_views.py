from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db import connection
import json
from ..models import SpeciesModel, VariableTypeModel, ReferenceModel
from ..forms import SpeciesForm
from ..permissions import GroupRequiredMixin, group_required
import subprocess




class SpeciesListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = SpeciesModel
    group_required = [u'visualizador', u'editor']
    template_name = 'arbolsaf/species/species_list.html'
    context_object_name = 'species'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(SpeciesListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'

        context['nombre_comun'] = self.request.GET.get('nombre_comun', '')

        #if 'nombre_comun' not in self.request.GET.keys():
        #    context['has_filters'] = False
        #else:
        #    context['has_filters'] = True



        variables =  VariableTypeModel.objects.order_by('variable')
        context['variables']=variables

        referencias =  ReferenceModel.objects.order_by('fuente_final')
        context['referencias']=referencias

        especies = SpeciesModel.objects.all()
        nombre_comun_values = list()
        for especie in especies.order_by('nombre_comun'):
            nombre_comun_values.append({"nombre_comun":especie.nombre_comun, "cod_esp":especie.cod_esp})
            #nombre_comun_values.append(f"{especie.nombre_comun} ({especie.cod_esp})")

        context['nombre_comun_values'] = nombre_comun_values

        nombre_cientifico_values = list()
        for especie in especies.order_by('nombre_cientifico'):
            nombre_cientifico_values.append({"nombre_cientifico":especie.nombre_cientifico, "cod_esp":especie.cod_esp}) 
            #nombre_cientifico_values.append(f"{especie.nombre_cientifico} ({especie.cod_esp})")

        context['nombre_cientifico_values'] = nombre_cientifico_values

        #context['value_cod_esp'] = self.request.GET.get('cod_esp', '')
        #context['value_taxonid_wfo'] = self.request.GET.get('taxonid_wfo', '')
        context['value_cod_esp'] = self.request.GET.get('cod_esp', '')
        
        context['value_nombre_comun'] = self.request.GET.get('nombre_comun', '')
        context['value_nombre_cientifico'] = self.request.GET.get('nombre_cientifico', '')
        context['value_tipo_variable'] = self.request.GET.get('tipo_variable', '')
        context['value_referencia'] = self.request.GET.get('referencia', '')

        filtrado = context['value_cod_esp'] + context['value_nombre_comun'] + context['value_nombre_cientifico'] + \
                   context['value_tipo_variable'] + context['value_referencia']

 
        context['ordenar_por'] = self.request.GET.get('ordenar_por', 'nombre_comun')

        context['has_filters'] = False

        if len(filtrado) > 0:
            context['has_filters'] = True

        

        if context['is_paginated']:
            list_pages = []

            first_range = self.request.GET.get('page', '1')
            actual_rows = round(int(first_range) * self.paginate_by)
            total_rows = len(SpeciesListView.get_queryset(self))

            context['count_actual_rows'] = total_rows if actual_rows > total_rows else actual_rows
            context['total_rows'] = total_rows

            if 'nombre_comun' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:

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

        query = {
            #'cod_esp': self.request.GET.get('cod_esp', None),
            #'taxonid_wfo': self.request.GET.get('taxonid_wfo', None),
            'cod_esp': self.request.GET.get('cod_esp', None),
            'nombre_comun': self.request.GET.get('nombre_comun', None),
            'nombre_cientifico': self.request.GET.get('nombre_cientifico', None),
            'tipo_variable': self.request.GET.get('tipo_variable', None),
            'referencia': self.request.GET.get('referencia', None),
            }

        tipos_de_orden = {
            'cod_esp': 'cod_esp',
            'cod_esp_dec': '-cod_esp',
            'nombre_comun': 'nombre_comun',
            'nombre_comun_dec': '-nombre_comun',
            'nombre_cientifico': 'nombre_cientifico',
            'nombre_cientifico_dec': '-nombre_cientifico',
            'familia': 'familia__familia',
            'familia_dec': '-familia__familia',
            'nativa_peru': 'nativa',
            'nativa_peru_dec': '-nativa',

        }
        orden = self.request.GET.get('ordenar_por', 'nombre_comun')


        query_result =  SpeciesModel.objects



           

        #if query['cod_esp'] and query['cod_esp'] != '':
        #    query_result = query_result.filter(cod_esp__icontains=query['cod_esp'])
        #if query['taxonid_wfo'] and query['taxonid_wfo'] != '':
        #    query_result = query_result.filter(taxonid_wfo__icontains=query['taxonid_wfo'])
        if query['cod_esp'] and query['cod_esp'] != '':
            query_result = query_result.filter(cod_esp__iexact=query['cod_esp'])
        if query['nombre_comun'] and query['nombre_comun'] != '':
            query_result = query_result.filter(nombre_comun__icontains=query['nombre_comun'])
        if query['nombre_cientifico'] and query['nombre_cientifico'] != '':
            query_result = query_result.filter(nombre_cientifico__icontains=query['nombre_cientifico'])
        
        if query['tipo_variable'] and query['tipo_variable'] != '':
            with connection.cursor() as cursor:
                
                cursor.execute(""" 
                    Select distinct as2.id from 
                    arbolsaf_species as2 join arbolsaf_variable av on(av.especie_id=as2.id)
                    join arbolsaf_variable_type avt on(avt.id=av.tipo_variable_id)
                    where avt.id={}
                """.format(int(query['tipo_variable'])))

                especies = cursor.fetchall()
                lista_variables = [x[0] for x in especies]
                query_result = query_result.filter(id__in=lista_variables)
        
        if query['referencia'] and query['referencia'] != '':
            with connection.cursor() as cursor:
                
                cursor.execute(""" 
                    Select distinct as2.id, as2.nombre_comun from arbolsaf_species as2 join arbolsaf_variable av on(av.especie_id=as2.id)
                    join arbolsaf_reference ar on (av.referencia_id= ar.id) 
                    where ar.id={}
                """.format(int(query['referencia'])))

                referencias = cursor.fetchall()
                lista_referencias = [x[0] for x in referencias]
                query_result = query_result.filter(id__in=lista_referencias)

        if orden in tipos_de_orden:
            query_result = query_result.order_by(tipos_de_orden[orden])
        else:
            query_result = query_result.order_by(tipos_de_orden['nombre_comun'])

        return query_result

class SpeciesDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = SpeciesModel
    group_required = [u'visualizador', u'editor']
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'specie'
    template_name = 'arbolsaf/species/species_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','species']
        context['active_menu'] ='arbolsaf'
        """
        Select avt.id, avt.variable from arbolsaf_variable_type avt where avt.id not in 
(select distinct av.tipo_variable_id from arbolsaf_variable av where av.especie_id=24)
        """
        return context

class SpeciesCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = SpeciesModel
    group_required = [u'editor']
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
        #("numerico", "Valor numérico"),
        #("texto", "Valor texto"),
        #("rango", "Rango"),
        #(#"cualitativo", "Cualitativo"),
        #("boolean", "Boolean"),

class SpeciesUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = SpeciesModel
    group_required = [u'editor']
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

@login_required(login_url='/login/')
@group_required('editor', raise_exception=True)
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




def species_list_json(request):
    resp = {}

    variables = VariableTypeModel.objects.all()
    especies = SpeciesModel.objects.all()
    especies_dict_list = []
    for especie in especies:
        valores_especie = {
        "CODIGO": especie.cod_esp,
        "NOMBRE COMUN": especie.nombre_comun or "",
        "NOMBRE CIENTIFICO": especie.nombre_cientifico or "",
        "VALOR MADERA": especie.valor_madera,
        "VALOR FRUTA": especie.valor_fruta,
        "VALOR OTROS USOS": especie.valor_otros_usos,
        "VALOR BIODIVERSIDAD": especie.valor_biodiversidad,
        "VALOR MICROCLIMA": especie.valor_microclima,
        "VALOR SUELO": especie.valor_suelo,
        "IVIM": round(especie.ivim, 0)
        }
        
        #temperatura máxima de su zona de distribución
        v100_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v100').first()
        if v100_instance:
            rango_inferior= v100_instance.rango_inferior or 0.0
            rango_superior= v100_instance.rango_superior or 0.0
            v100_temperatura_max_promedio = (rango_inferior+rango_superior)/2
            v100_temperatura_max =  str(v100_temperatura_max_promedio)
        else:
            v100_temperatura_max = ""
        valores_especie['v100_temperatura_max'] = v100_temperatura_max
        #temperatura mínima de su zona de distribución

        v101_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v101').first()
        if v101_instance:
            rango_inferior= v101_instance.rango_inferior or 0.0
            rango_superior= v101_instance.rango_superior or 0.0
            v101_temperatura_min_promedio = (rango_inferior+rango_superior)/2
            v101_temperatura_min = v101_temperatura_min_promedio
        else:
            v101_temperatura_min = ""
        valores_especie['v101_temperatura_min']=v101_temperatura_min

        v157_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v157').first()
        if v157_instance:
            rango_inferior= v157_instance.rango_inferior or 0.0
            rango_superior= v157_instance.rango_superior or 0.0
            v157_elevacion_min_promedio = (rango_inferior+rango_superior)/2
            v157_elevacion_min = str(v157_elevacion_min_promedio)
        else:
            v157_elevacion_min = ""
        valores_especie['v157_elevacion_min'] = v157_elevacion_min


        v158_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v158').first()
        if v158_instance:
            rango_inferior= v158_instance.rango_inferior or 0.0
            rango_superior= v158_instance.rango_superior or 0.0
            v158_elevacion_max_promedio = (rango_inferior+rango_superior)/2
            v158_elevacion_max = str(v158_elevacion_max_promedio)
        else:
            v158_elevacion_max = ""
        valores_especie['v158_elevacion_max'] = v158_elevacion_max

        v161_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v161').first()
        if v161_instance:
            valores = v161_instance.valores_cualitativos.all()
            nombres_valores_v161 = [valor.nombre for valor in valores]
            if len(nombres_valores_v161)>0:
                v161_tolerancia_condiciones = ','.join(nombres_valores_v161)
            else:
                v161_tolerancia_condiciones = ""
        else:
            v161_tolerancia_condiciones = ""
        valores_especie['v161_tolerancia_condiciones'] = v161_tolerancia_condiciones

        v81_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v81').first()
        if v81_instance:
            rango_inferior= v81_instance.rango_inferior or 0.0
            rango_superior= v81_instance.rango_superior or 0.0
            v81_precipitacion_max_promedio = (rango_inferior+rango_superior)/2
            v81_precipitacion_max= str(v81_precipitacion_max_promedio)
        else:
            v81_precipitacion_max = ""
        valores_especie['v81_precipitacion_max'] = v81_precipitacion_max

        v82_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v82').first()
        if v82_instance:
            rango_inferior= v82_instance.rango_inferior or 0.0
            rango_superior= v82_instance.rango_superior or 0.0
            v82_precipitacion_min_promedio = (rango_inferior+rango_superior)/2
            v82_precipitacion_min= str(v82_precipitacion_min_promedio)
        else:
            v82_precipitacion_min = ""
        valores_especie['v82_precipitacion_min'] = v82_precipitacion_min

        # PASO 3 SUELO

        #tipo de suelo óptimo/preferido
        v106_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v106').first()
        if v106_instance:
            valores = v106_instance.valores_cualitativos.all()
            nombres_valores_v106 = [valor.nombre for valor in valores]
            if len(nombres_valores_v106)>0:
                v106_tipo_suelo_optimo= ','.join(nombres_valores_v106)
            else:
                v106_tipo_suelo_optimo = ""
        else:
            v106_tipo_suelo_optimo = ""
        valores_especie['v106_tipo_suelo_optimo'] = v106_tipo_suelo_optimo

        #tolerancia a la acidéz del suelo
        v108_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v108').first()
        if v108_instance:
            v108_tolerancia_acidez = "SI" if v108_instance.valor_boolean else "NO"
        else:
            v108_tolerancia_acidez = ""
        valores_especie['v108_tolerancia_acidez'] = v108_tolerancia_acidez

        #tolerancia a la salinidad del suelo
        v109_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v109').first()
        if v109_instance:
            v109_tolerancia_salinidad = "SI" if v109_instance.valor_boolean else "NO"
        else:
            v109_tolerancia_salinidad = ""
        valores_especie['v109_tolerancia_salinidad'] = v109_tolerancia_salinidad

        #desarrollo en suelos rocosos

        v152_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v152').first()
        if v152_instance:
            v152_desarrollo_suelos_rocosos = "SI" if v152_instance.valor_boolean else "NO"
        else:
            v152_desarrollo_suelos_rocosos = ""
        valores_especie['v152_desarrollo_suelos_rocosos'] = v152_desarrollo_suelos_rocosos

        #desarrollo en suelos bien drenados

        v153_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v153').first()
        if v153_instance:
            v153_desarrollo_suelos_drenados = "SI" if v153_instance.valor_boolean else "NO"
        else:
            v153_desarrollo_suelos_drenados = ""
        valores_especie['v153_desarrollo_suelos_drenados'] = v153_desarrollo_suelos_drenados


        #pH de suelo máximo
        v159_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v159').first()
        if v159_instance:
            rango_inferior= v159_instance.rango_inferior or 0.0
            rango_superior= v159_instance.rango_superior or 0.0
            v159_ph_max_promedio = (rango_inferior+rango_superior)/2
            v159_ph_max= str(v159_ph_max_promedio)
        else:
            v159_ph_max = ""
        valores_especie['v159_ph_max'] = v159_ph_max

        #pH de suelo minimo
        v160_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v160').first()
        if v160_instance:
            rango_inferior= v160_instance.rango_inferior or 0.0
            rango_superior= v160_instance.rango_superior or 0.0
            v160_ph_min_promedio = (rango_inferior+rango_superior)/2
            v160_ph_min= str(v160_ph_min_promedio)
        else:
            v160_ph_min = ""
        valores_especie['v160_ph_min'] = v160_ph_min

        

        # exigencia de suelos fértiles
        v68_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v68').first()
        if v68_instance:
            valores = v68_instance.valores_cualitativos.all()
            nombres_valores_v68 = [valor.nombre for valor in valores]
            if len(nombres_valores_v68)>0:
                v68_exigencia_suelos_fertiles= ','.join(nombres_valores_v68)
            else:
                v68_exigencia_suelos_fertiles = ""
        else:
            v68_exigencia_suelos_fertiles = ""
        valores_especie['v68_exigencia_suelos_fertiles'] = v68_exigencia_suelos_fertiles

        # preferencia ph suelo

        v83_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v83').first()
        if v83_instance:
            valores = v83_instance.valores_cualitativos.all()
            nombres_valores_v83 = [valor.nombre for valor in valores]
            if len(nombres_valores_v83)>0:
                v83_preferencia_ph_suelo =  ','.join(nombres_valores_v83)
            else:
                v83_preferencia_ph_suelo = ""
        else:
            v83_preferencia_ph_suelo = ""
        valores_especie['v83_preferencia_ph_suelo'] = v83_preferencia_ph_suelo


        # PASO 4 ASOCIO

        # altura potencial de copa

        v1_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v1').first()
        if v1_instance:
            rango_inferior= v1_instance.rango_inferior or 0.0
            rango_superior= v1_instance.rango_superior or 0.0
            v1_altura_copa_promedio=(rango_inferior+rango_superior)/2
            v1_altura_copa= str(v1_altura_copa_promedio)
        else:
            v1_altura_copa = ""
        valores_especie['v1_altura_copa'] = v1_altura_copa

        # tipo raiz
        v118_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v118').first()
        if v118_instance:
            valores = v118_instance.valores_cualitativos.all()
            nombres_valores_v118 = [valor.nombre for valor in valores]
            if len(nombres_valores_v68)>0:
                v118_tipo_raiz= ','.join(nombres_valores_v118)
            else:
                v118_tipo_raiz = ""
        else:
            v118_tipo_raiz = ""
        valores_especie['v118_tipo_raiz'] = v118_tipo_raiz

        # capacidad de regeneración de ramas podadas
        v119_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v119').first()
        if v119_instance:
            valores = v119_instance.valores_cualitativos.all()
            nombres_valores_v119 = [valor.nombre for valor in valores]
            if len(nombres_valores_v119)>0:
                v119_capacidad_regeneracion= ','.join(nombres_valores_v119)
            else:
                v119_capacidad_regeneracion = ""
        else:
            v119_capacidad_regeneracion = ""
        valores_especie['v119_capacidad_regeneracion'] = v119_capacidad_regeneracion

        # tipo de ramificación de copa
        v13_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v13').first()
        if v13_instance:
            valores = v13_instance.valores_cualitativos.all()
            nombres_valores_v13 = [valor.nombre for valor in valores]
            if len(nombres_valores_v13)>0:
                v13_tipo_ramificacion_copa= ','.join(nombres_valores_v13)
            else:
                v13_tipo_ramificacion_copa = ""
        else:
            v13_tipo_ramificacion_copa = ""
        valores_especie['v13_tipo_ramificacion_copa'] = v13_tipo_ramificacion_copa

        # forma de corteza
        v143_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v143').first()
        if v143_instance:
            valores = v143_instance.valores_cualitativos.all()
            nombres_valores_v143 = [valor.nombre for valor in valores]
            if len(nombres_valores_v143)>0:
                v143_forma_corteza = ','.join(nombres_valores_v143)
            else:
                v143_forma_corteza = ""
        else:
            v143_forma_corteza = ""
        valores_especie['v143_forma_corteza'] = v143_forma_corteza


        #ancho potencial de copa

        v2_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v2').first()
        if v2_instance:
            rango_inferior= v2_instance.rango_inferior or 0.0
            rango_superior= v2_instance.rango_superior or 0.0
            v2_ancho_potencial_copa_promedio=(rango_inferior+rango_superior)/2
            v2_ancho_potencial_copa= str(v2_ancho_potencial_copa_promedio)
        else:
            v2_ancho_potencial_copa = ""
        valores_especie['v2_ancho_potencial_copa'] = v2_ancho_potencial_copa

        # fenología de las hojas

        v37_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v37').first()
        if v37_instance:
            valores = v37_instance.valores_cualitativos.all()
            nombres_valores_v37 = [valor.nombre for valor in valores]
            if len(nombres_valores_v37)>0:
                v37_fenologia_hojas = ','.join(nombres_valores_v37)
            else:
                v37_fenologia_hojas = ""
        else:
            v37_fenologia_hojas = ""
        valores_especie['v37_fenologia_hojas'] = v37_fenologia_hojas

        # densidad promedio de la copa

        v5_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v5').first()
        if v5_instance:
            rango_inferior= v5_instance.rango_inferior or 0.0
            rango_superior= v5_instance.rango_superior or 0.0
            v5_densidad_promedio_copa_promedio=(rango_inferior+rango_superior)/2
            v5_densidad_promedio_copa= str(v5_densidad_promedio_copa_promedio)
        else:
            v5_densidad_promedio_copa = ""
        valores_especie['v4_densidad_promedio_copa'] = v5_densidad_promedio_copa

        # follaje

        v6_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v6').first()
        if v6_instance:
            valores = v6_instance.valores_cualitativos.all()
            nombres_valores_v6 = [valor.nombre for valor in valores]
            if len(nombres_valores_v6)>0:
                v6_follage = ','.join(nombres_valores_v6)
            else:
                v6_follage = ""
        else:
            v6_follage = ""
        valores_especie['v6_follage'] = v6_follage

        # forma de la copa

        v7_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v7').first()
        if v7_instance:
            valores = v7_instance.valores_cualitativos.all()
            nombres_valores_v7 = [valor.nombre for valor in valores]
            if len(nombres_valores_v7)>0:
                v7_forma_copa = ','.join(nombres_valores_v7)
            else:
                v7_forma_copa = ""
        else:
            v7_forma_copa = ""
        valores_especie['v7_forma_copa'] = v7_forma_copa

        # gremio ecologico

        v73_instance = especie.variables.filter(tipo_variable__cod_var__iexact='v73').first()
        if v73_instance:
            valores = v73_instance.valores_cualitativos.all()
            nombres_valores_v73 = [valor.nombre for valor in valores]
            if len(nombres_valores_v73)>0:
                v73_gremio_ecologico = ','.join(nombres_valores_v73)
            else:
                v73_gremio_ecologico = ""
        else:
            v73_gremio_ecologico = ""
        valores_especie['v73_gremio_ecologico'] = v73_gremio_ecologico


        valores_especie['imagenes'] = [img.imagen.url for img in especie.get_imagenes]

        especies_dict_list.append(valores_especie)



    #resp = json.dumps(especies_dict_list)
    return  JsonResponse(especies_dict_list, status=200, safe=False)


class UpdateToolValuesView(View):
    #template_parcela ='agrimensuras/project_pdf_parcela.html' # the template 
    #template_lotificacion ='agrimensuras/project_pdf_lotificacion.html' 
    #template_header ='agrimensuras/project_pdf_header.html' 
    #template_footer ='agrimensuras/project_pdf_footer.html' 

    def post(self, request, **kw):


        result = subprocess.run(["python3", "manage.py", "updatedata"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        print(result.stderr.decode('ascii'))
        print(result.stdout.decode('ascii'))
        #return  JsonResponse( {'error':'internal server error'}, status=500, safe=False)
        return  JsonResponse( {'status':'ok'}, status=200, safe=False)
       
    





