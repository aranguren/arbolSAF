# Generated by Django 3.2.6 on 2023-06-14 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0014_alter_speciesmodel_taxonid_wfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variablemodel',
            name='tipo_variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.variabletypemodel', verbose_name='Variable'),
        ),
    ]
