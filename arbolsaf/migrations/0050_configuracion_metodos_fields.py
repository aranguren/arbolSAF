"""
Migration 0050: añade campos de Introducción y pestañas de Métodos al modelo Configuracion,
y los puebla con el contenido actualmente hardcodeado en las templates.
"""
from django.db import migrations, models
import ckeditor.fields


# ──────────────────────────────────────────────────────────────────────────────
# Contenido inicial de cada sección (extraído de los templates)
# ──────────────────────────────────────────────────────────────────────────────

TEXTO_INTRO = """<div class="intro-content">
  <h3>Sistema Integrado de Apoyo a la Selección de Árboles para sistemas Agroforestales: ÁrbolSAF</h3>
  <p>
    Un sistema agroforestal (SAF) con enfoque agroecológico es una asociación entre cultivos principales
    (anuales y/o perennes) y especies de asocio, generalmente árboles y palmeras, que establecidos bajo
    diferentes arreglos espaciales y temporales proveen una serie de beneficios monetarios, de seguridad
    alimentaria y ambientales a lo largo de su desarrollo.
  </p>
  <p>
    La implementación de un SAF requiere una importante inversión de recursos y tiempo, por lo que en su
    diseño y planificación es necesario considerar varias etapas.
  </p>

  <div class="codiseno-diagram">
    <div class="codiseno-diagram__title">Etapas de codiseño de un SAF</div>
    <div class="codiseno-diagram__flow">
      <div class="codiseno-box codiseno-box--outline">
        Diagnóstico integral del contexto, las capacidades, los objetivos y recursos de la familia/agricultor
      </div>
      <div class="codiseno-arrow" aria-hidden="true">
        <svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
          <polygon points="4,12 22,12 22,6 32,18 22,30 22,24 4,24"/>
        </svg>
      </div>
      <div class="codiseno-box codiseno-box--filled">
        Selección de especies y arreglo espacial y temporal considerando las especies de asocio
      </div>
      <div class="codiseno-arrow" aria-hidden="true">
        <svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
          <polygon points="4,12 22,12 22,6 32,18 22,30 22,24 4,24"/>
        </svg>
      </div>
      <div class="codiseno-box codiseno-box--outline">
        Evaluación de los costos y beneficios económicos y ambientales que requiere y proveerá el SAF
      </div>
    </div>
  </div>

  <div class="mt-4">
    <h2>ÁrbolSAF como herramienta de apoyo al codiseño</h2>
    <p>
      ÁrbolSAF es un sistema digital integrado diseñado para apoyar la <strong>SELECCIÓN DE ESPECIES DE ASOCIO</strong> que
      formarán parte de un sistema agroforestal.
    </p>
    <p>
      Cuenta con amplia información de un portafolio de árboles y palmeras. Su plataforma está compuesta
      de una base de datos relacional, un motor de análisis y una interfaz web.
    </p>
    <ul>
      <li>
        <strong>Su base de datos</strong> integra 84 especies de árboles y palmeras con sus respectivos datos de 165 tipos
        de variables morfológicas, climáticas, ecológicas, edáficas y de usos.
      </li>
      <li>
        <strong>Su interfaz web</strong> que sobre su base de datos evalúa y valora las especies usando su <strong>motor de análisis</strong>
        que categoriza las especies por usos y funciones ambientales y brinda información de sus requerimientos de clima,
        suelo y rasgos ecológicos y morfológicos.
      </li>
    </ul>
  </div>

  <div class="mt-4">
    <h2>Lo que encuentras en la interfaz-web</h2>
    <ul>
      <li>Un menú completo del portafolio de especies.</li>
      <li>Pasos secuenciales para armar tu lista o ensamble de especies (pasos 1 al 3).</li>
      <li>Evaluación visual de tu ensamble armado: los productos, servicios y la contribución
        a la conservación de la biodiversidad que este ensamble apoyará (Paso 4).</li>
      <li>La impresión de la consulta como un reporte.</li>
      <li>La plataforma de bases de datos de acceso restringido.</li>
    </ul>
    <p><i>Más detalles sobre la base de datos y categorización de las especies en la sección de metodología.</i></p>
  </div>

  <div class="mt-4">
    <h2>Otras herramientas digitales</h2>
    <p>
      CIFOR-ICRAF desarrolla varias herramientas de apoyo al codiseño de SAF. En la plataforma de DecisiónSAF encontrarás
      las herramientas como planSAF que te guía para realizar el diagnóstico, analiSAF y CarbonSAF que apoya para llevar
      adelante evaluaciones de los costos/beneficio económicos y ambientales (captura de carbono) de tu diseño de SAF.
    </p>
  </div>
</div>"""


