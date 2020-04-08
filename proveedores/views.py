from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import Proveedor,ComprasEncabezado,ComprasDetalle
from proveedores.forms import ProveedorForm,ComprasEncabezadoForm
from django.contrib.messages.views import SuccessMessageMixin
from bases.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from inventario.views import Producto
import datetime
from django.db.models import Sum

#CREACION DE MIXIN PARA EVITAR DUPLICADOS
class MixinFormInvalid:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


#VISUALIZA LA LISTA DE PROVEEDORES
class ProveedorView(SinPrivilegios, generic.ListView):
    model = Proveedor
    template_name = 'proveedores/proveedor_list.html'
    context_object_name = 'obj'

    # bloquear el permiso de ver la pagina
    permission_required = 'proveedores.view_proveedor'


#CREA UN NUEVO REGISTRO DE PROVEEDOR
class ProveedorNew(SuccessMessageMixin, MixinFormInvalid, SinPrivilegios, generic.CreateView):
    model = Proveedor
    template_name = 'proveedores/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores:proveedor_list')
    success_message = 'Categoria Creada Satisfactoriamente'
    permission_required = 'proveedores.add_proveedor'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)




#EDITA UN REGISTRO DE PROVEEDOR
class ProveedorEdit(SuccessMessageMixin, MixinFormInvalid, SinPrivilegios, generic.UpdateView):
    model = Proveedor
    template_name = 'proveedores/proveedor_form.html'
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedores:proveedor_list')
    success_message="Categoria Actualizada Satisfactoriamente"
    permission_required = 'proveedores.change_proveedor'


    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


#INACTIVA UN REGISTRO DE PROVEEDOR
@login_required(login_url='/login/')
@permission_required('proveedores.change_proveedor', login_url='bases:sin_privilegios')
def proveedorInactivar(request, id):
    template_name = 'proveedores/inactivar_proveedor.html'
    contexto = {}
    proveedor = Proveedor.objects.filter(pk=id).first()

    if not proveedor:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':proveedor}

    if request.method=='POST':
        proveedor.estado = False
        proveedor.save()
        contexto = {'obj':'OK'}
        return HttpResponse('Proveedor ' + proveedor.descripcion + ' inactivado')

    return render(request,template_name,contexto)


# /********************************
# /********************************

#VISUALIZA LA LISTA DE COMPRAS
class ComprasView(SinPrivilegios, generic.ListView):
    model = ComprasEncabezado
    template_name = 'proveedores/compras_list.html'
    context_object_name = 'obj'

    # bloquear el permiso de ver la pagina
    permission_required = 'proveedores.view_comprasencabezado'


@login_required(login_url='/login/')
@permission_required('proveedores.change_comprasencabezado', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name='proveedores/compras.html'

    # trae los productos habilitados en la bd de producto enlistados
    prod=Producto.objects.filter(estado=True)
    form_compras={}
    contexto={}

    #se activa cuando se da clic en nuevo o en editar un elemento de la tabla, revisa si hay datos
    #por tomar de los objetos o si vienen vacios.
    if request.method=='GET':
        form_compras=ComprasEncabezadoForm()
        #busca el id asociado para empezar la referencia
        enc = ComprasEncabezado.objects.filter(pk=compra_id).first()
        print("la variable enc tiene contenido:" + str(enc))

        if enc:
            #trae cada uno de los objetos contenidos en detalle
            det = ComprasDetalle.objects.filter(compra=enc)
            print("la variable det tiene contenido:" + str(det))
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }

            #SE COLOCAN LOS DATOS LOCALIZADOS EN LOS CAMPOS DEL FORMULARIO
            form_compras = ComprasEncabezadoForm(e)
        else:
            det = None

        contexto = {'productos':prod, 'encabezado':enc, 'detalle': det, 'form_encabezado':form_compras}



    if request.method=='POST':
        print('se activa metodo POST')
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        #COMO EL COMPRA_ID ESTA VACIO, SE PASAN LOS DATOS AGREGADOS.
        if not compra_id:
            print('compra id tiene valor de:' + str(compra_id))
            proveedor = Proveedor.objects.get(pk=proveedor)
            enc = ComprasEncabezado(
                fecha_compra = fecha_compra,
                observacion = observacion,
                no_factura = no_factura,
                fecha_factura = fecha_factura,
                proveedor = proveedor,
                usuarioCreado = request.user
            )
            if enc:
                print('despues de ver que compra_id esta vacio se guarda enc, porque enc esta lleno')
                enc.save()
                compra_id = enc.id

        #CUANDO SE DIRECCIONA PARA EDICION, COMO NO ESTA VACIO,
        else:
            print('el compra_id tiene valor de: ' + str(compra_id))
            enc = ComprasEncabezado.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura = no_factura
                enc.fecha_factura = fecha_factura
                enc.unidaddemedida = request.user.id
                enc.save()

        #SI DESPUES DE PASAR LOS DOS CONDICIONALES COMPRA_ID SIGUE ESTANDO NULO, MANDA A LA PRINCIPAL
        if not compra_id:
            return redirect("proveedores:compras_list")

        #TOMA EL RESTO DE DATOS PARA ENVIARLOS
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle = request.POST.get("id_descuento_detalle")
        total_detalle = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDetalle(
            compra =enc,
            producto = prod,
            cantidad = cantidad,
            precio_prv = precio,
            descuento = descuento_detalle,
            costo = 0,
            usuarioCreado = request.user
        )

        if det:
            print('ME DA LA IMPRESION QUE SIEMPRE ENTRA AQUI')
            det.save()
            sub_total = ComprasDetalle.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento = ComprasDetalle.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]
            enc.save()

        return redirect("proveedores:compras_edit", compra_id=compra_id)
    print('LUEGO DE QUE CARGA, REALIZA PROCESO DE RENDERIZADO')
    return render(request, template_name, contexto)


# /********************************************
# /********************************************

class CompraDetalleDelete(SinPrivilegios, generic.DeleteView):
    permission_required = 'proveedores.delete_comprasdetalle'
    model = ComprasDetalle
    template_name = 'proveedores/compras_detalle_del.html'
    context_object_name = 'obj'

    def get_success_url(self):
        compra_id=self.kwargs['compra_id']
        return reverse_lazy('proveedores:compras_edit', kwargs={'compra_id':compra_id})



