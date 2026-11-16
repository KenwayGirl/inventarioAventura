from django import forms
from experiencias.models import Categoria, Experiencia, Reserva

class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField()
    descripcion = forms.CharField()
    estado = forms.ChoiceField(choices=Categoria.ESTADOS)

    nombre.widget.attrs['class'] = 'form-control'
    descripcion.widget.attrs['class'] = 'form-control'
    estado.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Categoria
        fields = '__all__'


class ExperienciaForm(forms.ModelForm):
    titulo = forms.CharField()
    descripcion = forms.CharField()
    precio = forms.IntegerField()
    cupo_maximo = forms.IntegerField()
    fecha_realizacion = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(estado='Activo'))

    titulo.widget.attrs['class'] = 'form-control'
    descripcion.widget.attrs['class'] = 'form-control'
    precio.widget.attrs['class'] = 'form-control'
    cupo_maximo.widget.attrs['class'] = 'form-control'
    fecha_realizacion.widget.attrs['class'] = 'form-control'
    categoria.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'precio', 'cupo_maximo', 'fecha_realizacion', 'categoria']