from django import forms
#from leaflet.forms.widgets import LeafletWidget
from .models import *

#from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, ModelSelect2Mixin
from django.utils.translation import gettext_lazy as _


class SpeciesForm(forms.ModelForm):


    class Meta:
        model = SpeciesModel
        exclude = ("id",'created_by', 'modified_by')
        widgets = {
            'cod_esp':forms.TextInput(attrs={'class': 'form-control'}),
            'taxonid_wfo':forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comun':forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_cientifico':forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_cientifico_completo':forms.TextInput(attrs={'class': 'form-control'}),
            'familia': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'genero': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'epiteto':forms.TextInput(attrs={'class': 'form-control'}),
            'variedad_subespecie':forms.TextInput(attrs={'class': 'form-control'}),
            'autor':forms.TextInput(attrs={'class': 'form-control'}),
            'nativa': forms.CheckboxInput(attrs={'class': 'form-check-input '}),                                 
            }


class VariableO2MForm(forms.ModelForm):


    class Meta:
        model = VariableModel
        exclude = ("id",'created_by', 'modified_by')
        widgets = {
            #'nombre':forms.TextInput(attrs={'class': 'form-control'}),
            #'referencia': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'tipo_variable': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'referencia': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'referencia_2': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'valor_numerico':forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_texto':forms.TextInput(attrs={'class': 'form-control'}),
            'valor_boolean': forms.CheckboxInput(attrs={'class': 'form-check-input '}),    
            'rango_superior':forms.NumberInput(attrs={'class': 'form-control'}),
            'rango_inferior':forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_general':forms.TextInput(attrs={'class': 'form-control'}),
            'chequeo': forms.CheckboxInput(attrs={'class': 'form-check-input '}),     
            'especie': forms.HiddenInput(),
            'valor_cualitativo': forms.Select(attrs={'class': 'form-select form-select-lg'}),

            
            }


    def clean(self):
        data = super().clean()

        referencia1 = self.cleaned_data.get('referencia', '')
        referencia2 = self.cleaned_data.get('referencia_2', '')

        if referencia1 !=referencia2:
            raise forms.ValidationError(
                    {"referencia": "Los valores de referencia deben coincidir"})

        
        if self.cleaned_data.get('tipo_variable', False) and self.cleaned_data.get('tipo_variable', '').tipo_variables == 'rango':

            rango_superior = self.cleaned_data.get('rango_superior', 0)
            rango_inferior = self.cleaned_data.get('rango_inferior', 0)
            if rango_superior<rango_inferior:
                raise forms.ValidationError(
                    {"rango_superior": "El rango superior debe ser mayor o igual al rango inferior"})
        




        return data



#class CreateSynonimForm(forms.Form):
#    nombre = forms.CharField(label='Nombre', max_length=100)
#    forms.name = models.ForeignKey('TargetModel', related_name='', on_delete=models.CASCADE)
class SynonymousForm(forms.ModelForm):
    class Meta:
        model = SynonymousModel
        exclude = ("id",'created_by', 'modified_by')
        widgets = {
            'sinonimo':forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.HiddenInput(),
            }


class VariableTypeForm(forms.ModelForm):


    class Meta:
        model = VariableTypeModel
        exclude = ("id",'created_by', 'modified_by')
        widgets = {
            'cod_var':forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_variables': forms.Select(attrs={'class': 'form-select'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),    
            'variable':forms.TextInput(attrs={'class': 'form-control'}),
            'niveles_categoricos':forms.Textarea(attrs={'class': 'form-control'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control'}),
            'min':forms.NumberInput(attrs={'class': 'form-control'}),
            'max':forms.NumberInput(attrs={'class': 'form-control'}),
            }

class ReferenceForm(forms.ModelForm):


    class Meta:
        model = ReferenceModel
        exclude = ("id",'created_by', 'modified_by')
        widgets = {
            'fuente_final':forms.TextInput(attrs={'class': 'form-control'}),
            'cod_cita':forms.TextInput(attrs={'class': 'form-control'}),
            'referencia':forms.Textarea(attrs={'class': 'form-control'}),

            }