TEXTO_METODOS_SELECCION = """<ul>
  <li>El portafolio de especies está conformado por 84 especies, de las cuales 70 son nativas del Perú y 14 introducidas. Estas especies representan un subconjunto priorizado de
    164 especies de árboles y palmeras seleccionadas con base en criterios de frecuencia de registro en sistemas agroforestales, interés de los productores, importancia productiva,
    valor ecológico y experiencia técnica del equipo de trabajo.
  </li>
  <li>Para la construcción de este portafolio se utilizaron diversas fuentes de información. En primer lugar, se realizaron 224 encuestas a hogares de agricultores y familias con
    sistemas agroforestales de cacao y palma. En estas entrevistas se registraron tanto las especies presentes en los sistemas agroforestales como aquellas que los productores
    manifestaron interés en establecer. Las encuestas se llevaron a cabo en 11 distritos de la Amazonía peruana: Alexander von Humboldt, Curimaná, Irazola, Neshuya y Padre Abad,
    en la provincia de Padre Abad (Ucayali); Campo Verde, en la provincia de Coronel Portillo (Ucayali); y Tournavista y Yuyapichis, en la provincia de Puerto Inca (Huánuco).
    La lista de especies obtenida fue posteriormente complementada y corregida taxonómicamente mediante muestreos de campo, apoyados con colectas de material vegetal y registros
    fotográficos.
  </li>
  <li>En segundo lugar, se revisaron publicaciones científicas sobre sistemas agroforestales en la Amazonía peruana, seleccionándose aquellas especies reportadas en tres o más
    estudios. Asimismo, se incorporó la experiencia y conocimiento técnico de especialistas de campo involucrados en el diseño y establecimiento de sistemas agroforestales.
  </li>
  <li>La selección de especies también fue respaldada por diversas bases de datos recopiladas por ICRAF en proyectos previos, identificadas como fuentes de alta relevancia
    para este tipo de sistemas.
  </li>
  <li>En una segunda fase del proyecto se incorporaron 20 especies adicionales provenientes de parcelas establecidas por técnicos de ICRAF en el departamento de San Martín.
    Estas especies fueron registradas en inventarios agroforestales y priorizadas por el equipo técnico de ICRAF según su relevancia productiva, ecológica y de uso local.
  </li>
  <li>La validación taxonómica y la estandarización de la nomenclatura científica se realizaron utilizando la plataforma <a href="https://www.worldfloraonline.org/" target="_blank">World Flora Online</a>, empleada como referencia
    internacional para nombres botánicos aceptados y sinonimias.
  </li>
</ul>"""


