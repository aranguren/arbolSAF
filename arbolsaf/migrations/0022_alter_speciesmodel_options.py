# Generated by Django 3.2.6 on 2023-06-22 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0021_remove_variablemodel_valor_cualitativo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='speciesmodel',
            options={'managed': True, 'ordering': ['nombre_cientifico'], 'verbose_name': 'Especie', 'verbose_name_plural': 'Especies'},
        ),
    ]
