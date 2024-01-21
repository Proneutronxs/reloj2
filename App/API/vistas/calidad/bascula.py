
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


##### TRAE DATOS DE INICIO DESTINO, RESPONSABLE, DEFECTOS, TRATAMIENTO,CONDICIÓN CATEGORÍA
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
                cursor.execute("exec Destino_Mostrar'','','S'")
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
                cursor.execute("exec Defecto_Mostrar '','','N','I'")
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
                cursor.execute("exec Tratamiento_Mostrar'','','S'")
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
                cursor.execute("exec Condicion_Mostrar '','','S'")
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
                cursor.execute("exec Categoria_Mostrar '','','S'")
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
                cursor.execute("exec Responsable_Mostrar '','','N'")
                results = cursor.fetchall()
                if results:
                    for row in results:
                        ids = str(row[0])
                        responsable = str(row[1])
                        debaja = str(row[2])
                        datos = {'ID':ids,'Responsable':responsable, 'Baja':debaja}
                        DataResponsable.append(datos)

            DataPlantas = levantaPlantas()

            if DataResponsable and DataCategoria and DataCondicion and DataDefectos and DataDestino and DataTratamiento and DataPlantas:
                return JsonResponse({'Message': 'Success', 'Responsables': DataResponsable, 'Categorias': DataCategoria, 
                                     'Condiciones':DataCondicion, 'Defectos': DataDefectos, 'Destinos': DataDestino, 
                                     'Tratamientos': DataTratamiento, 'Plantas':DataPlantas})
            else:
                data = "No se encontraron Datos."
                return JsonResponse({'Message': 'Error', 'Nota': data})                
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