TEXTO_METODOS_CATEGORIZACION = """<p>Las especies del portafolio fueron clasificadas en cinco categorías funcionales según los productos, usos y servicios ecosistémicos que proporcionan: maderables,
  frutales, biodiversidad, suelos y otros usos. Cada categoría fue construida a partir de variables ecológicas, productivas y de aprovechamiento tradicional.
</p>
<p>La metodología combina tres enfoques complementarios:</p>
<ol style="list-style-type: lower-alpha;">
  <li><strong>Enfoque jerárquico</strong>, aplicado a categorías donde ciertos atributos tienen prioridad sobre otros, como madera y fruta.</li>
  <li><strong>Enfoque aditivo</strong>, utilizado en biodiversidad, suelos y otros usos, donde múltiples variables contribuyen de manera acumulativa al valor final.</li>
  <li><strong>Estandarización</strong>, mediante el reescalamiento de algunos indicadores para llevarlos a rangos comparables dentro del índice.</li>
</ol>

<p>Las categorías maderables, frutales, suelos y otros usos fueron expresadas en escalas de 0 a 3, mientras que biodiversidad fue reescalada a una escala de 0 a 6 debido
  a su mayor peso ecológico dentro de la evaluación.
</p>

<p>El Índice de Valor de Importancia Multifuncional (IVIM) corresponde a la suma de los valores obtenidos por cada especie en las cinco categorías evaluadas. De esta manera,
  el IVIM integra simultáneamente atributos productivos, ecológicos y funcionales, permitiendo identificar especies con mayor potencial multifuncional dentro de sistemas
  agroforestales y procesos de restauración.
</p>

<div class="mt-4">
  <p class="tool-subsection-title">Categoría maderables (0–3)</p>
  <p>Evalúa el potencial de aprovechamiento forestal de las especies según la calidad y relevancia de su madera.</p>
  <p>La clasificación sigue una lógica jerárquica:</p>
  <ol>
    <li><strong>Valor 3:</strong> especies de alta prioridad forestal y comercial.</li>
    <li><strong>Valor 2:</strong> especies con atributos maderables relevantes, pero de menor prioridad.</li>
    <li><strong>Valor 1:</strong> especies con usos maderables secundarios o locales.</li>
    <li><strong>Valor 0:</strong> especies sin registros maderables relevantes.</li>
  </ol>
</div>

<div class="mt-4">
  <p class="tool-subsection-title">Categoría frutal (0–3)</p>
  <p>Evalúa el potencial alimenticio y la vocación frutal de las especies dentro de sistemas agroforestales.</p>
  <p>La clasificación considera:</p>
  <ol>
    <li><strong>Valor 3:</strong> especies con vocación frutal reconocida.</li>
    <li><strong>Valor 2:</strong> especies con semillas utilizadas para consumo humano.</li>
    <li><strong>Valor 1:</strong> especies con frutos consumidos localmente o de manera complementaria.</li>
    <li><strong>Valor 0:</strong> especies sin registros de uso alimenticio.</li>
  </ol>
</div>

<div class="mt-4">
  <p class="tool-subsection-title">Categoría biodiversidad (0–6)</p>
  <p>Integra variables de conservación y relaciones ecológicas de las especies.</p>
  <p>El puntaje considera:</p>
  <ol>
    <li>condición de especie nativa o endémica,</li>
    <li>inclusión en CITES,</li>
    <li>categoría de amenaza según la IUCN,</li>
    <li>y registros de interacción con seis grupos de fauna: aves, micromamíferos, abejas, murciélagos, primates y mamíferos grandes.</li>
  </ol>

  <p>La categoría IUCN fue ponderada de la siguiente manera:</p>
  <ol>
    <li>En Peligro (EN) = 3 puntos,</li>
    <li>Vulnerable (VU) = 2 puntos,</li>
    <li>Casi Amenazada (NT) = 1 punto.</li>
  </ol>

  <p>El valor máximo posible es 12 y posteriormente fue reescalado a una escala de 0 a 6 para otorgar mayor peso relativo a la biodiversidad dentro del IVIM.</p>
</div>

<div class="mt-4">
  <p class="tool-subsection-title">Categoría suelos (0–3)</p>
  <p>Evalúa la contribución de las especies al mantenimiento y recuperación de las propiedades físicas, químicas y biológicas del suelo.</p>
  <p>El indicador considera:</p>
  <ol>
    <li>mejora de estructura del suelo,</li>
    <li>presencia de nódulos asociados a fijación biológica de nitrógeno,</li>
    <li>aporte de materia orgánica,</li>
    <li>recuperación de fertilidad,</li>
    <li>tolerancia a sequía,</li>
    <li>y asociaciones con bacterias o micorrizas.</li>
  </ol>

  <p>El tipo de follaje fue ponderado según su potencial de aporte de materia orgánica:</p>
  <ol>
    <li>caducifolio = 2 puntos,</li>
    <li>semicaducifolio = 1 punto.</li>
  </ol>

  <p>El valor máximo bruto fue posteriormente reescalado a una escala de 0 a 3.</p>
</div>

<div class="mt-4">
  <p class="tool-subsection-title">Categoría otros usos (0–3)</p>
  <p>Incluye aplicaciones complementarias no maderables ni alimenticias.</p>
  <p>Los usos fueron agrupados según su importancia relativa:</p>
  <ol>
    <li><strong>Valor 3:</strong> leña, carbón y forraje.</li>
    <li><strong>Valor 2:</strong> usos medicinales y artesanales.</li>
    <li><strong>Valor 1:</strong> cosméticos, repelentes, tintes y fibras.</li>
    <li><strong>Valor 0:</strong> ausencia de registros de uso adicional.</li>
  </ol>
</div>

<p>El valor final corresponde a la suma de categorías presentes, posteriormente ajustada para mantener compatibilidad con la escala general del IVIM.</p>"""


