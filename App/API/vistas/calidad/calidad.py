
from django.http import JsonResponse
from App.ZTime.conexion import *
import json
from django.http import HttpResponse, Http404
from PIL import Image
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.

##COMPROBAR SI LA IMAGEN EXISTE EN LA TABLA
def verificar_existencia(id):
    try:
        app = zetoneApp()
        cursor = app.cursor()
        sql =("SELECT Bulto FROM imagenes_reporte_empaque WHERE Bulto='" + str(id) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if consulta:
            return 1
        else:
            return 0
    except Exception as e:
        print("Error")
        print(e)
        return 5
    finally:
        cursor.close()
        app.close()

def inserta_nombre_caja(bulto,nombre):
    try:
        app = zetoneApp()
        cursor = app.cursor()
        sql =("INSERT INTO imagenes_reporte_empaque (Bulto, Caja) VALUES ('" + str(bulto) + "','" + str(nombre) + "')")
        cursor.execute(sql)
        cursor.commit()
    except Exception as e:
        print("Error")
        print(e)
        return 5
    finally:
        cursor.close()
        app.close()

@csrf_exempt
def image_caja(request):
    if request.method == 'POST' and request.POST.get('caja'):
        nombre_post = request.POST.get('id')
        imagen_codificada = request.POST.get('caja')
        imagen = base64.b64decode(imagen_codificada)
        nombre = "caja_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre , "wb") as image:
            image.write(imagen)
        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre)
        return JsonResponse({'mensaje': 'Imagen subida exitosamente.'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})
    
@csrf_exempt
def image_plu(request):
    if request.method == 'POST' and request.POST.get('plu'):
        nombre_post = request.POST.get('id')
        imagen_codificada = request.POST.get('plu')
        imagen = base64.b64decode(imagen_codificada)
        nombre = "plu_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre , "wb") as image:
            image.write(imagen)
        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre)
        return JsonResponse({'mensaje': 'Imagen subida exitosamente.'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})
    
@csrf_exempt
def image_caja_plu(request):
    if request.method == 'POST' and request.POST.get('caja'):
        nombre_post = request.POST.get('id')

        imagen_codificada_caja = request.POST.get('caja')
        imagen_caja = base64.b64decode(imagen_codificada_caja)
        nombre_caja = "caja_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre_caja , "wb") as image_caja:
            image_caja.write(imagen_caja)

        imagen_codificada_plu = request.POST.get('plu')
        imagen_plu = base64.b64decode(imagen_codificada_plu)
        nombre_plu = "plu_image_" + str(nombre_post) + ".jpeg"
        with open('App/API/media/images/Calidad/reportes_empaque/' + nombre_plu , "wb") as image_plu:
            image_plu.write(imagen_plu)

        if verificar_existencia(nombre_post) == 0:
            inserta_nombre_caja(nombre_post, nombre_caja)
        return JsonResponse({'mensaje': 'Imagen subida exitosamente.'})
    else:
        return JsonResponse({'error': 'Error al subir la imagen.'})
    

import os
from django.http import HttpResponse

def ver_caja(request, nombre):
    ruta_imagenes = 'App/API/media/images/Calidad/reportes_empaque/'
    
    ruta_completa = os.path.join(ruta_imagenes, nombre)
    
    if os.path.exists(ruta_completa):
        with open(ruta_completa, 'rb') as archivo_imagen:
            respuesta = HttpResponse(archivo_imagen.read(), content_type='image/jpeg')
            respuesta['Content-Disposition'] = 'inline; filename=' + os.path.basename(ruta_completa)
            return respuesta
    else:
        return HttpResponse(status=404)
