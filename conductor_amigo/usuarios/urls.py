
from django.urls import path
from . import views

# Configuración de URLs
urlpatterns = [
    path("busqueda_usuarios", views.buscar_usuario, name="busqueda"),
    path("usuario_discapacidad", views.usuario_discapacidad, name="discapacidad"),

    path("verificar_licencia",views.verificarLicencia, name= "verificar_licencia")
]