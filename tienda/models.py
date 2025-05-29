from django.db import models
from accounts.models import AppUser
from django.conf import settings
# Create your models here.

class Categoria(models.TextChoices):
    TEC = 'TEC','Tecnologia'
    DOM = 'DOM','Domesticos'
    DEP = 'DEP','Deportes'
    X = 'X','Otro'


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200,blank=False,null=False)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    estado = models.CharField(max_length=25)
    codigo = models.CharField(max_length=10,unique=True)
    categoria = models.CharField(choices=Categoria.choices, max_length=25,null=True,blank=True)
    usuario = models.ForeignKey(AppUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " de " + self.usuario.username


class Carrito(models.Model):
    usuario = models.OneToOneField(AppUser, on_delete=models.CASCADE,unique=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ProductoEnCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    comprado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"
    

class Orden(models.Model):
    carrito = models.ForeignKey(ProductoEnCarrito, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.carrito.carrito.id}"


class Comentario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    titulo = models.CharField(max_length=100, default="Sin título")
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='comentarios/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} por {self.usuario.username}'