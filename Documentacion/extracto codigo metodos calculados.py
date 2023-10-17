# EXTRACTICO DE CODIGO PARA EL CALCULOS DE LOS VALORES PARA LAS CATEGORRÍAS
    #campos calculados
@computed(models.IntegerField(_("Valor para  Madera"), default=0),
            depends=[('variables', ['valor_boolean'])])
def valor_madera(self):
    if len(self.get_variables)== 0:
        return 0

    # si una especie tiene la v104 como palmera o hervacea, entonces retornar 0
    # o sea si v104 = ('palmera','hervacea') retornar 0
    
    v104_instance = self.variables.filter(tipo_variable__cod_var__iexact='v104').first()
    if v104_instance:
        valores = v104_instance.valores_cualitativos.all()
        nombres_valores_v104 = [valor.nombre for valor in valores]
        if 'palmera' in nombres_valores_v104 or 'herbacea' in nombres_valores_v104:
            v104 = True
        else:
            v104 = False
    else:
        v104 = False 
    
    if v104:
        return 0
    
    v147_instance = self.variables.filter(tipo_variable__cod_var__iexact='v147').first()
    if v147_instance:
        v147 = v147_instance.valor_boolean or False
    else:
        v147 = False

    v167_instance = self.variables.filter(tipo_variable__cod_var__iexact='v167').first()
    if v167_instance:
        v167 = v167_instance.valor_boolean or False
    else:
        v167 = False
    
    if v147 or v167:
        return 3

    v163_instance = self.variables.filter(tipo_variable__cod_var__iexact='v163').first()
    if v163_instance:
        v163 = v163_instance.valor_boolean or False
    else:
        v163 = False
    
    if v163:
        return 2



    v168_instance = self.variables.filter(tipo_variable__cod_var__iexact='v168').first()
    if v168_instance:
        v168 = v168_instance.valor_boolean or False
    else:
        v168 = False  
    
    if v168:
        return 1

    return 0



@computed(models.IntegerField(_("Valor para  Fruta"), default=0),
            depends=[('variables', ['valor_boolean'])])
def valor_fruta(self):
    if len(self.get_variables)== 0:
        return 0
    
    v23_instance = self.variables.filter(tipo_variable__cod_var__iexact='v23').first()
    if v23_instance:
        v23 = v23_instance.valor_boolean or False
    else:
        v23 = False

    v24_instance = self.variables.filter(tipo_variable__cod_var__iexact='v24').first()
    if v24_instance:
        v24 = v24_instance.valor_boolean or False
    else:
        v24 = False

    v130_instance = self.variables.filter(tipo_variable__cod_var__iexact='v130').first()
    if v130_instance:
        v130 = v130_instance.valor_boolean or False
    else:
        v130 = False
    
    if v23 or v24 or v130:
        return 3
    else:
        return 0


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

    v142_instance = self.variables.filter(tipo_variable__cod_var__iexact='v142').first()
    if v142_instance:
        v142 = 1 if v142_instance.valor_boolean else 0 
    else:
        v142 = 0

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

    suma = v102 + v111 + v112 + v113 +  v142 + v162 + v39 + v70
    if suma>=5:
        return 3
    elif suma>=3:
        return 2
    elif suma>=1:
        return 1
    else:
        return 0
    

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
    
    suma  =v127 + v14 + v18 + v89 + v90 + v91                                          
    if suma>=5:
        return 3
    elif suma>=3:
        return 2
    elif suma>=1:
        return 1
    else:
        return 0

@computed(models.IntegerField(_("Valor para Microclima"), default=0),
            depends=[('variables', ['valor_boolean'])])
def valor_microclima(self):
    """V4 V58"""
    if len(self.get_variables)== 0:
        return 0
    
    v4_instance = self.variables.filter(tipo_variable__cod_var__iexact='v4').first()
    if v4_instance:
        v4 = v4_instance.valor_boolean or False
    else:
        v4 = False

    v58_instance = self.variables.filter(tipo_variable__cod_var__iexact='v58').first()
    if v58_instance:
        v58 = v58_instance.valor_boolean or False
    else:
        v58 = False

    v54_instance = self.variables.filter(tipo_variable__cod_var__iexact='v54').first()
    if v54_instance:
        v54 = v54_instance.valor_boolean or False
    else:
        v54 = False
    
    if v4 or v54 or v58:
        return 3
    else:
        return 0
    


#TODO pendiente por definir esto
@computed(models.IntegerField(_("Valor para el Suelo"), default=0),
            depends=[('variables', ['valor_boolean'])])
