from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from wkhtmltopdf.views import PDFTemplateResponse
import json
from django.conf import settings
from ..models import SpeciesModel, RegistroReporteHerramienta, Configuracion

class ToolView(TemplateView):
    template_name = "arbolsaf/tool/tool.html"

class IntroToolView(TemplateView):
    template_name = "arbolsaf/tool/tool_intro.html"

class AboutToolView(TemplateView):
    template_name = "arbolsaf/tool/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #settings_agrimensuras = SettinsAgrimensuras.load()
        settings_arbolsaf = Configuracion.objects.get()
        
        #project = get_object_or_404(Project, id = int(kwargs['pk']))

        context["settings_arbolsaf"] = settings_arbolsaf
        
       
       
        return context    



def get_tool_pdf_response(request, data):



    template_to_use ='arbolsaf/tool/tool_pdf.html' # the template 
    template_header ='arbolsaf/tool/tool_pdf_header.html' 
    template_footer ='arbolsaf/tool/tool_pdf_footer.html' 
   



    data['pdf_header'] = "{}{}".format(settings.STATIC_ROOT, '/assets/img/herramienta/Cabecera_1_ÁrbolSAF.png'),
    """
    response = PDFTemplateResponse(request=request,
                                    template=template_to_use,
                                    #header_template= template_header, 
                                    #footer_template= template_footer, 
                                    filename="Reporte herramienta ÁrbolSAF.pdf",
                                    context= data,
                                    show_content_in_browser=False,
                                    cmd_options={  'margin-top':0,
                                    'margin-left':0,
                                    'margin-right':0,
                                    "zoom":1,
                                    "viewport-size" :"1366x513",
                                    'javascript-delay':1000,
                                    'enable-local-file-access':True,
                                    'footer-center' :'[page]/[topage]',
                                    "no-stop-slow-scripts":True},
                                    )
    """
    response = PDFTemplateResponse(request=request,
                                    template=template_to_use,
                                    header_template= template_header, 
                                    #footer_template= template_footer, 
                                    filename="Reporte herramienta ÁrbolSAF.pdf",
                                    context= data,
                                    show_content_in_browser=False,
                                    cmd_options={  'margin-top':33,
                                    'margin-bottom':15,
                                    'margin-left':0,
                                    'margin-right':0,
                                    'header-spacing':10,
                                    "zoom":1,
                                    "viewport-size" :"1366x513",
                                    'javascript-delay':1000,
                                    'enable-local-file-access':True,
                                    'footer-center' :'[page]/[topage]',
                                    "no-stop-slow-scripts":True},
                                    )
    """
    response = PDFTemplateResponse(request=request,
                                    template=self.template,
                                    filename="hello.pdf",
                                    context= data,
                                    show_content_in_browser=False,
                                    cmd_options={'margin-top': 10,
                                    "zoom":1,
                                    "viewport-size" :"1366 x 513",
                                    'javascript-delay':1000,
                                    'footer-center' :'[page]/[topage]',
                                    "no-stop-slow-scripts":True},
                                    )
    """
    return response
from django.views.decorators.csrf import csrf_exempt


class ToolPDFView(View):
    #template_parcela ='agrimensuras/project_pdf_parcela.html' # the template 
    #template_lotificacion ='agrimensuras/project_pdf_lotificacion.html' 
    #template_header ='agrimensuras/project_pdf_header.html' 
    #template_footer ='agrimensuras/project_pdf_footer.html' 

    def post(self, request, **kw):

        especies = request.POST.get('especies', None)

        especies_obj = json.loads(especies)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("-------------------------------------------------------------------------------------------------------------------")
        print(request.POST)
        print("-------------------------------------------------------------------------------------------------------------------")

        response = get_tool_pdf_response(request)
        return response

