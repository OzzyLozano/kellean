from django.urls import path, include

from . import views

app_name='tienda'

urlpatterns = [
    path('inicio/', views.Inicio.as_view(),name="inicio"),
    path('crear-produto/', views.CrearProducto.as_view(),name="crear_producto"),
    path('editar-producto/<int:pk>', views.EditarProducto.as_view(),name="editar_producto"),
    path('eliminar-producto/<int:pk>', views.EliminarProducto.as_view(),name="eliminar_producto"),
    path('ver-producto/<int:pk>', views.VerProducto.as_view(),name="ver_producto"),

    path('mis-productos/<int:pk>', views.MisProductos.as_view(), name="mis_productos"),

    path('ver-carrito/<int:pk>',views.VerCarrito.as_view(),name="ver_carrito"),
    path('agregar-carrito/<int:pk>', views.AgregarProductoCarrito.as_view(),name="agregar_carrito"),
    path('eliminar-producto-carrito/<int:pk>', views.eliminar_producto_carrito,name="eliminar_producto_carrito"),

    path('all-products', views.AllProducts.as_view(),name="all_products"),


    path('about/', views.About.as_view(),name="about"),
    path('checkout/<int:pk>',views.Checkout.as_view(),name="checkout"),
    path('pedido/', views.CotLista.as_view(),name="cot_lista"),


    path('tecnologia/', views.TecnologiaView.as_view(),name="tecnologia"),
    path('deportes/', views.DeportesView.as_view(),name="deportes"),
    path('domesticos/', views.DomesticosView.as_view(),name="domesticos"),

    path('blog/', views.Blog.as_view(), name="blog"),
    path('comentar/', views.ComentarView.as_view(), name='comentar'),
    path('eliminar-comentario/<int:pk>', views.EliminarComentario.as_view(), name="eliminar_comentario")
]

