from django.urls import path
from App.Frio import views

urlpatterns = [
    
    path('', views.indexFrio, name="Index_frio"),
    path('camaras/controlTemperaturas', views.control_camaras, name="control_camaras"),

    ##JS


    path('espacio', views.espacioUsado, name="espa-cio"),#VERIFICA EL ESPACIO
    path('compresspdf', views.zipPDF, name="compressPDF"),#DEVUELVE NOMBRE DEL ZIP
    path('descargazip/<str:zip_name>', views.download_zip, name="descarga_ZIP"),#DESCARGA EL ARCHIVO ZIP
    path('delete/zip-pdf', views.borrar_pdf_zip, name="delete_zip_pdf"),#BORRA ARCHIVOS ZIP Y PDF
    path('delete/excel-files', views.delete_xlsx, name="delete_excel"),#BORRA ARCHIVOS EXCEL
    path('delete/images', views.borrar_imagenes, name="delete_excel"),#BORRA IMAGENES

]