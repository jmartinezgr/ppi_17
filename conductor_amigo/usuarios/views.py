from django.shortcuts import render
from .forms import UserSearchForm

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

    