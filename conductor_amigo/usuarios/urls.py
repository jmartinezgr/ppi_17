
from django.urls import path
from . import views

# Configuración de URLs
urlpatterns = [
    path("busqueda_usuarios", views.buscar_usuario, name="busqueda"),
    path("usuario_discapacidad", views.usuario_discapacidad, name="discapacidad"),
    path("login", views.login_view, name="login_view")
]