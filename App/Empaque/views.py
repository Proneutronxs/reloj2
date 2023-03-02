from django.shortcuts import render

# Create your views here.


def indexEmpaque(request):
    return render (request, 'Empaque/Inicio/index.html')