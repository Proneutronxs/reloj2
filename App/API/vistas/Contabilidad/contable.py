
from django.http import JsonResponse
from App.ZTime.conexion import *
import json
import os
from django.http import HttpResponse, Http404
from PIL import Image
from datetime import datetime
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import connections



@csrf_exempt
def guardar_periodo_habilitado(request):
    if request.method == 'POST':
        try:
            Fecha = str(request.POST.get('Fecha'))
            Empresa = str(request.POST.get('Empresa'))
            Accion = str(request.POST.get('Accion'))
            values = [Empresa,Fecha]
            with connections['ZETONE_9'].cursor() as cursor:
                cursor.execute('exec sp_usr_periodo %s,%s', values)
                cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
                affected_rows = cursor.fetchone()[0]
            if affected_rows > 0:
                if Accion == "H":
                    return JsonResponse({'Message': 'Success', 'Nota': "El periodo se Habilitó correctamente. " + str(values)})
                else: 
                    return JsonResponse({'Message': 'Success', 'Nota': "El periodo se Cerró correctamente. " + str(values)})
            else:
                return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo realizar la petición.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ZETONE_9'].close()
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
