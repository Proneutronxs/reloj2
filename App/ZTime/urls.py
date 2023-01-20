from django.urls import path
from App.ZTime import views

urlpatterns = [
path('', views.index, name="index"),
path('registros/ver', views.verRegistros, name="verRegistros"),
]