from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import AppUser
from tienda.models import Carrito
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from tienda.models import *

class VendedorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('accounts.puede_vender')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permiso para acceder a esta página.")
        return super().handle_no_permission()
    

class CompradorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('accounts.puede_comprar')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permiso para acceder a esta página.")
        return super().handle_no_permission()


class Inicio(View):
    def get(self, request, *args, **kwargs):
        usuarios = AppUser.objects.all()
        context = {
            'usuarios': usuarios
        }
        return render(request, 'accounts/inicio.html', context)
    

class VerUsuario(View):
    def get(self,request,pk,*args, **kwargs):
        usuario = AppUser.objects.get(pk=pk)
        productos = Producto.objects.filter(usuario=usuario)
        context = {
            'usuario':usuario,
            'productos': productos
        }
        return render(request,'accounts/usuarios/ver-usuario.html',context) 

class CrearUsuario(View):
    def get(self, request, *args, **kwargs):
        context = {
            'formulario': CustomUserCreationForm
        }
        return render(request, 'accounts/usuarios/crear-usuario.html', context)
    def post(self, request, *args, **kwargs):
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = AppUser.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email'],user_type=request.POST['user_type'])
                if request.POST['user_type'] == "CMP":
                    permiso = Permission.objects.get(codename='puede_comprar')
                    usuario.user_permissions.add(permiso)

                elif request.POST['user_type'] == "VND":
                    permiso = Permission.objects.get(codename='puede_vender')
                    usuario.user_permissions.add(permiso)
                carrito_usuario = Carrito.objects.create(usuario = usuario)
                return redirect(reverse('tienda:inicio'))
            except IntegrityError:
                context = {
                    'form': CustomUserCreationForm,
                    'error': 'Error al crear el usuario'
                }
                return render(request, 'accounts/usuarios/crear-usuario.html',context)
        context = {
            'formulario': CustomUserCreationForm,
            'error': 'Error al crear el usuario'
        }
        return render(request, 'accounts/usuarios/crear-usuario.html',context)
    

class EditarUsuario(View):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(AppUser, pk=pk)
        form = CustomUserChangeForm(instance=usuario)
        context = {
            'usuario': usuario,
            'form': form
        }
        return render(request, 'accounts/usuarios/editar-usuario.html', context)
    def post(self,request,pk,*args, **kwargs):
        usuario = AppUser.objects.get(pk=pk)
        nombre = request.POST['username']
        email = request.POST['email']
        usuario.username = nombre
        usuario.email = email
        usuario.save()
        return redirect(reverse('accounts:ver_usuario',args=[usuario.id]))



class EliminarUsuario(View):
    def post(self, request, pk):
        try:
            usuario = AppUser.objects.get(pk=pk)
            usuario.delete()
            return redirect('accounts:inicio')
        except AppUser.DoesNotExist:
            print('Error')


class IniciarSesion(View):
    def get(self, request, *args, **kwargs):
        context ={
            'form': AuthenticationForm,
        }
        return render(request, 'accounts/iniciar-sesion.html',context)
    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {
                'form': AuthenticationForm,
                'error': "Usuario o contraseña incorrectos"
            }
            return render(request,'accounts/iniciar-sesion.html', context)
        else:
            login(request,user)
            return redirect(reverse("tienda:inicio"))
        

@login_required(login_url='/accounts/login/')
def CerrarSesion(request,):
    logout(request)
    return redirect('tienda:inicio')


