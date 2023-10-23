from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login, logout
from .forms import CustomUserCreationForm
from .forms import UserSearchForm


def home(request):
    
    eventos = [
    {'titulo': 'Retraso en la Línea 1', 'descripcion': 'Se reporta un retraso en la Línea 1 debido a problemas técnicos.', 'fecha': '2023-10-10'},
    {'titulo': 'Cierre temporal de estación', 'descripcion': 'La estación Plaza Mayor estará cerrada temporalmente por mantenimiento.', 'fecha': '2023-10-12'},
    {'titulo': 'Nuevo horario de servicio', 'descripcion': 'A partir de hoy, la red de metro operará con un nuevo horario de servicio.', 'fecha': '2023-10-15'},
    {'titulo': 'Apertura de una nueva estación', 'descripcion': 'La estación Central Park abre sus puertas al público a partir de mañana.', 'fecha': '2023-10-18'},
    {'titulo': 'Trabajo en vías', 'descripcion': 'Se llevarán a cabo trabajos en las vías de la Línea 3, lo que podría causar retrasos temporales.', 'fecha': '2023-10-20'},
    {'titulo': 'Evento especial en estación', 'descripcion': 'Hoy habrá un evento especial en la estación Waterfront, con actividades y entretenimiento para los pasajeros.', 'fecha': '2023-10-22'},
    {'titulo': 'Cambio en el acceso a la estación', 'descripcion': 'El acceso a la estación Riverside se cambiará temporalmente debido a construcción.', 'fecha': '2023-10-25'},
]

    context = {'eventos': eventos}
    
    return render(request, "mainapp/home.html",context)

def login(request):
    return render(request, "registration/login.html")

#@login_required
def busquedaGeneral(request):
    return render(request, "mainapp/busqueda.html")

def exit(request):
    logout(request)
    return redirect("home")

def register(request):
    data = {
        "form": CustomUserCreationForm()
    }

    if request.method == "POST":
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data["username"],
                                 password=user_creation_form.cleaned_data["password1"])
            login(request, user)

            return redirect("home")
    return render(request, "registration/register.html", data)

def verificarLicencia(request):
    return render(request, "mainapp/verificarLicencia.html")

def buscar_usuario(request):
    form = UserSearchForm(request.POST)
    data_returned = None
    if request.method == 'POST':
        if form.is_valid():
           data_returned = form.search()
        else:
            form = UserSearchForm()

    return render(request, 'mainapp/busqueda.html', {'form': form, 'data_returned': data_returned})

def detalle_viaje(request):
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
    return render(request, 'mainapp/viajes.html', context)

def lista_viajes(request):
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
    return render(request, 'mainapp/lista_viajes.html', context)