from django.urls import path
from App.Empaque import views

urlpatterns = [

    path('', views.indexEmpaque, name="Index_empaque"),

    path('new-empaque/', views.newIndexEmpaque, name="new_empaque"),

    path('new-reportes/', views.newReportes, name="new_reportes_calidad"),

    

    path('reportes/camaras', views.reportes_camaras, name="reportes_camaras"),

    ###POST SCRIPT JS
    path('reportes/camaras/buscar', views.post_busqueda_reporte_camaras, name="buscar_reportes_camaras"),
    ##DESCARGA DEL PDF
    path('reportes/donwload/<str:filename>', views.descarga_pdf_control_camaras, name="download_pdf_control_camaras"),


    ###NUEVAAAA
    path('calidad-reportes/', views.ReportesEmpaqueCalidad, name="reportes_calidad_empaque"),

    path('calidad-reportes/busqueda-cajas/', views.consultaCajas, name='calidad_busqueda_cajas'),

    path('calidad-reportes/mostrar-caja/<str:nombre>', views.vizualizarImagen, name='empaque_calidad_mostrar_caja'),


]