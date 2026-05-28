from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from computedfields.models import ComputedFieldsModel, computed, compute
import urllib.parse
from django.core.cache import cache
from ckeditor.fields import RichTextField

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
        ordering = ["sinonimo"]
        verbose_name = 'Sinónimo'
        verbose_name_plural = 'Sinónimo'

class FamilyModel(BasicAuditModel):

    familia = models.CharField(_("familia"), max_length=50)
    def __str__(self):
        return self.familia

    class Meta:
        db_table = 'arbolsaf_family'
        managed = True
        ordering = ["familia"]
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'

class GenderModel(BasicAuditModel):

    genero = models.CharField(_("género"), max_length=50)
    
    def __str__(self):
        return self.genero

    class Meta:
        db_table = 'arbolsaf_gender'
        managed = True
        ordering = ["genero"]
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
        ordering = ["fuente_final"]
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
        ordering = ["abreviatura"]
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
        ordering = ["nombre"]
        verbose_name = 'Grupo de variable'
        verbose_name_plural = 'Grupos de variables'

class VariableTypeModel(BasicAuditModel):

    TYPE_CHOICES = (
        ("boolean", "Boolean"),
        ("cualitativo", "Cualitativo"),
        ("numerico", "Numérico"),
        ("rango", "Rango"),
        ("texto", "Texto"),
    )
    seleccion_multiple = models.BooleanField(_("Es selección múltiple? (Aplicable solo a variables cualitativas)"), default=False)

    cod_var = models.CharField(_("código variable"), max_length=50)
    tipo_variables = models.CharField(_("tipo variable"), 
                    choices=TYPE_CHOICES, max_length=50, blank=True, null=True)
    
    unidad_medida =  models.ForeignKey("arbolsaf.MeasureUnitTypeModel", verbose_name=_("Unidad de medida"), 
                on_delete=models.SET_NULL, blank=True, null=True)
    
    familia =  models.ForeignKey("arbolsaf.VariableTypeFamilyModel", verbose_name=_("Grupo"),
                on_delete=models.SET_NULL, blank=True, null=True)

                
    variable = models.CharField(_("variable"), max_length=255)
    niveles_categoricos = models.TextField(_("Niveles categóricos"))
    descripcion = models.TextField(_("descripción"), blank=True, null=True)    

    min = models.FloatField(_("Valor mínimo"), blank=True, null=True)
    max = models.FloatField(_("Valor máximo"), blank=True, null=True)

    uso_herramienta = models.BooleanField(_("Utilizada en herramienta"), default=False)

    def __str__(self):
        return f"{self.variable} ({self.cod_var})"

    class Meta:
        db_table = 'arbolsaf_variable_type'
        ordering = ["variable"]
        managed = True
        verbose_name = 'Tipo de variable'
        verbose_name_plural = 'Tipos de variable'


