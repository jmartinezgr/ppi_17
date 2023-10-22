from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'celular', 'politicas_de_privacidad']

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo.endswith('@unal.edu.co'):
            raise forms.ValidationError('El correo electrónico debe terminar en @unal.edu.co')
        return correo
