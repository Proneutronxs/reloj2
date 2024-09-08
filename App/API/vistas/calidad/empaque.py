
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
        if consultaExisteCaja(caja):
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
            data = "La Caja ya se guardó."
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
def consultaExisteCaja(IdCaja):
    values = [IdCaja]
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
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    

def insertaCaja(IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario):
    values = [IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario]
    try:
        with connections['ZetoneApp'].cursor() as cursor:
            sql = """
                    INSERT INTO DefectosCaja (IdCaja, numeroCaja, Fecha, Hora, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas,roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario) 
                    Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            cursor.execute(sql, values)
            return True
    except Exception as e:
        error = str(e)
        return False
    
def insertaImagen(IdCaja, Imagen, Tipo,):
    values = [IdCaja, Tipo, Imagen]
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
        return False