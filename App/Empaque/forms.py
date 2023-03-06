from pyexpat import model
from django import forms
from App.Empaque.models import *

class form_ver_registros(forms.ModelForm):
    fechaReporte = forms.DateField()
    planta = forms.CharField(max_length=25)

    class Meta:
        model = model_buscar_reportes_camaras
        fields = ['fechaReporte', 'planta']


class form_ver_reportes_camara(forms.ModelForm):
    fechaReporte = forms.DateField()
    hora = forms.CharField(max_length=25)
    planta = forms.CharField(max_length=25)

    class Meta:
        model = model_buscar_reportes_camaras
        fields = ['fechaReporte', 'hora', 'planta']