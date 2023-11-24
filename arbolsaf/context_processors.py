from arbolsaf.models import Configuracion
from django.conf import settings
import os

def settings(request):
    return {'settings_arbolsaf': Configuracion.load()}




     