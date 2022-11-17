from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from . import models

"""
class GenderSpecieResource(resources.ModelResource):
    class Meta:
        model = models.GenderSpecie


class GenderSpecieAdmin(ImportExportModelAdmin):
    resource_class = GenderSpecieResource
"""
class SynonymousInline(admin.TabularInline):
    model = models.SynonymousModel
    fields = ['sinonimo',]
    extra = 3 

class VariableInline(admin.TabularInline):
    model = models.VariableModel
    fields = ['nombre' ,
                'referencia', 
                'tipo_variable',            
                'cantidad', 
                'rango_superior', 
                'rango_inferior',
                'categoria']
    extra = 3 

class MenaceInline(admin.TabularInline):
    model = models.DistributionMenaceModel
    fields = ['nombre','tipo_variable']
    extra = 3 



class FamilyAdmin(admin.ModelAdmin):
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

admin.site.register(models.FamilyModel, FamilyAdmin)

class GenderAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
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


class MeasureUnitTypeAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['nombre', 'abreviatura']}),
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

admin.site.register(models.FunctiomModel, FunctionAdmin)


class VariableTypeResource(resources.ModelResource):
    class Meta:
        model = models.VariableTypeModel

class VariableTypeAdmin(ImportExportModelAdmin):
    resource_class = VariableTypeResource
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion tipo variable', {'fields': [ 'variable','cod_var', 'tipo_variables', 'unidad_medida',
                             'niveles_categoricos','descripcion', 
                            'min' ,'max',]}),
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]


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



class VariableAdmin(ImportExportModelAdmin):
    resource_class = VariableResource
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         ('Informacion variable', {'fields': [ 'nombre' ,
                                                'referencia', 
                                                'tipo_variable',            
                                                'cantidad', 
                                                'rango_superior', 
                                                'rango_inferior',
                                                'categoria', 
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


class SpeciesResource(resources.ModelResource):
    class Meta:
        model = models.SpeciesModel

class SpeciesAdmin(ImportExportModelAdmin):
    resource_class = SpeciesResource
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
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
         ('Informacion registro BD', {'fields': ['created','created_by','modified','modified_by']}),   
    ]


    inlines = [SynonymousInline, VariableInline, MenaceInline]

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

admin.site.register(models.PriorityModel, PriorityAdmin)


class ReferenceAdmin(admin.ModelAdmin):
    #fields = ['name', 'geom']
    #list_display = ('name','codigo','provincia','created','created_by','modified','modified_by')
    readonly_fields = ['created','created_by','modified','modified_by']
    fieldsets = [
        #(None,               {'fields': ['question_text']}),
         (None, {'fields': ['referencia','cod_cita','fuente_final']}),
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





 #inlines = [SynonymousInline,]

# TODO SynonymousModel, hacerlo cono inline de especie
# TODO referencia, hacerlo como inline de variable NO ES NECESARIO
# TODO DistributionMenaceModel tengo dudas
# TODO variables cono lista de especies
