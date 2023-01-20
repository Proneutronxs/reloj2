from pyexpat import model
from django import forms
from App.ZTime.models import model_buscar_legajo

class form_ver_registros(forms.ModelForm):
    legajo = forms.IntegerField()
    departamento = forms.CharField(max_length=25)
    desde = forms.DateField()
    hasta = forms.DateField()

    class Meta:
        model = model_buscar_legajo
        fields = ['legajo', 'departamento', 'desde', 'hasta']