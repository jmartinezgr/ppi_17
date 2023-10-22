from django import forms

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
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=False,
        label="Tipo de Usuario",
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
