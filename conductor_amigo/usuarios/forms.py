from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm


class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=False, 
        label="Nombre de Usuario", 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control rounded-pill'
                }
            )
        )
    
    identification = forms.CharField(
        max_length=20, required=False, 
        label="Identificación de Usuario", 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control rounded-pill'
                }
            )
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
        username = self.cleaned_data.get('username')
        identification = self.cleaned_data.get('identification')
        user_type = self.cleaned_data.get('user_type')

        # Aquí puedes realizar la lógica de búsqueda
        print('Nombre de Usuario:', username)
        print('Identificación de Usuario:', identification)
        print('Tipo de Usuario:', user_type)

        return username

    def search_user_disability(self):
        result = ""
        username = self.cleaned_data['username']
        identification = self.cleaned_data['identification']
        disability_type = self.cleaned_data.get('disability_type')

        # Realiza la validación específica aquí

        # Ejemplo: Validación simple para mostrar un mensaje de éxito
        
        if disability_type:
            result += f", Tipo de Discapacidad: {disability_type}"
        else:
            result = f"Usuario validado - Nombre: {username}, Identificación: {identification}"

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )