from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('página_de_gracias')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

def privacidad(request):

    return render(request,'privacidad.html')
