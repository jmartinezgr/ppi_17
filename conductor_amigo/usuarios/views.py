from django.shortcuts import render,redirect
from .forms import UserSearchForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required   
from .forms import RegistroForm 
from django.contrib import messages


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

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Tu cuenta ha sido creada. Ahora puedes iniciar sesión.")
            return redirect('login_view')
        else:
            print(form.errors) 
    else:
        form = RegistroForm()
    return render(request, 'pasajeros/registro.html', {'form': form})

def privacidad(request):
    return render(request,'pasajeros/privacidad.html')