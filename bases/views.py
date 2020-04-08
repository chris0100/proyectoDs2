from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


# la clase home hereda de generic el TemplateView y tambien loginremixin(van siempre a la izq)
class Home(LoginRequiredMixin, generic.TemplateView):
    # asi se le va a llamar a la plantilla
    template_name = 'bases/home.html'

    #obliga a que el usuario se loguee para ver contenido.
    login_url = 'bases:login'

# redirige a la plantilla
class HomeSinPrivilegios(generic.TemplateView):
    login_url = 'bases:login'
    template_name = 'bases/sin_privilegios.html'


# hereda y aplica funcionalidad
class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'bases:login'
    raise_exception = False
    redirect_field_name = 'redirect_to'

    def handle_no_permission(self):
        # ********************
        # CONFIGURAR USUARIO ANONIMO QUE INGRESE CON EL LINK DEL APLICATIVO
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url = 'bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))
