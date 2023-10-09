
from django.urls import path
from .views import login, home, busqueda, register, exit

urlpatterns = [
    path("", home, name="home"),
    path("login", login, name="login"),
    path("busqueda", busqueda, name="busqueda"),
    path("register", register, name="register"),
    path("logout/", exit, name="exit"),
    path('eventos/', home, name='lista_eventos'),
]