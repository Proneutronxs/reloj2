
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
def buscaRegistros(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            inicio = str(json.loads(body)['Inicio'])
            final = str(json.loads(body)['Final'])
            ubicacion = str(json.loads(body)['Ubicacion'])
            try:
                with connections['Softland'].cursor() as cursor:
                    sql = """ 
                            SELECT        CASE WHEN CONVERT(VARCHAR(25),(SELECT Nombre FROM ZetoneTime.dbo.Legajos WHERE Legajos = PS_Registros.CodLegajo)) IS NULL THEN 'NO ENCONTRADO' 
                                            ELSE CONVERT(VARCHAR(25),(SELECT Nombre FROM ZetoneTime.dbo.Legajos WHERE Legajos = PS_Registros.CodLegajo)) END AS LEGAJO, 
                                    PS_Ubicacion.UbicacionNombre AS UBICACIÓN, 
                                    CASE WHEN PS_Puntos.PuntoNombre IS NULL THEN 'PUNTO SIN REGISTRAR' ELSE PS_Puntos.PuntoNombre END AS LUGAR_PUNTO, 
                                    (CONVERT(VARCHAR(10),PS_Registros.FechaLectura, 103) + ' - ' + CONVERT(VARCHAR(8),PS_Registros.FechaLectura, 108) + ' Hs.') AS FECHA_LECTURA
                            FROM            PS_Registros INNER JOIN
                                                    PS_Ubicacion ON PS_Registros.CodUbicacion = PS_Ubicacion.CodUbicacion LEFT JOIN
                                                    PS_Puntos ON PS_Registros.CodPunto = PS_Puntos.CodPunto
                            WHERE CONVERT(DATE, PS_Registros.FechaLectura) >= %s AND CONVERT(DATE, PS_Registros.FechaLectura) <= %s
                                    AND PS_Ubicacion.CodUbicacion = %s
                            ORDER BY FECHA_LECTURA
                         """
                    cursor.execute(sql, [inicio,final,ubicacion])  
                    results = cursor.fetchoall()
                    listado = []
                    if results:
                        for row in results:
                            nombre = str(row[0])
                            ubi = str(row[1])
                            punto = str(row[2])
                            fecha = str(row[3])
                            registro = {'Nombre':nombre, 'Ubicacion': ubi, 'Punto':punto, 'Fecha':fecha}
                            listado.append(registro)
                        return JsonResponse({'Message': 'Success', 'Data': listado})
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
    
@csrf_exempt
def insertaRegistrosRondin(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            for item in datos:
                registro = item['Registro']
                legajo = item['Legajo']
                ubicacion = item['Ubicacion']
                punto = item['Sector']
                fecha = item['FechaAlta']
                insertaRegistroNuevo(registro,legajo,ubicacion,punto,fecha)
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
                    cursor.execute(sql, [legajo])  
                    results = cursor.fetchone()
                    if results:
                        CodLegajo = str(results[0])
                        CodNombre = str(results[1])
                        if listadoPuntos():
                            listado = listadoPuntos()
                        else:
                            listado = [{'CodPunto': 'NONE', 'CodNombre': 'NONE'}]
                        return JsonResponse({'Message': 'Success', 'Legajo': CodLegajo, 'Nombre':CodNombre, 'DataPuntos': listado})
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

@csrf_exempt
def devuelveNombreSector(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            codigo = str(json.loads(body)['CodUbicacion'])
            try:
                with connections['PsRondin'].cursor() as cursor:
                    sql = """ 
                            SELECT CodUbicacion, UbicacionNombre
                            FROM PS_Ubicacion
                            WHERE CodUbicacion = %s
                         """
                    cursor.execute(sql, [codigo])  
                    results = cursor.fetchone()
                    if results:
                        CodUbicacion = str(results[0])
                        NombreUbicacion = str(results[1])
                        return JsonResponse({'Message': 'Success', 'Codigo': CodUbicacion, 'Nombre':NombreUbicacion})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos con ese Código.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

    

def insertaRegistroNuevo(idInterno,idLegajo,idUbicacion,idPunto,fechaAlta):

    try:
        with connections['PsRondin'].cursor() as cursor:
            sql = "INSERT INTO PS_Registros (RegistroInterno, CodLegajo, CodUbicacion, CodPunto, FechaLectura, FechaAlta) VALUES (%s, %s, %s, %s, %s, GETDATE())"
            values = (idInterno,idLegajo,idUbicacion,idPunto,fechaAlta)
            cursor.execute(sql, values)  
    except Exception as e:
        error = str(e)
        print(error)
    finally:
        cursor.close()
        connections['PsRondin'].close()     

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

def listadoPuntos():
    listado = []
    try:
        with connections['PsRondin'].cursor() as cursor:
            sql = """ 
                    SELECT CodPunto, PuntoNombre
                    FROM PS_Puntos
                    """
            cursor.execute(sql)  
            results = cursor.fetchall()
            if results:
                for row in results:
                    CodPunto = str(row[0])
                    CodNombre = str(row[1])
                    punto = {'CodPunto': CodPunto, 'CodNombre': CodNombre}
                    listado.append(punto)
                return listado
            else:
                return listado
    except Exception as e:
        error = str(e)
        #print(error)


















