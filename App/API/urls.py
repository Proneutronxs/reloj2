from django.urls import path
from App.API.vistas.calidad import calidad 

urlpatterns = [
    ######################### CALIDAD EMPAQUE ###################################

    path('calidad/image/caja', calidad.image_caja, name="guarda_caja_imagen"),
    path('calidad/image/plu', calidad.image_plu, name="guarda_plu_imagen"),
    path('calidad/image/caja_plu', calidad.image_caja_plu, name="guarda_plu_caja"),
    path('calidad/caja/<str:nombre>', calidad.ver_caja, name='ver_caja'),

    path('calidad/prueba', calidad.pruebas_sql, name="pruebas_sql"),

    ######################## MADUREZ DE FRUTOS ###########################

    path('calidad/presiones/inserta', calidad.inserta_presiones, name='inserta_presiones'),
    path('calidad/presiones/busqueda', calidad.busca_presiones, name='busca_presiones'),
    path('calidad/presiones/mostrar', calidad.muestra_presiones, name='muestra_presiones'),
    path('calidad/presiones/promedio', calidad.promedio_presiones, name='promedio_presiones'),

]