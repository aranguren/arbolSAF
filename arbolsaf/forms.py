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
            'familia': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
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
            'nombre':forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.Select(attrs={'class': 'form-control'}),
            'tipo_variable': forms.Select(attrs={'class': 'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class': 'form-control'}),
            'rango_superior':forms.NumberInput(attrs={'class': 'form-control'}),
            'rango_inferior':forms.NumberInput(attrs={'class': 'form-control'}),
            'referencia': forms.Select(attrs={'class': 'form-control'}),
            'categoria':forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.HiddenInput(),
            }





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
