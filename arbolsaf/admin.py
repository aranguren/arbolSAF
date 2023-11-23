from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin, ExportMixin
# Register your models here.

from . import models

"""
class GenderSpecieResource(resources.ModelResource):
    class Meta:
        model = models.GenderSpecie


class GenderSpecieAdmin(ImportExportModelAdmin):
    resource_class = GenderSpecieResource
"""
class SynonymousResource(resources.ModelResource):
    class Meta:
        model = models.SynonymousModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('sinonimo','especie',)

class SynonymousAdmin(ImportExportModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    resource_classes = [SynonymousResource]
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['sinonimo','especie']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.SynonymousModel, SynonymousAdmin)

class SynonymousInline(admin.TabularInline):
    model = models.SynonymousModel
    fields = ['sinonimo',]
    extra = 3 

class VariableInline(admin.StackedInline):
    model = models.VariableModel
    fields = [
                'referencia', 
                'tipo_variable',            
                'valor_numerico', 
                'valor_texto',
                'rango_superior', 
                'rango_inferior',
                'valor_boolean'
               ]
    extra = 1 

class MenaceInline(admin.TabularInline):
    model = models.DistributionMenaceModel
    fields = ['nombre','tipo_variable']
    extra = 3 

class FamilyResource(resources.ModelResource):
    class Meta:
        model = models.FamilyModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('familia',)

class FamilyAdmin(ImportExportModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    resource_classes = [FamilyResource]
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['familia',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.FamilyModel, FamilyAdmin)


class GenderResource(resources.ModelResource):
    class Meta:
        model = models.GenderModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('genero',)

class GenderAdmin(ImportExportModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    resource_classes = [GenderResource]
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['genero',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.GenderModel, GenderAdmin)


class MeasureUnitTypeResource(resources.ModelResource):
    class Meta:
        model = models.MeasureUnitTypeModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('abreviatura',)

class MeasureUnitTypeAdmin(ImportExportModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    resource_classes = [MeasureUnitTypeResource]
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['abreviatura', 'nombre' ]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.MeasureUnitTypeModel, MeasureUnitTypeAdmin)


class FunctionAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['nombre',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

#admin.site.register(models.FunctiomModel, FunctionAdmin)



class VariableTypeFamilyAdmin(admin.ModelAdmin):

    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['nombre','descripcion']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.VariableTypeFamilyModel, VariableTypeFamilyAdmin)

class VariableTypeResource(resources.ModelResource):
    class Meta:
        model = models.VariableTypeModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('cod_var',)

class VariableTypeOptionInline(admin.TabularInline):
    model = models.VariableTypeOption
    fields = ['nombre',]
    extra = 3 

class VariableTypeAdmin(ImportExportModelAdmin):
    resource_classes = [VariableTypeResource]
    search_fields = ['cod_var', 'variable']
    #fields = ['name', 'geom']
    list_display = ('cod_var', 'variable', 'tipo_variables','familia', 'unidad_medida',)
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion tipo variable', {'fields': [ 'variable','cod_var', 'familia', 'tipo_variables', 'seleccion_multiple',
                             'unidad_medida',
                             'niveles_categoricos','descripcion', 
                            'min' ,'max',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]

    inlines = [VariableTypeOptionInline,]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.VariableTypeModel, VariableTypeAdmin)

class VariableResource(resources.ModelResource):
    class Meta:
        model = models.VariableModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        #import_id_fields = ('nombre',)



class VariableAdmin(ImportExportModelAdmin):
    resource_classes = [VariableResource]
    #fields = ['name', 'geom']
    list_display = ('id', 'tipo_variable', 'especie', 'referencia', 'valor_general')
    search_fields = ['id', 'valor_general']
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion variable', {'fields': [ 
                                                'referencia', 
                                                'tipo_variable',            
                                                'valor_numerico', 
                                                'valor_texto',
                                                'rango_superior', 
                                                'rango_inferior',
                                                'valor_boolean',
                                                'valor_general',
                                                'chequeo',
                                                'especie' ,]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]


    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.VariableModel, VariableAdmin)


