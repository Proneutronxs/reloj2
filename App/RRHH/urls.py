from django.urls import path
from App.RRHH import views

urlpatterns = [

### sólo renderizado
path('', views.rrhh, name="rrhh"),

path('departamentos/', views.departamentos, name="departamentos"),

path('horarios/', views.horarios, name="horarios"),



path('fichadas/', views.fichadas, name="fichadas"),

### JAVASCRIPT
path('departamentos/llama-departamentos/', views.llamaDepartamentos, name="llamaDepartamentos"),
path('departamentos/guarda-departamentos/', views.guardaDepartamento, name="guardaDepartamentos"),

path('horarios/guarda-horarios/', views.guardaTurno, name="guardaTurnos"),
path('horarios/muestra-legajos-departamentos/', views.llamaLegajos_Departamentos, name="llamaLegajos_Departamentos"),
path('horarios/carga-combox-horarios/', views.llamaTurnosHorarios, name="carga-combox-horarios"),


path('formulario-quejas/comentario/', views.guardaFormulario, name="guarda_comentario_quejas"),


path('fichadas/carga-departamentos/', views.cargaDepartamentos, name="fichadas_carga_departamentos"),


]