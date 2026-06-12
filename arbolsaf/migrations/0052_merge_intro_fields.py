"""
Migration 0052: fusiona texto_seccion_arbolsaf + texto_intro_despues en un
solo campo, con el diagrama codiseño embebido como <img> entre los dos bloques.
El diagrama ya está guardado como imagen estática en:
  apps/static/assets/img/codiseno-diagram.png
"""
from django.db import migrations
import ckeditor.fields


DIAGRAM_IMG = (
    '<p style="text-align:center;margin:1.75rem 0;">'
    '<img src="/static/assets/img/codiseno-diagram.png" '
    'alt="Etapas de codiseño de un SAF" '
    'style="max-width:100%;height:auto;">'
    '</p>'
)


def merge_intro(apps, schema_editor):
    Configuracion = apps.get_model('arbolsaf', 'Configuracion')
    obj, _ = Configuracion.objects.get_or_create(pk=1)
    antes = obj.texto_seccion_arbolsaf or ''
    despues = obj.texto_intro_despues or ''
    obj.texto_seccion_arbolsaf = antes + DIAGRAM_IMG + despues
    obj.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0051_configuracion_intro_split'),
    ]

    operations = [
        # 1. Fusionar contenido antes de borrar el campo
        migrations.RunPython(merge_intro, noop),

        # 2. Eliminar el campo separado
        migrations.RemoveField(
            model_name='configuracion',
            name='texto_intro_despues',
        ),

        # 3. Renombrar el campo para reflejar que ya no hay división
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_arbolsaf',
            field=ckeditor.fields.RichTextField(
                default='',
                verbose_name='Introducción',
            ),
        ),
    ]
