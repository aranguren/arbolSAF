from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from computedfields.models import ComputedFieldsModel, computed, compute
# Create your models here.

class BasicAuditModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                related_name="+",
                verbose_name=_("Creado por"), 
                null=True,
                blank=False,
                on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                    related_name="+",
                    verbose_name=_("Modificado por"), 
                    null=True,
                    blank=False,
                    on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha creado"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("Fecha modificado"))
    #active = models.BooleanField(default=True, verbose_name=_("Activo"))

    class Meta:
        abstract = True

class SynonymousModel(BasicAuditModel):

    sinonimo = models.CharField(_("sinónimo"), max_length=255)
    especie = models.ForeignKey("arbolsaf.SpeciesModel", verbose_name=_("Especie"), 
                    related_name="sinonimos", on_delete=models.CASCADE)
    def __str__(self):
        return self.sinonimo

    class Meta:
        db_table = 'arbolsaf_synonymous'
        managed = True
        verbose_name = 'Sinónimo'
        verbose_name_plural = 'Sinónimo'

class FamilyModel(BasicAuditModel):

    familia = models.CharField(_("familia"), max_length=50)
    def __str__(self):
        return self.familia

    class Meta:
        db_table = 'arbolsaf_family'
        managed = True
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'

class GenderModel(BasicAuditModel):

    genero = models.CharField(_("género"), max_length=50)
    
    def __str__(self):
        return self.genero

    class Meta:
        db_table = 'arbolsaf_gender'
        managed = True
        verbose_name = 'Género'
        verbose_name_plural = 'Género'

class ReferenceModel(BasicAuditModel):

    fuente_final = models.CharField(_("Cita"), max_length=255)
    cod_cita = models.CharField(_("código cita"), max_length=50, unique=True)
    referencia = models.TextField(_("Fuente"), blank=True, null=True)

    def __str__(self):
        return self.fuente_final

    class Meta:
        db_table = 'arbolsaf_reference'
        managed = True
        verbose_name = 'Referencia'
        verbose_name_plural = 'Referencias'

class MeasureUnitTypeModel(BasicAuditModel):

    abreviatura = models.CharField(_("abreviatura"), max_length=50)
    nombre = models.CharField(_("nombre"), max_length=50, blank=True, null=True)

    

    def __str__(self):
        return self.abreviatura

    class Meta:
        db_table = 'arbolsaf_measure_unit_type'
        managed = True
        verbose_name = 'Tipo unidad de medidas'
        verbose_name_plural = 'Tipos unidad de medidas'

class FunctiomModel(BasicAuditModel):


    nombre = models.CharField(_("nombre"), max_length=50)

    

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'arbolsaf_function'
        managed = True
        verbose_name = 'Función'
        verbose_name_plural = 'Funciones'