##### LEVANTA PLANTAS SELECCIONADAS
def levantaPlantas():
    DataPlantas = []
    try:
        with connections['General'].cursor() as cursor:
            sql = """
                SELECT sttdeh_deposi, sttdeh_descrp,CASE WHEN (SELECT (Trazabilidad.dbo.Galpon.Id_galpon) 
                        FROM Trazabilidad.dbo.Galpon 
                        WHERE id_deposito = sttdeh_deposi) IS NULL THEN '0' ELSE (SELECT (Trazabilidad.dbo.Galpon.Id_galpon) 
                        FROM Trazabilidad.dbo.Galpon 
                        WHERE id_deposito = sttdeh_deposi) END AS Id_galpon
                FROM  [10.32.26.5].Softland.dbo.sttdeh
                WHERE 
                    (sttdeh_deposi between '110108' and '110109' 
                    or  sttdeh_deposi = '110113'
                    or  sttdeh_deposi = '315300'
                    or  sttdeh_deposi = '315200')
                    or  sttdeh_deposi = '110879'
                    or  sttdeh_deposi= '110883'
                    or  sttdeh_deposi= '111071' 
                    or  sttdeh_deposi= '110880' 
                    or  sttdeh_deposi= '110881' 
                    or  sttdeh_deposi= '110884'
                    or  sttdeh_deposi= '110882'
                    or  sttdeh_deposi= '110878'
                    or  sttdeh_deposi= '110877'
                    or  sttdeh_deposi= '110869'
                    or  sttdeh_deposi= '110502'
                    or  sttdeh_deposi = '110111' 
                UNION
                SELECT '8','PLANTA EMPAQUE 1 - MANZANA','8'
                UNION
                SELECT '110107','PLANTA EMPAQUE 1','1'
                ORDER BY 2
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                for row in results:
                    ids = str(row[0])
                    planta = str(row[1])
                    idPlanta = str(row[2])
                    datos = {'ID':ids,'Planta':planta,'IdPlanta':idPlanta}
                    DataPlantas.append(datos)
            return DataPlantas
    except Exception as e:
        data = str(e)
        return DataPlantas

##### TRAE LOS LOTES SEGUN LA PLANTA Y LA FECHA 
@csrf_exempt
def traeLotes(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        fecha = formatear_fecha(str(json.loads(body)['fecha']))
        planta = str(json.loads(body)['planta'])
        values = [fecha, planta, 'N']
        DataLotes = []
        try:
            with connections['Trazabilidad'].cursor() as cursor:
                cursor.execute('exec LoteCalidad_Mostrar %s,%s,%s', values)
                results = cursor.fetchall()
                if results:
                    for row in results:
                        lote = str(row[0])
                        planta = str(row[2])
                        data = {'Lote':lote,'Planta':planta}
                        DataLotes.append(data)
                    return JsonResponse({'Message': 'Success', 'Lotes': DataLotes})
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

##### LLAMA LOS DETALLES DE LOS LOTES EN CASO DE ENCONTRAR
@csrf_exempt
def traeDetalleLotes(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        lote = str(json.loads(body)['lote'])
        planta = str(json.loads(body)['planta'])
        values = [lote, planta]
        DataDetalle = []
        try:
            with connections['General'].cursor() as cursor:
                cursor.execute('exec sp_mc_Levanta_Datos_Lote %s,%s', values)
                results = cursor.fetchall()
                if results:
                    for row in results:
                        lote = str(row[0])
                        productor = str(row[1])
                        variedad = str(row[2])
                        umi = str(row[3])
                        cantidad = str(row[4])
                        up = str(row[7])
                        data = {'Lote':lote, 'Productor':productor, 'Variedad':variedad, 'UMI':umi, 'Cantidad':cantidad, 'UP':up}
                        DataDetalle.append(data)
                    return JsonResponse({'Message': 'Success', 'Detalle': DataDetalle})
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
            connections['General'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)

def formatear_fecha(fecha_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
        fecha_formateada = fecha_obj.strftime('%Y-%m-%d 00:00:00')
        return str(fecha_formateada)
    except ValueError:
        return None
    

@csrf_exempt
def Ejecuta_Procedimientos(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        idLote = str(json.loads(body)['idLote'])
        idGalpon = str(json.loads(body)['idGalpon'])
        idCategoria = str(json.loads(body)['idCategoria'])
        idCondicion = str(json.loads(body)['idCondicion'])
        idTratamiento = str(json.loads(body)['idTratamiento'])
        solubles = str(json.loads(body)['solubles'])
        almidon = str(json.loads(body)['almidon'])
        acidez = str(json.loads(body)['acidez'])
        carpocapsa = str(json.loads(body)['carpocapsa'])
        idDestino = str(json.loads(body)['idDestino'])
        observaciones = str(json.loads(body)['observaciones'])
        idResponsable = str(json.loads(body)['idResponsable'])
        LV = str(json.loads(body)['LV'])
        carpoReal = str(json.loads(body)['carpoReal'])
        LVReal = str(json.loads(body)['LVReal'])
        infoReal = str(json.loads(body)['infoReal'])
        primera = str(json.loads(body)['primera'])
        segunda = str(json.loads(body)['segunda'])
        tercera = str(json.loads(body)['tercera'])
        descarte = str(json.loads(body)['descarte'])
        
        InsertaDataPrueba("EJECUTA PROCEDIMIENTOS", str(body))
        # result = ControlCalidad_Insert(idLote,idGalpon,idCategoria,idCondicion,idTratamiento,
        #                                solubles,almidon,acidez,carpocapsa,idDestino,observaciones,
        #                                idResponsable,LV,carpoReal,LVReal,infoReal,primera,segunda,tercera,descarte)
        # if result:
        #     InsertaDataPrueba("ID CALIDAD", str(result))
        # InsertaDataPrueba("ID CALIDAD", str(result))

        response_data = {
        'Message': 'Success', 'Nota':'Ingreso.'
        }
        return JsonResponse(response_data)

    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    

def ControlCalidad_Insert(idLote,idGalpon,idCategoria,idCondicion,idTratamiento,Solubles,Almidon,Acidez,
                          Carpocapsa,idDestino,Observaciones,idResponsable,LV,CarpoReal,LVReal,InfoReal,
                          Primera,Segunda,Tercera,Descarte):

    values = [idLote,idGalpon,idCategoria,idCondicion,idTratamiento,Solubles,Almidon,Acidez,
                          Carpocapsa,idDestino,Observaciones,idResponsable,LV,CarpoReal,LVReal,InfoReal,
                          Primera,Segunda,Tercera,Descarte]
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            cursor.execute(""" exec ControlCalidad_Insert %s,%s,%s,%s,%s,%s,%s,%s,
                           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s""", values)
            result = cursor.fetchone()
            return str(result[0])
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['Trazabilidad'].close()

# @@idLote integer,
# @@idGalpon integer,
# @@idCategoria integer,
# @@idCondicion integer,
# @@idTratamiento varchar(10),
# @@Solubles numeric(18,4),
# @@Almidon numeric(18,4),
# @@Acidez numeric(18,4),
# @@Carpocapsa numeric(18,2),
# @@idDestino integer,
# @@Observaciones varchar(100),
# @@idRespnsable integer,
# @@LV integer,
# @@CarpoReal  numeric(18,2),
# @@LVReal integer,
# @@InfoReal integer,
# @@Primera numeric(18,2),
# @@Segunda numeric(18,2),
# @@Tercera numeric(18,2),
# @@Descarte numeric(18,2)

def CalidadPresion_Insert(idCalidad,NroPresion,Presion1,Presion2):

    values = [idCalidad,NroPresion,Presion1,Presion2]
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            cursor.execute(""" exec CalidadPresion_Insert %s,%s,%s,%s """, values)
            
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['Trazabilidad'].close()

# @@idCalidad integer,
# @@NroPresion integer,
# @@Presion1 decimal(18,4),
# @@Presion2 decimal(18,4)


def CalidadDefecto_Insert(idCalidad,idDefecto,Leve,Moderado,Severo,Porcentaje):

    values = [idCalidad,idDefecto,Leve,Moderado,Severo,Porcentaje]
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            cursor.execute(""" exec CalidadDefecto_Insert %s,%s,%s,%s,%s,%s """, values)
            
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['Trazabilidad'].close()

# @@idCalidad integer,
# @@idDefecto integer,
# @@Leve bit,
# @@Moderado bit,
# @@Severo bit,
# @@Porcentaje numeric(18,2)


def InsertaDataPrueba(funcion,json):

    values = [funcion,json]
    try:
        with connections['default'].cursor() as cursor:
            sql = """ INSERT INTO Data_Json (Funcion,FechaAlta,Json) VALUES (%s,GETDATE(),%s) """
            cursor.execute(sql, values)
            cursor.execute("SELECT @@ROWCOUNT AS AffectedRows")
            affected_rows = cursor.fetchone()[0]

            if affected_rows > 0:
                return 1
            else:
                return 0

    except Exception as e:
        error = str(e)
        return 8
    finally:
        connections['default'].close()

def resultadosInsert(request):
    if request.method == 'GET':
        try:
            listado = []
            with connections['default'].cursor() as cursor:
                cursor.execute(""" Select Json FROM Data_Json""")
                results = cursor.fetchall()
                index = 0
                if results:
                    for row in results:
                        dato = str(row[0])
                        datos = {'ID':str(index),'Json':dato}
                        listado.append(datos) 

                        index = index +1  
                if listado:
                    return JsonResponse({'Message': 'Success', 'Listado': listado})
                else:
                    data = "No se encontraron Datos."
                    return JsonResponse({'Message': 'Error', 'Nota': data})    
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})