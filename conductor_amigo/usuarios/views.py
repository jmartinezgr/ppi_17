from .forms import UserSearchForm
from .forms import CustomAuthenticationForm # Importa el formulario personalizado
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def buscar_usuario(request):
    data_returned = None
    
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            data_returned = form.search()
    else:
        form = UserSearchForm()

    return render(request, 'pasajeros/busqueda_usuarios.html', {'form': form, 'data_returned': data_returned})

def usuario_discapacidad(request):
    data_returned = None
    
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            data_returned = form.search_user_disability()
    else:
        form = UserSearchForm()

    return render(request, 'pasajeros/usuario_discapacidad.html', {'form': form, 'data_returned': data_returned})


def login_view(request):
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
    
    return render(request, 'pasajeros/login.html', {'form': form})
    