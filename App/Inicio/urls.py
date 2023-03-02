from django.urls import path
from App.Inicio import views

urlpatterns = [

    path('menu/', views.Index_inicio, name="Index_inicio"),
    path('', views.inicio, name="Inicio"),


    path('user/permissions/modulo=<str:modulo>', views.json_premissions, name="permisos_json"),

]