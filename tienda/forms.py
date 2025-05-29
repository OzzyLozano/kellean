from django import forms
from .models import *

class CrearProductoForm(forms.Form):
    nombre = forms.CharField(
        max_length=50,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=200,
        label='Descripción'
    )
    precio = forms.FloatField(
        label='Precio',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    imagen = forms.FileField(
        required=False,
        label='Imagen',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    estado = forms.CharField(
        max_length=25,
        label='Estado',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    categoria = forms.ChoiceField(
        choices=Categoria.choices,
        required=False,
        label='Categoría',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class EditarProductoForm(forms.Form):
    nombre = forms.CharField(
        max_length=50,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=200,
        label='Descripción'
    )
    precio = forms.FloatField(
        label='Precio',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    imagen = forms.FileField(
        required=False,
        label='Imagen',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    estado = forms.CharField(
        max_length=25,
        label='Estado',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    categoria = forms.ChoiceField(
        choices=Categoria.choices,
        required=False,
        label='Categoría',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ComentarioForm(forms.Form):
    titulo = forms.CharField(
        max_length=100,
        label="Título",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contenido = forms.CharField(
        max_length=1000,
        label="Contenido",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    imagen = forms.ImageField(
        label="Imagen (opcional)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )