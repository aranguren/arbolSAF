"""
Migration 0053:
 1. Fusiona texto_metodos_versiones_antes + imagen arbolsafv1.png +
    texto_metodos_versiones_despues en un solo campo texto_metodos_versiones.
 2. Elimina imagen_arbolsaf_v1 (ya embebida como <img> en el texto).
 3. Prepend <h2>Título</h2> al inicio de cada campo de las pestañas para
    que el título sea editable desde el admin de Django.
"""
from django.db import migrations, models
import ckeditor.fields


IMAGE_V1 = (
    '<p style="text-align:center;margin:1.5rem 0;">'
    '<img src="/static/assets/img/arbolsafv1.png" '
    'alt="ÁrbolSAF v.1.0-beta (2023)" '
    'style="max-width:100%;height:auto;">'
    '</p>'
)

TITLES = {
    'texto_metodos_seleccion':              '<h2>Selección de especies</h2>',
    'texto_metodos_categorizacion':         '<h2>Categorización &amp; IVIM</h2>',
    'texto_metodos_datos':                  '<h2>Datos y referencias</h2>',
    'texto_seccion_descargo_responsabilidad': '<h2>Descargo de responsabilidad</h2>',
}
TITLE_VERSIONES = '<h2>Versiones y créditos</h2>'


def apply_changes(apps, schema_editor):
    Configuracion = apps.get_model('arbolsaf', 'Configuracion')
    obj, _ = Configuracion.objects.get_or_create(pk=1)

    # 1. Fusionar versiones
    antes   = obj.texto_metodos_versiones_antes or ''
    despues = obj.texto_metodos_versiones_despues or ''
    obj.texto_metodos_versiones = TITLE_VERSIONES + antes + IMAGE_V1 + despues

    # 2. Agregar títulos a los demás campos
    for field, title in TITLES.items():
        current = getattr(obj, field) or ''
        setattr(obj, field, title + current)

    obj.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0052_merge_intro_fields'),
    ]

    operations = [
        # Añadir nuevo campo unificado de versiones
        migrations.AddField(
            model_name='configuracion',
            name='texto_metodos_versiones',
            field=ckeditor.fields.RichTextField(
                default='',
                verbose_name='Métodos: Versiones y créditos',
            ),
        ),

        # Migrar contenido (fusión + títulos)
        migrations.RunPython(apply_changes, noop),

        # Eliminar los campos separados
        migrations.RemoveField(model_name='configuracion', name='texto_metodos_versiones_antes'),
        migrations.RemoveField(model_name='configuracion', name='texto_metodos_versiones_despues'),
        migrations.RemoveField(model_name='configuracion', name='imagen_arbolsaf_v1'),
    ]
