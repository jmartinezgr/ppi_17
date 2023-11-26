# Este código utiliza el framework Django para desarrollo web.
# Contiene vistas y funcionalidades relacionadas con la gestión de usuarios y viajes.

import json

import googlemaps

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserSearchForm, CustomAuthenticationForm, LicenseVerificationForm,RegistroConductorForm, RegistroEstudianteForm, CoordenadaForm, UserForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import (
    UserSearchForm,
    CustomAuthenticationForm,
    LicenseVerificationForm,
    RegistroConductorForm,
    RegistroEstudianteForm,
    CoordenadaForm,
    CalificacionForm,
)
from .models import Role, Usuario, Calificacion
import conductor_amigo.settings as settings 

@login_required
def buscar_usuario(request):
    """
    Muestra una lista de usuarios filtrados según los parámetros de búsqueda.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.

    Returns:
        HttpResponse: Una respuesta HTTP que muestra la plantilla 'pasajeros/busqueda_usuarios.html'
                     con la lista de usuarios filtrados.

    Raises:
        None

    Notes:
        - Esta vista requiere que el usuario esté autenticado. La decoración '@login_required' se
          encarga de redirigir a la página de inicio de sesión si el usuario no ha iniciado sesión.
    # Obtén los parámetros de búsqueda del request
    """
    username = request.GET.get('username', '')

    # Filtra los usuarios según los parámetros de búsqueda
    users = Usuario.objects.filter(username__icontains=username)

    # Renderiza la plantilla con los resultados de la búsqueda
    return render(request, 'pasajeros/busqueda_usuarios.html', {'users': users})

def usuario_discapacidad(request):
    """
    Vista para buscar usuarios con discapacidad y mostrar los resultados.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'pasajeros/usuario_discapacidad.html' con el formulario y los datos devueltos.
    """
    data_returned = None
    
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            data_returned = form.search_user_disability()
    else:
        form = UserSearchForm()

    return render(request, 'pasajeros/usuario_discapacidad.html', {'form': form, 'data_returned': data_returned})

@login_required
def verificar_licencia(request):
    """
    Vista para verificar la licencia de un conductor.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'conductores/verificar_licencia.html' con el formulario de verificación de licencia.
    """
    form = LicenseVerificationForm()

    return render(request, 'conductores/verificar_licencia.html', {'form': form})

