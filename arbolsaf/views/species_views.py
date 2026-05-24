from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.paginator import Paginator
import json
from ..models import SpeciesModel, VariableTypeModel, ReferenceModel
from ..forms import SpeciesForm
from ..permissions import GroupRequiredMixin, group_required
import subprocess
from django.shortcuts import render, redirect, get_object_or_404


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
        context['value_habilitada_herramienta'] = self.request.GET.get('habilitada_herramienta', '')
        context['value_sinonimos'] = self.request.GET.get('sinonimos', '')

        filtrado = context['value_cod_esp'] + context['value_nombre_comun'] + context['value_nombre_cientifico'] + \
                   context['value_tipo_variable'] + context['value_referencia'] + context['value_habilitada_herramienta'] + context['value_sinonimos'] 

 
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

        # ── Extra data per species for card display ──────────────────
        for specie in context['species']:
            endemismo = False
            amenaza_iucn = None
            amenaza_nacional = None
            primera_imagen = None

            for var in specie.variables.all():   # uses prefetch cache
                if not var.tipo_variable or not var.tipo_variable.cod_var:
                    continue
                cod = var.tipo_variable.cod_var.lower()
                if cod == 'v64':
                    endemismo = bool(var.valor_boolean)
                elif cod == 'v56':
                    quals = list(var.valores_cualitativos.all())
                    if quals:
                        amenaza_iucn = quals[0].nombre
                    elif var.valor_texto:
                        amenaza_iucn = var.valor_texto
                elif cod == 'v59':
                    quals = list(var.valores_cualitativos.all())
                    if quals:
                        amenaza_nacional = quals[0].nombre
                    elif var.valor_texto:
                        amenaza_nacional = var.valor_texto

            imgs = list(specie.imagenes.all())
            primera_imagen = imgs[0] if imgs else None

            specie.card_endemismo = endemismo
            specie.card_amenaza_iucn = amenaza_iucn
            specie.card_amenaza_nacional = amenaza_nacional
            specie.card_primera_imagen = primera_imagen

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
            'habilitada_herramienta': self.request.GET.get('habilitada_herramienta', None),
            'sinonimos': self.request.GET.get('sinonimos', None),

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
            'habilitada_herramienta': 'habilitada_herramienta',
            'habilitada_herramienta_dec': '-habilitada_herramienta',

        }
        orden = self.request.GET.get('ordenar_por', 'nombre_comun')


        query_result =  SpeciesModel.objects



           

        #if query['cod_esp'] and query['cod_esp'] != '':
        #    query_result = query_result.filter(cod_esp__icontains=query['cod_esp'])
        #if query['taxonid_wfo'] and query['taxonid_wfo'] != '':
        #    query_result = query_result.filter(taxonid_wfo__icontains=query['taxonid_wfo'])

        if query['sinonimos'] and query['sinonimos'] != '':
            query_result = query_result.filter(sinonimos__sinonimo__icontains=query['sinonimos'])

        if query['habilitada_herramienta'] and query['habilitada_herramienta'] != ''and  query['habilitada_herramienta']=='habilitada' :
            query_result = query_result.filter(habilitada_herramienta=True)
        elif query['habilitada_herramienta'] and query['habilitada_herramienta'] != ''and  query['habilitada_herramienta']=='desabilitada' :
            query_result = query_result.filter(habilitada_herramienta=False)

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

        return query_result.prefetch_related(
            'variables__tipo_variable',
            'variables__valores_cualitativos',
            'imagenes',
        )

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
    page_size = int(request.GET.get('page_size', 0))
    page_num  = int(request.GET.get('page', 1))

    if request.GET.get('todos', '0') == '1':
        qs = SpeciesModel.objects.all()
    else:
        qs = SpeciesModel.objects.filter(habilitada_herramienta=True)

    qs = qs.prefetch_related(
        'variables__tipo_variable',
        'variables__valores_cualitativos',
        'variables__referencia',
        'variables__referencia_2',
        'imagenes',
    ).order_by('pk')

    if page_size > 0:
        paginator = Paginator(qs, page_size)
        page_obj  = paginator.get_page(page_num)
        especies  = list(page_obj)
        has_next  = page_obj.has_next()
    else:
        especies = list(qs)
        has_next = False

    def qual_names(instance):
        if instance is None:
            return []
        return [v.nombre for v in instance.valores_cualitativos.all()]

    especies_dict_list = []
    for especie in especies:
        vars_by_cod = {
            var.tipo_variable.cod_var.lower(): var
            for var in especie.variables.all()
        }

        # Build refs dict: {cod_var: "Fuente 1 / Fuente 2"} — used for tooltips
        refs = {}
        for cod, var in vars_by_cod.items():
            parts = []
            if var.referencia_id and var.referencia:
                parts.append(var.referencia.fuente_final)
            if var.referencia_2_id and var.referencia_2:
                f2 = var.referencia_2.fuente_final
                if f2 not in parts:
                    parts.append(f2)
            if parts:
                refs[cod] = ' / '.join(parts)

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
            "IVIM": round(especie.ivim, 0),
        }

        v100 = vars_by_cod.get('v100')
        if v100:
            valores_especie['v100_temperatura_max'] = str(((v100.rango_inferior or 0.0) + (v100.rango_superior or 0.0)) / 2)
        else:
            valores_especie['v100_temperatura_max'] = ""

        v101 = vars_by_cod.get('v101')
        if v101:
            valores_especie['v101_temperatura_min'] = ((v101.rango_inferior or 0.0) + (v101.rango_superior or 0.0)) / 2
        else:
            valores_especie['v101_temperatura_min'] = ""

        v157 = vars_by_cod.get('v157')
        if v157:
            valores_especie['v157_elevacion_min'] = str(round(((v157.rango_inferior or 0) + (v157.rango_superior or 0)) / 2))
        else:
            valores_especie['v157_elevacion_min'] = ""

        v158 = vars_by_cod.get('v158')
        if v158:
            valores_especie['v158_elevacion_max'] = str(round(((v158.rango_inferior or 0) + (v158.rango_superior or 0)) / 2))
        else:
            valores_especie['v158_elevacion_max'] = ""

        nombres = qual_names(vars_by_cod.get('v161'))
        valores_especie['v161_tolerancia_condiciones'] = ','.join(nombres) if nombres else ""

        v81 = vars_by_cod.get('v81')
        if v81:
            valores_especie['v81_precipitacion_max'] = str(round(((v81.rango_inferior or 0) + (v81.rango_superior or 0)) / 2))
        else:
            valores_especie['v81_precipitacion_max'] = ""

        v82 = vars_by_cod.get('v82')
        if v82:
            valores_especie['v82_precipitacion_min'] = str(round(((v82.rango_inferior or 0.0) + (v82.rango_superior or 0.0)) / 2))
        else:
            valores_especie['v82_precipitacion_min'] = ""

        nombres = qual_names(vars_by_cod.get('v106'))
        valores_especie['v106_tipo_suelo_optimo'] = ','.join(nombres) if nombres else ""

        v108 = vars_by_cod.get('v108')
        valores_especie['v108_tolerancia_acidez'] = ("SI" if v108.valor_boolean else "NO") if v108 else ""

        v109 = vars_by_cod.get('v109')
        valores_especie['v109_tolerancia_salinidad'] = ("SI" if v109.valor_boolean else "NO") if v109 else ""

        v152 = vars_by_cod.get('v152')
        valores_especie['v152_desarrollo_suelos_rocosos'] = ("SI" if v152.valor_boolean else "NO") if v152 else ""

        v153 = vars_by_cod.get('v153')
        valores_especie['v153_desarrollo_suelos_drenados'] = ("SI" if v153.valor_boolean else "NO") if v153 else ""

        v159 = vars_by_cod.get('v159')
        if v159:
            valores_especie['v159_ph_max'] = str(((v159.rango_inferior or 0.0) + (v159.rango_superior or 0.0)) / 2)
        else:
            valores_especie['v159_ph_max'] = ""

        v160 = vars_by_cod.get('v160')
        if v160:
            valores_especie['v160_ph_min'] = str(((v160.rango_inferior or 0.0) + (v160.rango_superior or 0.0)) / 2)
        else:
            valores_especie['v160_ph_min'] = ""

        nombres_v68 = qual_names(vars_by_cod.get('v68'))
        valores_especie['v68_exigencia_suelos_fertiles'] = ','.join(nombres_v68) if nombres_v68 else ""

        nombres = qual_names(vars_by_cod.get('v83'))
        valores_especie['v83_preferencia_ph_suelo'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v281'))
        valores_especie['v281_pluviosidad'] = ','.join(nombres) if nombres else ""

        v1 = vars_by_cod.get('v1')
        if v1:
            valores_especie['v1_altura_copa'] = str(((v1.rango_inferior or 0.0) + (v1.rango_superior or 0.0)) / 2)
            valores_especie['v1_altura_min'] = str(v1.rango_inferior) if v1.rango_inferior is not None else ''
            valores_especie['v1_altura_max'] = str(v1.rango_superior) if v1.rango_superior is not None else ''
        else:
            valores_especie['v1_altura_copa'] = ""
            valores_especie['v1_altura_min'] = ''
            valores_especie['v1_altura_max'] = ''

        # Original code gated v118 on v68 names being non-empty (preserved as-is)
        nombres_v118 = qual_names(vars_by_cod.get('v118'))
        valores_especie['v118_tipo_raiz'] = ','.join(nombres_v118) if nombres_v68 else ""

        nombres = qual_names(vars_by_cod.get('v119'))
        valores_especie['v119_capacidad_regeneracion'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v13'))
        valores_especie['v13_tipo_ramificacion_copa'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v143'))
        valores_especie['v143_forma_corteza'] = ','.join(nombres) if nombres else ""

        v2 = vars_by_cod.get('v2')
        if v2:
            valores_especie['v2_ancho_potencial_copa'] = str(((v2.rango_inferior or 0.0) + (v2.rango_superior or 0.0)) / 2)
            valores_especie['v2_ancho_min'] = str(v2.rango_inferior) if v2.rango_inferior is not None else ''
            valores_especie['v2_ancho_max'] = str(v2.rango_superior) if v2.rango_superior is not None else ''
        else:
            valores_especie['v2_ancho_potencial_copa'] = ""
            valores_especie['v2_ancho_min'] = ''
            valores_especie['v2_ancho_max'] = ''

        nombres = qual_names(vars_by_cod.get('v37'))
        valores_especie['v37_fenologia_hojas'] = ','.join(nombres) if nombres else ""

        v5 = vars_by_cod.get('v5')
        if v5:
            valores_especie['v4_densidad_promedio_copa'] = str(round(((v5.rango_inferior or 0) + (v5.rango_superior or 0)) / 2))
        else:
            valores_especie['v4_densidad_promedio_copa'] = ""

        nombres = qual_names(vars_by_cod.get('v6'))
        valores_especie['v6_follage'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v7'))
        valores_especie['v7_forma_copa'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v73'))
        valores_especie['v73_gremio_ecologico'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v144'))
        valores_especie['v144_forma_fuste'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v9'))
        valores_especie['v9_frecuencia_poda'] = ','.join(nombres) if nombres else ""

        v35 = vars_by_cod.get('v35')
        if v35:
            nombres = qual_names(v35)
            if nombres:
                valores_especie['v35_epoca_caida_hojas'] = ','.join(nombres)
            elif v35.rango_inferior is not None and v35.rango_superior is not None:
                valores_especie['v35_epoca_caida_hojas'] = str(v35.rango_inferior) + '–' + str(v35.rango_superior)
            else:
                valores_especie['v35_epoca_caida_hojas'] = ''
        else:
            valores_especie['v35_epoca_caida_hojas'] = ''

        nombres = qual_names(vars_by_cod.get('v80'))
        valores_especie['v80_grupo_funcional'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v95'))
        valores_especie['v95_fertilidad'] = ','.join(nombres) if nombres else ""

        nombres = qual_names(vars_by_cod.get('v115'))
        valores_especie['v115_microorganismos'] = ','.join(nombres) if nombres else ""

        bool_vars_map = {
            'v167': 'v167_madera_muebles',
            'v163': 'v163_madera_construccion',
            'v168': 'v168_madera_postes',
            'v170': 'v170_fruta',
            'v130': 'v130_semilla_consumo',
            'v18':  'v18_abejas',
            'v89':  'v89_aves',
            'v90':  'v90_micromamiferos',
            'v116': 'v116_mejora_estructura',
            'v171': 'v171_nodulos',
            'v176': 'v176_mamiferos_mayores',
            'v91':  'v91_murcielagos',
            'v142': 'v142_carbon',
            'v162': 'v162_lena',
            'v39':  'v39_forraje',
            'v113': 'v113_medicinal',
            'v111': 'v111_artesanias',
            'v112': 'v112_cosmeticos',
            'v102': 'v102_tintes',
            'v70':  'v70_fibra',
        }
        for cod, key in bool_vars_map.items():
            instance = vars_by_cod.get(cod)
            valores_especie[key] = bool(instance.valor_boolean) if instance else False

        valores_especie['refs'] = refs
        valores_especie['imagenes'] = [img.imagen.url for img in especie.get_imagenes]
        valores_especie['nativa'] = bool(especie.nativa)

        v64 = vars_by_cod.get('v64')
        valores_especie['v64_endemismo'] = bool(v64.valor_boolean) if v64 else False

        v56 = vars_by_cod.get('v56')
        if v56:
            q56 = list(v56.valores_cualitativos.all())
            valores_especie['v56_amenaza_iucn'] = q56[0].nombre if q56 else (v56.valor_texto or '')
        else:
            valores_especie['v56_amenaza_iucn'] = ''

        v59 = vars_by_cod.get('v59')
        if v59:
            q59 = list(v59.valores_cualitativos.all())
            valores_especie['v59_amenaza_nacional'] = q59[0].nombre if q59 else (v59.valor_texto or '')
        else:
            valores_especie['v59_amenaza_nacional'] = ''

        # v175: cualitativo "categoría amenaza Perú" (sin cambio)
        v175_cual = next(
            (var for var in especie.variables.all()
             if var.tipo_variable.cod_var.lower() == 'v175'
             and var.tipo_variable.tipo_variables == 'cualitativo'),
            None
        )
        if v175_cual:
            q175 = list(v175_cual.valores_cualitativos.all())
            valores_especie['v175_amenaza_peru'] = q175[0].nombre if q175 else (v175_cual.valor_texto or '')
        else:
            valores_especie['v175_amenaza_peru'] = ''

        # v177: boolean "recurso para primates" (antes v175 boolean)
        v177 = next(
            (var for var in especie.variables.all()
             if var.tipo_variable.cod_var.lower() == 'v177'),
            None
        )
        valores_especie['v177_primates'] = bool(v177.valor_boolean) if v177 else False

        especies_dict_list.append(valores_especie)

    if page_size > 0:
        return JsonResponse({'especies': especies_dict_list, 'has_next': has_next}, status=200)
    return JsonResponse(especies_dict_list, status=200, safe=False)


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
       

class SpeciesActivateInToolView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        species = get_object_or_404(SpeciesModel, pk=pk)
        species.habilitada_herramienta = True
        species.save()
        redirection = reverse_lazy("arbolsaf:species_detail", kwargs={"pk": pk}) 
        return redirect(redirection)
    

class SpeciesDeactivateInToolView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # <view logic>

        species = get_object_or_404(SpeciesModel, pk=pk)
        species.habilitada_herramienta = False
        species.save()
        redirection = reverse_lazy("arbolsaf:species_detail", kwargs={"pk": pk}) 
        return redirect(redirection)
    
    





