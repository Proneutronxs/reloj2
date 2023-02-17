from django.urls import path
from App.ZTime import views

urlpatterns = [

### sólo renderizado
path('', views.index, name="index"),
path('resgistros/calculo', views.renderCalcHoras, name="calculo_horas"),
path('registros/ver', views.renderVerRegistros, name="ver_registros"),


##A JAVASCRIPT
path('resgistros/calculo/horas', views.calculoHorasJson, name="registros_calculo"),
path('registros/sin/proceso', views.ver_registros_sin_proceso , name='registros_no_proceso'),


path('prueba/html', views.pruebaHTML, name="pruebahtml"),
path('prueba', views.prueba, name="prueba"),

##PRUEBA POST DATA http://10.32.26.49:8000/post/data
path('post/data', views.post_recive_data, name="post_recive_data"),


## CREACIÓN DEL EXCEL SOLO REGISTROS
path('create/excel/registros', views.excelCreateRegistros, name='create_excel'),
## CREACIÓN DEL EXCEL CALCULO DE HORAS
path('create/excel/calculo', views.createExcelCalculo, name='create_excel'),
## DESCARGA EXCEL 
path('download-excel/<str:file_path>', views.download_excel, name='download_excel'),
## ELIMINAR ARCHIVOS
path('delete/file/excel', views.delete_xlsx_files, name='delete_file'),




]