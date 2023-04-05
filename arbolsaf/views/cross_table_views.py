import csv

from django.http import HttpResponse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import SpeciesModel, VariableTypeModel, ReferenceModel, VariableModel


class CrossTableListView(LoginRequiredMixin, ListView):
    model = SpeciesModel
    template_name = 'arbolsaf/cross_table/cross_table_list.html'
    context_object_name = 'cross_table'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(CrossTableListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf', 'cross_table']
        context['active_menu'] = 'arbolsaf'

        context['nombre_comun'] = self.request.GET.get('nombre_comun', '')

        if 'nombre_comun' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True

        variables = VariableTypeModel.objects.order_by('variable')
        context['variables'] = variables

        referencias = ReferenceModel.objects.order_by('fuente_final')
        context['referencias'] = referencias

        nombre_comun = SpeciesModel.objects.all()

        # context['value_cod_esp'] = self.request.GET.get('cod_esp', '')
        # context['value_taxonid_wfo'] = self.request.GET.get('taxonid_wfo', '')
        context['value_nombre_comun'] = self.request.GET.get('nombre_comun', '')
        context['value_nombre_cientifico'] = self.request.GET.get('nombre_cientifico', '')
        context['value_tipo_variable'] = self.request.GET.get('tipo_variable', '')
        context['value_referencia'] = self.request.GET.get('referencia', '')

        if context['is_paginated']:
            list_pages = []

            first_range = self.request.GET.get('page', '1')
            actual_rows = round(int(first_range) * self.paginate_by)
            total_rows = len(CrossTableListView.get_queryset(self))

            context['count_actual_rows'] = total_rows if actual_rows > total_rows else actual_rows
            context['total_rows'] = total_rows

            if 'nombre_comun' not in self.request.GET:
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

        return query_result


class ExportCsvView(LoginRequiredMixin, View):

    def get(self, request):
        query = {
            'nombre_comun': self.request.GET.get('nombre_comun', None),
            'nombre_cientifico': self.request.GET.get('nombre_cientifico', None),
            'tipo_variable': self.request.GET.get('tipo_variable', None),
            'referencia': self.request.GET.get('referencia', None),
        }
        print('OK')
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

        response = HttpResponse('text/csv')
        response['Content-Disposition'] = 'attachment; filename=tabla_cruzada.csv'
        writer = csv.writer(response)
        writer.writerow([])
        writer.writerow(['Nombre Común', 'Nombre Científico', 'Tipo de variable', 'Referencia', 'Valor'])
        # studs = students.values_list('id', 'roll', 'sclass', 'fname', 'lname')
        # for std in studs:
        #     writer.writerow(std)
        print(f"{query_result}")
        for item in query_result:
            especie = item.especie
            writer.writerow([especie.nombre_comun, especie.nombre_cientifico, item.tipo_variable,
                            item.referencia, item.valor_general])

        return response
