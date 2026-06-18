from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from wkhtmltopdf.views import PDFTemplateResponse
import json
import math
import unicodedata
from datetime import date
from django.conf import settings
from ..models import SpeciesModel, RegistroReporteHerramienta, ReferenceModel, VariableModel, Configuracion


# ── Helpers para gráficos SVG en el PDF ────────────────────────────────────

def _make_bar_svg(bars, width=600, row_h=30, label_w=130):
    """
    Genera SVG de barras horizontales para el PDF.
    bars: lista de (label, pct_int, color_hex)
    Usa width="100%" + viewBox para que escale al ancho del contenedor.
    """
    bar_area = width - label_w - 44   # espacio para barra + etiqueta de %
    total_h  = len(bars) * row_h + 24

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {} {}" '
           'style="font-family:Arial,sans-serif;display:block;">'.format(width, total_h)]

    # Líneas guía verticales + etiquetas de eje
    for tick in [0, 25, 50, 75, 100]:
        x = label_w + int(tick * bar_area / 100)
        svg.append('<line x1="{0}" y1="2" x2="{0}" y2="{1}" '
                   'stroke="#ddd" stroke-width="1"/>'.format(x, total_h - 18))
        svg.append('<text x="{}" y="{}" text-anchor="middle" '
                   'font-size="9" fill="#aaa">{}%</text>'.format(x, total_h - 4, tick))

    for i, (label, pct, color) in enumerate(bars):
        y      = i * row_h + 4
        bar_px = int(pct * bar_area / 100)
        ty     = y + row_h * 0.60

        # Etiqueta izquierda
        svg.append('<text x="{}" y="{:.1f}" text-anchor="end" '
                   'font-size="11" fill="#444">{}</text>'.format(label_w - 5, ty, label))

        # Fondo de barra
        svg.append('<rect x="{}" y="{}" width="{}" height="18" '
                   'fill="#f0f0f0" rx="3"/>'.format(label_w, y + 4, bar_area))

        # Barra de valor
        if bar_px > 0:
            svg.append('<rect x="{}" y="{}" width="{}" height="18" '
                       'fill="{}" rx="3"/>'.format(label_w, y + 4, bar_px, color))

        # Porcentaje
        if pct > 0:
            if bar_px > 28:
                svg.append('<text x="{}" y="{:.1f}" text-anchor="end" '
                           'font-size="10" fill="white" font-weight="bold">{}%</text>'.format(
                               label_w + bar_px - 4, ty, pct))
            else:
                svg.append('<text x="{}" y="{:.1f}" text-anchor="start" '
                           'font-size="10" fill="#666">{}%</text>'.format(
                               label_w + bar_px + 4, ty, pct))

    svg.append('</svg>')
    return ''.join(svg)


def _make_fauna_pie_svg(fauna_active, size=200):
    """
    Genera SVG de pastel con 6 sectores iguales para grupos de fauna.
    fauna_active: lista de (label, is_active)  — label puede contener \\n
    """
    cx = cy = size / 2.0
    r  = size * 0.43
    n  = len(fauna_active)
    GREEN = '#21ac8d'
    GRAY  = '#d8d8d8'

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{0}" viewBox="0 0 {0} {0}">'.format(size)]

    for i, (label, active) in enumerate(fauna_active):
        color      = GREEN if active else GRAY
        text_color = 'white' if active else '#888'

        start_deg = i * (360.0 / n) - 90
        end_deg   = (i + 1) * (360.0 / n) - 90
        sr, er    = math.radians(start_deg), math.radians(end_deg)

        x1, y1 = cx + r * math.cos(sr), cy + r * math.sin(sr)
        x2, y2 = cx + r * math.cos(er), cy + r * math.sin(er)

        d = 'M {:.2f},{:.2f} L {:.2f},{:.2f} A {:.2f},{:.2f} 0 0,1 {:.2f},{:.2f} Z'.format(
            cx, cy, x1, y1, r, r, x2, y2)
        svg.append('<path d="{}" fill="{}" stroke="white" stroke-width="2"/>'.format(d, color))

        # Texto centrado en el sector
        mid_rad = math.radians((start_deg + end_deg) / 2)
        lx = cx + r * 0.62 * math.cos(mid_rad)
        ly = cy + r * 0.62 * math.sin(mid_rad)

        words = label.replace('\\n', '\n').split('\n')
        lh = 12
        if len(words) == 1:
            svg.append('<text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
                       'dominant-baseline="middle" font-size="10" font-weight="bold" '
                       'fill="{}">{}</text>'.format(lx, ly, text_color, words[0]))
        else:
            svg.append('<text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
                       'font-size="10" font-weight="bold" fill="{}">'.format(
                           lx, ly - lh / 2.0, text_color))
            for j, word in enumerate(words):
                svg.append('<tspan x="{:.1f}" dy="{}">{}</tspan>'.format(
                    lx, 0 if j == 0 else lh, word))
            svg.append('</text>')

    svg.append('</svg>')
    return ''.join(svg)