@csrf_exempt
def tool_print_pdf_view(request):
    especies = request.POST.get('especies', None)
    if especies:
        especies_obj = json.loads(especies)
    post_data = request.POST
    data={
        "nombre": post_data['nombre'] or '-',
        "region": post_data['region'] or '-',
        "provincia": post_data['provincia'] or '-',
        "distrito": post_data['distrito'] or '-',
        "tipo_intervencion": post_data['tipo_de_intervencion'] or '-',
        "tam_finca": post_data['tamano_de_finca'] or '-',
        "tam_parcela": post_data['tamano_de_parcela'] or '-',
        "tipo_usuario": post_data['tipo_de_usuario'] or '-',
        "genero": post_data['identidad_de_genero'] or '-',
        "edad": post_data['edad_del_usuario'] or '-', 
        "especies":especies_obj 
    }
    """
    registro = RegistroReporteHerramienta(
        nombre_productor = post_data['nombre'] or '-',
        region = post_data['region'] or '-',
        provincia = post_data['provincia'] or '-',
        distrito = post_data['distrito'] or '-',
        tipo_intervencion = post_data['tipo_de_intervencion'] or '-',
        finca_ha = post_data['tamano_de_finca'] or '-',
        parcela_ha = post_data['tamano_de_parcela'] or '-',
        tipo_usuario =  post_data['tipo_de_usuario'] or '-',
        identidad_genero =  post_data['identidad_de_genero'] or '-',
        edad_usuario = post_data['edad_del_usuario'] or '-', 
    )
    """
    data_registro ={
         'nombre_productor' : post_data.get('nombre', None),
    }

    if post_data.get('region', '') != '' :
        data_registro['region'] = post_data.get('region', None)
    if post_data.get('provincia', '') != '' :
        data_registro['provincia'] = post_data.get('provincia', None)
    if post_data.get('distrito','') != '' :
        data_registro['distrito'] = post_data.get('distrito', None)
    if post_data.get('tipo_de_intervencion', '') != '' :
        data_registro['tipo_intervencion'] = post_data.get('tipo_de_intervencion', None)
    if post_data.get('tamano_de_finca','') != '' :
        data_registro['finca_ha'] = post_data.get('tamano_de_finca', None)
    if post_data.get('tamano_de_parcela', '') != '' :
        data_registro['parcela_ha'] = post_data.get('tamano_de_parcela', None)
    if post_data.get('tipo_de_usuario', '') != '' :
        data_registro['tipo_usuario'] = post_data.get('tipo_de_usuario', None)
    if post_data.get('identidad_de_genero', '') != '' :
        data_registro['identidad_genero'] = post_data.get('identidad_de_genero', None)
    if post_data.get('edad_del_usuario', '') != '' :
        data_registro['edad_usuario'] = post_data.get('edad_del_usuario', None)

    
    registro = RegistroReporteHerramienta(**data_registro)
    registro.save()
    especies_str = ""

    for index, especie in enumerate(especies_obj):
        print("-------------------------------------------------------------------------------------------------------------------")
        
        print(f"Mostrando especie con nombre {especie.get('NOMBRE COMUN','')}")
        print(f"SEMAFORO_PASO_2-> {especie.get('SEMAFORO_PASO_2','')}")
        print(f"SEMAFORO_PASO_3-> {especie.get('SEMAFORO_PASO_3','')}")
        print(f"NOTAS-> {especie.get('NOTAS','')}")
        
        especie['nombre_comun'] = especie.get('NOMBRE COMUN','-')
        especie['nombre_cientifico'] = especie.get('NOMBRE CIENTIFICO','')
        especie['valor_madera'] = True if especie.get('VALOR MADERA',0) >0  else False
        especie['valor_fruta'] =  True if especie.get('VALOR FRUTA',0) >0 else False
        especie['valor_otros_usos'] = True if especie.get('VALOR OTROS USOS',0) >0 else False
        especie['valor_biodiversidad'] = True if especie.get('VALOR BIODIVERSIDAD',0) >0 else False
        especie['valor_microclimea'] = True if especie.get('VALOR MICROCLIMA',0 ) >0  else False
        especie['valor_suelo'] = True if especie.get('VALOR SUELO','') >0  else False

  
        codigo = especie.get('CODIGO',False)
        especienodel = SpeciesModel.objects.filter(cod_esp=codigo).first()
        registro.especies.add(especienodel)
        especies_str+= f"{especienodel.nombre_cientifico} ({especienodel.cod_esp})"

        if index != len(especies_obj) - 1:
            especies_str+=", "

        v56_instance = especienodel.variables.filter(tipo_variable__cod_var__iexact='v56').first()
        if v56_instance:
            valores = v56_instance.valores_cualitativos.all()
            nombres_valores_v56 = [valor.nombre for valor in valores]
            if len(nombres_valores_v56)>0:
                v56_categoria_amenaza_iucn = ','.join(nombres_valores_v56)
            else:
                v56_categoria_amenaza_iucn = ""
        else:
            v56_categoria_amenaza_iucn = ""

        especie['v56_categoria_amenaza_iucn'] = v56_categoria_amenaza_iucn


        v59_instance = especienodel.variables.filter(tipo_variable__cod_var__iexact='v59').first()
        if v59_instance:
            valores = v59_instance.valores_cualitativos.all()
            nombres_valores_v59 = [valor.nombre for valor in valores]
            if len(nombres_valores_v59)>0:
                v59_categoria_amenaza_cites = ','.join(nombres_valores_v59)
            else:
                v59_categoria_amenaza_cites = ""
        else:
            v59_categoria_amenaza_cites = ""
            
        especie['v59_categoria_amenaza_cites'] = v59_categoria_amenaza_cites


        v136_instance = especienodel.variables.filter(tipo_variable__cod_var__iexact='v136').first()
        if v136_instance:
            valores = v136_instance.valores_cualitativos.all()
            nombres_valores_v136 = [valor.nombre for valor in valores]
            if len(nombres_valores_v136)>0:
                v136_tipo_semilla_viabilidad = ','.join(nombres_valores_v136)
            else:
                v136_tipo_semilla_viabilidad = ""
        else:
            v136_tipo_semilla_viabilidad = ""
            
        especie['v136_tipo_semilla_viabilidad'] = v136_tipo_semilla_viabilidad

    registro.especies_str = especies_str
    registro.save()
    response = get_tool_pdf_response(request, data=data)
    return response

