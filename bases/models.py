from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

# se crean los parametros que tendra la tabla estado,fechaCreacion,fechaModificacion,usuarioCreado,usuarioModificado
class Modelado(models.Model):
    estado = models.BooleanField(default=True)

    # se actualiza unicamente cuando el registro se cree
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    #se coloca cada vez que haya una modificacion
    fechaModificacion = models.DateTimeField(auto_now=True)

    usuarioCreado = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarioModificado = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True


class Modelado2(models.Model):
    estado = models.BooleanField(default=True)

    # se actualiza unicamente cuando el registro se cree
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    #se coloca cada vez que haya una modificacion
    fechaModificacion = models.DateTimeField(auto_now=True)

    usuarioCreado = UserForeignKey(auto_user_add=True, related_name='+')
    usuarioModificado = UserForeignKey(auto_user=True, related_name='+')

    class Meta:
        abstract=True