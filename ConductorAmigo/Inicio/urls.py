
from django.urls import path
from . import views

# Configuración de URLs
urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("busqueda", views.busqueda, name="busqueda"),
    path("register", views.register, name="register"),
    path("verficarLicencia", views.verificarLicencia, name="verificarLicencia"),
    path("logout/", exit, name="exit"),
    path("viaje",views.detalle_viaje, name="detalleViaje"),
]