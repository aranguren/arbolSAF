# Generated by Django 3.2.6 on 2022-12-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0007_alter_variabletypefamilymodel_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='variablemodel',
            name='chequeo',
            field=models.BooleanField(default=False, verbose_name='Chequeada?'),
        ),
    ]
