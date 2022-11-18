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
            'nativa': forms.CheckboxInput(),                      
            }
