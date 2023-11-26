# Este código utiliza el framework Django para desarrollo web.
# Contiene vistas y funcionalidades relacionadas con la gestión de usuarios y viajes.

####Librerias del Framework
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.http import Http404
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

@login_required
def ingresar_coordenada(request):
    """
    Vista que permite a un usuario ingresar coordenadas y calcula la distancia y tiempo de viaje entre ellas.

    Esta vista utiliza un formulario (CoordenadaForm) para obtener las coordenadas del usuario
    y realiza cálculos utilizando las funciones calcular_punto_medio y calcular_distancia_tiempo.
    El resultado incluye información sobre la distancia y tiempo de viaje, así como un mapa interactivo.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'conductores/rutas_similares.html'
                      con el formulario, el resultado y el mapa.
    """
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


@login_required
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

@login_required
def crear_viaje(request):
    """
    Vista que permite a un usuario conductor crear un nuevo viaje.

    Esta vista verifica si el usuario tiene un rol de 'Pasajero' y levanta un error Http404 si es así.
    Luego, verifica si el usuario ya tiene algún viaje activo o en curso y muestra un mensaje de error en ese caso.
    Si la solicitud es un POST, procesa el formulario (ViajesForm) y crea un nuevo objeto Viaje.
    Finalmente, redirige a la página de detalles del viaje creado.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige a la página de detalles del viaje creado
                      o renderiza la plantilla 'conductores/crear_viaje.html' con el formulario.
    """

    if request.user.rol == 'Pasajero':
        raise Http404('Si quieres crear un viaje cambia tu perfil a conductor')

    usuario_pre = Usuario.objects.get(username=request.user.username)

    viajes_activos_en_curso = Viaje.objects.filter(conductor=usuario_pre, condicion__in=('Activo', 'En curso'))

    # Verifica si hay algún viaje activo o en curso
    if viajes_activos_en_curso.exists():
        # Levanta un error Http404 con un mensaje personalizado
        messages.error(request,"Ya tienes un viaje activo!")
        return redirect('viaje')
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
    """
    Vista que muestra los detalles de un viaje, incluyendo información sobre la ruta y el mapa interactivo.

    Esta vista utiliza el ID del viaje para obtener la instancia correspondiente del modelo Viaje.
    Luego, procesa los datos del viaje, como las coordenadas de inicio y destino, y calcula el punto medio.
    También utiliza la función calcular_distancia_tiempo para obtener información sobre la distancia y el tiempo de viaje.
    Finalmente, renderiza la plantilla 'pasajeros/detalle_viaje.html' con los datos obtenidos.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.
        viaje_id (int): El ID del viaje del cual se mostrarán los detalles.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'pasajeros/detalle_viaje.html'
                      con los detalles del viaje, incluyendo información sobre la ruta y el mapa interactivo.
    """
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


@login_required
def viaje(request):
    """
    Vista que redirige a la página de detalles de un viaje activo en curso del usuario actual.

    Esta vista obtiene el usuario actual y busca un viaje en el que el usuario sea el conductor o
    haga parte de los pasajeros y tenga una condición de 'Activo' o 'En curso'. Si no hay un viaje activo,
    muestra un mensaje de error y redirige al usuario a crear un nuevo viaje (para conductores) o unirse
    a un viaje existente (para pasajeros).

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige a la página de detalles del viaje activo en curso
                      o a la creación/join de un nuevo viaje.
    """
    # Obtén el usuario actual
    usuario = request.user

    # Busca un viaje en el que el usuario sea el conductor o haga parte de los pasajeros
    viaje = Viaje.objects.filter(Q(conductor=usuario, condicion__in=('Activo', 'En curso')) | Q(pasajeros=usuario, condicion__in=('Activo', 'En curso'))).first()

    if viaje is None:
        if usuario.rol.name == 'Conductor':
            messages.error(request, 'No tienes un viaje activo, puedes crear alguno')
            return redirect('crear_viaje')
        else:
            messages.error(request, 'No tienes un viaje activo, puedes unirte a alguno')
            return redirect('lista_viajes')

    return redirect('detalle_viaje', viaje_id=viaje.id)

@login_required
def accion_viaje(request, accion, viaje_id):
    """
    Vista que realiza acciones específicas en un viaje, como iniciar, cancelar, unirse o finalizar.

    Esta vista recibe la acción a realizar ('iniciar', 'cancelar', 'unirse', 'finalizar') y el ID del viaje.
    Dependiendo de la acción y del usuario que realiza la solicitud, realiza las operaciones correspondientes
    y redirige a la página adecuada. En caso de una acción no válida, levanta un error Http404.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.
        accion (str): La acción a realizar ('iniciar', 'cancelar', 'unirse', 'finalizar').
        viaje_id (int): El ID del viaje en el cual realizar la acción.

    Returns:
        HttpResponse: Una respuesta HTTP que redirige a la página adecuada después de realizar la acción.

    Raises:
        Http404: Si la acción no es válida o si el usuario no tiene permisos para realizar la acción.
    """
    viaje = Viaje.objects.get(id=viaje_id)
    if accion == 'iniciar' and viaje.conductor == request.user:
        viaje.condicion = 'En curso'
        viaje.save()
        return redirect('viaje')
    elif accion == 'cancelar' and viaje.conductor == request.user:
        viaje.condicion = 'Cancelado'
        viaje.save()
        return redirect('crear_viaje')
    elif accion == 'unirse' and request.user not in viaje.pasajeros.all():
        viaje.unirse_al_viaje(request.user)
        viaje.save()
        return redirect('viaje')
    elif accion == 'finalizar' and viaje.conductor == request.user:
        viaje.condicion = 'Finalizado'
        viaje.save()
        return redirect('crear_viaje')
    else:
        raise Http404('No es una acción válida')