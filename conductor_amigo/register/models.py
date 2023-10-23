from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=15)
    apellido = models.CharField(max_length=15)
    correo = models.EmailField()
    celular = models.CharField(max_length=15)
    politicas_de_privacidad = models.BooleanField(default=False)
