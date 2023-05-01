# Generated by Django 3.2.6 on 2023-04-26 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0009_auto_20230426_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariableTypeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('tipo_variable', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.variabletypemodel', verbose_name='Tipo Variable')),
            ],
            options={
                'verbose_name': 'Opción Tipo Variable',
                'verbose_name_plural': 'Opciones Tipo Variable',
                'db_table': 'arbolsaf_variable_type_option',
                'managed': True,
            },
        ),
    ]