def valor_suelo(self):
    """V4 V58"""
    if len(self.get_variables)== 0:
        return 0
    
    v114_instance = self.variables.filter(tipo_variable__cod_var__iexact='v114').first()
    if v114_instance:
        v114 = 1 if v114_instance.valor_boolean else 0
    else:
        v114 = 0

    v115_instance = self.variables.filter(tipo_variable__cod_var__iexact='v115').first()
    if v115_instance:
        valores = v115_instance.valores_cualitativos.all()
        nombres_valores_v115 = [valor.nombre for valor in valores]
        if 'bacterias' in nombres_valores_v115:
            v115 =1
        else:
            v115 =0
    else:
        v115 =0

    v116_instance = self.variables.filter(tipo_variable__cod_var__iexact='v116').first()
    if v116_instance:
        v116 = 1 if v116_instance.valor_boolean else 0
    else:
        v116 = 0

    v37_instance = self.variables.filter(tipo_variable__cod_var__iexact='v37').first()
    if v37_instance:
        valores = v37_instance.valores_cualitativos.all()
        nombres_valores_v37 = [valor.nombre for valor in valores]
        if 'caducifolio' in nombres_valores_v37 or 'semicaducifolio' in nombres_valores_v37:
            v37 =1
        else:
            v37 =0
    else:
        v37 =0


    v71_instance = self.variables.filter(tipo_variable__cod_var__iexact='v71').first()
    if v71_instance:
        valores = v71_instance.valores_cualitativos.all()
        nombres_valores_v71 = [valor.nombre for valor in valores]
        if 'leguminosa' in nombres_valores_v71:
            v71 =1
        else:
            v71 =0
    else:
        v71 =0

    v95_instance = self.variables.filter(tipo_variable__cod_var__iexact='v95').first()
    if v95_instance:
        valores = v95_instance.valores_cualitativos.all()
        nombres_valores_v95 = [valor.nombre for valor in valores]
        if 'fertilidad del suelo' in nombres_valores_v95 or 'recuperacion de suelo' in nombres_valores_v95:
            v95 =1
        else:
            v95 =0
    else:
        v95 =0
    
    suma = v114 + v115 + v116 + v37 + v71 + v95

    if suma>=5:
        return 3
    elif suma>=3:
        return 2
    elif suma>=1:
        return 1
    else:
        return 0


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
        valor = 'ninguno' 
    elif self.valor_otros_usos == 1:
        valor = 'bajo'
    elif self.valor_otros_usos == 2:
        valor = 'medio'
    elif self.valor_otros_usos == 3:
        valor = 'alto'

    return valor

@computed(models.CharField(_("Valor para Biodiversidad"), max_length=50, 
                            choices=VALUES_CHOICES, default='ninguno'),
                            depends=[('self', ['valor_biodiversidad'])])
def valor_biodiversidad_category(self):


    if self.valor_biodiversidad == 0:
        valor = 'ninguno' 
    elif self.valor_biodiversidad == 1:
        valor = 'bajo'
    elif self.valor_biodiversidad == 2:
        valor = 'medio'
    elif self.valor_biodiversidad == 3:
        valor = 'alto'

    return valor

@computed(models.CharField(_("Valor para Microclima"), max_length=50, 
                            choices=VALUES_CHOICES, default='ninguno'),
                            depends=[('self', ['valor_microclima'])])
def valor_microclima_category(self):


    if self.valor_microclima == 0:
        valor = 'ninguno' 
    elif self.valor_microclima == 1:
        valor = 'bajo'
    elif self.valor_microclima == 2:
        valor = 'medio'
    elif self.valor_microclima == 3:
        valor = 'alto'

    return valor

@computed(models.CharField(_("Valor para Suelo"), max_length=50, 
                            choices=VALUES_CHOICES, default='ninguno'),
            depends=[('self', ['valor_suelo'])])
def valor_suelo_category(self):

    if self.valor_suelo == 0:
        valor = 'ninguno' 
    elif self.valor_suelo == 1:
        valor = 'bajo'
    elif self.valor_suelo == 2:
        valor = 'medio'
    elif self.valor_suelo == 3:
        valor = 'alto'

    return valor


@computed(models.FloatField(_("Índice Multiuso"), default=0.0),
            depends=[('self', ['valor_madera','valor_fruta','valor_otros_usos',
                                'valor_biodiversidad','valor_microclima','valor_suelo'])])
def indice_multiuso(self):
    count = 0
    if self.valor_madera>0:
        count+=1
    if self.valor_fruta>0:
        count+=1
    if self.valor_otros_usos>0:
        count+=1
    if self.valor_biodiversidad>0:
        count+=1
    if self.valor_microclima>0:
        count+=1
    if self.valor_suelo>0:
        count+=1


    return round(count/6*100, 2)

@computed(models.FloatField(_("Índice de valor de uso relativo"), default=0.0),
            depends=[('self', ['valor_madera','valor_fruta','valor_otros_usos',
                                'valor_biodiversidad','valor_microclima','valor_suelo'])])
def indice_valor_uso_relativo(self):
    
    suma = self.valor_madera + self.valor_fruta + self.valor_otros_usos+\
            self.valor_biodiversidad + self.valor_microclima + self.valor_suelo


    return round(suma/18*100, 2)

@computed(models.FloatField(_("IVIM"), default=0.0),
            depends=[('self', ['indice_multiuso','indice_valor_uso_relativo'])])
def ivim(self):
    

    return self.indice_multiuso+ self.indice_valor_uso_relativo
    
