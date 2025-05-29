from tienda.models import Categoria

def categorias_context(request):
    # Retorna todas las categorías para todas las plantillas
    return {
        'categorias': Categoria.choices,  # o tu forma de obtener la lista de categorías
    }