class VariableTypeFamilyModel(BasicAuditModel):

    nombre = models.CharField(_("nombre"), max_length=50)
    descripcion = models.TextField(_("descripción"), blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'arbolsaf_variable_type_family'
        managed = True
        verbose_name = 'Grupo de variable'
        verbose_name_plural = 'Grupos de variables'

class VariableTypeModel(BasicAuditModel):

    TYPE_CHOICES = (
        ("numerico", "Numérico"),
        ("texto", "Texto"),
        ("rango", "Rango"),
        ("cualitativo", "Cualitativo"),
        ("boolean", "Boolean"),
    )
    seleccion_multiple = models.BooleanField(_("Es selección múltiple? (Aplicable solo a variables cualitativas)"), default=False)

    cod_var = models.CharField(_("código variable"), max_length=50)
    tipo_variables = models.CharField(_("tipo variable"), 
                    choices=TYPE_CHOICES, max_length=50, blank=True, null=True)
    
    unidad_medida =  models.ForeignKey("arbolsaf.MeasureUnitTypeModel", verbose_name=_("Unidad medida"), 
                on_delete=models.SET_NULL, blank=True, null=True)
    
    familia =  models.ForeignKey("arbolsaf.VariableTypeFamilyModel", verbose_name=_("Grupo"),
                on_delete=models.SET_NULL, blank=True, null=True)

                
    variable = models.CharField(_("variable"), max_length=255)
    niveles_categoricos = models.TextField(_("Niveles categóricos"))
    descripcion = models.TextField(_("descripción"), blank=True, null=True)    

    min = models.FloatField(_("Valor mínimo"), blank=True, null=True)
    max = models.FloatField(_("Valor máximo"), blank=True, null=True)

    def __str__(self):
        return self.variable

    class Meta:
        db_table = 'arbolsaf_variable_type'
        ordering = ["variable"]
        managed = True
        verbose_name = 'Tipo de variable'
        verbose_name_plural = 'Tipos de variable'


class VariableTypeOption(models.Model):

    def __str__(self):
        return self.nombre

    tipo_variable = models.ForeignKey("arbolsaf.VariableTypeModel", verbose_name=_("Tipo Variable"), 
                on_delete=models.RESTRICT) 
    
    nombre = models.CharField(_("Nombre"), max_length=50)

    class Meta:
        db_table = 'arbolsaf_variable_type_option'
        managed = True
        verbose_name = 'Opción Tipo Variable'
        verbose_name_plural = 'Opciones Tipo Variable'

class VariableModel(BasicAuditModel):


    referencia = models.ForeignKey("arbolsaf.ReferenceModel", verbose_name=_("Fuente"), 
                        on_delete=models.RESTRICT,  blank=True, null=True)
    referencia_2 = models.ForeignKey("arbolsaf.ReferenceModel", verbose_name=_("Repetir fuente"), 
                        on_delete=models.RESTRICT,  blank=True, null=True, related_name="+")
    tipo_variable = models.ForeignKey("arbolsaf.VariableTypeModel", verbose_name=_("Variable"), 
                    on_delete=models.RESTRICT)                    
    #nombre = models.CharField(_("nombre"), max_length=255)

    valor_numerico = models.FloatField(_("Valor numérico"), blank=True, null=True)
    rango_superior = models.FloatField(_("rango superior"), blank=True, null=True)
    rango_inferior = models.FloatField(_("rango inferior"), blank=True, null=True)
    valor_texto = models.CharField(_("Valor texto"), max_length=255, blank=True, null=True)
    valor_boolean = models.BooleanField(_("Verdadero?"), default=False, null=True)

    valor_general = models.CharField(_("Valor general"), max_length=255, blank=True, null=True)
    #valor_cualitativo = models.ForeignKey("arbolsaf.VariableTypeOption", verbose_name=_("Valor cualitativo"), 
    #                on_delete=models.RESTRICT, blank=True, null=True) 
    valores_cualitativos =   models.ManyToManyField("arbolsaf.VariableTypeOption", verbose_name=_("Valores cualitativos"), 
                                                    related_name="+", blank=True, null=True)
    #TODO averiguar si categoria puede ser una llave foranea

    #categoria = models.CharField(_("categoria"), max_length=50, blank=True, null=True)
    
    especie = models.ForeignKey("arbolsaf.SpeciesModel", related_name="variables", verbose_name=_("Especie"), on_delete=models.CASCADE)

    chequeo = models.BooleanField(_("Chequeada?"), default=False) 
    
    def __str__(self):
        return "{} - Especie: {}".format(self.tipo_variable, self.especie)
    
    @property
    def get_valor_general(self):
        if self.valor_general:
            valor = self.valor_general
        elif self.tipo_variable.tipo_variables == 'cualitativo':
            nombres=  [valor.nombre for valor in self.valores_cualitativos.all()]
            valor = ','.join(nombres)
        elif self.tipo_variable.tipo_variables == 'numerico': 
            valor = f"{self.rango_inferior}:{self.rango_superior}"
        elif self.tipo_variable.tipo_variables == 'texto': 
            valor = self.valor_texto
        elif self.tipo_variable.tipo_variables == 'rango': 
            valor = f"{self.rango_inferior}:{self.rango_superior}"
        elif self.tipo_variable.tipo_variables == 'boolean': 
            valor = "SI" if self.valor_boolean else "NO"
        return valor

    class Meta:
        db_table = 'arbolsaf_variable'
        managed = True
        verbose_name = 'Variable'
        verbose_name_plural = 'Variable'


class DistributionMenaceModel(BasicAuditModel):


    nombre = models.CharField(_("nombre"), max_length=50)

    tipo_variable = models.ForeignKey("arbolsaf.VariableTypeModel", verbose_name=_("Variable"), on_delete=models.RESTRICT)

    especie = models.ForeignKey("arbolsaf.SpeciesModel", verbose_name=_(""), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'arbolsaf_distribution_menace'
        managed = True
        verbose_name = 'Amenaza distribución'
        verbose_name_plural = 'Amenazas distribución'

class SpeciesModel(BasicAuditModel, ComputedFieldsModel):

    VALUES_CHOICES = (
        ("ninguno", "Ninguno"),
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
    )
        
    cod_esp = models.CharField(_("Código especie"), max_length=50, unique=True)
    taxonid_wfo = models.CharField(_("Taxon ID WFO"), max_length=50)
    nombre_comun = models.CharField(_("Nombre común"), max_length=255)
    nombre_cientifico = models.CharField(_("Nombre científico"), max_length=255)
    nombre_cientifico_completo = models.CharField(_("Nombre científico completo"), max_length=255)
    familia = models.ForeignKey("arbolsaf.FamilyModel", verbose_name=_("Familia"), on_delete=models.RESTRICT)
    genero = models.ForeignKey("arbolsaf.GenderModel", verbose_name=_("Género"), on_delete=models.RESTRICT)
    epiteto = models.CharField(_("Epíteto"), max_length=50)
    
    variedad_subespecie = models.CharField(_("Variedad/Subespecie"), max_length=50, blank=True, null=True)
    autor = models.CharField(_("Autor"), max_length=255, blank=True, null=True)

    nativa = models.BooleanField(_("Nativa?"))

    #campos calculados
    @computed(models.IntegerField(_("Valor para  Madera"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_madera(self):
        if len(self.get_variables)== 0:
            return 0
     
        v163 = 0
        v167 = 0
        v168 = 0

        v163_instance = self.variables.filter(tipo_variable__cod_var__iexact='v163').first()
        if v163_instance:
            v163 = 1 if v163_instance.valor_boolean else 0 
        else:
            v163 = 0

        v167_instance = self.variables.filter(tipo_variable__cod_var__iexact='v167').first()
        if v167_instance:
            v167 = 1 if v167_instance.valor_boolean else 0 
        else:
            v167 = 0 

        v168_instance = self.variables.filter(tipo_variable__cod_var__iexact='v168').first()
        if v168_instance:
            v168 = 1 if v167_instance.valor_boolean else 0 
        else:
            v168 = 0     


        
        return v163 + v167 + v168

    @computed(models.IntegerField(_("Valor para  Fruta"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_fruta(self):
        if len(self.get_variables)== 0:
            return 0
     
        v23_instance = self.variables.filter(tipo_variable__cod_var__iexact='v23').first()
        if v23_instance:
            v23 = 3 if v23_instance.valor_boolean else 0 
        else:
            v23 = 0

        return v23

    @computed(models.IntegerField(_("Valor para Otros usos"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_otros_usos(self):
        """ V102 V111 V112 V113 V162 V39 V70"""
        if len(self.get_variables)== 0:
            return 0
        

        #v102_instance = self.variables.filter(tipo_variable__cod_var__in=['V102', 'V111', 'V112', 'V113', 'V162', 'V39', 'V70']).first()


        v102_instance = self.variables.filter(tipo_variable__cod_var__iexact='v102').first()
        if v102_instance:
            v102 = 1 if v102_instance.valor_boolean else 0 
        else:
            v102 = 0

        v111_instance = self.variables.filter(tipo_variable__cod_var__iexact='v111').first()
        if v111_instance:
            v111 = 1 if v111_instance.valor_boolean else 0 
        else:
            v111 = 0

        v112_instance = self.variables.filter(tipo_variable__cod_var__iexact='v112').first()
        if v112_instance:
            v112 = 1 if v112_instance.valor_boolean else 0 
        else:
            v112 = 0

        v113_instance = self.variables.filter(tipo_variable__cod_var__iexact='v113').first()
        if v113_instance:
            v113 = 1 if v113_instance.valor_boolean else 0 
        else:
            v113 = 0

        v162_instance = self.variables.filter(tipo_variable__cod_var__iexact='v162').first()
        if v162_instance:
            v162 = 1 if v162_instance.valor_boolean else 0 
        else:
            v162 = 0

        v39_instance = self.variables.filter(tipo_variable__cod_var__iexact='v39').first()
        if v39_instance:
            v39 = 1 if v39_instance.valor_boolean else 0 
        else:
            v39 = 0


        v70_instance = self.variables.filter(tipo_variable__cod_var__iexact='v70').first()
        if v70_instance:
            v70 = 1 if v70_instance.valor_boolean else 0 
        else:
            v70 = 0

        return v102 + v111 + v112 + v113 +  v162 + v39 + v70
    
    @computed(models.IntegerField(_("Valor para Biodiversidad"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_biodiversidad(self):
        """V127	V14	V18	V89	V90	V91"""
        if len(self.get_variables)== 0:
            return 0
     

        v127_instance = self.variables.filter(tipo_variable__cod_var__iexact='v127').first()
        if v127_instance:
            v127 = 1 if v127_instance.valor_boolean else 0 
        else:
            v127 = 0

        v14_instance = self.variables.filter(tipo_variable__cod_var__iexact='v14').first()
        if v14_instance:
            v14 = 1 if v14_instance.valor_boolean else 0 
        else:
            v14 = 0
  
        v18_instance = self.variables.filter(tipo_variable__cod_var__iexact='v18').first()
        if v18_instance:
            v18 = 1 if v18_instance.valor_boolean else 0 
        else:
            v18 = 0

        v89_instance = self.variables.filter(tipo_variable__cod_var__iexact='v89').first()
        if v89_instance:
            v89 = 1 if v89_instance.valor_boolean else 0 
        else:
            v89 = 0

        v90_instance = self.variables.filter(tipo_variable__cod_var__iexact='v90').first()
        if v90_instance:
            v90 = 1 if v90_instance.valor_boolean else 0 
        else:
            v90 = 0

        v91_instance = self.variables.filter(tipo_variable__cod_var__iexact='v91').first()
        if v91_instance:
            v91 = 1 if v91_instance.valor_boolean else 0 
        else:
            v91 = 0
                                
        return v127 + v14 + v18 + v89 + v90 + v91

    @computed(models.IntegerField(_("Valor para Microclima"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_microclima(self):
        """V4 V58"""
        if len(self.get_variables)== 0:
            return 0
        
        v4_instance = self.variables.filter(tipo_variable__cod_var__iexact='v4').first()
        if v4_instance:
            v4 = 3 if v4_instance.valor_boolean else 0 
        else:
            v4 = 0

        v58_instance = self.variables.filter(tipo_variable__cod_var__iexact='v58').first()
        if v58_instance:
            v58 = 3 if v58_instance.valor_boolean else 0 
        else:
            v58 = 0
        
        return max(v4, v58)
    
    #TODO pendiente por definir esto
    @computed(models.IntegerField(_("Valor para el Suelo"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_suelo(self):
        """V4 V58"""
        if len(self.get_variables)== 0:
            return 0
    
        return 0
    

    @computed(models.CharField(_("Valor para Madera"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                depends=[('self', ['valor_madera'])])
    def valor_madera_category(self):

        match self.valor_madera:
            case 0:
                valor = 'ninguno' 
            case 1:
                valor = 'bajo'
            case 2:
                valor = 'medio'
            case 3:
                valor = 'alto'

        return valor

    @computed(models.CharField(_("Valor para Fruta"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_fruta'])])
    def valor_fruta_category(self):

        if self.valor_fruta==3:
            valor = 'alto' 
        else:
            valor = 'ninguno'

        return valor
    
    @computed(models.CharField(_("Valor para otros Usos"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_otros_usos'])])
    def valor_otros_usos_category(self):

        if self.valor_otros_usos==0:
            valor = 'ninguno' 
        elif self.valor_otros_usos<=2:
            valor = 'bajo'
        elif self.valor_otros_usos<=4:
            valor = 'medio'
        elif self.valor_otros_usos>=5:
            valor = 'alto'

        return valor

    @computed(models.CharField(_("Valor para Biodiversidad"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_biodiversidad'])])
    def valor_biodiversidad_category(self):

        if self.valor_biodiversidad==0:
            valor = 'ninguno' 
        elif self.valor_biodiversidad<=2:
            valor = 'bajo'
        elif self.valor_biodiversidad<=4:
            valor = 'medio'
        elif self.valor_biodiversidad>=5:
            valor = 'alto'

        return valor

    @computed(models.CharField(_("Valor para Microclima"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_microclima'])])
    def valor_microclima_category(self):

        if self.valor_microclima==3:
            valor = 'alto' 
        else:
            valor = 'ninguno'

        return valor

    @computed(models.CharField(_("Valor para Suelo"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                depends=[('self', ['valor_suelo'])])
    def valor_suelo_category(self):

        valor = 'ninguno'

        return valor
            
    @property
    def get_variables(self):
        return self.variables.all()

    @property
    def get_variables_no_diligenciadas(self):
        #variables = VariableTypeModel.objects.raw("""Select avt.id, avt.variable from arbolsaf_variable_type avt where avt.id not in 
        #        (select distinct av.tipo_variable_id from arbolsaf_variable av where av.especie_id=%s)
        #    """, [self.id])
        variables = VariableTypeModel.objects.all()
        return variables




    @property
    def get_sinonimos(self):
        return self.sinonimos.all()

        

    def __str__(self):
        return self.nombre_cientifico

    class Meta:
        db_table = 'arbolsaf_species'
        managed = True
        ordering = ["nombre_cientifico"]
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'

class PriorityModel(BasicAuditModel):


    prioridad = models.CharField(_("nombre"), max_length=50)
    especie = models.ForeignKey("arbolsaf.SpeciesModel", verbose_name=_("Especie"), on_delete=models.CASCADE)
    variable = models.ForeignKey("arbolsaf.VariableModel", verbose_name=_("Variable"), on_delete=models.CASCADE)
    referencia = models.ForeignKey("arbolsaf.ReferenceModel", verbose_name=_("Referencia"), on_delete=models.CASCADE)



    def __str__(self):
        return self.prioridad

    class Meta:
        db_table = 'arbolsaf_priority'
        managed = True
        verbose_name = 'Prioridad'
        verbose_name_plural = 'Prioridad'