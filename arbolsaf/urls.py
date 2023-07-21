from .views.species_views import *
from .views.variables_views import *
from .views.variable_type_views import *
from .views.reference_views import *
from .views.cross_table_views import *
from .views.tool_views import *
from .views.synonymous_views import sinonimo_delete, create_sinonimo, Synonymous2MCreateView
from django.urls import path 

app_name = 'arbolsaf'

urlpatterns = [
  
    path('especie/listado', SpeciesListView.as_view(),name='species_list'),
    path('especie/listado/json/', species_list_json ,name='species_list_json'),
    
    path('especie/detalles/<str:pk>', SpeciesDetailView.as_view(),name='species_detail'),
    path('especie/crear', SpeciesCreateView.as_view(),name='species_create'),
    path('especie/modificar/<str:pk>', SpeciesUpdateView.as_view(), name='species_update'),
    path('especie/eliminar', species_delete, name='species_delete'),
    
    path('especie/<int:pk>/variable', create_variable_o2m, name='species_create_variable'),
    path('especie/<int:pk>/variable/diligenciar/<int:tipo>/', create_variable_o2m, name='species_diligenciar_variable'),
    
    #path('especie/<int:pk>/variable', VariableO2MCreateView.as_view(), name='species_create_variable'),
    #path('especie/<int:pk>/variable/diligenciar/<int:tipo>/', VariableO2MCreateView.as_view(), name='species_diligenciar_variable'),

    path('especie/variable/modificar/<str:pk>', VariableO2MUpdateView.as_view(), name='species_update_variable'),
    path('especie/variable/detalles/<str:pk>', Variable2MDetailView.as_view(),name='species_detail_variable'),
    path('variable/tipo', variable_tipo_get, name='variable_tipo'),
    path('variable/eliminar', variable_delete, name='variable_delete'),
    path('variable/opciones/', variable_get_opciones, name='variable_get_opciones'),
    path('especie/<int:pk>/sinonimo', Synonymous2MCreateView.as_view(), name='species_create_synonymous'),
    path('sinonimo/eliminar', sinonimo_delete, name='sinonimo_delete'),
    path('sinonimo/crear', create_sinonimo, name='sinonimo_create'),

    path('tipos_variable/listado', VariableTypeListView.as_view(),name='variable_type_list'),
    path('tipos_variable/detalles/<str:pk>', VariableTypeDetailView.as_view(),name='variable_type_detail'),
    path('tipos_variable/crear', VariableTypeCreateView.as_view(),name='variable_type_create'),
    path('tipos_variable/modificar/<str:pk>', VariableTypeUpdateView.as_view(), name='variable_type_update'),
    path('tipos_variable/eliminar', variable_type_delete, name='variable_type_delete'),


    path('referencia/listado', ReferenceListView.as_view(),name='reference_list'),
    path('referencia/detalles/<str:pk>', ReferenceDetailView.as_view(),name='reference_detail'),
    path('referencia/crear', ReferenceCreateView.as_view(),name='reference_create'),
    path('referencia/modificar/<str:pk>', ReferenceUpdateView.as_view(), name='reference_update'),
    path('referencia/eliminar', reference_delete, name='reference_delete'),

    path('tabla_cruzada/listado', CrossTableListView.as_view(), name='cross_table_list'),
    path('tabla_cruzada/exportar', ExportCsvView.as_view(), name='cross_table_export'),


    path('variable-especie/listado', VariableSpeciesListView.as_view(), name='variable_species_list'),


    path('variable-especie/detalles/<str:pk>', VariableSpeciesDetailView.as_view(),name='variable_species_detail'),
    path('tabla_cruzada/detalles/<str:pk>', CrossTableDetailView.as_view(),name='cross_table_detail'),
    

    
    path('variable-especie/crear', create_variable_specie, name='variable_species_create'),
    path('variable-especie/modificar/<str:pk>', VariableSpeciesUpdateView.as_view(),name='variable_species_update'),

    path('herramienta/', ToolView.as_view(), name='tool_part1'),
    path('herramienta/intro/', IntroToolView.as_view(), name='tool_part0'),


]