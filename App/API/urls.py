from django.urls import path
from App.API.vistas.calidad import calidad 

urlpatterns = [
    
    path('calidad/image/caja', calidad.image_caja, name="guarda_caja_imagen"),
    path('calidad/image/plu', calidad.image_plu, name="guarda_plu_imagen"),
    path('calidad/image/caja_plu', calidad.image_caja_plu, name="guarda_plu_caja"),
    path('calidad/caja/<str:nombre>', calidad.ver_caja, name='ver_caja'),

]