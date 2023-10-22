
from django.urls import path
from . import views

# Configuración de URLs
urlpatterns = [
    path("busqueda_usuarios", views.buscar_usuario, name="busqueda"),
]