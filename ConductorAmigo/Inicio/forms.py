from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, label="Nombre de Usuario")
    identification = forms.CharField(max_length=20, required=False, label="Identificación de Usuario")
    user_type = forms.ChoiceField(choices=[('estudent', 'Estudiante'), ('conductor', 'Condcutor')], required=False, label="Tipo de Usuario")

    def search(self):
        username = self.cleaned_data.get('username')
        identification = self.cleaned_data.get('identification')

        # Ahora puedes acceder a los valores de 'username' e 'identification'
        # y realizar cualquier lógica de búsqueda que necesites aquí
        print('Nombre de Usuario:', username)
        print('Identificación de Usuario:', identification)

        return username


# class UserSearchForm(UserCreationForm):
    
#     class Meta:
#         model = User
#         fields = ["first_name", "id"]
