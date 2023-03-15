from django.http import JsonResponse
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.



@csrf_exempt
def image_caja(request):
    if request.method == 'POST' and request.POST.get('imagen'):
        nombre_post = request.POST.get('id')
        imagen_codificada = request.POST.get('imagen')
        imagen = base64.b64decode(imagen_codificada)
        nombre = "image_" + str(nombre_post) + ".JPEG"
        with open('App/API/media/images/reportes_empaque/' + nombre , "wb") as image:
            image.write(imagen)
        
        return JsonResponse({'mensaje': 'Imagen subida exitosamente.'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})