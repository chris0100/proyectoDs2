from django import forms
from .models import Categoria
from .models import SubCategoria
from .models import Marca
from .models import UnidadDeMedida
from .models import Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields= ['descripcion','estado']
        labels={'descripcion':"Descripicion de la categoria",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })



class SubCategoriaForm(forms.ModelForm):
    # muestra solo los elementos activos de la categoria
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
            .order_by('descripcion')
    )

    class Meta:
        model=SubCategoria
        fields= ['categoria','descripcion','estado']
        labels={'descripcion':"Sub Categoria",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    #define la forma de mostrar en el formulario, ahi se llama el form-control que a su vez usa un select.
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        #cuando este vacio el combo de categorias, muestra opcion de seleccione categoria.
        self.fields['categoria'].empty_label = "Seleccione Categoria"



class MarcaForm(forms.ModelForm):
    class Meta:
        model= Marca
        fields= ['descripcion','estado']
        labels={'descripcion':"Descripicion de la marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })



class UnidadDeMedidaForm(forms.ModelForm):
    class Meta:
        model=UnidadDeMedida
        fields=['descripcion','estado']
        labels={'descripcion':"Descripcion de la unidad de medida",
                'estado':"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['codigo','codigo_barra','descripcion','estado', 'precio', 'existencia', 'ultima_compra', 'marca',
                'subCategoria', 'unidad_medida']
        exclude=['usuarioModificado','fechamodificacion', 'usuarioCreado','fechaCreacion']
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True