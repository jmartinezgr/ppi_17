from django.urls import path
from .views import registro_usuario, privacidad

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('privacidad/', privacidad, name='privacidad'),
]
