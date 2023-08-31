# Generated by Django 3.2.6 on 2023-08-24 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0032_bitacora'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bitacora',
            options={'managed': True, 'verbose_name': 'Bitacora', 'verbose_name_plural': 'Bitacora'},
        ),
        migrations.AddField(
            model_name='bitacora',
            name='asunto',
            field=models.CharField(default='hola', max_length=255, verbose_name='Asunto'),
            preserve_default=False,
        ),
    ]