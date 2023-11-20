# Este código utiliza el framework Django para desarrollo web.
# Contiene vistas y funcionalidades relacionadas con la gestión de usuarios y viajes.

####Librerias del Framework
from django.shortcuts import render, redirect, get_object_or_404
import folium
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
####Librerias de Terceros
from utils.calcular_distancia import calcular_punto_medio
from utils.obtener_coordenadas import calcular_distancia_tiempo
####Librerias de Python
from datetime import datetime
import folium
####Librerias de la app
from .models import Viaje
from .forms import ViajesForm,CoordenadaForm
####Librerias de otras apps
from usuarios.models import Usuario

def ingresar_coordenada(request):
    # Inicializa la variable que contendrá el resultado
    data_ret = None
    mapa_html = None  # Definir mapa_html por defecto

    # Inicializa el mapa de Folium fuera del bloque if
    mapa = folium.Map(location=[0, 0], zoom_start=12)

    if request.method == 'POST':
        # Crea un formulario a partir de los datos POST
        form = CoordenadaForm(request.POST)
        
        
        if form.is_valid():
            # Procesa los datos si el formulario es válido
           
            selected_option = form.cleaned_data.get('starting_place_type')
            
            # Busca las coordenadas correspondientes a la opción seleccionada
            
            selected_option_2 = form.cleaned_data.get('ending_place_type')

            # convertir selected_option a coordenadas
            start_coord = eval(selected_option)
            end_coord = eval(selected_option_2)
            
            punto_medio = calcular_punto_medio(start_coord[0], start_coord[1], end_coord[0], end_coord[1])
            
            # Calcula la distancia usando las coordenadas del usuario y las coordenadas temporales
            data_ret = calcular_distancia_tiempo(start_coord, end_coord)
            
            # Crear el mapa de Folium
            mapa = folium.Map(location=punto_medio, zoom_start=15)
            folium.Marker([start_coord[0], start_coord[1]], popup='Coordenada 1').add_to(mapa)
            folium.Marker([end_coord[0], end_coord[1]], popup='Coordenada 2').add_to(mapa)

            # Convertir el mapa de Folium a HTML
            mapa_html = mapa._repr_html_()
        else:
            # Si el formulario no es válido, muestra un mensaje de error
            messages.error(request, "Por favor, selecciona una opción válida.")
    else:
        # Si no es una solicitud POST, crea un formulario vacío
        form = CoordenadaForm()

    # Renderiza la plantilla 'rutas_similares.html' con el formulario y el resultado
    return render(request, 'conductores/rutas_similares.html', {'form': form, 'data_ret': data_ret, 'mapa': mapa_html })

def lista_viajes(request):
    """
    Vista para mostrar una lista de viajes activos ordenados por fecha de inicio.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'pasajeros/lista_viajes.html' con la lista de viajes.
    """
    # Obtener viajes activos ordenados por fecha de inicio
    viajes_activos = Viaje.objects.filter(
        Q(condicion='Activo')
    ).order_by('fecha_inicio')

    # Preparar datos para el contexto
    viajes = [
        {
            'conductor': viaje.conductor.username,  # Asumiendo que el conductor es un usuario
            'destino': viaje.destino,
            'hora_salida': viaje.fecha_inicio.strftime('%I:%M %p'),
            'id':viaje.id
        }
        for viaje in viajes_activos
    ]

    context = {'viajes': viajes}
    return render(request, 'pasajeros/lista_viajes.html', context)  
"""
@login_required
def detalle_viaje(request):
    
    Vista para mostrar detalles de un viaje.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'conductores/viaje.html' con los detalles del viaje.

    viaje = {
        'nombre_conductor': 'Juan Pérez',
        'nombre_usuario': 'María González',
        'documento_conductor': '123456789',
        'documento_usuario': '987654321',
        'lugar_destino': 'Plaza Principal Marinilla',
        'distancia': '50 km',
        'precio': '$5000.00',
        'tiempo_inicial': '2023-10-10 06:00 PM',
    }

    context = {'viaje': viaje}
    return render(request, 'conductores/viaje.html', context)
"""
@login_required
def crear_viaje(request):
    if request.user.rol == 'Pasajero':
        raise 
    
    if request.method == 'POST':
        form = ViajesForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y crear el objeto Viaje
            inicio = form.cleaned_data['inicio']
            destino = form.cleaned_data['destino']
            fecha_inicio_str = form.cleaned_data['fecha_inicio']
            observaciones = form.cleaned_data['observaciones']
            puestos_maximos = form.cleaned_data['puestos_maximos']
            discapacidades_aceptadas = form.cleaned_data['discapacidades_aceptadas']

            print(puestos_maximos)
            print(fecha_inicio_str)
            print(destino)

            conductor = Usuario.objects.get(username=request.user.username)
            
            viaje = Viaje.objects.create(
                inicio=inicio,
                destino=destino,
                conductor=conductor,
                fecha_inicio=fecha_inicio_str,
                observaciones=observaciones,
                puestos_maximos=puestos_maximos,
                discapacidades=discapacidades_aceptadas,
            )

            # Redirigir a alguna página de éxito o detalles del viaje
            return redirect('detalle_viaje', viaje_id=viaje.id)
            
        else:
            messages.error(request, 'Error en el formulario. Por favor, revise los campos.')
            print(form.errors)

    else:
        form = ViajesForm()

    return render(request, 'conductores/crear_viaje.html', {'form': form})

@login_required
def detalle_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)

    data_ret = None
    mapa_html = None

    mapa = folium.Map(location=[0, 0], zoom_start=12)
    # Procesa los datos si el formulario es válido
    selected_option = viaje.inicio
    selected_option_2 = viaje.destino

    start_coord = eval(selected_option)
    end_coord = eval(selected_option_2)
            
    punto_medio = calcular_punto_medio(start_coord[0], start_coord[1], end_coord[0], end_coord[1])
            
    data_ret = calcular_distancia_tiempo(start_coord, end_coord)
            
    mapa = folium.Map(location=punto_medio, zoom_start=15)
    folium.Marker([start_coord[0], start_coord[1]], popup='Coordenada 1').add_to(mapa)
    folium.Marker([end_coord[0], end_coord[1]], popup='Coordenada 2').add_to(mapa)

    mapa_html = mapa._repr_html_()

    return render(request, 'pasajeros/detalle_viaje.html', {'data_ret': data_ret, 'mapa': mapa_html, 'viaje': viaje,'numeros':range(viaje.puestos_maximos)})