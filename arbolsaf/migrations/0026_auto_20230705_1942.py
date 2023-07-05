# Generated by Django 3.2.6 on 2023-07-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0025_auto_20230704_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciesmodel',
            name='indice_multiuso',
            field=models.FloatField(default=0.0, editable=False, verbose_name='Índice Multiuso'),
        ),
        migrations.AlterField(
            model_name='speciesmodel',
            name='indice_valor_uso_relativo',
            field=models.FloatField(default=0.0, editable=False, verbose_name='Índice de valor de uso relativo'),
        ),
    ]
