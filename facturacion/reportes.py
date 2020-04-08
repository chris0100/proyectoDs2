from django.shortcuts import render
from .models import FacturaEncabezado,FacturaDetalle

def imprimir_factura_recibo(request,id):
    template_name = 'facturacion/factura_one.html'

    enc = FacturaEncabezado.objects.get(id=id)
    det = FacturaDetalle.objects.filter(factura=id)

    context = {
        'request':request,
        'enc':enc,
        'detalle':det
    }
    print('se trae el contexto asi: ' + str(context))

    return render(request,template_name,context)
