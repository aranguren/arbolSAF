from .views.species_views import *
from .views.variables_views import *
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

    path('variable/eliminar', variable_delete, name='variable_delete'),

]