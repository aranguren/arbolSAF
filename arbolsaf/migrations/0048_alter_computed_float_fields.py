from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0047_variabletypemodel_uso_herramienta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciesmodel',
            name='valor_otros_usos',
            field=models.FloatField(default=0.0, verbose_name='Valor para Otros usos'),
        ),
        migrations.AlterField(
            model_name='speciesmodel',
            name='valor_biodiversidad',
            field=models.FloatField(default=0.0, verbose_name='Valor para Biodiversidad'),
        ),
        migrations.AlterField(
            model_name='speciesmodel',
            name='valor_suelo',
            field=models.FloatField(default=0.0, verbose_name='Valor para el Suelo'),
        ),
    ]
