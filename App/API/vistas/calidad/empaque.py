
from django.http import JsonResponse
from App.ZTime.conexion import *
import json
import os
from django.http import HttpResponse, Http404
from datetime import datetime
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import connections


@csrf_exempt
def busquedaCaja(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        caja = str(json.loads(body)['caja'])
        values = [caja]
        Data = []
        try:
            with connections['Trazabilidad'].cursor() as cursor:
                sql = """ 
                        SELECT Id_bulto AS id, Marca.Nombre_marca AS Marca, Calidad.nombre_calidad AS Calidad, Variedad.nombre_variedad AS Variedad, 
                                Especie.nombre_especie AS Especie, CASE WHEN Bulto.id_galpon = '8' THEN 'MANZANA' WHEN Bulto.id_galpon = '5' THEN 'PERA' ELSE 'OTRO' END AS Galpon, 
                                Envase.nombre_envase AS Envase, Calibre.nombre_calibre AS Calibre, 
                                General.dbo.USR_MCCUADRO.USR_CUAD_UMI AS UMI, General.dbo.USR_MCCUADRO.USR_CUAD_UP AS UP, Embalador.nombre_embalador AS Embalador, 
                                General.dbo.USR_MCLOTE.USR_LOTE_NUMERO AS Lote, CONVERT(varchar(10), Bulto.fecha_alta_bulto, 103) AS Fecha, CONVERT(varchar(8), 
                                Bulto.fecha_alta_bulto, 108) AS Hora
                        FROM Especie INNER JOIN 
                                Variedad ON Especie.id_especie = Variedad.id_especie INNER JOIN 
                                Bulto INNER JOIN 
                                Configuracion ON Bulto.id_configuracion = Configuracion.id_configuracion INNER JOIN 
                                Marca ON Configuracion.id_marca = Marca.id_marca INNER JOIN 
                                Calidad ON Configuracion.id_calidad = Calidad.Id_calidad ON Variedad.Id_variedad = Configuracion.id_variedad INNER JOIN 
                                Envase ON Configuracion.id_envase = Envase.id_envase INNER JOIN Calibre ON Configuracion.id_calibre = Calibre.Id_calibre INNER JOIN 
                                LoteEtiquetado ON Bulto.id_loteEtiquetado = LoteEtiquetado.id_loteEtiquetado INNER JOIN 
                                General.dbo.USR_MCLOTE ON LoteEtiquetado.id_lote = General.dbo.USR_MCLOTE.USR_LOTE_NUMERO INNER JOIN 
                                General.dbo.USR_MCCUADRO ON General.dbo.USR_MCLOTE.USR_CUAD_ALIAS = General.dbo.USR_MCCUADRO.USR_CUAD_ALIAS INNER JOIN 
                                Embalador ON Bulto.id_embalador = Embalador.Id_embalador INNER JOIN General.dbo.USR_MCCHACRA ON General.dbo.USR_MCCUADRO.USR_CHAC_ALIAS = General.dbo.USR_MCCHACRA.USR_CHAC_ALIAS
                        WHERE (Id_bulto > 17988845 AND Bulto.numero_bulto = %s)
                     """
                cursor.execute(sql, values)
                results = cursor.fetchone()
                if results:
                    idBulto = str(results[0])
                    marca = str(results[1])
                    calidad = str(results[2])
                    variedad = str(results[3])
                    especie = str(results[4])
                    galpon = str(results[5])
                    envase = str(results[6])
                    calibre = str(results[7])
                    umi = str(results[8])
                    up = str(results[9])
                    embalador = str(results[10])
                    lote = str(results[11])
                    fecha = str(results[12])
                    hora = str(results[13])
                    data = {'Id':idBulto, 'Marca':marca, 'Calidad':calidad, 'Variedad':variedad, 'Especie':especie, 'Galpon':galpon,'Envase':envase, 'Calibre':calibre, 'Umi':umi, 'Up':up,
                            'Embalador':embalador, 'Lote':lote, 'Fecha':fecha, 'Hora':hora}
                    Data.append(data)
                    return JsonResponse({'Message': 'Success', 'Caja': Data})
                else:
                    data = "No se encontraron Datos."
                    return JsonResponse({'Message': 'Error', 'Nota': data}) 
        except Exception as e:
            error = str(e)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
        finally:
            connections['Trazabilidad'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)