from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Categoria
from .forms import CategoriaForm
from .forms import SubCategoriaForm
from .models import SubCategoria
from django.urls import reverse_lazy
from .models import Marca
from .forms import MarcaForm
from .models import UnidadDeMedida
from .forms import UnidadDeMedidaForm
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages
from bases.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required

# SE APLICO HEREDACION MULTIPLE DE PARTE DE SINPRIVILEGIOS
class CategoriaView(SinPrivilegios, generic.ListView):
    permission_required = 'inventario.view_categoria'
    model = Categoria
    template_name = "inventario/categoria_list.html"
    context_object_name = "obj"



# CREAR UN REGISTRO
class CategoriaNew(SinPrivilegios, generic.CreateView):
    model = Categoria
    template_name = "inventario/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:categoria_list")
    permission_required = 'inventario.add_categoria'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)


# EDITAR UN REGISTRO
class CategoriaEdit(SinPrivilegios, generic.UpdateView):
    model = Categoria
    template_name = "inventario/categoria_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:categoria_list")
    permission_required = 'inventario.change_categoria'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)


# BORRAR UN REGISTRO
class CategoriaDel(SinPrivilegios,generic.DeleteView):
    model = Categoria
    template_name = 'inventario/catalogos_del.html'
    context_object_name = "obj"
    success_url = reverse_lazy("inventario:categoria_list")
    permission_required = 'inventario.delete_categoria'



#/*****************************************
#/*****************************************


#VER REGISTRO SUBCATEGORIA
class SubCategoriaView(SinPrivilegios, generic.ListView):
    model = SubCategoria
    template_name = "inventario/subcategoria_list.html"
    context_object_name = "obj"
    permission_required = 'inventario.view_subcategoria'


# CREAR UN REGISTRO DE SUBCATEGORIA
class SubCategoriaNew(SinPrivilegios, generic.CreateView):
    model = SubCategoria
    template_name = "inventario/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inventario:subcategoria_list")
    permission_required = 'inventario.add_subcategoria'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)


# EDITAR UN REGISTRO EN SUBCATEGORIA
class SubCategoriaEdit(SinPrivilegios, generic.UpdateView):
    model = SubCategoria
    template_name = "inventario/subcategoria_form.html"
    context_object_name = "obj"
    form_class = SubCategoriaForm
    success_url = reverse_lazy("inventario:subcategoria_list")
    permission_required = 'inventario.change_subcategoria'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)


# BORRAR UN REGISTRO EN SUBCATEGORIA
class SubCategoriaDel(SinPrivilegios,generic.DeleteView):
    model = SubCategoria
    template_name = 'inventario/catalogos_del.html'
    context_object_name = "obj"
    success_url = reverse_lazy("inventario:subcategoria_list")
    permission_required = 'inventario.delete_subcategoria'



#/*****************************************
#/*****************************************

# MOSTRAR UN REGISTRO DE MARCA
class MarcaView(SinPrivilegios, generic.ListView):
    model = Marca
    template_name = 'inventario/marca_list.html'
    context_object_name = 'obj'
    permission_required = 'inventario.view_marca'


#CREAR UN REGISTRO DE MARCA
class MarcaNew(SinPrivilegios, generic.CreateView):
    model = Marca
    template_name = 'inventario/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy("inventario:marca_list")
    permission_required = 'inventario.add_marca'


    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)


#EDITAR UN REGISTRO DE MARCA
class MarcaEdit(SinPrivilegios, generic.UpdateView):
    model = Marca
    template_name = 'inventario/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy("inventario:marca_list")
    permission_required = 'inventario.change_marca'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)



#INACTIVAR REGISTRO DE MARCA
# -obliga al usuario a loguearse, y si no tiene privilegios a la pagina, muestra mensaje de no permitido.
@login_required(login_url='/login/')
@permission_required('inventario.change_marca', login_url='bases:sin_privilegios')
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto ={}
    template_name="inventario/catalogos_del.html"

    # si marcar no existe, redirecciones
    if not marca:
        return redirect("inv:marca_list")

    if request.method=='GET':
        contexto={'obj':marca}

    # cuando realice el POST lo cambie a falso y me devuelva a la pagina donde estan las marcas
    if request.method=='POST':
        marca.estado=False
        marca.save()
        messages.success(request,'Marca inactivada')
        return redirect('inventario:marca_list')

    return render(request,template_name,contexto)


#/*****************************************
#/*****************************************

# MOSTRAR UN REGISTRO DE UNIDAD DE MEDIDA
class UnidadDeMedidaView(SinPrivilegios, generic.ListView):
    model = UnidadDeMedida
    template_name = 'inventario/um_list.html'
    context_object_name = 'obj'
    permission_required = 'inventario.view_unidaddemedida'


#CREAR UN REGISTRO DE UNIDAD DE MEDIDA
class UnidadDeMedidaNew(SinPrivilegios, generic.CreateView):
    model = UnidadDeMedida
    template_name = 'inventario/um_form.html'
    context_object_name = 'obj'
    form_class = UnidadDeMedidaForm
    success_url = reverse_lazy("inventario:um_list")
    permission_required = 'inventario.add_unidaddemedida'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)



#EDITAR UN REGISTRO DE UNIDAD DE MEDIDA
class UnidadDeMedidaEdit(SinPrivilegios, generic.UpdateView):
    model = UnidadDeMedida
    template_name = 'inventario/um_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy("inventario:um_list")
    permission_required = 'inventario.edit_unidaddemedida'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)



#INACTIVAR REGISTRO DE MARCA
@login_required(login_url='/login/')
@permission_required('inventario.change_unidaddemedida', login_url='bases:sin_privilegios')
def um_inactivar(request, id):
    um = UnidadDeMedida.objects.filter(pk=id).first()
    contexto ={}
    template_name="inventario/catalogos_del.html"

    # si marcar no existe, redireccione
    if not um:
        return redirect("inv:um_list")

    if request.method=='GET':
        contexto={'obj':um}

    # cuando realice el POST lo cambie a falso y me devuelva a la pagina donde estan las marcas
    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect('inventario:um_list')

    return render(request,template_name,contexto)



#/*****************************************
#/*****************************************

#MOSTRAR REGISTROS DE PRODUCTOS
class ProductoView(SinPrivilegios, generic.ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'obj'
    permission_required = 'inventario.view_producto'


#CREA UN PRODUCTO
class ProductoNew(SinPrivilegios, generic.CreateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url=reverse_lazy('inventario:producto_list')
    permission_required = 'inventario.add_producto'

    def form_valid(self, form):
        form.instance.usuarioCreado = self.request.user
        return super().form_valid(form)


#EDITA UN PRODUCTO
class ProductoEdit(SinPrivilegios, generic.UpdateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy('inventario:producto_list')
    permission_required = 'inventario.change_producto'

    def form_valid(self, form):
        form.instance.usuarioModificado = self.request.user.id
        return super().form_valid(form)


#INACTIVA UN PRODUCTO
@login_required(login_url='/login/')
@permission_required('inventario.change_producto', login_url='bases:sin_privilegios')
def producto_inactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    contexto={}
    template_name='inventario/catalogos_del.html'

    if not prod:
        return redirect('inventario:producto_list')

    if request.method=='GET':
        contexto={'obj':prod}

    if request.method=='POST':
        prod.estado=False
        prod.save()
        return redirect('inventario:producto_list')

    return render(request,template_name,contexto)















