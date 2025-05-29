from django.contrib import admin
from .models import Producto,ProductoEnCarrito,Orden,Carrito
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Carrito)
admin.site.register(ProductoEnCarrito)
admin.site.register(Producto)
admin.site.register(Orden)