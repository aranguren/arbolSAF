# Generated by Django 3.2.6 on 2023-08-25 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0034_auto_20230825_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speciesmodel',
            name='imagen',
        ),
        migrations.CreateModel(
            name='ImageSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255, verbose_name='Descripción')),
                ('imagen', models.ImageField(upload_to='imagenes_especie', verbose_name='Imagen')),
                ('especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='arbolsaf.speciesmodel', verbose_name='Especie')),
            ],
            options={
                'verbose_name': 'Imagen Specie',
                'verbose_name_plural': 'Imágen Specie',
                'db_table': 'arbolsaf_imagen_species',
                'managed': True,
            },
        ),
    ]
