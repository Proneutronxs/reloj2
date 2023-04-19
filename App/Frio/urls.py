from django.urls import path
from App.Frio import views

urlpatterns = [
    
    path('', views.indexFrio, name="Index_frio"),
    path('camaras/controlTemperaturas', views.control_camaras, name="control_camaras"),

]