from django.db import models
from bases.models import Modelado
from inventario.models import Producto

#para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

# SE CREA EL MODELO PROVEEDOR
class Proveedor(Modelado):
    descripcion=models.CharField(
        max_length=200,
        unique=True
    )
    direccion=models.CharField(
        max_length=250,
        null=True,
        blank=True
    )
    contacto=models.CharField(
        max_length=100
    )
    telefono=models.CharField(
        max_length=10,
        null=True,blank=True
    )
    email=models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Proveedor,self).save()

    class Meta:
        verbose_name_plural = "Proveedores"



#SE CREA EL MODELO COMPRAS ENCABEZADO
class ComprasEncabezado(Modelado):
    fecha_compra = models.DateField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    no_factura = models.CharField(max_length=100)
    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __srt__(self):
        return '{}'.format(self.observacion)

    def save(self):
        self.observacion = self.observacion.upper()
        self.total = self.sub_total - self.descuento
        super(ComprasEncabezado, self).save()

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name = "Encabezado Compra"


#SE CREA MODELO COMPRAS DETALLE
class ComprasDetalle(Modelado):
    compra = models.ForeignKey(ComprasEncabezado, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio_prv = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    def __set__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDetalle,self).save()

    class Meta:
        verbose_name_plural = "Detalles compras"
        verbose_name = "Detalle Compra"




#MANTENER SIEMPRE ACTUALIZADO ASI SE BORRE O SE AÑADA ALGO A LA LISTA.
@receiver(post_delete, sender=ComprasDetalle)
def detalle_compra_borrar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    id_compra = instance.compra.id

    enc = ComprasEncabezado.objects.filter(pk=id_compra).first()

    if enc:
        sub_total = ComprasDetalle.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDetalle.objects.filter(compra=id_compra).aggregate(Sum('descuento'))
        enc.sub_total = sub_total['sub_total__sum']
        enc.descuento=descuento['descuento__sum']
        enc.save()

    prod = Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()

@receiver(post_save,sender=ComprasDetalle)
def detalle_compra_guardar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    fecha_compra = instance.compra.fecha_compra

    prod = Producto.objects.filter(pk=id_producto).first()

    if prod:
        cantidad = int(prod.existencia) + int(instance.cantidad)
        prod.existencia = cantidad
        prod.ultima_compra = fecha_compra
        prod.save()


