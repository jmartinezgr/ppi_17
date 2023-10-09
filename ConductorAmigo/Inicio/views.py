from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login, logout
from .forms import CustomUserCreationForm
from .forms import UserSearchForm


def home(request):
    return render(request, "mainapp/home.html")

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