# Este código hace uso de funcionalidades proporcionadas por Django,
# un framework de desarrollo web de código abierto. Utiliza modelos
# personalizados para gestionar sus urls y direcciones

from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="landing"),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout_view'),
    path('nosotros/',views.nosotros,name="nosotros"),
]