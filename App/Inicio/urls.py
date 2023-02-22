from django.urls import path
from App.Inicio import views

urlpatterns = [

    path('', views.index, name="Index"),
]