from django import forms
from .models import Proveedor,ComprasEncabezado


class ProveedorForm(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields = ['estado','descripcion','direccion','contacto','telefono','email']
        exclude = ['usuarioModificado', 'fechaModificacion', 'usuarioCreado', 'fechaCreacion']
        widget= {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    # REVISA QUE NO SE REPITAN DATOS
    def clean(self):
        try:
            sc = Proveedor.objects.get(descripcion=self.cleaned_data['descripcion'].upper())

            if not self.instance.pk:
                print('Registro ya existe')
                raise forms.ValidationError('Registro ya existe')
            elif self.instance.pk!=sc.pk:
                print('cambio no permitido')
                raise forms.ValidationError('Cambio no permitido')
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data




class ComprasEncabezadoForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model = ComprasEncabezado
        fields=['proveedor','fecha_compra','observacion','no_factura','fecha_factura','sub_total','descuento','total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True




