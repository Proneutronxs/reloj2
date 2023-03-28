from pyexpat import model
from django import forms
from App.ZTime.models import *

class form_ver_registros(forms.ModelForm):
    legajo = forms.IntegerField()
    departamento = forms.CharField(max_length=25)
    desde = forms.DateField()
    hasta = forms.DateField()

    class Meta:
        model = model_buscar_legajo
        fields = ['legajo', 'departamento', 'desde', 'hasta']

class form_export_registros(forms.ModelForm):
    legajo = forms.IntegerField()
    departamento = forms.CharField(max_length=25)
    desde = forms.DateField()
    hasta = forms.DateField()
    export = forms.CharField(max_length=25)

    class Meta:
        model = model_exportar_legajo
        fields = ['legajo', 'departamento', 'desde', 'hasta', 'export']

class form_proceso_fichadas(forms.ModelForm):
    fecha = forms.DateField()
    departamento = forms.CharField(max_length=25)
    
    class Meta:
        model = model_proceso_fichadas
        fields = ['fecha', 'departamento']
