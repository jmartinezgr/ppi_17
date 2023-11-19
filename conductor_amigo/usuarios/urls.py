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
    path('registro/inicial',views.registro_inicial,name='registro_inicial'),
    path('registro/conductor',views.registro_conductor,name='registro_conductor'),
    path('registro/estudiante',views.registro_estudiante,name='registro_estudiante'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('verficar_licencia/',views.verificar_licencia,name='verificar_licencia'),
    path('lista_viajes/', views.lista_viajes, name='lista_viajes'),
    path("viaje/",views.detalle_viaje, name="detalle_viaje"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("rutas_similares", views.ingresar_coordenada, name='rutas_similares'),
    path("Usuario Discapacidad", views.usuario_discapacidad, name='usuario_discapacidad')

]