def _normalize_key(s):
    """Normaliza una cadena: minúsculas + sin tildes (para matching de polinizadores)."""
    s = (s or '').lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Variables referenciadas en los pasos 2 (clima/suelo) y 3 (forma/ecología) de la herramienta
TOOL_STEP_2_3_COD_VARS = [
    'v1', 'v2', 'v6', 'v7', 'v9', 'v13', 'v35', 'v37',
    'v68', 'v73', 'v80', 'v81', 'v82', 'v83',
    'v100', 'v101', 'v106', 'v108',
    'v144', 'v152', 'v153', 'v157', 'v158', 'v161', 'v281',
]


class ToolView(TemplateView):
    template_name = "arbolsaf/tool/tool.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = ["herramienta"]

        cod_vars_lower = [c.lower() for c in TOOL_STEP_2_3_COD_VARS]
        ref_ids = set(
            VariableModel.objects
            .filter(tipo_variable__cod_var__iregex=r'^(' + '|'.join(cod_vars_lower) + r')$')
            .values_list('referencia_id', 'referencia_2_id')
            .iterator()
        )
        flat_ids = {rid for tup in ref_ids for rid in tup if rid is not None}
        context["tool_references"] = (
            ReferenceModel.objects.filter(id__in=flat_ids).order_by('fuente_final')
        )
        context["config"] = Configuracion.load()
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
        especie['valor_suelo'] = True if especie.get('VALOR SUELO','') >0  else False
        # Valores numéricos para los círculos en la tabla detalle
        especie['valor_madera_num']       = float(especie.get('VALOR MADERA') or 0)
        especie['valor_fruta_num']        = float(especie.get('VALOR FRUTA') or 0)
        especie['valor_biodiversidad_num']= float(especie.get('VALOR BIODIVERSIDAD') or 0)
        especie['valor_suelo_num']        = float(especie.get('VALOR SUELO') or 0)
        especie['valor_otros_usos_num']   = float(especie.get('VALOR OTROS USOS') or 0)
        try:
            especie['IVIM'] = float(especie.get('IVIM') or 0)
        except (ValueError, TypeError):
            especie['IVIM'] = 0
        especie['NOTAS_FORMA']    = especie.get('NOTAS_FORMA', '') or ''
        especie['NOTAS_ECOLOGIA'] = especie.get('NOTAS_ECOLOGIA', '') or ''

  
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

    # ── Datos para el nuevo diseño del reporte ─────────────────────────────
    n = len(especies_obj)

    # a) Composición del portafolio
    data['fecha']       = date.today().strftime('%d/%m/%Y')
    data['n_especies']  = n
    data['n_nativas']   = sum(1 for e in especies_obj if e.get('nativa'))
    data['n_endemicas'] = sum(1 for e in especies_obj if e.get('v64_endemismo'))
    data['n_amenaza']   = sum(1 for e in especies_obj if
                              any(cat in (e.get('v56_amenaza_iucn') or '').upper()
                                  for cat in ('VU', 'EN')))
    ivim_vals  = [float(e.get('IVIM') or 0) for e in especies_obj]
    ivim_valid = [v for v in ivim_vals if v > 0]
    data['ivim_promedio'] = ('{:.1f}'.format(sum(ivim_valid) / len(ivim_valid))
                             if ivim_valid else '—')

    # b) Porcentajes para gráficos de barras
    def _pct(cond):
        return round(sum(1 for e in especies_obj if cond(e)) * 100 / n) if n else 0

    bars_main = [
        ('Maderables',    _pct(lambda e: (e.get('VALOR MADERA') or 0) > 0),    '#85604b'),
        ('Frutales',      _pct(lambda e: (e.get('VALOR FRUTA') or 0) > 0),     '#806377'),
        ('Suelos',        _pct(lambda e: (e.get('VALOR SUELO') or 0) > 0),     '#aa4207'),
        ('Biodiversidad', _pct(lambda e: (e.get('VALOR BIODIVERSIDAD') or 0) > 0), '#00a44d'),
    ]
    bars_otros = [
        ('Artesanías', _pct(lambda e: e.get('v111_artesanias')), '#c8a951'),
        ('Carbón',     _pct(lambda e: e.get('v142_carbon')),     '#c8a951'),
        ('Cosméticos', _pct(lambda e: e.get('v112_cosmeticos')), '#c8a951'),
        ('Fibra',      _pct(lambda e: e.get('v70_fibra')),       '#c8a951'),
        ('Forraje',    _pct(lambda e: e.get('v39_forraje')),     '#c8a951'),
        ('Leña',       _pct(lambda e: e.get('v162_lena')),       '#c8a951'),
        ('Medicinal',  _pct(lambda e: e.get('v113_medicinal')),  '#c8a951'),
        ('Tintes',     _pct(lambda e: e.get('v102_tintes')),     '#c8a951'),
    ]
    data['bar_chart_main']  = _make_bar_svg(bars_main)
    data['bar_chart_otros'] = _make_bar_svg(bars_otros)

    # c) Fauna: pastel de grupos
    fauna_groups = [
        ('Abejas',              'v18_abejas'),
        ('Aves',                'v89_aves'),
        ('Mamíferos\npequeños', 'v90_micromamiferos'),
        ('Mamíferos\nmayores',  'v176_mamiferos_mayores'),
        ('Murciélagos',         'v91_murcielagos'),
        ('Primates',            'v177_primates'),
    ]
    fauna_active = [(lbl, any(e.get(key) for e in especies_obj))
                    for lbl, key in fauna_groups]
    data['fauna_pie'] = _make_fauna_pie_svg(fauna_active, size=260)

    # c) Polinizadores: qué íconos se iluminan
    present_pol = set()
    for e in especies_obj:
        for val in (e.get('v14_polinizadores') or []):
            present_pol.add(_normalize_key(str(val)))

    POLINIZADORES_DEF = [
        ('Abejas',      'abejas',      'assets/img/fauna/abeja.png'),
        ('Abejorros',   'abejorros',   'assets/img/fauna/abejorro.png'),
        ('Avispas',     'avispas',     'assets/img/fauna/avispa.png'),
        ('Chinches',    'chinches',    'assets/img/fauna/chinche.png'),
        ('Colibríes',   'colibries',   'assets/img/fauna/colibri.png'),
        ('Escarabajos', 'escarabajos', 'assets/img/fauna/escarabajo.png'),
        ('Gorgojos',    'gorgojos',    'assets/img/fauna/gorgojo.png'),
        ('Hormigas',    'hormigas',    'assets/img/fauna/hormiga.png'),
        ('Mariposas',   'mariposas',   'assets/img/fauna/mariposa.png'),
        ('Moscas',      'moscas',      'assets/img/fauna/mosca.png'),
        ('Murciélagos', 'murcielagos', 'assets/img/fauna/murcielago.png'),
        ('Polillas',    'polillas',    'assets/img/fauna/polilla.png'),
    ]
    data['polinizadores'] = [
        {'label': lbl, 'img': img, 'active': key in present_pol}
        for lbl, key, img in POLINIZADORES_DEF
    ]

    response = get_tool_pdf_response(request, data=data)
    return response

