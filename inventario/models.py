from django.db import models
from bases.models import Modelado

# /*****************************************
# /*****************************************

class Categoria(Modelado):
    descripcion = models.CharField(
        max_length= 100,
        help_text='Descripcion de la categoria',
        unique=True
    )

    #asi es como se va a mostrar, solo descripcion
    def __str__(self):
        return '{}'.format(self.descripcion)

    def _save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()


    class Meta:
        verbose_name_plural = "Categorias"

# /*****************************************
# /*****************************************

class SubCategoria(Modelado):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length= 100,
        help_text='Descripcion de la categoria',
        unique=True
    )

    def __str__(self):
        return '{} : {}'.format(self.categoria.descripcion,self.descripcion)

    def _save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = "SubCategorias"
        unique_together = ('categoria', 'descripcion')


# /*****************************************
# /*****************************************

class Marca(Modelado):
    descripcion = models.CharField(
        max_length= 100,
        help_text='Descripcion de la marca',
        unique=True
    )

    #asi es como se va a mostrar, solo descripcion
    def __str__(self):
        return '{}'.format(self.descripcion)

    def _save(self):
        self.descripcion = self.descripcion.upper()
        super(Marca, self).save()


    class Meta:
        verbose_name_plural = "Marcas"


# /*****************************************
# /*****************************************

class UnidadDeMedida(Modelado):
    descripcion = models.CharField(
        max_length= 100,
        help_text='Descripcion de la unidad de medida',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(UnidadDeMedida, self).save()

    class Meta:
        verbose_name_plural = "Unidades de Medida"


# /*****************************************
# /*****************************************

class Producto(Modelado):
    codigo = models.CharField(
        max_length=20,
        unique=True
    )
    codigo_barra = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    existencia = models.IntegerField(default=0)

    ultima_compra = models.DateField(null=True, blank=True)

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE)
    subCategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto, self).save()

    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('codigo', 'codigo_barra')
















