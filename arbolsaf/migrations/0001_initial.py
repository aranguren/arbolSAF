# Generated by Django 3.2.6 on 2022-12-06 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('familia', models.CharField(max_length=50, verbose_name='familia')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Familia',
                'verbose_name_plural': 'Familias',
                'db_table': 'arbolsaf_family',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GenderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('genero', models.CharField(max_length=50, verbose_name='género')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Género',
                'verbose_name_plural': 'Género',
                'db_table': 'arbolsaf_gender',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MeasureUnitTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('abreviatura', models.CharField(max_length=50, verbose_name='abreviatura')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True, verbose_name='nombre')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Tipo unidad de medidas',
                'verbose_name_plural': 'Tipos unidad de medidas',
                'db_table': 'arbolsaf_measure_unit_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ReferenceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('fuente_final', models.CharField(max_length=255, verbose_name='referencia')),
                ('cod_cita', models.CharField(max_length=50, unique=True, verbose_name='código cita')),
                ('referencia', models.TextField(blank=True, null=True, verbose_name='fuente')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Referencia',
                'verbose_name_plural': 'Referencias',
                'db_table': 'arbolsaf_reference',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SpeciesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('cod_esp', models.CharField(max_length=50, unique=True, verbose_name='Código especie')),
                ('taxonid_wfo', models.CharField(max_length=50, verbose_name='Taxon ID WFO')),
                ('nombre_comun', models.CharField(max_length=255, verbose_name='Nombre comun')),
                ('nombre_cientifico', models.CharField(max_length=255, verbose_name='Nombre científico')),
                ('nombre_cientifico_completo', models.CharField(max_length=255, verbose_name='Nombre científico completo')),
                ('epiteto', models.CharField(max_length=50, verbose_name='Epíteto')),
                ('variedad_subespecie', models.CharField(blank=True, max_length=50, null=True, verbose_name='Variedad/Subespecie')),
                ('autor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Autor')),
                ('nativa', models.BooleanField(verbose_name='Nativa?')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.familymodel', verbose_name='Familia')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.gendermodel', verbose_name='Género')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Especie',
                'verbose_name_plural': 'Especies',
                'db_table': 'arbolsaf_species',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VariableTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('cod_var', models.CharField(max_length=50, verbose_name='código variable')),
                ('tipo_variables', models.CharField(blank=True, choices=[('numerico', 'Valor numérico'), ('texto', 'Valor texto'), ('rango', 'Rango'), ('cualitativo', 'Cualitativo'), ('boolean', 'Boolean')], max_length=50, null=True, verbose_name='tipo variable')),
                ('variable', models.CharField(max_length=255, verbose_name='variable')),
                ('niveles_categoricos', models.TextField(verbose_name='Niveles categóricos')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='descripción')),
                ('min', models.FloatField(blank=True, null=True, verbose_name='Valor mínimo')),
                ('max', models.FloatField(blank=True, null=True, verbose_name='Valor máximo')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('unidad_medida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arbolsaf.measureunittypemodel', verbose_name='Unidad medida')),
            ],
            options={
                'verbose_name': 'Tipo de variable',
                'verbose_name_plural': 'Tipos de variable',
                'db_table': 'arbolsaf_variable_type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VariableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('valor_numerico', models.FloatField(blank=True, null=True, verbose_name='Valor numérico')),
                ('rango_superior', models.FloatField(blank=True, null=True, verbose_name='rango superior')),
                ('rango_inferior', models.FloatField(blank=True, null=True, verbose_name='rango inferior')),
                ('valor_texto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Valor texto')),
                ('valor_boolean', models.BooleanField(default=False, null=True, verbose_name='Verdadero?')),
                ('valor_general', models.CharField(blank=True, max_length=255, null=True, verbose_name='Valor general')),
                ('categoria', models.CharField(blank=True, max_length=50, null=True, verbose_name='categoria')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='arbolsaf.speciesmodel', verbose_name='Especie')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.referencemodel', verbose_name='Referencia')),
                ('tipo_variable', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.variabletypemodel', verbose_name='Tipo Variable')),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variable',
                'db_table': 'arbolsaf_variable',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SynonymousModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('sinonimo', models.CharField(max_length=255, verbose_name='sinónimo')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sinonimos', to='arbolsaf.speciesmodel', verbose_name='Especie')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Sinónimo',
                'verbose_name_plural': 'Sinónimo',
                'db_table': 'arbolsaf_synonymous',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PriorityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('prioridad', models.CharField(max_length=50, verbose_name='nombre')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbolsaf.speciesmodel', verbose_name='Especie')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbolsaf.referencemodel', verbose_name='Referencia')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbolsaf.variablemodel', verbose_name='Variable')),
            ],
            options={
                'verbose_name': 'Prioridad',
                'verbose_name_plural': 'Prioridad',
                'db_table': 'arbolsaf_priority',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FunctiomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Función',
                'verbose_name_plural': 'Funciones',
                'db_table': 'arbolsaf_function',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DistributionMenaceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbolsaf.speciesmodel', verbose_name='')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('tipo_variable', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.variabletypemodel', verbose_name='Variable')),
            ],
            options={
                'verbose_name': 'Amenaza distribución',
                'verbose_name_plural': 'Amenazas distribución',
                'db_table': 'arbolsaf_distribution_menace',
                'managed': True,
            },
        ),
    ]
