from django.urls import path
from App.Empaque import views

urlpatterns = [

    path('', views.indexEmpaque, name="Index_empaque"),
    path('reportes/camaras', views.reportes_camaras, name="reportes_camaras"),

    ###POST SCRIPT JS
    path('reportes/camaras/buscar', views.post_busqueda_reporte_camaras, name="buscar_reportes_camaras"),
    ##DESCARGA DEL PDF
    path('reportes/donwload/<str:filename>', views.descarga_pdf_control_camaras, name="download_pdf_control_camaras"),


]