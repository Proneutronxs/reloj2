
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
        caja = str(json.loads(body)['Caja'])
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
    
def consultaExisteCaja(IdCaja):
    values = (IdCaja,)
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    SELECT IdCaja FROM DefectosCaja WHERE IdCaja = %s
                """
            cursor.execute(sql, values)
            results = cursor.fetchone()
            if results:
                return False
            return True
    except Exception as e:
        error = str(e)
        return True

@csrf_exempt
def guardaCaja(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        id_caja = str(data['IdCaja'])
        caja = str(data['Caja'])
        fecha = str(data['Fecha'])
        hora = str(data['Hora'])
        peso_neto = str(data['PesoNeto'])
        peso_bruto = str(data['PesoBruto'])
        plu = str(data['Plu'])
        observaciones = str(data['Observaciones'])
        deformadas = str(data['Deformadas'])
        tamaño_incorrecto = str(data['TamañoIncorrecto'])
        falta_color = str(data['FaltaColor'])
        russeting = str(data['Russeting'])
        heladas = str(data['Heladas'])
        roce_bins = str(data['RoceBins'])
        asoleado = str(data['Asoleado'])
        quemado_sol = str(data['QuemadoSol'])
        fitotoxicidad = str(data['Fitotoxicidad'])
        rolado = str(data['Rolado'])
        golpes = str(data['Golpes'])
        heridas = str(data['Heridas'])
        heridas_viejas = str(data['HeridasViejas'])
        cracking = str(data['Cracking'])
        bitterpit = str(data['Bitterpit'])
        granizo = str(data['Granizo'])
        daño_insecto = str(data['DañoInsecto'])
        pedunculo = str(data['Pedunculo'])
        desvio = str(data['Desvio'])
        segunda_flor = str(data['SegundaFlor'])
        madurez = str(data['Madurez'])
        deshidratacion = str(data['Deshidratacion'])
        decaimiento = str(data['Decaimiento'])
        moho_humedo = str(data['MohoHumedo'])
        moho_seco = str(data['MohoSeco'])
        moho_acuoso = str(data['MohoAcuoso'])
        rameado = str(data['Rameado'])
        firmeza_max = str(data['FirmezaMax'])
        firmeza_min = str(data['FirmezaMin'])
        firmeza_pro = str(data['FirmezaPro'])
        falta_boro = str(data['FaltaBoro'])
        maquina = str(data['Maquina'])
        usuario = str(data['Usuario'])
        if consultaExisteCaja(id_caja):
            try:
                if insertaCaja(id_caja,caja,fecha,hora,peso_neto,peso_bruto,plu,observaciones,deformadas,tamaño_incorrecto,falta_color,russeting,heladas,
                            roce_bins,asoleado,quemado_sol,fitotoxicidad,rolado,golpes,heridas,heridas_viejas,cracking,bitterpit,granizo,daño_insecto,pedunculo,desvio,
                            segunda_flor,madurez,deshidratacion,decaimiento,moho_humedo,moho_seco,moho_acuoso,rameado,firmeza_max,firmeza_min,firmeza_pro,
                            falta_boro,maquina,usuario):
                    imagenes = data['Imagenes']
                    for imagen in imagenes:
                        imagen_caja = str(imagen['ImagenCaja'])
                        imagen_plu = str(imagen['ImagenPlu'])
                        if imagen_caja != "0":
                            insertaImagen(id_caja, imagen_caja, "C")
                        if imagen_plu != "0":
                            insertaImagen(id_caja, imagen_plu, "P")
                    
                    return JsonResponse({'Message': 'Success', 'Nota':'La Caja se guardó correctamente.'})
                else:
                    data = "Ocurrió un error al intentar guardar la Caja."
                    return JsonResponse({'Message': 'Error', 'Nota': data}) 
            except Exception as e:
                error = str(e)
                response_data = {
                    'Message': 'Error',
                    'Nota': error
                }
                return JsonResponse(response_data)
        else:
            data = "La Caja ya existe en el reporte."
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
def insertaCaja(IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, 
                roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, 
                FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, 
                FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario):
    values = (IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario)
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    INSERT INTO DefectosCaja (IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas,roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario) 
                    Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            cursor.execute(sql, values)
            return True
    except Exception as e:
        error = str(e)
        InsertaDataError("INSERTA CAJA", error)
        return False
    
def insertaImagen(IdCaja, Imagen, Tipo,):
    values = (IdCaja, Tipo, Imagen)
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    INSERT INTO  Imagenes_Cajas_Calidad (IdCaja, Tipo, Imagen) 
                    Values (%s,%s,%s)
                """
            cursor.execute(sql, values)
            return True
    except Exception as e:
        error = str(e)
        InsertaDataError("INSERTA IMAGEN", error)
        return False    

def InsertaDataError(funcion,json):

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

