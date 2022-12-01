from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
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

    referencia = models.CharField(_("referencia"), max_length=50)
    cod_cita = models.CharField(_("código cita"), max_length=50)
    fuente_final = models.CharField(_("fuente"), max_length=255)
    

    def __str__(self):
        return self.referencia

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


class VariableTypeModel(BasicAuditModel):

    TYPE_CHOICES = (
        ("numerico", "Valor numérico"),
        ("texto", "Valor texto"),
        ("rango", "Rango"),
        ("cualitativo", "Cualitativo"),
        ("boolean", "Boolean"),
    )


    cod_var = models.CharField(_("código variable"), max_length=50)
    tipo_variables = models.CharField(_("tipo variable"), 
                    choices=TYPE_CHOICES, max_length=50, blank=True, null=True)
    
    unidad_medida =  models.ForeignKey("arbolsaf.MeasureUnitTypeModel", verbose_name=_("Unidad medida"), 
                on_delete=models.CASCADE, blank=True, null=True)
    variable = models.CharField(_("variable"), max_length=255)
    niveles_categoricos = models.TextField(_("Niveles categóricos"))
    descripcion = models.TextField(_("descripción"))    

    min = models.FloatField(_("Valor mínimo"), blank=True, null=True)
    max = models.FloatField(_("Valor máximo"), blank=True, null=True)

    def __str__(self):
        return self.variable

    class Meta:
        db_table = 'arbolsaf_variable_type'
        managed = True
        verbose_name = 'Tipo de variable'
        verbose_name_plural = 'Tipos de variable'


class VariableModel(BasicAuditModel):


    referencia = models.ForeignKey("arbolsaf.ReferenceModel", verbose_name=_("Referencia"), 
                        on_delete=models.RESTRICT)
    tipo_variable = models.ForeignKey("arbolsaf.VariableTypeModel", verbose_name=_("Tipo Variable"), 
                    on_delete=models.RESTRICT)                    
    nombre = models.CharField(_("nombre"), max_length=50)

    cantidad = models.FloatField(_("Cantidad"), blank=True, null=True)
    rango_superior = models.FloatField(_("rango superior"), blank=True, null=True)
    rango_inferior = models.FloatField(_("rango inferior"), blank=True, null=True)
    #TODO averiguar si categoria puede ser una llave foranea

    categoria = models.CharField(_("categoria"), max_length=50)
    
    especie = models.ForeignKey("arbolsaf.SpeciesModel", related_name="variables", verbose_name=_("Especie"), on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

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

class SpeciesModel(BasicAuditModel):


    cod_esp = models.CharField(_("Código especie"), max_length=50)
    taxonid_wfo = models.CharField(_("Taxon ID WFO"), max_length=50)
    nombre_comun = models.CharField(_("Nombre comun"), max_length=255)
    nombre_cientifico = models.CharField(_("Nombre científico"), max_length=255)
    nombre_cientifico_completo = models.CharField(_("Nombre científico completo"), max_length=255)
    familia = models.ForeignKey("arbolsaf.FamilyModel", verbose_name=_("Familia"), on_delete=models.RESTRICT)
    genero = models.ForeignKey("arbolsaf.GenderModel", verbose_name=_("Género"), on_delete=models.RESTRICT)
    epiteto = models.CharField(_("Epíteto"), max_length=50)
    
    variedad_subespecie = models.CharField(_("Variedad/Subespecie"), max_length=50, blank=True, null=True)
    autor = models.CharField(_("Autor"), max_length=255, blank=True, null=True)

    nativa = models.BooleanField(_("Nativa?"))

    @property
    def get_variables(self):
        return self.variables.all()

    @property
    def get_sinonimos(self):
        return self.sinonimos.all()

        

    def __str__(self):
        return self.nombre_comun

    class Meta:
        db_table = 'arbolsaf_species'
        managed = True
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