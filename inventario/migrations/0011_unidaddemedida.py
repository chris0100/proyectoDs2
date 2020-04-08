# Generated by Django 3.0.4 on 2020-03-29 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0010_marca'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnidadDeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('usuarioModificado', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(help_text='Descripcion de la unidad de medida', max_length=100, unique=True)),
                ('usuarioCreado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Unidades de Medida',
            },
        ),
    ]
