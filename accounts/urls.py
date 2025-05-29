from django.urls import path, include

from . import views

app_name='accounts'

urlpatterns = [
    path('',views.Inicio.as_view(),name='inicio'),
    path('ver-usuario/<int:pk>',views.VerUsuario.as_view(),name='ver_usuario'),
    path('crear-usuario/',views.CrearUsuario.as_view(),name='crear_usuario'),
    path('editar-usuario/<int:pk>',views.EditarUsuario.as_view(),name='editar_usuario'),
    path('eliminar-usuario/<int:pk>', views.EliminarUsuario.as_view(),name="eliminar_usuario"),

    path('iniciar-sesion/',views.IniciarSesion.as_view(),name='iniciar_sesion'),
    path('logout/',views.CerrarSesion,name='cerrar_sesion'),
]
