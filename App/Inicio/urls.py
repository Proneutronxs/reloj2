from django.urls import path
from App.Inicio import views

urlpatterns = [

    path('old/', views.inicioMenu, name="inicio_principal"),

    path('', views.newIndex, name="new_principal"),

    path('repassword/', views.repassword, name="repassword"),

    #path('inicio/', views.inicioMenu, name="inicio_menu"),

    path('user/permissions/modulo=<str:modulo>', views.json_premissions, name="permisos_json"),
]