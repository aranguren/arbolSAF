# Generated by Django 3.2.6 on 2023-06-19 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0017_auto_20230616_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='variablemodel',
            name='valores_cualitativos',
            field=models.ManyToManyField(related_name='_arbolsaf_variablemodel_valores_cualitativos_+', to='arbolsaf.VariableTypeOption', verbose_name='Valores cualitativos'),
        ),
    ]
