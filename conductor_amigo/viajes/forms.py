from django import forms
from .models import Viaje
from django.utils import timezone

ENDING_PLACE_CHOICES = [
    ('None', "Selecciona una opción"),
    ((6.253520142772332, -75.58292149217107), 'Metro Suramericana - Salida de la 65'),
    ((6.2592766751606215, -75.59785206576802), 'Metro Floresta - Salida Autopista Norte'),
    ((6.278480487535483, -75.56953613913925), 'Metro Caribe - Salida de la 80'),
    ((6.269538437023643, -75.56620835977748), 'Metro UdeA - Salida de la 66b'),
    ((6.230579395186508, -75.57593281026912), 'Metro Industriales - Autopista Norte'),
]

STARTING_PLACE_CHOICES = [
    ('None', "Selecciona una opción"),
    ((6.260699999606895, -75.57953881377448), 'Sede Volador - Salida de la 65'),
    ((6.259629620843638, -75.57556499754875), 'Sede Volador - Salida Autopista Norte'),
    ((6.274057506330517, -75.59252364426453), 'Sede Robledo - Salida de la 80'),
    ((6.275527354991391, -75.59099154868524), 'Sede Robledo - Salida de la 66b'),
    ((6.263575166707227, -75.57482065639084), 'Sede Rio - Autopista Norte'),
]

class CoordenadaForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'})
    )

    ending_place_type = forms.ChoiceField(
        choices=ENDING_PLACE_CHOICES,
        required=False,
        label="Lugar de destino",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )

    starting_place_type = forms.ChoiceField(
        choices=STARTING_PLACE_CHOICES,
        required=False,
        label="Lugar de partida",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )

class ViajesForm(forms.Form):
    inicio = forms.ChoiceField(
        choices=STARTING_PLACE_CHOICES,
        label="Lugar de Partida",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'})
    )

    destino = forms.ChoiceField(
        choices=ENDING_PLACE_CHOICES,
        label="Destino",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'})
    )

    fecha_inicio = forms.DateTimeField(
        label="Fecha de Inicio",
        widget=forms.DateTimeInput(attrs={'class': 'form-control rounded-pill', 'type': 'datetime-local'}),
    )

    observaciones = forms.CharField(
        label="Observaciones",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
    )

    puestos_maximos = forms.IntegerField(
        label="Puestos Máximos",
        initial=1,
        max_value=4,
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-pill'}),
    )

    discapacidades_aceptadas = forms.ChoiceField(
        choices=Viaje.INCAPACIDAD_CHOICES,
        label="Situaciones de discapacidad Aceptadas",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
    )
    
    tipo_vehiculo = forms.ChoiceField(
        choices=[
            ('carro', 'Carro'),
            ('moto', 'Moto'),
        ],
        label="Tipo de Vehículo",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill'}),
    )

    placa_vehiculo = forms.CharField(
        max_length=10,
        label="Placa del Vehículo",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
    )