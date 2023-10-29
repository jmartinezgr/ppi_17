# Este código utiliza el framework Django para desarrollo web.
# Contiene vistas y funcionalidades relacionadas con la gestión de usuarios y viajes.

from django.shortcuts import render, redirect
from .forms import UserSearchForm, CustomAuthenticationForm, LicenseVerificationForm,RegistroConductorForm, RegistroEstudianteForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Role,Usuario
import json

@login_required
def buscar_usuario(request):
    """
    Vista para buscar usuarios y mostrar los resultados.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'pasajeros/busqueda_usuarios.html' con el formulario y los datos devueltos.
    """
    data_returned = None
    
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            data_returned = form.search()
    else:
        form = UserSearchForm()

    return render(request, 'pasajeros/busqueda_usuarios.html', {'form': form, 'data_returned': data_returned})

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

@login_required
def detalle_viaje(request):
    """
    Vista para mostrar detalles de un viaje.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'conductores/viaje.html' con los detalles del viaje.
    """
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

@login_required
def lista_viajes(request):
    """
    Vista para mostrar una lista de viajes.

    Args:
        request: Solicitud HTTP enviada por el cliente.

    Returns:
        Renderiza la plantilla 'pasajeros/lista_viajes.html' con la lista de viajes.
    """
    viajes = [
        {
            'conductor': 'Juan Pérez',
            'destino': 'Plaza Principal',
            'hora_salida': '09:00 AM',
        },
        {
            'conductor': 'María González',
            'destino': 'Parque Central',
            'hora_salida': '10:30 AM',
        },
        {
            'conductor': 'Carlos Rodríguez',
            'destino': 'Estación de Tren',
            'hora_salida': '12:15 PM',
        },
        {
            'conductor': 'Laura Martínez',
            'destino': 'Centro Comercial',
            'hora_salida': '02:00 PM',
        },
        {
            'conductor': 'Pedro Sánchez',
            'destino': 'Museo de Arte',
            'hora_salida': '03:45 PM',
        },
    ]

    context = {'viajes': viajes}
    return render(request, 'pasajeros/lista_viajes.html', context)

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
        user = Usuario.object.get(username=username)
    else:
        user = current_user
    return render(request, 'pasajeros/profile.html', {'user': user})