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
