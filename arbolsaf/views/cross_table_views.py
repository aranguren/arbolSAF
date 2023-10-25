import csv

from django.http import HttpResponse
from django.views.generic import ListView, View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import SpeciesModel, VariableTypeModel, ReferenceModel, VariableModel
from ..forms import VariableSpeciesForm
from django.urls import reverse_lazy
from ..permissions import GroupRequiredMixin, group_required


class CrossTableListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = SpeciesModel
    group_required = [u'visualizador', u'editor']
    template_name = 'arbolsaf/cross_table/cross_table_list.html'
    context_object_name = 'cross_table'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(CrossTableListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf', 'cross_table']
        context['active_menu'] = 'arbolsaf'

        context['nombre_comun'] = self.request.GET.get('nombre_comun', '')
        context['value_nombre_comun'] = self.request.GET.get('nombre_comun', '')
        context['value_nombre_cientifico'] = self.request.GET.get('nombre_cientifico', '')
        context['value_tipo_variable'] = self.request.GET.get('tipo_variable', '')
        context['value_referencia'] = self.request.GET.get('referencia', '')
        context['value_cod_var'] = self.request.GET.get('cod_var', '')
        context['value_cod_esp'] = self.request.GET.get('cod_esp', '')

        
        
        filtrado = context['nombre_comun'] + context['value_nombre_comun'] + context['value_nombre_cientifico'] + \
                   context['value_tipo_variable'] + context['value_referencia'] +  context['value_cod_var'] + context['value_cod_esp']

        print(len(filtrado))

        context['ordenar_por'] = self.request.GET.get('ordenar_por', 'nombre_comun')

        context['has_filters'] = False

        if len(filtrado) > 0:
            context['has_filters'] = True

        especies = SpeciesModel.objects.all()

        #nombre_comun_values = list()
        #for especie in especies.order_by('nombre_comun'):
        #    nombre_comun_values.append(f"{especie.nombre_comun} ({especie.cod_esp})")

        #context['nombre_comun_values'] = nombre_comun_values

        nombre_cientifico_values = list()
        for especie in especies.order_by('nombre_cientifico'):
            nombre_cientifico_values.append({"nombre_cientifico":especie.nombre_cientifico,"cod_esp":especie.cod_esp})

        context['nombre_cientifico_values'] = nombre_cientifico_values

        
        variables = VariableTypeModel.objects.order_by('variable')
        context['variables'] = variables

        referencias = ReferenceModel.objects.order_by('fuente_final')
        context['referencias'] = referencias

        if context['is_paginated']:
            list_pages = []

            first_range = self.request.GET.get('page', '1')
            actual_rows = round(int(first_range) * self.paginate_by)
            total_rows = len(CrossTableListView.get_queryset(self))

            context['count_actual_rows'] = total_rows if actual_rows > total_rows else actual_rows
            context['total_rows'] = total_rows

            if 'nombre_cientifico' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:

                if len(CrossTableListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(CrossTableListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(CrossTableListView.get_queryset(self)) / self.paginate_by) + 1

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
            #'nombre_comun': self.request.GET.get('nombre_comun', None),
            'cod_var': self.request.GET.get('cod_var', None),
            'cod_esp': self.request.GET.get('cod_esp', None),
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

        #if query['nombre_comun'] and query['nombre_comun'] != '':
        #    query_result = query_result.filter(especie__nombre_comun__icontains=query['nombre_comun'])
        if query['nombre_cientifico'] and query['nombre_cientifico'] != '':
            query_result = query_result.filter(especie__nombre_cientifico__icontains=query['nombre_cientifico'])
        
        if query['cod_var'] and query['cod_var'] != '':
            query_result = query_result.filter(tipo_variable__cod_var__iexact=query['cod_var'])
        if query['cod_esp'] and query['cod_esp'] != '':
            query_result = query_result.filter(especie__cod_esp__iexact=query['cod_esp'])

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


class ExportCsvView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = [u'visualizador', u'editor']

    def get(self, request):
        query = {
            'nombre_comun': self.request.GET.get('nombre_comun', None),
            'nombre_cientifico': self.request.GET.get('nombre_cientifico', None),
            'tipo_variable': self.request.GET.get('tipo_variable', None),
            'referencia': self.request.GET.get('referencia', None),
        }

        query_result = VariableModel.objects.order_by('especie__nombre_comun')

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

        #response = HttpResponse('text/csv')
        #response['Content-Disposition'] = 'attachment; filename=tabla_cruzada.csv'

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="tabla_cruzada.csv"'},
            )
        
        writer = csv.writer(response)
        writer.writerow(['ID','Código especie','Nombre Común', 'Nombre Científico','Código Variable', 'Tipo de variable', 'Código referencia', 'Referencia', 'Valor'])

        for item in query_result:

            
            especie = item.especie
            valor=False
            if item.tipo_variable.tipo_variables == 'cualitativo':
                nombres=  [valor.nombre for valor in item.valores_cualitativos.all()]
                valor = ','.join(nombres)
            elif item.tipo_variable.tipo_variables == 'numerico': 
                valor = f"{item.rango_inferior};{item.rango_superior}"
            elif item.tipo_variable.tipo_variables == 'texto': 
                valor = item.valor_texto
            elif item.tipo_variable.tipo_variables == 'rango': 
                valor = f"{item.rango_inferior};{item.rango_superior}"
            elif item.tipo_variable.tipo_variables == 'boolean': 
                valor = "SI" if item.valor_boolean else "NO"
            else:
                valor = item.valor_general or ""
            
            if not valor or valor=='':
                valor = item.valor_general or ""


            valor_general = valor

            writer.writerow([item.id, especie.cod_esp, especie.nombre_comun, especie.nombre_cientifico, item.tipo_variable.cod_var, item.tipo_variable,
                            item.referencia.cod_cita, item.referencia, valor_general])

        return response

