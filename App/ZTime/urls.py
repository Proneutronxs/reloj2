from django.urls import path
from App.ZTime import views

urlpatterns = [

### sólo renderizado
path('', views.index, name="index"),
path('resgistros/calculo', views.renderCalcHoras, name="calculo_horas"),
path('registros/ver', views.renderVerRegistros, name="ver_registros"),


##A JAVASCRIPT
path('json', views.calculoHorasJson, name="json"),
path('registros/sin/proceso', views.ver_registros_sin_proceso , name='registros_no_proceso'),


path('prueba/html', views.pruebaHTML, name="pruebahtml"),
path('prueba', views.prueba, name="prueba"),


path('download/register', views.downloadRegister, name="downloadRegister"),

## DESCARGA EXCEL 
path('download/excel', views.descargar_archivo, name="downloadExcel"),



]