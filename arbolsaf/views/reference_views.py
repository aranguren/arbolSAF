from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import RestrictedError
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db import connection
import json
from ..models import ReferenceModel
from ..forms import ReferenceForm




class ReferenceListView(LoginRequiredMixin, ListView):
    model = ReferenceModel
    template_name = 'arbolsaf/reference/reference_list.html'
    context_object_name = 'references'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(ReferenceListView, self).get_context_data(*args, **kwargs)

        context['segment'] = ['arbolsaf','reference']
        context['active_menu'] ='arbolsaf'




        if 'fuente_final' not in self.request.GET.keys():
            context['has_filters'] = False
        else:
            context['has_filters'] = True



        context['value_fuente_final'] = self.request.GET.get('fuente_final', '')
        context['value_cod_cita'] = self.request.GET.get('cod_cita', '')

        context['value_referencia'] = self.request.GET.get('referencia', '')

        filtrado = context['value_fuente_final'] + context['value_cod_cita'] + context['value_referencia']

        context['ordenar_por'] = self.request.GET.get('ordenar_por', 'cod_cita')

        context['has_filters'] = False

        if len(filtrado) > 0:
            context['has_filters'] = True

        if context['is_paginated']:
            list_pages = []

            first_range = self.request.GET.get('page', '1')
            actual_rows = round(int(first_range) * self.paginate_by)
            total_rows = len(ReferenceListView.get_queryset(self))

            context['count_actual_rows'] = total_rows if actual_rows > total_rows else actual_rows
            context['total_rows'] = total_rows

            if 'cod_cita' not in self.request.GET:
                for i in range(context['page_obj'].number, context['page_obj'].number + 5):
                    if i <= context['page_obj'].paginator.num_pages:
                        list_pages.append(i)
            else:
                first_range = self.request.GET.get('page', '1')

                if len(ReferenceListView.get_queryset(self)) % self.paginate_by == 0:
                    paginated = int(len(ReferenceListView.get_queryset(self)) / self.paginate_by)
                else:
                    paginated = int(len(ReferenceListView.get_queryset(self)) / self.paginate_by) + 1

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
            'fuente_final': self.request.GET.get('fuente_final', None),
            'cod_cita': self.request.GET.get('cod_cita', None),
            'referencia': self.request.GET.get('referencia', None),
            }


        tipos_de_orden = {
            'cod_cita': 'cod_cita',
            'cod_cita_dec': '-cod_cita',
            'cita': 'fuente_final',
            'cita_dec': '-fuente_final',

        }
        orden = self.request.GET.get('ordenar_por', 'nombre_comun')

        query_result =  ReferenceModel.objects


        if query['fuente_final'] and query['fuente_final'] != '':
            query_result = query_result.filter(fuente_final__icontains=query['fuente_final'])

        if query['cod_cita'] and query['cod_cita'] != '':
            query_result = query_result.filter(cod_cita__icontains=query['cod_cita'])

        if query['referencia'] and query['referencia'] != '':
            query_result = query_result.filter(referencia__icontains=query['referencia'])


        
        if orden in tipos_de_orden:
            query_result = query_result.order_by(tipos_de_orden[orden])
        else:
            query_result = query_result.order_by(tipos_de_orden['cod_cita'])


        return query_result


class ReferenceDetailView(LoginRequiredMixin, DetailView):
    model = ReferenceModel
    #group_required = [u'Auxiliar Legal', 'Jefe de la Oficina Local', 'Jefe de la RBRP']
    context_object_name = 'reference'
    template_name = 'arbolsaf/reference/reference_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','reference']
        context['active_menu'] ='arbolsaf'
        return context


class ReferenceCreateView(LoginRequiredMixin, CreateView):
    model = ReferenceModel
    context_object_name = 'reference'
    template_name = 'arbolsaf/reference/reference_form.html'
    form_class = ReferenceForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','reference']
        context['active_menu'] ='arbolsaf'

        return context

    def get_success_url(self):
        return reverse_lazy("arbolsaf:reference_detail", kwargs={"pk":self.object.id})   
    


    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.created_by = self.request.user 
        farm.active=True
        farm.save()
        return super(ReferenceCreateView, self).form_valid(form)
        #return HttpResponseRedirect(self.get_success_url())
    

class ReferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = ReferenceModel
    context_object_name = 'reference'
    template_name = 'arbolsaf/reference/reference_form.html'
    form_class = ReferenceForm
    
    def get_success_url(self):
        return reverse_lazy("arbolsaf:reference_detail", kwargs={"pk":self.object.id})   
    

    def form_valid(self, form):
        farm = form.save(commit=False)
        #User = get_user_model()

        farm.modified_by = self.request.user # use your own profile here
        farm.active=True
        farm.save()
        return super(ReferenceUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['segment'] = ['arbolsaf','reference']
        context['active_menu'] ='arbolsaf'
        return context



@login_required(login_url='/login/')
def reference_delete(request):
    resp = {}
    query = {'id': request.GET.get('id', None)}
    id= query['id']
    print(id)
    reference = ReferenceModel.objects.get(pk=id)
    try:
        reference.delete()
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



