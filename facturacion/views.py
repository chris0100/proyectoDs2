from django.shortcuts import render, redirect
from .models import Cliente,FacturaDetalle,FacturaEncabezado
from bases.views import SinPrivilegios
from django.views import generic
from .forms import ClienteForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from inventario.views import ProductoView,Producto
from django.contrib import messages
from django.contrib.auth import authenticate


class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = 'facturacion/cliente_list.html'
    context_object_name = 'obj'
    permission_required = 'facturacion.view_cliente'


#/************************************************************************************
#/*********************SUPER CLASES**************************************************
#/************************************************************************************

class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = Cliente
    context_object_name = 'obj'
    success_message = 'Operacion Satisfactoria'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = Cliente
    context_object_name = 'obj'
    success_message = 'Operacion Satisfactoria'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)

#/************************************************************************************
#/************************************************************************************
#/************************************************************************************


class ClienteNew(VistaBaseCreate):
    template_name = 'facturacion/cliente_form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('facturacion:cliente_list')
    permission_required = 'facturacion.add_cliente'

class ClienteEdit(VistaBaseEdit):
    template_name = 'facturacion/cliente_form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('facturacion:cliente_list')
    permission_required = 'facturacion.chage_cliente'


@login_required(login_url='/login/')
@permission_required('facturacion.change_cliente', login_url='/login/')
def clienteInactivar(request, id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse('OK')
        return HttpResponse('FAIL')

    return HttpResponse('FAIL')



#***************FACTURAS*****************
class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEncabezado
    template_name = 'facturacion/factura_list.html'
    context_object_name = 'obj'
    permission_required = 'facturacion.view_facturaencabezado'



@login_required(login_url='/login/')
@permission_required('facturacion.change_facturaencabezado', login_url='bases:sin_privilegios')
def facturaRealizar(request, id=None):
    template_name = 'facturacion/facturas.html'

    # encabezado = {
    #     'fecha':datetime.today()
    # }
    detalle = {}
    clientes = Cliente.objects.filter(estado=True)

    if request.method == "GET":
        enc = FacturaEncabezado.objects.filter(pk=id).first()
        print('inicial enc ' + str(enc))
        if not enc:
            print('NO HAY ENC (GET) ' + str(enc))
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total':0.00
            }
            detalle = None
        else:
            print('SI HAY ENC (GET) ' + str(enc))
            encabezado = {
                'id': enc.id,
                'fecha': enc.fecha,
                'cliente': enc.cliente,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            detalle = FacturaDetalle.objects.filter(factura=enc)

        contexto={"enc":encabezado, "det":detalle, "clientes":clientes}



    if request.method == "POST":
        cliente = request.POST.get('encabezado_cliente')
        print('el cliente para POST es: ' + cliente)
        fecha = request.POST.get('fecha')
        cli = Cliente.objects.get(pk=cliente)

        if not id:
            print('no existe un id, por lo tanto toma datos de factura encabezado')
            enc = FacturaEncabezado(
                cliente = cli,
                fecha = fecha
            )
            print('ahora se imprime a encabezado: ' + str(enc))
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEncabezado.objects.filter(pk=id).first()
            print('entra en el else y tiene por valor a enc ' + str(enc))
            if enc:
                print('llega a guardar el dato en enc' + str(enc))
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request,'No puedo continuar, no se detecta el No de Factura')
            return redirect("facturacion:factura_list")

        codigo = request.POST.get('codigo')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        sub_total = request.POST.get('sub_total_detalle')
        descuento = request.POST.get('descuento_detalle')
        total = request.POST.get('total_detalle')
        print('finalmente estos son datas' + str(codigo) + ':' + str(cantidad) + ':' + str(precio) + ':' + str(sub_total) + ':' + str(descuento) + ':' + str(total))

        prod = Producto.objects.get(codigo=codigo)
        detalle = FacturaDetalle(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = sub_total,
            descuento = descuento,
            total = total
        )

        if detalle:
            detalle.save()

        return redirect("facturacion:factura_edit", id=id)

    return render(request,template_name,contexto)



class ProductoView(ProductoView):
    template_name='facturacion/buscar_producto.html'


def borrar_detalle_factura(request, id):
    template_name = 'facturacion/factura_borrar_detalle.html'

    det = FacturaDetalle.objects.get(pk=id)

    if request.method == 'GET':
        context={'det':det}

    if request.method == "POST":
        usr = request.POST.get('usuario')
        pas = request.POST.get('pass')

        user = authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o clave incorrecta")

        if not user.is_active:
            return HttpResponse("Usuario inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            # se coloca el id en vacio para que asi cree uno nuevo para hacer la parte negativa que resta
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")

    return render(request,template_name,context)



