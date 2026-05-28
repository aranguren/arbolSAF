from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0048_alter_computed_float_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speciesmodel',
            name='valor_microclima',
        ),
        migrations.RemoveField(
            model_name='speciesmodel',
            name='valor_microclima_category',
        ),
        migrations.RemoveField(
            model_name='speciesmodel',
            name='indice_multiuso',
        ),
        migrations.RemoveField(
            model_name='speciesmodel',
            name='indice_valor_uso_relativo',
        ),
    ]
