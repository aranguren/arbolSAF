# Generated by Django 3.2.6 on 2023-09-05 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0038_alter_speciesmodel_taxonid_wfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variabletypemodel',
            name='unidad_medida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arbolsaf.measureunittypemodel', verbose_name='Unidad de medida'),
        ),
    ]
