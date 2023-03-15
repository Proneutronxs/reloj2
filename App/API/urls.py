from django.urls import path
from App.API.vistas.calidad import calidad 

urlpatterns = [
    
    path('calidad/image/box', calidad.image_caja, name="guarda_caja_imagen"),

]