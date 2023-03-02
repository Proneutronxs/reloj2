from django.urls import path
from App.Empaque import views

urlpatterns = [

    path('', views.indexEmpaque, name="Index_empaque"),
]