class VariableTypeOption(models.Model):

    def __str__(self):
        return self.nombre

    tipo_variable = models.ForeignKey("arbolsaf.VariableTypeModel", verbose_name=_("Tipo de Variable"), 
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
    valores_cualitativos =   models.ManyToManyField("arbolsaf.VariableTypeOption", verbose_name=_("Valores cualitativos"), blank=True, null=True)
    #TODO averiguar si categoria puede ser una llave foranea

    #categoria = models.CharField(_("categoria"), max_length=50, blank=True, null=True)
    
    especie = models.ForeignKey("arbolsaf.SpeciesModel", related_name="variables", verbose_name=_("Especie"), on_delete=models.CASCADE)

    chequeo = models.BooleanField(_("Chequeada?"), default=False) 
    
    def __str__(self):
        return "{} - Especie: {}".format(self.tipo_variable, self.especie)
    
    @property
    def get_valor_general(self):
        valor=""

        if self.tipo_variable.tipo_variables == 'cualitativo':
            nombres=  [valor.nombre for valor in self.valores_cualitativos.all()]
            valor = ','.join(nombres)
        elif self.tipo_variable.tipo_variables == 'numerico': 
            valor = f"{self.rango_inferior};{self.rango_superior}"
        elif self.tipo_variable.tipo_variables == 'texto': 
            valor = self.valor_texto
        elif self.tipo_variable.tipo_variables == 'rango': 
            valor = f"{self.rango_inferior};{self.rango_superior}"
        elif self.tipo_variable.tipo_variables == 'boolean': 
            valor = "SI" if self.valor_boolean else "NO"
        else:
            valor = self.valor_general or ""

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
    """ Modelo para la gestion de especies """

    habilitada_herramienta = models.BooleanField(_("Habilitada en herramienta"), default=False)

    VALUES_CHOICES = (
        ("ninguno", "Ninguno"),
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
    )
        
    cod_esp = models.CharField(_("Código especie"), max_length=50, unique=True)
    taxonid_wfo = models.CharField(_("Taxón ID WFO"), max_length=50, unique=True)
    nombre_comun = models.CharField(_("Nombre común"), max_length=255)
    nombre_cientifico = models.CharField(_("Nombre científico"), max_length=255)
    nombre_cientifico_completo = models.CharField(_("Nombre científico completo"), max_length=255)
    familia = models.ForeignKey("arbolsaf.FamilyModel", verbose_name=_("Familia"), on_delete=models.RESTRICT)
    genero = models.ForeignKey("arbolsaf.GenderModel", verbose_name=_("Género"), on_delete=models.RESTRICT)
    epiteto = models.CharField(_("Epíteto"), max_length=50)
    
    variedad_subespecie = models.CharField(_("Variedad/Subespecie"), max_length=50, blank=True, null=True)
    autor = models.CharField(_("Autor"), max_length=255, blank=True, null=True)

    nativa = models.BooleanField(_("Nativa?"))

    notas = models.TextField(_("Notas"), blank=True, null=True)

    #link_cifor_icraf = models.URLField(_("Link CIFOR-ICRAF"), max_length=200, null=True, blank=True)
    
    
    @property
    def get_link_icraf(self):
        if not self.nombre_cientifico:
            return False
        url_prefix ='https://apps.worldagroforestry.org/products/switchboard/index.php/name_like/'
        url_name = urllib.parse.quote(self.nombre_cientifico)
        link_cifor = f"{url_prefix}{url_name}"
        return link_cifor

    #imagen = models.ImageField(verbose_name=_("Imagen"), upload_to="imagenes_especie",
    #                                            null=True, blank=True)
    
    @property
    def get_imagenes(self):
        return self.imagenes.all()

    #campos calculados
    @computed(models.IntegerField(_("Valor para  Madera"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_madera(self):
        if len(self.get_variables) == 0:
            return 0

        v169_instance = self.variables.filter(tipo_variable__cod_var__iexact='v169').first()
        v169 = bool(v169_instance and v169_instance.valor_boolean)

        v147_instance = self.variables.filter(tipo_variable__cod_var__iexact='v147').first()
        v147 = bool(v147_instance and v147_instance.valor_boolean)

        if v169 and v147:
            return 3

        if v169:
            return 2

        v163_instance = self.variables.filter(tipo_variable__cod_var__iexact='v163').first()
        v163 = bool(v163_instance and v163_instance.valor_boolean)

        v167_instance = self.variables.filter(tipo_variable__cod_var__iexact='v167').first()
        v167 = bool(v167_instance and v167_instance.valor_boolean)

        v168_instance = self.variables.filter(tipo_variable__cod_var__iexact='v168').first()
        v168 = bool(v168_instance and v168_instance.valor_boolean)

        if v163 or v167 or v168:
            return 1

        return 0



    @computed(models.IntegerField(_("Valor para  Fruta"), default=0),
                depends=[('variables', ['valor_boolean'])])
    def valor_fruta(self):
        if len(self.get_variables) == 0:
            return 0

        v170_instance = self.variables.filter(tipo_variable__cod_var__iexact='v170').first()
        if v170_instance and v170_instance.valor_boolean:
            return 3

        v130_instance = self.variables.filter(tipo_variable__cod_var__iexact='v130').first()
        if v130_instance and v130_instance.valor_boolean:
            return 2

        v23_instance = self.variables.filter(tipo_variable__cod_var__iexact='v23').first()
        if v23_instance and v23_instance.valor_boolean:
            return 1

        return 0


    @computed(models.FloatField(_("Valor para Otros usos"), default=0.0),
                depends=[('variables', ['valor_boolean'])])
    def valor_otros_usos(self):
        if len(self.get_variables) == 0:
            return 0.0

        def _bool(cod):
            inst = self.variables.filter(tipo_variable__cod_var__iexact=cod).first()
            return bool(inst and inst.valor_boolean)

        # grupo alto (leña, carbón, forraje)
        alto = 3 if any(_bool(c) for c in ('v162', 'v142', 'v39')) else 0
        # grupo medio (medicinal, artesanías)
        medio = 2 if any(_bool(c) for c in ('v113', 'v111')) else 0
        # grupo bajo (tintes-pigmentos, cos-rep, fibra)
        bajo = 1 if any(_bool(c) for c in ('v102', 'v112', 'v70')) else 0

        return round((alto + medio + bajo) / 2.0, 2)
        
    
    @computed(models.FloatField(_("Valor para Biodiversidad"), default=0.0),
                depends=[('variables', ['valor_boolean']), ('self', ['nativa'])])
    def valor_biodiversidad(self):
        if len(self.get_variables) == 0:
            return 0.0

        nativa = 1.0 if self.nativa else 0.0

        # v56 IUCN (cualitativa): EN=1, VU=0.5, NT=0.25
        v56_instance = self.variables.filter(tipo_variable__cod_var__iexact='v56').first()
        if v56_instance:
            nombres_v56 = [v.nombre.lower().strip() for v in v56_instance.valores_cualitativos.all()]
            if 'en' in nombres_v56:
                v56 = 1.0
            elif 'vu' in nombres_v56:
                v56 = 0.5
            elif 'nt' in nombres_v56:
                v56 = 0.25
            else:
                v56 = 0.0
        else:
            v56 = 0.0

        # v59 CITES (cualitativa): Apéndice II = 1
        v59_instance = self.variables.filter(tipo_variable__cod_var__iexact='v59').first()
        if v59_instance:
            nombres_v59 = [v.nombre.lower().strip() for v in v59_instance.valores_cualitativos.all()]
            v59 = 1.0 if 'ii' in nombres_v59 else 0.0
        else:
            v59 = 0.0

        def _bool(cod):
            inst = self.variables.filter(tipo_variable__cod_var__iexact=cod).first()
            return 1.0 if (inst and inst.valor_boolean) else 0.0

        v64  = _bool('v64')   # endémica
        v89  = _bool('v89')   # aves
        v90  = _bool('v90')   # micromamíferos
        v18  = _bool('v18')   # abejas
        v91  = _bool('v91')   # murciélagos
        v177 = _bool('v177')  # primates
        v176 = _bool('v176')  # mamíferos grandes

        suma = nativa + v56 + v59 + v64 + v89 + v90 + v18 + v91 + v177 + v176
        return round(suma * 6.0 / 10.0, 2)

    @computed(models.FloatField(_("Valor para el Suelo"), default=0.0),
                depends=[('variables', ['valor_boolean'])])
    def valor_suelo(self):
        if len(self.get_variables) == 0:
            return 0.0

        # v116 mejora estructura suelo (boolean)
        v116_instance = self.variables.filter(tipo_variable__cod_var__iexact='v116').first()
        v116 = 1 if (v116_instance and v116_instance.valor_boolean) else 0

        # v171 presencia nódulos (boolean)
        v171_instance = self.variables.filter(tipo_variable__cod_var__iexact='v171').first()
        v171 = 1 if (v171_instance and v171_instance.valor_boolean) else 0

        # v37 caducifolio (cualitativa): caducifolio=2, semicaducifolio=1
        v37_instance = self.variables.filter(tipo_variable__cod_var__iexact='v37').first()
        if v37_instance:
            nombres_v37 = [v.nombre.lower().strip() for v in v37_instance.valores_cualitativos.all()]
            if 'caducifolio' in nombres_v37:
                v37 = 2
            elif 'semicaducifolio' in nombres_v37:
                v37 = 1
            else:
                v37 = 0
        else:
            v37 = 0

        # v95 aporta fertilidad (cualitativa)
        v95_instance = self.variables.filter(tipo_variable__cod_var__iexact='v95').first()
        if v95_instance:
            nombres_v95 = [v.nombre.lower().strip() for v in v95_instance.valores_cualitativos.all()]
            v95 = 1 if any(n in nombres_v95 for n in ('fertilidad del suelo', 'recuperacion de suelos', 'recuperacion de suelo')) else 0
        else:
            v95 = 0

        # v161 tolera sequía (cualitativa)
        v161_instance = self.variables.filter(tipo_variable__cod_var__iexact='v161').first()
        if v161_instance:
            nombres_v161 = [v.nombre.lower().strip() for v in v161_instance.valores_cualitativos.all()]
            v161 = 1 if 'sequia' in nombres_v161 or 'sequía' in nombres_v161 else 0
        else:
            v161 = 0

        # v115 asociación microbiana (cualitativa): bacterias o micorrizas
        v115_instance = self.variables.filter(tipo_variable__cod_var__iexact='v115').first()
        if v115_instance:
            nombres_v115 = [v.nombre.lower().strip() for v in v115_instance.valores_cualitativos.all()]
            v115 = 1 if any(n in nombres_v115 for n in ('bacterias', 'micorrizas')) else 0
        else:
            v115 = 0

        # max bruto = 7 (2+1+1+1+1+1), normalizado a escala 0-3
        puntaje_bruto = v116 + v171 + v37 + v95 + v161 + v115
        return round(puntaje_bruto * 3.0 / 7.0, 2)

    
    @computed(models.CharField(_("Valor para Madera"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                depends=[('self', ['valor_madera'])])
    def valor_madera_category(self):


        if self.valor_madera == 0:
            valor = 'ninguno' 
        elif self.valor_madera == 1:
            valor = 'bajo'
        elif self.valor_madera == 2:
            valor = 'medio'
        elif self.valor_madera == 3:
            valor = 'alto'

        return valor

    @computed(models.CharField(_("Valor para Fruta"), max_length=50, 
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_fruta'])])
    def valor_fruta_category(self):

        if self.valor_fruta == 0:
            valor = 'ninguno' 
        elif self.valor_fruta == 1:
            valor = 'bajo'
        elif self.valor_fruta == 2:
            valor = 'medio'
        elif self.valor_fruta == 3:
            valor = 'alto'

        return valor
    
    @computed(models.CharField(_("Valor para otros Usos"), max_length=50,
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_otros_usos'])])
    def valor_otros_usos_category(self):
        if self.valor_otros_usos == 0:
            return 'ninguno'
        elif self.valor_otros_usos <= 1:
            return 'bajo'
        elif self.valor_otros_usos <= 2:
            return 'medio'
        else:
            return 'alto'

    @computed(models.CharField(_("Valor para Biodiversidad"), max_length=50,
                               choices=VALUES_CHOICES, default='ninguno'),
                                depends=[('self', ['valor_biodiversidad'])])
    def valor_biodiversidad_category(self):
        if self.valor_biodiversidad == 0:
            return 'ninguno'
        elif self.valor_biodiversidad <= 2:
            return 'bajo'
        elif self.valor_biodiversidad <= 4:
            return 'medio'
        else:
            return 'alto'


    @computed(models.CharField(_("Valor para Suelo"), max_length=50,
                               choices=VALUES_CHOICES, default='ninguno'),
                depends=[('self', ['valor_suelo'])])
    def valor_suelo_category(self):
        if self.valor_suelo == 0:
            return 'ninguno'
        elif self.valor_suelo <= 1:
            return 'bajo'
        elif self.valor_suelo <= 2:
            return 'medio'
        else:
            return 'alto'


    @computed(models.FloatField(_("IVIM"), default=0.0),
                depends=[('self', ['valor_madera','valor_fruta','valor_otros_usos',
                                   'valor_biodiversidad','valor_suelo'])])
    def ivim(self):
        return round(
            self.valor_madera + self.valor_fruta + self.valor_otros_usos +
            self.valor_biodiversidad + self.valor_suelo, 2
        )
    

    @property
    def get_variables(self):
        return self.variables.all()

    @property
    def get_variables_no_diligenciadas(self):
        variables = VariableTypeModel.objects.raw("""Select avt.id, avt.variable from arbolsaf_variable_type avt where avt.id not in 
                (select distinct av.tipo_variable_id from arbolsaf_variable av where av.especie_id=%s)
            """, [self.id])
        #variables = VariableTypeModel.objects.all()
        return variables




    @property
    def get_sinonimos(self):
        return self.sinonimos.all()

        

    def __str__(self):
        return f"{self.nombre_cientifico} ({self.cod_esp})"

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


class Bitacora(BasicAuditModel):


    MODELO_CHOICES = (
        ("general", "General"),
        ("especie", "Especie"),
        ("variable", "Variable"),
    )
    
    def __str__(self):
        return f"{self.entidad_modificada} {self.asunto}"


    entidad_modificada = models.CharField(_("Entidad"), max_length=50, choices=MODELO_CHOICES)
    codigo_especie = models.CharField(_("Código especie"), max_length=50, blank=True, null=True)
    codigo_variable = models.CharField(_("Código variable"), max_length=50, blank=True, null=True)
    asunto = models.CharField(_("Asunto"), max_length=255)
    descripcion_cambio = models.TextField(_("Descripción del cambio"))
    class Meta:
        db_table = 'arbolsaf_bitacora_cambios'
        managed = True
        ordering = ["-created"]
        verbose_name = 'Bitacora'
        verbose_name_plural = 'Bitacora'


class SpeciesAdminModel(SpeciesModel):
    class Meta:
        proxy = True
        verbose_name = 'Categorización Especies'
        verbose_name_plural = 'Categorización Especies'


class ImageSpecies(models.Model):

    descripcion = models.CharField(_("Descripción"), max_length=255)
    especie = models.ForeignKey("arbolsaf.SpeciesModel", verbose_name=_("Especie"), 
                    related_name="imagenes", on_delete=models.CASCADE)

    imagen = models.ImageField(verbose_name=_("Imagen"), upload_to="imagenes_especie")


    def __str__(self):
        return self.descripcion


    class Meta:
        db_table = 'arbolsaf_imagen_species'
        managed = True
        verbose_name = 'Imagen Especie'
        verbose_name_plural = 'Imágenes Especies'

class RegistroReporteHerramienta(models.Model):

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha reporte"))

    nombre_productor = models.CharField(_("Nombre del productor"), max_length=255)
    region = models.CharField(_("Región"), max_length=50, blank=True, null=True)
    provincia = models.CharField(_("Provincia"), max_length=50, blank=True, null=True)
    distrito = models.CharField(_("Distrito"), max_length=50, blank=True, null=True)
    tipo_intervencion = models.CharField(_("Tipo de intervención"), max_length=50, blank=True, null=True)

    finca_ha = models.IntegerField(_("Tamaño de la finca (ha)"), blank=True, null=True)
    parcela_ha = models.IntegerField(_("Tamaño de la parcela (ha)"), blank=True, null=True)
    tipo_usuario = models.CharField(_("Tipo de usuario"), max_length=50, blank=True, null=True)
    identidad_genero = models.CharField(_("Identidad de género"), max_length=50, blank=True, null=True)
    edad_usuario = models.CharField(_("Edad del usuario"), max_length=50, blank=True, null=True)

    especies_str = models.TextField(_("Especies"), blank=True, null=True)

    especies = models.ManyToManyField("arbolsaf.SpeciesModel", verbose_name=_("Especies"))


    def __str__(self):
        return f"{self.nombre_productor} ({self.created})"

    class Meta:
        db_table = 'arbolsaf_registro_reporte'
        managed = True
        ordering = ["-created"]
        verbose_name =  'Registro reporte herramienta'
        verbose_name_plural =  'Registros reporte herramienta'



class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)
    

class Configuracion(SingletonModel):

    nombre = models.CharField(_("Nombre"), max_length=50, default="Configuración")
    texto_seccion_arbolsaf = RichTextField("Texto pestaña Arbolsaf", default="Escriba su texto aquí")
    texto_seccion_creditos = RichTextField("Texto pestaña Créditos", default="Escriba los créditos")
    texto_seccion_descargo_responsabilidad = RichTextField("Texto pestaña Descargo de responsabilidad", default="Escriba el texto")
    texto_seccion_agradecimientos = RichTextField("Texto pestaña Agradecimientos", default="Escriba el texto")


    class Meta:
        db_table = 'arbolsaf_configuracion'
        managed = True
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuración Textos'