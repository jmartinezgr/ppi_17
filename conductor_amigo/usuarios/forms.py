# Este código utiliza funciones y clases proporcionadas por Django para
# definir formularios de autenticación, búsqueda y registro de usuarios.

from django import forms
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
    nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    incapacidad = forms.ChoiceField(
        choices=Usuario.INCAPACIDAD_CHOICES,
        required=True,
        label="Incapacidad",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
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
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['privacidad'].widget.attrs.update()
        self.fields['foto_carnet'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_licencia_conducir'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_usuario'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['incapacidad'].widget.attrs.update({'class': 'form-control'})

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

    nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    incapacidad = forms.ChoiceField(
        choices=Usuario.INCAPACIDAD_CHOICES,
        required=True,
        label="Incapacidad",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )
    
    def __init__(self, *args, **kwargs):
        super(RegistroEstudianteForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombres'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class': 'form-control'})
        self.fields['nacimiento'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['privacidad'].widget.attrs.update()
        self.fields['foto_carnet'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['foto_usuario'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['incapacidad'].widget.attrs.update({'class': 'form-control'})        


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

class CoordenadaForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill'})
    )

    ENDING_PLACE_CHOICES = [
        ('None', "Selecciona una opción"),
        ((6.253520142772332, -75.58292149217107), 'Metro Suramericana - Salida de la 65'),
        ((6.2592766751606215, -75.59785206576802), 'Metro Floresta - Salida Autopista Norte'),
        ((6.278480487535483, -75.56953613913925), 'Metro Caribe - Salida de la 80'),
        ((6.269538437023643, -75.56620835977748), 'Metro UdeA - Salida de la 66b'),
        ((6.230579395186508, -75.57593281026912), 'Metro Industriales - Autopista Norte'),

    ]

    STARTING_PLACE_CHOICES = [
        ('None', "Selecciona una opción"),
        ((6.260699999606895, -75.57953881377448), 'Sede Volador - Salida de la 65'),
        ((6.259629620843638, -75.57556499754875), 'Sede Volador - Salida Autopista Norte'),
        ((6.274057506330517, -75.59252364426453), 'Sede Robledo - Salida de la 80'),
        ((6.275527354991391, -75.59099154868524), 'Sede Robledo - Salida de la 66b'),
        ((6.263575166707227, -75.57482065639084), 'Sede Rio - Autopista Norte'),
    ]

    ending_place_type = forms.ChoiceField(
        choices = ENDING_PLACE_CHOICES,
        required=False,
        label="Lugar de destino",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )


    starting_place_type = forms.ChoiceField(
        choices=STARTING_PLACE_CHOICES,
        required=False,
        label="Lugar de partida",
        widget=forms.Select(attrs={'class': 'form-control rounded-pill', 'style': 'text-align:center;'})
    )