def login_view(request):
    """
    Vista para el inicio de sesión de usuarios.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'ingreso/login.html' con el formulario de inicio de sesión.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")              
            else:
                messages.error(request, "Error: Credenciales inválidas. Inténtalo de nuevo.")
                return redirect('login_view')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'ingreso/login.html', {'form': form})

def registro_inicial(request):
    """
    Vista para la página de registro inicial.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'ingreso/registro_inicial.html' para el registro inicial.
    """
    return render(request, 'ingreso/registro_inicial.html')

def registro_conductor(request):
    """
    Vista para el registro de conductores.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'ingreso/registro_conductor.html' con el formulario de registro de conductores.
    """
    if request.method == 'POST':
        form = RegistroConductorForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = Role.objects.get(name="Conductor")
            
            # Verifica y valida las imágenes subidas
            for file, field_name in [(user.foto_carnet, 'foto_carnet'), (user.foto_licencia_conducir, 'foto_licencia_conducir'), (user.foto_usuario, 'foto_usuario')]:
                if user.foto_usuario and not file.name.lower().endswith('.png'):
                    form.add_error(field_name, "Por favor, sube solo archivos PNG.")
                    messages.error(request, "Por favor, sube solo archivos PNG.")
                    return render(request, 'ingreso/registro_conductor.html', {'form': form})
                elif not user.foto_usuario and not file.name.lower().endswith('.png'):
                    form.add_error(field_name, "Por favor, sube solo archivos PNG.")
                    messages.error(request, "Por favor, sube solo archivos PNG.")                   
                    return render(request, 'ingreso/registro_conductor.html', {'form': form})
            
            user.save()
            messages.success(request, "Tu cuenta de conductor ha sido creada. Ahora puedes iniciar sesión.")
            return redirect('login_view')
        else:
            if 'username' in form.errors:
                messages.error(request, "Nombre de usuario ya existe.")
            elif 'password2' in form.errors:
                messages.error(request, "Contraseña no es suficiente segura. Prueba agregar todo tipo de caracteres")
            elif 'foto_carnet' in form.errors or 'foto_licencia_conducir' in form.errors:
                messages.error(request, "Por favor, sube tu licencia y carnet")
    else:
        form = RegistroConductorForm()

    return render(request, 'ingreso/registro_conductor.html', {'form': form})

def registro_estudiante(request):
    """
    Vista para el registro de estudiantes.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'ingreso/registro_estudiante.html' con el formulario de registro de estudiantes.
    """
    if request.method == 'POST':
        form = RegistroEstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = Role.objects.get(name="Pasajero")

            # Verifica y valida las imágenes subidas
            if user.foto_usuario:
                for file, field_name in [(user.foto_carnet, 'foto_carnet'), (user.foto_usuario, 'foto_usuario')]:
                    if not file.name.lower().endswith('.png'):
                        form.add_error(field_name, "Por favor, sube solo archivos PNG.")
                        messages.error(request, "Por favor, sube solo archivos PNG.")                        
                        return render(request, 'ingreso/registro_estudiante.html', {'form': form})
            else:
                for file, field_name in [(user.foto_carnet, 'foto_carnet')]:
                    if not file.name.lower().endswith('.png'):
                        form.add_error(field_name, "Por favor, sube solo archivos PNG.")
                        messages.error(request, "Por favor, sube solo archivos PNG.")   
                        return render(request, 'ingreso/registro_estudiante.html', {'form': form})
            user.save()
            messages.success(request, "Tu cuenta de estudiante ha sido creada. Ahora puedes iniciar sesión.")
            return redirect('login_view')
        else:
            if 'username' in form.errors:
                messages.error(request, "Nombre de usuario ya existe.")
            elif 'password2' in form.errors:
                messages.error(request, "Contraseña no es suficientemente segura. Prueba agregar diferentes tipos de caracteres.")
            elif 'foto_carnet' in form.errors:
                messages.error(request, "Por favor, sube una imagen PNG como foto de tu carnet")
    else:
        form = RegistroEstudianteForm()

    return render(request, 'ingreso/registro_estudiante.html', {'form': form})



def privacidad(request):
    """
    Vista para la página de políticas de privacidad.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'pasajeros/privacidad.html'.
    """
    return render(request, 'pasajeros/privacidad.html')

def profile(request, username=None):
    """
    Muestra el perfil del usuario actual o del usuario especificado.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        username (str, opcional): El nombre de usuario del usuario cuyo perfil se va a mostrar.
            Si no se proporciona, se mostrará el perfil del usuario actual.

    Returns:
        HttpResponse: Renderiza la página de perfil del usuario.
    """
    current_user = request.user
    if username and username != current_user.username:
        user = Usuario.objects.get(username=username)
    else:
        user = current_user
    return render(request, 'pasajeros/profile.html', {'user': user})

def get_route(request):
    """
    Obtiene y muestra la ruta entre dos ubicaciones utilizando la API de Google Maps.

    Si la solicitud es un POST, se procesa el formulario con las ubicaciones de origen
    y destino, y se utiliza la API de direcciones de Google Maps para obtener la ruta.
    Luego, se renderiza la página 'ruta.html' con los resultados de la dirección.

    Si la solicitud no es un POST, se renderiza la página 'formulario.html' para que
    el usuario ingrese las ubicaciones de origen y destino.

    Args:
        request (HttpRequest): El objeto HttpRequest que representa la solicitud del usuario.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página 'ruta.html' con los resultados
                     de la dirección si la solicitud es un POST; de lo contrario, renderiza
                     la página 'formulario.html'.
    """

    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')

        # Crear una instancia del cliente de Google Maps utilizando la clave API de configuración
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        # Obtener la ruta utilizando la API de direcciones de Google Maps
        directions_result = gmaps.directions(origin, destination, mode="driving")

        # Renderizar la página de la ruta con los resultados de la dirección
        return render(request, 'ruta.html', {'directions': directions_result})
    else:
        # Si la solicitud no es un POST, renderizar el formulario de entrada
        return render(request, 'formulario.html')

class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Vista basada en clase para la actualización del perfil de usuario.

    Esta vista utiliza el modelo de Usuario para actualizar la información del usuario
    actualmente autenticado. Requiere autenticación para acceder y muestra un formulario
    con campos específicos para la edición del perfil.

    Attributes:
        model (Model): El modelo que se está actualizando (Usuario en este caso).
        template_name (str): El nombre de la plantilla utilizada para la vista.
        fields (list): Lista de campos que se mostrarán y podrán editar en el formulario.
        success_message (str): Mensaje de éxito mostrado después de una actualización exitosa.

    Methods:
        get_object(queryset=None): Obtiene el objeto que se va a actualizar (usuario actual).
        form_valid(form): Asigna el usuario actual al campo 'usuario' en el formulario y
        llama al método form_valid de la clase padre.
    """
    model = Usuario

    # Nombre de la plantilla utilizada para la vista
    template_name = 'pasajeros/editar_usuario.html'

    # Campos que se mostrarán y se podrán editar en el formulario
    fields = ["username", "direccion", "foto_usuario", "rol", "incapacidad", "bibliografia"]

    # Mensaje de éxito mostrado después de una actualización exitosa
    success_message = "Perfil actualizado exitosamente"

    def get_object(self, queryset=None):
        """
        Obtiene el objeto que se va a actualizar (usuario actual).

        Args:
            queryset: Conjunto de objetos desde el cual seleccionar el objeto.

        Returns:
            Model: Objeto de modelo que se va a actualizar (usuario actual).
        """
        return self.request.user

    def form_valid(self, form):
        """
        Asigna el usuario actual al campo 'usuario' en el formulario y
        llama al método form_valid de la clase padre.

        Args:
            form: El formulario utilizado en la vista.

        Returns:
            HttpResponse: Respuesta HTTP después de una actualización exitosa.
        """
        # Asigna el usuario actual al campo 'usuario' en el formulario
        form.instance.usuario = self.request.user

        # Llama al método form_valid de la clase padre
        response = super(UserProfileUpdateView, self).form_valid(form)

        return response

    def get_success_url(self):
        # Retorna la URL de éxito después de la actualización
        return reverse('profile', args=[str(self.request.user.username)])

