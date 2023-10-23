# Este código hace uso de funcionalidades proporcionadas por Django,
# un framework de desarrollo web de código abierto. Utiliza modelos
# personalizados para gestionar sus urls y direcciones

from django.urls import path
from . import views

# Configuración de URLs
urlpatterns = [
    path("busqueda_usuarios/", views.buscar_usuario, name="busqueda"),
    path("usuario_discapacidad/", views.usuario_discapacidad, name="discapacidad"),
    path("login/", views.login_view, name="login_view"),
    path('registro/', views.registro_view, name='registro'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('verficar_licencia/',views.verificar_licencia,name='verificar_licencia'),
    path('lista_viajes/', views.lista_viajes, name='lista_viajes'),
    path("viaje/",views.detalle_viaje, name="detalle_viaje"),
]