from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from cuentas.models import Perfil

# Formulario para crear nuevos usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    telefono = forms.CharField()
    rol = forms.ChoiceField(choices=Perfil.ROLES)

    email.widget.attrs['class'] = 'form-control'
    telefono.widget.attrs['class'] = 'form-control'
    rol.widget.attrs['class'] = 'form-control'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Perfil.objects.update_or_create(
                usuario=user,
                defaults={
                    'rol': self.cleaned_data['rol'],
                    'telefono': self.cleaned_data['telefono']
                }
            )
        return user


# Formulario para Editar el Rol y Teléfono de un Usuario
class PerfilEditarForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=Perfil.ROLES)
    telefono = forms.CharField()

    rol.widget.attrs['class'] = 'form-control'
    telefono.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Perfil
        fields = ['rol', 'telefono']