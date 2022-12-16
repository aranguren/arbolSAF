from .views.species_views import *
from .views.variables_views import *
from .views.variable_type_views import *
from .views.synonymous_views import sinonimo_delete, create_sinonimo, Synonymous2MCreateView
from django.urls import path 

app_name = 'arbolsaf'

urlpatterns = [
    path('especie/listado', SpeciesListView.as_view(),name='species_list'),
    path('especie/detalles/<str:pk>', SpeciesDetailView.as_view(),name='species_detail'),
    path('especie/crear', SpeciesCreateView.as_view(),name='species_create'),
    path('especie/modificar/<str:pk>', SpeciesUpdateView.as_view(), name='species_update'),
    path('especie/eliminar', species_delete, name='species_delete'),
    
    path('especie/<int:pk>/variable', VariableO2MCreateView.as_view(), name='species_create_variable'),
    path('especie/variable/modificar/<str:pk>', VariableO2MUpdateView.as_view(), name='species_update_variable'),
    path('especie/variable/detalles/<str:pk>', Variable2MDetailView.as_view(),name='species_detail_variable'),
    path('variable/tipo', variable_tipo_get, name='variable_tipo'),
    path('variable/eliminar', variable_delete, name='variable_delete'),
    path('especie/<int:pk>/sinonimo', Synonymous2MCreateView.as_view(), name='species_create_synonymous'),
    path('sinonimo/eliminar', sinonimo_delete, name='sinonimo_delete'),
    path('sinonimo/crear', create_sinonimo, name='sinonimo_create'),

    path('tipos_variable/listado', VariableTypeListView.as_view(),name='variable_type_list'),
    path('tipos_variable/detalles/<str:pk>', VariableTypeDetailView.as_view(),name='variable_type_detail'),

    path('tipos_variable/crear', VariableTypeCreateView.as_view(),name='variable_type_create'),
    path('tipos_variable/modificar/<str:pk>', VariableTypeUpdateView.as_view(), name='variable_type_update'),
    

]