TEXTO_METODOS_DATOS = """<p class="tool-subsection-title">Consideraciones sobre la información presentada en la plataforma</p>
<p>En el paso 2 se presentan datos relacionados con los requerimientos climáticos y edáficos de las especies, mientras que en el paso 3 se muestran
  características morfológicas y ecológicas de las especies seleccionadas por el usuario.
</p>
<p>Al pasar el cursor sobre cada dato, es posible visualizar la fuente bibliográfica o documental de donde fue obtenida la información.</p>
<p>En algunos casos pueden existir diferencias o aparentes contradicciones entre fuentes. Esto se debe a que una misma especie puede presentar
  variaciones en sus requerimientos, comportamiento ecológico o características morfológicas dependiendo de la región geográfica, las condiciones
  ambientales o el contexto en el que fue estudiada. Por ello, la información presentada debe ser interpretada como una referencia técnica de apoyo
  y complementarse con la experiencia de técnicos de campo, conocimiento local y otras fuentes de información relevantes.
</p>
<p>En el caso de los grupos de fauna utilizados en la categoría de biodiversidad, las búsquedas bibliográficas priorizaron estudios realizados en
  la Amazonía peruana, y luego en el resto de las regiones Amazónicas. Sin embargo, minoritariamente, también se incorporó información de otras
  regiones tropicales, incluyendo algunos estudios realizados en África, con el fin de ampliar el entendimiento de las relaciones ecológicas entre
  las especies vegetales y distintos grupos de fauna.
</p>
<p>El equipo de Árbol SAF continúa realizando procesos de curaduría, validación y actualización de datos con el objetivo de mejorar progresivamente
  las futuras versiones de la interfaz y de la plataforma de información.
</p>
<p>Si tiene observaciones, correcciones o información adicional que pueda contribuir a mejorar la calidad de la plataforma, puede comunicarse con: [correo o contacto].</p>"""


TEXTO_VERSIONES_ANTES = """<p class="tool-subsection-title">ÁrbolSAF v.1.1 (2026)</p>
<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Principales mejoras</p>
<ul>
  <li>Se incorporaron 18 nuevas especies al portafolio, incluyendo información morfológica, fisiológica, ecológica, requerimientos ambientales y usos.</li>
  <li>Se amplió la recopilación de información sobre interacciones ecológicas con distintos grupos de fauna, priorizando literatura relevante para la Amazonía peruana (Reporte interno de J. Cornelius, 2025).</li>
  <li>Se desarrollaron nuevas variables para mejorar la representación de categorías de amenaza y relaciones ecológicas dentro de los indicadores de biodiversidad.</li>
  <li>La interfaz fue ampliada mediante la incorporación de tarjetas con el portafolio completo de especies disponibles en ÁrbolSAF.</li>
  <li>Se mejoró la información presentada en las categorías de selección de especies y se ajustaron tanto los criterios de categorización como los valores asignados a cada especie dentro del IVIM.</li>
  <li>Se añadió un nuevo paso (Paso 4) orientado a visibilizar características del conjunto de especies seleccionadas por el usuario, particularmente relacionadas con su contribución a la biodiversidad a escala de parcela y paisaje.</li>
  <li>Los reportes generados por consulta fueron ampliados para incorporar la información correspondiente a los nuevos pasos y funcionalidades de la plataforma.</li>
</ul>

<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Financiamiento</p>
<p>Las mejoras y ampliaciones de la versión 1.1 fueron desarrolladas en el marco del proyecto "Biodiversidad para ecosistemas resilientes en paisajes multifuncionales", financiado por el GAC
  y parte del programa Multifunctional Landscapes (MFL) del CGIAR.
</p>

<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Equipo de trabajo</p>
<p>
  <strong>Plataforma de datos:</strong> Geovana Carreño-Rocabado y Katherine Ramos.<br>
  <strong>Herramienta interactiva:</strong> Geovana Carreño-Rocabado, Lourdes Quiñones y Valentina Robiglio.<br>
  <strong>Desarrollo tecnológico:</strong> Equipo de Deneb Latinoamericana Inc.
</p>

<p class="tool-subsection-title">ÁrbolSAF v.1.0-beta (2023)</p>
<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Principales características</p>
<p>La primera versión pública de ÁrbolSAF incluyó un portafolio inicial de 62 especies y una interfaz interactiva que permitía al usuario construir listas de especies según categorías funcionales
  y ajustar la selección en función de requerimientos climáticos, edáficos, morfológicos y ecológicos.
</p>"""


