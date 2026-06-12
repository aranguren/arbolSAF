"""
Migration 0051: divide el texto de introducción en dos campos
(antes y después del diagrama codiseño) porque CKEditor 4 elimina SVG.
"""
from django.db import migrations
import ckeditor.fields


TEXTO_INTRO_ANTES = """<h3>Sistema Integrado de Apoyo a la Selección de Árboles para sistemas Agroforestales: ÁrbolSAF</h3>
<p>
  Un sistema agroforestal (SAF) con enfoque agroecológico es una asociación entre cultivos principales
  (anuales y/o perennes) y especies de asocio, generalmente árboles y palmeras, que establecidos bajo
  diferentes arreglos espaciales y temporales proveen una serie de beneficios monetarios, de seguridad
  alimentaria y ambientales a lo largo de su desarrollo.
</p>
<p>
  La implementación de un SAF requiere una importante inversión de recursos y tiempo, por lo que en su
  diseño y planificación es necesario considerar varias etapas.
</p>"""


TEXTO_INTRO_DESPUES = """<div class="mt-4">
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
</div>"""


def split_intro(apps, schema_editor):
    Configuracion = apps.get_model('arbolsaf', 'Configuracion')
    obj, _ = Configuracion.objects.get_or_create(pk=1)
    obj.texto_seccion_arbolsaf = TEXTO_INTRO_ANTES
    obj.texto_intro_despues = TEXTO_INTRO_DESPUES
    obj.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0050_configuracion_metodos_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='texto_intro_despues',
            field=ckeditor.fields.RichTextField(
                default='',
                verbose_name='Introducción — texto DESPUÉS del diagrama',
            ),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_arbolsaf',
            field=ckeditor.fields.RichTextField(
                default='',
                verbose_name='Introducción — texto ANTES del diagrama',
            ),
        ),
        migrations.RunPython(split_intro, noop),
    ]
