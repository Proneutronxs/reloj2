from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def indexFrio(request):
    return render (request, 'Frio/Inicio/index.html')

@login_required
def control_camaras(request):
    return render (request, 'Frio/ControlCamaras/ControlTemp.html')