class ImageSpeciesInline(admin.TabularInline):
    model = models.ImageSpecies
    fields = ['descripcion','imagen']
    extra = 5 

class SpeciesResource(resources.ModelResource):
    class Meta:
        model = models.SpeciesModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('cod_esp',)

class SpeciesAdmin(ImportExportModelAdmin):
    resource_classes = [SpeciesResource]
    search_fields = ['cod_esp', 'nombre_comun', 'nombre_cientifico']
    list_display = ['cod_esp', 'nombre_comun', 'nombre_cientifico', 'familia', 
                                        'genero',]
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by','valor_madera', 
                                        'valor_madera_category' ,
                                        'valor_fruta', 
                                        'valor_fruta_category',
                                        'valor_otros_usos', 
                                        'valor_otros_usos_category', 
                                        'valor_biodiversidad',
                                        'valor_biodiversidad_category' ,
                                        'valor_microclima' ,
                                        'valor_microclima_category', 
                                        'valor_suelo' ,
                                        'valor_suelo_category', 
                                        'indice_multiuso',
                                        'indice_valor_uso_relativo',
                                        'ivim'
                                        ]
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion variable', {'fields': [
                                        'habilitada_herramienta',
                                        'cod_esp', 
                                        'taxonid_wfo' ,
                                        'nombre_comun', 
                                        'nombre_cientifico',
                                        'nombre_cientifico_completo', 
                                        'familia', 
                                        'genero',
                                        'epiteto' ,
                                        'variedad_subespecie' ,
                                        'autor', 
                                        'nativa', ]}),
        ('Valores índices', {'fields': ['valor_madera', 
                                        'valor_madera_category' ,
                                        'valor_fruta', 
                                        'valor_fruta_category',
                                        'valor_otros_usos', 
                                        'valor_otros_usos_category', 
                                        'valor_biodiversidad',
                                        'valor_biodiversidad_category' ,
                                        'valor_microclima' ,
                                        'valor_microclima_category', 
                                        'valor_suelo' ,
                                        'valor_suelo_category', 
                                        'indice_multiuso',
                                        'indice_valor_uso_relativo',
                                        'ivim',
                                        ]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]


    inlines = [SynonymousInline, ImageSpeciesInline]

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.SpeciesModel, SpeciesAdmin)


class PriorityAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['familia',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

#admin.site.register(models.PriorityModel, PriorityAdmin)


class ReferenceResource(resources.ModelResource):
    class Meta:
        model = models.ReferenceModel
        skip_unchanged = True
        report_skipped = True
        exclude = ('created','created_by','modified','modified_by',)
        import_id_fields = ('cod_cita',)

class ReferenceAdmin(ImportExportModelAdmin):
    resource_classes = [ReferenceResource]
    #fields = ['name', 'geom']
    list_display = ('cod_cita','fuente_final', 'referencia')
    search_fields = ['cod_cita','fuente_final', 'referencia']
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['cod_cita','fuente_final', 'referencia']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.ReferenceModel, ReferenceAdmin)


class VariableTypeOptionAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('nombre','tipo_variable')
    
    fields = [
       'tipo_variable', 'nombre'  
    ]


admin.site.register(models.VariableTypeOption, VariableTypeOptionAdmin)

class BitacoraAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    list_display = ('entidad_modificada','codigo_especie','codigo_variable','asunto','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['entidad_modificada','codigo_especie', 'codigo_variable', 'asunto', 'descripcion_cambio']}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.Bitacora, BitacoraAdmin)



class SpeciesExportResource(resources.ModelResource):
    class Meta:
        model = models.SpeciesModel
        skip_unchanged = True
        report_skipped = True
        fields = ('cod_esp', 'nombre_comun', 'nombre_cientifico', 
                                        'valor_madera', 
                                        'valor_fruta', 
                                        'valor_otros_usos', 
                                        'valor_biodiversidad',
                                        'valor_microclima' ,
                                        'valor_suelo' ,
                                        'indice_multiuso',
                                        'ivim',)
        import_id_fields = ('cod_esp',)

class CategorizacionAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [SpeciesExportResource]
    search_fields = ['cod_esp', 'nombre_comun', 'nombre_cientifico']
    list_display = ['cod_esp', 'nombre_comun', 'nombre_cientifico', 
                                        'valor_madera', 
                                        'valor_fruta', 
                                        'valor_otros_usos', 
                                        'valor_biodiversidad',
                                        'valor_microclima' ,
                                        'valor_suelo' ,
                                        'indice_multiuso',
                                        'indice_valor_uso_relativo',
                                        'ivim',]
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by','valor_madera', 
                                        'valor_madera_category' ,
                                        'valor_fruta', 
                                        'valor_fruta_category',
                                        'valor_otros_usos', 
                                        'valor_otros_usos_category', 
                                        'valor_biodiversidad',
                                        'valor_biodiversidad_category' ,
                                        'valor_microclima' ,
                                        'valor_microclima_category', 
                                        'valor_suelo' ,
                                        'valor_suelo_category', 
                                        'indice_multiuso',
                                        'indice_valor_uso_relativo',
                                        'ivim'
                                        ]
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion variable', {'fields': ['cod_esp', 
                                        'taxonid_wfo' ,
                                        'nombre_comun', 
                                        'nombre_cientifico',
                                        'nombre_cientifico_completo', 
                                        'familia', 
                                        'genero',
                                        'epiteto' ,
                                        'variedad_subespecie' ,
                                        'autor', 
                                        'nativa', ]}),
        ('Valores índices', {'fields': ['valor_madera', 
                                        'valor_madera_category' ,
                                        'valor_fruta', 
                                        'valor_fruta_category',
                                        'valor_otros_usos', 
                                        'valor_otros_usos_category', 
                                        'valor_biodiversidad',
                                        'valor_biodiversidad_category' ,
                                        'valor_microclima' ,
                                        'valor_microclima_category', 
                                        'valor_suelo' ,
                                        'valor_suelo_category', 
                                        'indice_multiuso',
                                        'indice_valor_uso_relativo',
                                        'ivim',
                                        ]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]
    def has_delete_permission(self, request, obj = None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_add_permission(self, request, obj = None):
        return False


admin.site.register(models.SpeciesAdminModel, CategorizacionAdmin)



class SpeciesModelInline(admin.TabularInline):
    model =  model = models.RegistroReporteHerramienta.especies.through
    model._meta.verbose_name_plural = "Especies seleccionadas"
    model._meta.verbose_name = "Especie seleccionada"
    

    #fields = ['cod_esp','nombre_cientifico','nombre_comun']
  

class RegistroReporteHerramientaResource(resources.ModelResource):
    class Meta:
        model = models.RegistroReporteHerramienta
        
        skip_unchanged = True
        report_skipped = True
        fields = ('created', 'nombre_productor', 'region', 
                                        'provincia', 
                                        'distrito', 
                                        'tipo_intervencion', 
                                        'finca_ha',
                                        'parcela_ha' ,
                                        'tipo_usuario' ,
                                        'identidad_genero',
                                        'edad_usuario',
                                        'especies_str')
        import_id_fields = ('nombre_productor','created')

class RegistroReporteHerramientaAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [RegistroReporteHerramientaResource]
    search_fields = ['cod_esp', 'nombre_comun', 'nombre_cientifico']
    list_display = ['nombre_productor','created', 'region', 
                                        'provincia', 
                                        'distrito', ]

    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion registro', {'fields': ['created', 'nombre_productor', 'region', 
                                        'provincia', 
                                        'distrito', 
                                        'tipo_intervencion', 
                                        'finca_ha',
                                        'parcela_ha' ,
                                        'tipo_usuario' ,
                                        'identidad_genero',
                                        'edad_usuario',
                                        'especies_str' ]}),
    ]
    inlines = [SpeciesModelInline,]
    readonly_fields=['created',]
    #def has_delete_permission(self, request, obj = None):
    #    return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_add_permission(self, request, obj = None):
        return False


admin.site.register(models.RegistroReporteHerramienta, RegistroReporteHerramientaAdmin)