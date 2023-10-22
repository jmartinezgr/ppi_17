from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login, logout

# Create your views here.

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

    user = request.user  # Obtén el usuario autenticado
    context = {'eventos': eventos, 'user': user}
    
    return render(request, "unregister/home.html",context)  

def nosotros(request):

    return render(request,'unregister/nosotros.html')

def logout_view(request):
    logout(request=request)
    return redirect('login_view')