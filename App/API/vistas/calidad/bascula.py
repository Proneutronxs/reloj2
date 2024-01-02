
from django.http import JsonResponse
from App.ZTime.conexion import *
import json
import os
from django.http import HttpResponse, Http404
from PIL import Image
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import connections



# exec Responsable_Mostrar '','','N'  id, responsable, de baja
# exec Defecto_Mostrar '','','N','I' id, defecto, descrip, de baja
# exec Tratamiento_Mostrar '','','S' id, trataiento, descrip, de baja
# exec Condicion_Mostrar '','','S' id, condicion, descripcion, de baja
# exec Categoria_Mostrar '','','S' id, categoría, descrip, de baja

@csrf_exempt
def dataInicial(request):
    if request.method == 'GET':
        try:
            DataDestino = []
            DataResponsable = []
            DataDefectos = []
            DataTratamiento = []
            DataCondicion = []
            DataCategoria = []
            with connections['Trazabilidad'].cursor() as cursor:

                # exec Destino_Mostrar '','','S' id, destino, descripcion,debaja
                cursor.callproc('Destino_Mostrar', ['','','S'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        destino = str(row[1])
                        descripcion = str(row[2])
                        debaja = str(row[3])
                        datos = {'ID':ids,'Destino':destino, 'Descripcion':descripcion, 'Baja':debaja}
                        DataDestino.append(datos)

                # exec Defecto_Mostrar '','','N','I' id, defecto, descrip, de baja
                cursor.callproc('Defecto_Mostrar', ['','','N','I'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        defecto = str(row[1])
                        descripcion = str(row[2])
                        debaja = str(row[3])
                        datos = {'ID':ids,'Defecto':defecto, 'Descripcion':descripcion, 'Baja':debaja}
                        DataDefectos.append(datos)

                # exec Tratamiento_Mostrar '','','S' id, trataiento, descrip, de baja
                cursor.callproc('Tratamiento_Mostrar', ['','','S'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        tratamiento = str(row[1])
                        descripcion = str(row[2])
                        debaja = str(row[3])
                        datos = {'ID':ids,'Tratamiento':tratamiento, 'Descripcion':descripcion, 'Baja':debaja}
                        DataTratamiento.append(datos)

                # exec Condicion_Mostrar '','','S' id, condicion, descripcion, de baja
                cursor.callproc('Condicion_Mostrar', ['','','S'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        condicion = str(row[1])
                        descripcion = str(row[2])
                        debaja = str(row[3])
                        datos = {'ID':ids,'Condicion':condicion, 'Descripcion':descripcion, 'Baja':debaja}
                        DataCondicion.append(datos)
                
                # exec Categoria_Mostrar '','','S' id, categoría, descrip, de baja
                cursor.callproc('Categoria_Mostrar', ['','','S'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        categoria = str(row[1])
                        descripcion = str(row[2])
                        debaja = str(row[3])
                        datos = {'ID':ids,'Categoria':categoria, 'Descripcion':descripcion, 'Baja':debaja}
                        DataCategoria.append(datos)

                # exec Responsable_Mostrar '','','N'  id, responsable, de baja
                cursor.callproc('Responsable_Mostrar', ['','','N'])
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        responsable = str(row[1])
                        debaja = str(row[2])
                        datos = {'ID':ids,'Responsable':responsable, 'Baja':debaja}
                        DataResponsable.append(datos)

            if DataResponsable and DataCategoria and DataCondicion and DataDefectos and DataDestino and DataTratamiento:
                return JsonResponse({'Message': 'Success', 'Responsables': DataResponsable, 'Categorias': DataCategoria, 
                                     'Condiciones':DataCondicion, 'Defectos': DataDefectos, 'Destinos': DataDestino, 
                                     'Tratamientos': DataTratamiento})
            else:
                data = "No se encontraron Datos."
                return JsonResponse({'Message': 'Error', 'Nota': data})                
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})



