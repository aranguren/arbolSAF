# Generated by Django 3.2.6 on 2023-09-04 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0036_auto_20230828_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciesmodel',
            name='taxonid_wfo',
            field=models.CharField(max_length=50, unique=True, verbose_name='Taxon ID WFO'),
        ),
    ]