
from django.db import connections
from django.http import JsonResponse
from App.ZTime.conexion import *
#import requests
from requests.auth import HTTPBasicAuth
import json
import os
from django.http import HttpResponse, Http404
from PIL import Image
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render




# PreparedStatement pat = conexionBD().prepareStatement("insert into Registro (sereno,planta,punto,fecha,hora,pasos) values(?,?,?,?,?,?)");


@csrf_exempt
def insert_fichada_rondin(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            for item in datos:
                legajo = item['Legajo']
                planta = item['Planta']
                punto = item['Punto']
                fecha = item['Fecha']
                hora = item['Hora']
                paso = item['Paso']
                insertaFichadaSql(legajo,planta,punto,fecha,hora,paso)
            nota = "Los registros se guardaron exitosamente."
            return JsonResponse({'Message': 'Success', 'Nota': nota})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def devuelveLegajoNombre(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            legajo = str(json.loads(body)['Legajo'])
            try:
                with connections['Softland'].cursor() as cursor:
                    sql = """ 
                            SELECT SJMLGH_NROLEG AS LEGAJO, CONVERT(VARCHAR(25),SJMLGH_NOMBRE) AS NOMBRES 
                            FROM [10.32.26.5].Softland.dbo.SJMLGH 
                            WHERE SJMLGH_NROLEG = %s
                         """
                    values = (legajo)
                    cursor.execute(sql, values)  
                    results = cursor.fetchone()
                    if results:
                        CodLegajo = str(results[0])
                        CodNombre = str(results[1])
                        return JsonResponse({'Message': 'Success', 'Legajo': CodLegajo, 'Nombre':CodNombre})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos con ese número de Legajo.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})  
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


    


def insertaFichadaSql(sereno,planta,punto,fecha,hora,pasos):
    try:
        with connections['MyZetto'].cursor() as cursor:
            sql = "INSERT INTO Registro (sereno,planta,punto,fecha,hora,pasos) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (sereno,planta,punto,fecha,hora,pasos)
            cursor.execute(sql, values)  
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        cursor.close()
        connections['MyZetto'].close()     


