TEXTO_VERSIONES_DESPUES = """<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Financiamiento</p>
<p>El desarrollo de ÁrbolSAF v.1.0-beta (2023) fue realizado en el marco de los proyectos:</p>
<ul>
  <li>"Cacao Agroecológico Regenerativo", financiado por el Fondo Francés para el Medio Ambiente Mundial (FFEM).</li>
  <li>"Paisajes Productivos Sostenibles de la Amazonía Peruana", financiado por el Fondo para el Medio Ambiente Mundial (GEF).</li>
  <li>Proyecto Agrofor financiado por Iniciativa Internacional de Clima y Bosques de Noruega (NICFI).</li>
</ul>

<p style="font-style:italic;font-weight:600;margin-bottom:0.3rem;">Equipo de trabajo</p>
<p>
  <strong>Plataforma de datos:</strong> Geovana Carreño-Rocabado, Katherine Ramos, Fred Ramírez y Jean Valverde.<br>
  <strong>Herramienta interactiva:</strong> Geovana Carreño-Rocabado, Lourdes Quiñones, Alejandra Visscher y Valentina Robiglio.<br>
  <strong>Desarrollo tecnológico:</strong> Equipo de Deneb Latinoamericana Inc.
</p>"""


TEXTO_DESCARGO = """<p>La información contenida en este sitio web o aplicación, incluidas las hojas informativas asociadas, es sólo para fines de información general.
  Con respecto al material o la información contenida en este sitio web o aplicación, las organizaciones o personas involucradas en la creación de la
  herramienta interactiva ÁrbolSAF no hacen declaraciones o garantías de ningún tipo, expresas o implícitas (incluyendo la idoneidad para un propósito
  particular) y no aceptan ninguna responsabilidad legal por la exactitud, fiabilidad, adecuación, disponibilidad, integridad o utilidad de cualquier
  información, producto o proceso divulgado. Por lo tanto, el uso del material o la información contenidos en este sitio web o aplicación corre estrictamente
  por su cuenta y riesgo.
</p>"""


def populate_configuracion(apps, schema_editor):
    Configuracion = apps.get_model('arbolsaf', 'Configuracion')
    obj, _ = Configuracion.objects.get_or_create(pk=1)
    obj.texto_seccion_arbolsaf = TEXTO_INTRO
    obj.texto_metodos_seleccion = TEXTO_METODOS_SELECCION
    obj.texto_metodos_categorizacion = TEXTO_METODOS_CATEGORIZACION
    obj.texto_metodos_datos = TEXTO_METODOS_DATOS
    obj.texto_metodos_versiones_antes = TEXTO_VERSIONES_ANTES
    obj.texto_metodos_versiones_despues = TEXTO_VERSIONES_DESPUES
    obj.texto_seccion_descargo_responsabilidad = TEXTO_DESCARGO
    obj.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0049_remove_microclima_and_indices'),
    ]

    operations = [
        # ── Campos nuevos ──────────────────────────────────────────────
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_seleccion',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Selección de especies'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_categorizacion',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Categorización & IVIM'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_datos',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Datos y referencias (texto introductorio)'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_versiones_antes',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Versiones y créditos (antes de la imagen)'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_versiones_despues',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Versiones y créditos (después de la imagen)'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='imagen_arbolsaf_v1',
            field=models.ImageField(
                blank=True, null=True,
                upload_to='configuracion/',
                verbose_name='Imagen ÁrbolSAF v1.0 (sección Versiones)',
            ),
        ),
        # ── Actualizar etiquetas de campos existentes ──────────────────
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_arbolsaf',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Introducción (panel de bienvenida)'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_descargo_responsabilidad',
            field=ckeditor.fields.RichTextField(default='', verbose_name='Métodos: Descargo de responsabilidad'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_creditos',
            field=ckeditor.fields.RichTextField(default='', verbose_name='(legado) Créditos'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_agradecimientos',
            field=ckeditor.fields.RichTextField(default='', verbose_name='(legado) Agradecimientos'),
        ),
        # ── Poblar con el contenido actual de las templates ────────────
        migrations.RunPython(populate_configuracion, noop),
    ]