@csrf_exempt
def busquedaCajaDia(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        fecha = str(json.loads(body)['Fecha'])
        values = [fecha]
        Data = []
        try:
            with connections['ZetoneApp'].cursor() as cursor:
                sql = """ 
                        SELECT IdCaja, numeroCaja 
                        FROM DefectosCaja
                        WHERE CONVERT(DATE, Fecha) = %s
                    """
                cursor.execute(sql, values)
                results = cursor.fetchall()
                if results:
                    for row in results:
                        idBulto = str(row[0])
                        numCaja = str(row[1])
                        data = {'IdBulto':idBulto, 'NumCaja':numCaja}
                        Data.append(data)
                    return JsonResponse({'Message': 'Success', 'Cajas': Data})
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
            connections['ZetoneApp'].close()
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
def consultaImagenes(IdCaja,Tipo):
    values = [IdCaja,Tipo]
    imagen64 = "0"
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    SELECT Imagen FROM Imagenes_Cajas_Calidad WHERE IdCaja = %s AND Tipo = %s
                """
            cursor.execute(sql, values)
            results = cursor.fetchone()
            if results:
                imagen64 = str(results[0])
                return imagen64
            return imagen64
    except Exception as e:
        error = str(e)
        InsertaDataError("CONSULTA IMAGEN", error)
        return imagen64

def consultaCajaUpdate(IdCaja):
    values = [IdCaja]
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
                        WHERE (Id_bulto > 17988845 AND Id_bulto = %s)
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
                return Data
            return Data
    except Exception as e:
        error = str(e)
        InsertaDataError("CONSULTA CAJA UPDATE", error)
        return Data

def consultaDefectosCajaUpdate(IdCaja):
    values = [IdCaja]
    Data = []
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    SELECT IdCaja, CONVERT(varchar(10), Fecha, 3) AS Fecha, CONVERT(varchar(8), Hora, 108) AS Hora, PesoNeto, PesoBruto, PLU, Observaciones, 
                            Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, 
                            Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, 
                            Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Rameado
                    FROM DefectosCaja
                    WHERE IdCaja = %s
                """
            cursor.execute(sql, values)
            results = cursor.fetchone()
            if results:
                idBulto = str(results[0])
                fecha = str(results[1])
                hora = str(results[2])
                pNeto = str(results[3])
                pBruto = str(results[4])
                plu = str(results[5])
                obs = str(results[6])
                deformadas = str(results[7])
                tIncorrecto = str(results[8])
                fColor = str(results[9])
                russeting = str(results[10])
                heladas = str(results[11])
                roceBins = str(results[12])
                asoleado = str(results[13])
                quemado = str(results[14])
                fito = str(results[15])
                rolado = str(results[16])
                golpes = str(results[17])
                heridas = str(results[18])
                hViejas = str(results[19])
                craking = str(results[20])
                bitter = str(results[21])
                granizo = str(results[22])
                dañoInsecto = str(results[23])
                fPedunculo = str(results[24])
                desvio = str(results[25])
                sFlor = str(results[26])
                madurez = str(results[27])
                deshidratacion = str(results[28])
                decaimiento = str(results[29])
                mHumedo = str(results[30]) 
                mSeco = str(results[31])
                mAcuoso = str(results[32])
                pulpaMax = str(results[33])
                pulpaMin = str(results[34])
                pulpaPro = str(results[35])
                fBoro = str(results[36])
                maquina = str(results[37])
                rameado = str(results[38])
                data = {'Id':idBulto, 'Fecha':fecha, 'Hora':hora, 'Neto':pNeto, 'Bruto':pBruto, 'PLU':plu, 'Obs':obs, 'Deformada':deformadas, 'Incorrecto':tIncorrecto, 'Color':fColor,
                        'Russeting':russeting, 'Heladas':heladas, 'RBins':roceBins, 'Asoleado':asoleado, 'Quemado':quemado, 'Fitotoxicidad':fito, 'Rolado':rolado, 'Golpes':golpes,
                        'Heridas':heridas, 'HViejas':hViejas, 'Craking':craking, 'Bitterpit':bitter, 'Granizo':granizo, 'DañoInsecto':dañoInsecto, 'Pedunculo':fPedunculo, 'Desvio':desvio,
                        'SFlor':sFlor, 'Madurez':madurez, 'Deshidratacion': deshidratacion, 'Decaimiento':decaimiento, 'MHumedo':mHumedo, 'MSeco':mSeco, 'MAcuoso':mAcuoso, 'PulpaMax':pulpaMax,
                        'PulpaMin':pulpaMin, 'PulpaPro':pulpaPro, 'Boro':fBoro,'Maquina':maquina, 'Rameado':rameado}
                Data.append(data)
                return Data
            return Data
    except Exception as e:
        error = str(e)
        InsertaDataError("CONSULTA DEFECTOS CAJA UPDATE", error)
        return Data

@csrf_exempt
def busquedaCajaUpdate(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        caja = str(json.loads(body)['Caja'])
        dataCaja = consultaCajaUpdate(caja)
        dataDefectos = consultaDefectosCajaUpdate(caja)
        dataImagenes = []
        if  dataCaja and dataDefectos:
            pluFoto = consultaImagenes(caja, "P")
            cajaFoto = consultaImagenes(caja,"C") 
            dataImagenes = [pluFoto, cajaFoto]
            return JsonResponse({'Message': 'Success', 'DataCaja': dataCaja, 'DataDefectos':dataDefectos, 'DataImagenes':dataImagenes})
        else:
            data = "No se encontraron Datos."
            return JsonResponse({'Message': 'Error', 'Nota': data}) 
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)





































