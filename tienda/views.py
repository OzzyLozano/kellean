import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from .forms import * 
from django.db import IntegrityError
from django.http import JsonResponse
from accounts.models import *
from accounts.views import VendedorRequiredMixin, CompradorRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def generate_code() -> int :
    num = ''
    for x in range(10):
        num+= str(random.randint(0,9))
    return num


class Inicio(View):
    def get(self, request):
        context = {
        }
        return render(request,'producto/inicio.html',context)
    

class About(View):
    def get(self, request):
        return render(request, 'about.html')


class AllProducts(View):
    def get(self, request):
        productos = Producto.objects.all()
        categorias = Categoria.choices
        context = {
            'productos': productos,
            'categorias': categorias
        }
        return render(request, 'producto/all-products.html', context)


class CrearProducto(VendedorRequiredMixin,View):
    def get(self, request):
        form = CrearProductoForm()
        context = {
            'form': form
        }
        return render(request, 'producto/crear.html', context)
    def post(self, request):
        form = CrearProductoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                usuario = AppUser.objects.get(id=request.user.id)
                producto = Producto.objects.create(
                    nombre = form.cleaned_data['nombre'],
                    descripcion = form.cleaned_data['descripcion'],
                    precio = form.cleaned_data['precio'],
                    imagen = form.cleaned_data['imagen'],
                    estado = form.cleaned_data['estado'],
                    categoria = form.cleaned_data['categoria'],
                    codigo = generate_code(),
                    usuario = usuario
                )    
                return redirect('accounts:ver_usuario', request.user.id)
            except IntegrityError:
                print(request, "Hubo un error al crear el producto")


class EditarProducto(VendedorRequiredMixin,View):
    def get(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        form = EditarProductoForm(initial={
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': producto.precio,
            'imagen': producto.imagen,
            'estado': producto.estado,
            'categoria': producto.categoria
        })
        context = {
            'producto': producto,
            'form': form
        }
        return render(request, 'producto/editar.html', context)
    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        form = EditarProductoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                producto.nombre = form.cleaned_data['nombre']
                producto.descripcion = form.cleaned_data['descripcion']
                producto.precio = form.cleaned_data['precio']
                producto.imagen = form.cleaned_data['imagen']
                producto.estado = form.cleaned_data['estado']
                producto.categoria = form.cleaned_data['categoria']
                producto.save()
                return HttpResponseRedirect(reverse('accounts:ver_usuario', args=[request.user.id]))
            except IntegrityError:
                print(request, "Hubo un error al crear el producto")

        context = {
            'proucto': producto,
            'form': form
        }   
        return render(request, 'producto/editar.html',context)




class EliminarProducto(VendedorRequiredMixin, View):
    def post(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
            producto.delete()
            return redirect(reverse('accounts:ver_usuario', args=[producto.usuario.id]))
        except Producto.DoesNotExist:
            print("error")
        

class VerProducto(View):
    def get(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        context = {
            'producto': producto
        }
        return render(request, 'producto/ver.html', context)
    

class MisProductos(VendedorRequiredMixin,View):
    def get(self, request, pk):
        usuario = AppUser.objects.get(pk=pk)
        productos = Producto.objects.filter(usuario = usuario)
        carrito = Carrito.objects.get(usuario = usuario)
        prodcar = ProductoEnCarrito.objects.filter(carrito=carrito)
        context = {
            'productos': productos,
            'prodcar': prodcar
        }
        return render(request, 'producto/mis-productos.html', context)


class VerCarrito(CompradorRequiredMixin, View):
    def get(self, request, pk):
        usuario = AppUser.objects.get(pk=pk)
        carrito = Carrito.objects.get(usuario=usuario)
        prodcar = ProductoEnCarrito.objects.filter(carrito=carrito)
        total = 0
        for producto in prodcar:
            total += producto.producto.precio
        context = {
            'prods_carrito': prodcar,
            'usuario': usuario,
            'total': total,
            'carrito': carrito
        }
        return render(request, 'producto/vercarrito.html', context)



class AgregarProductoCarrito(CompradorRequiredMixin, View):
    def post(self, request, pk):
        try:
            usuario = AppUser.objects.get(pk=request.user.id)
            producto = Producto.objects.get(pk=pk)
            carrito = Carrito.objects.get(usuario = usuario)
            item = ProductoEnCarrito.objects.create(
                producto=producto,
                carrito=carrito,
                comprado=False,
                cantidad=1
            )
            return redirect(reverse('tienda:all_products'))
        except IntegrityError:
            print(request,"Ocurrio un error al agregar el producto al carrito")



class EliminarProductoCarrito(CompradorRequiredMixin, View):
    def post(self, request, pk):
        try:
            prodcar = ProductoEnCarrito.objects.get(pk=pk)
            prodcar.delete()
            return redirect(reverse('tienda:ver_carrito', args=[request.user.id]))
        except IntegrityError:
            print(request,"Ocurrio un error al agregar el producto al carrito")



def es_comprador(user):
    return user.has_perm('accounts.puede_comprar')



@user_passes_test(es_comprador)
def eliminar_producto_carrito(request, pk):
    prodcar = ProductoEnCarrito.objects.get(pk=pk)
    prodcar.delete()
    return redirect('tienda:inicio')



class Checkout(CompradorRequiredMixin, View):
    def get(self, request,pk):
        carrito = Carrito.objects.get(pk=pk)
        prodcar = ProductoEnCarrito.objects.filter(carrito=carrito)
        total = 0
        for producto in prodcar:
            total += producto.producto.precio
        context = { 
            'carrito': carrito,
            'prodcar': prodcar,
            'total': total,
            'total1': total + 50
        }   
        return render(request, 'producto/checkout.html',context)
    def post(self, request, pk):
        return redirect('tienda:cot_lista')
    

class CotLista(CompradorRequiredMixin,View):
    def get(self, request): return render(request, 'producto/cotlista.html')


class DeportesView(View):
    def get(self, request):
        productos = Producto.objects.filter(categoria="DEP")
        context= {
            'productos':productos
        }
        return render(request, 'producto/deportes.html', context)


class TecnologiaView(View):
    def get(self, request):
        productos = Producto.objects.filter(categoria="TEC")
        context= {
            'productos':productos
        }
        return render(request, 'producto/tecnologia.html', context)


class DomesticosView(View):
    def get(self, request):
        productos = Producto.objects.filter(categoria="DOM")
        context= {
            'productos':productos
        }
        return render(request, 'producto/domesticos.html', context)
    

class Blog(View):
    def get(self, request):
        comentarios = Comentario.objects.all()
        context = {
            'comentarios': comentarios
        }
        return render(request, 'producto/blog.html', context)
    

class ComentarView(CompradorRequiredMixin,View):
    def get(self, request):
        form = ComentarioForm()
        return render(request, 'producto/comentar.html', {'form': form})
    def post(self, request):
        form = ComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            Comentario.objects.create(
                usuario=request.user,
                titulo=form.cleaned_data['titulo'],
                contenido=form.cleaned_data['contenido'],
                imagen=form.cleaned_data.get('imagen')
            )
            return redirect(reverse('tienda:blog')) 
        return render(request, 'producto/comentar.html', {'form': form})



class EliminarComentario(CompradorRequiredMixin,View):
    def post(self, requet, pk):
        try:
            comentario = Comentario.objects.get(pk=pk)
            comentario.delete()
            return redirect('tienda:blog')
        except IntegrityError:
            print("Error")