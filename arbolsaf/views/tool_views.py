from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from wkhtmltopdf.views import PDFTemplateResponse
import json
from django.conf import settings
from ..models import SpeciesModel

class ToolView(TemplateView):
    template_name = "arbolsaf/tool/tool.html"

class IntroToolView(TemplateView):
    template_name = "arbolsaf/tool/tool_intro.html"

class AboutToolView(TemplateView):
    template_name = "arbolsaf/tool/about.html"



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
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("-------------------------------------------------------------------------------------------------------------------")
    print(request.POST)
    post_data = request.POST
    print("-------------------------------------------------------------------------------------------------------------------")
    data={
        "nombre": post_data['NOMBRE'] or '-',
        "region": post_data['REGION'] or '-',
        "provincia": post_data['PROVINCIA'] or '-',
        "distrito": post_data['DISTRITO'] or '-',
        "tipo_intervencion": post_data['TIPO DE INTERVENCION'] or '-',
        "tam_finca": post_data['TAMANO DE FINCA'] or '-',
        "tam_parcela": post_data['TAMANO DE PARCELA'] or '-',
        "tipo_usuario": post_data['TIPO DE USUARIO'] or '-',
        "genero": post_data['IDENTIDAD DE GENERO'] or '-',
        "edad": post_data['EDAD DEL USUARIO'] or '-', 
        "especies":especies_obj 
    }
    cuenta = 0
    for especie in especies_obj:
         
        if cuenta==0:
            cuenta+=1 
            continue
        cuenta+=1 
  
        codigo = especie.get('CODIGO',False)
        especienodel = SpeciesModel.objects.filter(cod_esp=codigo).first()

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


    response = get_tool_pdf_response(request, data=data)
    return response