# Generated by Django 3.0.4 on 2020-04-02 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0002_comprasdetalle_comprasencabezado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasencabezado',
            name='fecha_compra',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='comprasencabezado',
            name='observacion',
            field=models.TextField(null=True),
        ),
    ]
