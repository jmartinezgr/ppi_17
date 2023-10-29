# Este código utiliza funciones y clases proporcionadas por Django para
# definir formularios de autenticación, búsqueda y registro de usuarios.

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario


class UserSearchForm(forms.Form):
    """
    Formulario para buscar usuarios.

    Permite buscar usuarios por nombre de usuario, identificación, tipo de usuario y tipo de discapacidad.
    """
    username = forms.CharField(
        max_length=100,
        required=False,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'})
    )
    
    identification = forms.CharField(
        max_length=20,
        required=False,
        label="Identificación de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'})
    )
    
    USER_TYPE_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('conductor', 'Conductor'),
    ]

    DISABILITY_TYPE_CHOICES = [
        ('None', "Selecciona una opción"),
        ('silla de ruedas', 'Silla de ruedas'),
        ('muletas', 'Muletas'),
        ('discapacidad auditiva', 'Discapacidad Auditiva'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=False,
        label="Tipo de Usuario",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )

    disability_type = forms.ChoiceField(
        choices=DISABILITY_TYPE_CHOICES,
        required=False,
        label="Tipo de Discapacidad",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )

    def search(self):
        """
        Realiza una búsqueda de usuarios.

        Returns:
            str: Nombre de usuario buscado.
        """
        username = self.cleaned_data.get('username')
        identification = self.cleaned_data.get('identification')
        user_type = self.cleaned_data.get('user_type')

        # Lógica de búsqueda aquí
        return username

    def search_user_disability(self):
        """
        Realiza una búsqueda de usuarios con discapacidad.

        Returns:
            str: Resultado de la búsqueda.
        """
        result = ""
        username = self.cleaned_data['username']
        identification = self.cleaned_data['identification']
        disability_type = self.cleaned_data.get('disability_type')

        # Realiza la validación específica aquí
        if disability_type:
            result += f", Tipo de Discapacidad: {disability_type}"
        else:
            result = f"Usuario validado - Nombre: {username}, Identificación: {identification}"

class RegistroConductorForm(UserCreationForm):
    foto_carnet = forms.ImageField(
        required=False,
        help_text='Sube una imagen PNG de tu carné de conductor.'
    )
    foto_licencia_conducir = forms.ImageField(
        required=False,
        help_text='Sube una imagen PNG de tu licencia de conducir.'
    )
    foto_usuario = forms.ImageField(
        required=False,
        help_text='Sube una imagen PNG de tu perfil.'
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'nombres', 'apellidos', 'nacimiento', 'direccion', 'privacidad', 'foto_carnet', 'foto_licencia_conducir', 'foto_usuario']
    def __init__(self, *args, **kwargs):
        super(RegistroConductorForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombres'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class': 'form-control'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['privacidad'].widget.attrs.update()
        self.fields['foto_carnet'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_licencia_conducir'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_usuario'].widget.attrs.update({'class': 'custom-file-input'})

class RegistroEstudianteForm(UserCreationForm):
    foto_carnet = forms.ImageField(
        required=False,
        help_text='Sube una imagen PNG de tu carné de conductor.'
    )
    
    foto_usuario = forms.ImageField(
        required=False,
        help_text='Sube una imagen PNG de tu perfil.'
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'nombres', 'apellidos', 'nacimiento', 'direccion', 'privacidad', 'foto_usuario','foto_carnet']

    def __init__(self, *args, **kwargs):
        super(RegistroEstudianteForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombres'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class': 'form-control'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['privacidad'].widget.attrs.update()
        self.fields['foto_carnet'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_usuario'].widget.attrs.update({'class': 'custom-file-input'})


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado.

    Personaliza el formulario de autenticación de Django para el inicio de sesión.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class LicenseVerificationForm(forms.Form):
    """
    Formulario de verificación de licencia de conductor.

    Permite a los conductores verificar su número de licencia.
    """
    license_number = forms.CharField(
        max_length=20,
        label="Número de Licencia",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'})
    )
