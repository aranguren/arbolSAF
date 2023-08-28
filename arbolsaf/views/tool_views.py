from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from wkhtmltopdf.views import PDFTemplateResponse
import json

class ToolView(TemplateView):
    template_name = "arbolsaf/tool/tool.html"

class IntroToolView(TemplateView):
    template_name = "arbolsaf/tool/tool_intro.html"

class AboutToolView(TemplateView):
    template_name = "arbolsaf/tool/about.html"



def get_tool_pdf_response(request):



    template_to_use ='arbolsaf/tool/tool_pdf.html' # the template 
   

    identificador_cusaf = 1
    data = {
        'cusaf':'Cusaf00001',

        #'imagen':imagen
    }
    response = PDFTemplateResponse(request=request,
                                    template=template_to_use,
                                    #header_template= template_header, 
                                    #footer_template= template_footer, 
                                    filename="Ficha cusaf {}.pdf".format(identificador_cusaf),
                                    context= data,
                                    show_content_in_browser=False,
                                    cmd_options={  'margin-top':10,
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
    print("-------------------------------------------------------------------------------------------------------------------")

    response = get_tool_pdf_response(request)
    return response