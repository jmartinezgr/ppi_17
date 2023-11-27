# Este código hace uso de funcionalidades proporcionadas por Django,
# un framework de desarrollo web de código abierto. Utiliza modelos
# personalizados para gestionar de viajes y sus usuarios.

from django.db import models
from usuarios.models import Usuario

class Viaje(models.Model):
    # Opciones para el campo "condicion"
    CONDICIONES_VIAJE = (
        ('Activo', 'Activo'),
        ('A la espera de arranque', 'A la espera de arranque'),
        ('En curso', 'En curso'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    )

    INCAPACIDAD_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('silla_de_ruedas', 'Silla de ruedas'),
        ('muletas', 'Muletas'),
        ('vision_reducida', 'Visión reducida'),
    ]
    
    inicio = models.CharField('Lugar de Partida',max_length=200,default=(6.260699999606895, -75.57953881377448))
    destino = models.CharField('Destino', max_length=200)
    conductor = models.ForeignKey(Usuario, related_name='viajes_conducidos', on_delete=models.CASCADE)
    pasajeros = models.ManyToManyField(Usuario, related_name='viajes_realizados', blank=True)
    observaciones = models.TextField('Observaciones', blank=True)
    fecha_inicio = models.DateTimeField('Fecha de Inicio')
    fecha_fin = models.DateTimeField('Fecha de Finalización', null=True, blank=True)
    condicion = models.CharField('Condición del Viaje', max_length=23, choices=CONDICIONES_VIAJE, default='Activo')
    puestos_maximos = models.IntegerField('Puestos Máximos', default=1)
    discapacidades = models.CharField('Discapacidades Aceptadas',choices=INCAPACIDAD_CHOICES,default='ninguna',max_length=30)
    tipo_vehiculo = models.CharField('Tipo de Vehículo', max_length=50, choices=(('Carro', 'Carro'), ('Moto', 'Moto')),default="Carro")
    placa_vehiculo = models.CharField('Placa del Vehículo', max_length=20,default="XXXXXXX")

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto Viaje.

        Returns:
            str: Representación del viaje en formato "Viaje de {conductor} a {destino}".
        """
        return f'Viaje de {self.conductor} a {self.destino}'

    def actualizar_condicion(self):
        """
        Actualiza la condición del viaje basándose en la disponibilidad de puestos.

        Si no hay puestos disponibles, cambia la condición a "A la espera de arranque".
        Si hay puestos disponibles, mantiene la condición como "Activo".
        """
        puestos_disponibles = self.puestos_maximos - self.pasajeros.count()
        if puestos_disponibles == 0:
            self.condicion = 'A la espera de arranque'
        else:
            self.condicion = 'Activo'

    def unirse_al_viaje(self, usuario):
        """
        Permite que un usuario se una al viaje y actualiza la condición del viaje.

        Args:
            usuario (Usuario): El usuario que se está uniendo al viaje.
        """
        puestos_disponibles = self.puestos_maximos - self.pasajeros.count()
        if puestos_disponibles > 0 and usuario not in self.pasajeros.all():
            self.pasajeros.add(usuario)
            self.actualizar_condicion()