class ProfilePasswordChangeView(PasswordChangeView):
    """
    Vista basada en clase para el cambio de contraseña de perfil de usuario.

    Esta vista hereda de PasswordChangeView de Django y personaliza algunos aspectos,
    como el template utilizado, la URL de éxito y el formulario de cambio de contraseña.

    Attributes:
        template_name (str): El nombre de la plantilla utilizada para la vista.
        success_url (str): La URL a la que se redirige después de un cambio de contraseña exitoso.
        form_class (Form): Clase del formulario utilizado para el cambio de contraseña.

    Methods:
        get_context_data(**kwargs): Obtiene datos de contexto y agrega información adicional.
        form_valid(form): Realiza acciones adicionales después de un cambio de contraseña exitoso.
        form_invalid(form): Muestra un mensaje de error en caso de problemas con el formulario.
    """

    template_name = 'pasajeros/cambio_contraseña.html'
    success_url = reverse_lazy('login_view')
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
        """
        Obtiene datos de contexto y agrega información adicional.

        Args:
            **kwargs: Argumentos clave adicionales.

        Returns:
            dict: Datos de contexto actualizados.
        """
        context = super().get_context_data(**kwargs)
        context['password_changed'] = self.request.session.get('password_changed', False)
        return context

    def form_valid(self, form):
        """
        Realiza acciones adicionales después de un cambio de contraseña exitoso.

        Args:
            form: El formulario utilizado en la vista.

        Returns:
            HttpResponse: Respuesta HTTP después de un cambio de contraseña exitoso.
        """
        usuario = Usuario.objects.get(username=self.request.user.username)
        usuario.created_by_admin = False
        usuario.save()

        # Mostrar mensaje de éxito y actualizar la sesión de autenticación
        messages.success(self.request, 'Cambio de contraseña exitoso')
        update_session_auth_hash(self.request, form.user)
        self.request.session['password_changed'] = True
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Muestra un mensaje de error en caso de problemas con el formulario.

        Args:
            form: El formulario utilizado en la vista.

        Returns:
            HttpResponse: Respuesta HTTP después de un problema con el formulario.
        """
        # Mostrar mensaje de error en caso de un problema con el formulario
        messages.error(
            self.request,
            'Hubo un error al momento de intentar cambiar la contraseña: {}.'.format(
                form.errors.as_text()
            )
        )
        return super().form_invalid(form)

@login_required
def calificar_usuario(request, username):
    """
    Vista para calificar a un usuario. Requiere autenticación.

    Parameters:
    - request: La solicitud HTTP.
    - username: El nombre de usuario del usuario a calificar.

    Returns:
    - Si la solicitud es un POST y el formulario es válido, redirecciona al perfil del usuario calificado.
    - Si la solicitud no es un POST, muestra el formulario de calificación vacío.
    """
    # Obtener el usuario calificado y el calificador
    calificado = get_object_or_404(Usuario, username=username)
    calificador = request.user

    if request.method == 'POST':
        # Procesar el formulario si la solicitud es un POST
        form = CalificacionForm(request.POST, user_role=calificado.rol_id)
        if form.is_valid():
            # Guardar la calificación y actualizar los promedios
            calificacion = form.save(commit=False)
            calificacion.calificador = calificador
            calificacion.calificado = calificado
            calificacion.save()

            actualizar_promedios(calificado)

            return redirect('profile', username=username)
    else:
        # Mostrar un formulario vacío si la solicitud no es un POST
        form = CalificacionForm(user_role=calificado.rol_id)

    # Renderizar la plantilla con el formulario y el usuario calificado
    return render(request, 'pasajeros/calificar.html', {'form': form, 'calificado': calificado})

def actualizar_promedios(usuario):
    """
    Actualiza los promedios de un usuario basado en sus calificaciones.

    Parameters:
    - usuario: El objeto de usuario cuyos promedios se deben actualizar.
    """
    # Obtener todas las calificaciones para el usuario dado
    calificaciones = Calificacion.objects.filter(calificado=usuario)

    # Inicializar variables para calcular los promedios
    suma_manejo = suma_higiene = suma_charla = suma_puntualidad = suma_general = 0
    conteo_manejo = conteo_higiene = conteo_charla = conteo_puntualidad = conteo_general = 0

    # Iterar sobre todas las calificaciones y actualizar las sumas y conteos
    for calificacion in calificaciones:
        if calificacion.categoria == 'Manejo':
            suma_manejo += int(calificacion.calificacion)
            conteo_manejo += 1
        elif calificacion.categoria == 'Higiene':
            suma_higiene += int(calificacion.calificacion)
            conteo_higiene += 1
        elif calificacion.categoria == 'Charla':
            suma_charla += int(calificacion.calificacion)
            conteo_charla += 1
        elif calificacion.categoria == 'Puntualidad':
            suma_puntualidad += int(calificacion.calificacion)
            conteo_puntualidad += 1
        elif calificacion.categoria == 'General':
            suma_general += int(calificacion.calificacion)
            conteo_general += 1

    # Calcular promedios y actualizar el objeto usuario
    usuario.promedio_manejo = suma_manejo / conteo_manejo if conteo_manejo != 0 else 0
    usuario.promedio_higiene = suma_higiene / conteo_higiene if conteo_higiene != 0 else 0
    usuario.promedio_charla = suma_charla / conteo_charla if conteo_charla != 0 else 0
    usuario.promedio_puntualidad = suma_puntualidad / conteo_puntualidad if conteo_puntualidad != 0 else 0
    usuario.promedio_general = suma_general / conteo_general if conteo_general != 0 else 0

    # Guardar los cambios en el objeto usuario
    usuario.save()