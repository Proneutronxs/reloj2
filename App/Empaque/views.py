from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from App.ZTime.conexion import *
from App.Empaque.modelosPDF.modelosPDF import *
import os

from App.Empaque.forms import *
##LOGIN
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def indexEmpaque(request):
    return render (request, 'Empaque/Inicio/index.html')

@login_required
def reportes_camaras(request):
    return render (request, 'Empaque/Reportes/reportes.html')

def fecha_actual():
    hoy = datetime.now()
    dia = hoy.day
    mes = hoy.month
    if hoy.day < 10:
        dia = "0" + str(hoy.day)
    if hoy.month < 10:
        mes = "0" + str(hoy.month)
    return(str(dia) + "/" + str(mes) + "/" + str(hoy.year))

def consultaTopCaja(fecha):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT (SELECT TOP(1)IdCaja FROM DefectosCaja WHERE TRY_CONVERT(DATE, Fecha) ='" + str(fecha) + "') - 5")
        cursor.execute(sql5)
        consulta = cursor.fetchone()
        if consulta:
            id = str(consulta[0])
            return id
        else:
            id = "0"
            return
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

@csrf_exempt
def post_busqueda_reporte_camaras(request):
    form = form_ver_reportes_camara(request.POST)
    if form.is_valid():
        fecha = form.cleaned_data['fechaReporte']
        Tipo = (form.cleaned_data['hora'])##CAMBIÓ A EMPAQUE
        planta = form.cleaned_data['planta']
        if str(Tipo) == "Control Cámaras":
            try:
                data_principal = []
                ZetoApp = zetoneApp()
                cursorZetoApp = ZetoApp.cursor()
                consulta_data_principal = ("SELECT ID, CONVERT(VARCHAR(10), Fecha, 103) AS Fecha, Hora, Observaciones, Usuario FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
                cursorZetoApp.execute(consulta_data_principal)
                consulta_general = cursorZetoApp.fetchone()
                if consulta_general:
                    data_principal.append(str(consulta_general[0])) ##ID
                    data_principal.append(str(consulta_general[1])) ##FECHA
                    data_principal.append(str(consulta_general[2])) ##HORA
                    data_principal.append(str(consulta_general[3])) ##OBSERVACIONES
                    data_principal.append(str(consulta_general[4])) ##USUARIO

                    id_reporte = str(data_principal[0])
                    fecha = str(data_principal[1])
                    hora = str(data_principal[2])
                    fecha_name = str(data_principal[1]).replace('/', '')
                    hora_name = str(data_principal[2]).replace(':', '')
                    lista_user = str(data_principal[4]).split('@')
                    user_name = str(lista_user[0])
                    consulta_data_camaras = ("SELECT Camara, Especie, Envase, Temperatura FROM Control_Camaras WHERE ID_Reporte='" + id_reporte + "' ORDER BY Camara, Envase")
                    cursorZetoApp.execute(consulta_data_camaras)
                    consulta_camaras = cursorZetoApp.fetchall()
                    pdf = control_camaras_PDF()
            
                    pdf.alias_nb_pages()
                    pdf.add_page()
                    pdf.set_font('Times', 'I', 12)
                    pdf.text(x=12, y=40, txt= 'Fecha Control: ' + str(data_principal[1]))
                    pdf.text(x=65, y=40, txt= 'Hora Control: ' + str(data_principal[2]) + ' Hs.')
                    pdf.set_font('Arial', 'B', 10)
                    pdf.text(x=16.5, y=286, txt= user_name)
                    pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                    pdf.set_font('Arial', 'B', 10)
                    pdf.rect(x=10,y=43,w=190,h=5)
                    pdf.text(x=16, y=47.5, txt= 'CÁMARA')
                    pdf.line(40,43,40,48)
                    pdf.text(x=55, y=47.5, txt= 'ESPECIE')
                    pdf.line(85,43,85,48)
                    pdf.text(x=100, y=47.5, txt= 'ENVASE')
                    pdf.line(130,43,130,48)
                    pdf.text(x=150, y=47.5, txt= 'TEMPERATURA') 
                    cantidad = 0
                    if consulta_camaras:
                        for i in consulta_camaras:
                            envase = str(i[2])
                            if envase == "SELECCIONE":
                                envase = "-"
                            pdf.set_font('Arial', '', 8)
                            pdf.cell(w=30, h=3, txt= str(i[0]), border='LBR', align='C', fill=0)
                            pdf.cell(w=45, h=3, txt= str(i[1]), border='BR', align='C', fill=0)
                            pdf.cell(w=45, h=3, txt= envase, border='BR', align='C', fill=0)
                            pdf.multi_cell(w=70, h=3, txt= str(i[3] + ' °C'), border='BR', align='C', fill=0)
                            cantidad = cantidad + 1

                        if cantidad > 76:
                            pdf.set_font('Times', 'I', 12)
                            pdf.text(x=12, y=40, txt= 'Fecha Control: ' + fecha)
                            pdf.text(x=65, y=40, txt= 'Hora Control: ' + hora + ' Hs.')
                            pdf.set_font('Arial', 'B', 10)
                            pdf.text(x=16.5, y=286, txt= user_name)
                            pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                            pdf.set_font('Arial', 'B', 10)
                            pdf.rect(x=10,y=43,w=190,h=5)
                            pdf.text(x=16, y=47.5, txt= 'CÁMARA')
                            pdf.line(40,43,40,48)
                            pdf.text(x=55, y=47.5, txt= 'ESPECIE')
                            pdf.line(85,43,85,48)
                            pdf.text(x=100, y=47.5, txt= 'ENVASE')
                            pdf.line(130,43,130,48)
                            pdf.text(x=150, y=47.5, txt= 'TEMPERATURA')     
                            
                        ##OBSERVACIONES
                
                        pdf.add_page()
                        pdf.set_font('Times', 'I', 12)
                        pdf.text(x=12, y=40, txt= 'Fecha Control: ' + str(data_principal[1]))
                        pdf.text(x=65, y=40, txt= 'Hora Control: ' + str(data_principal[2]) + ' Hs.')
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=16.5, y=286, txt= user_name)
                        pdf.text(x=45, y=286, txt= str(fecha_actual()))## Traer fecha actual
                        pdf.rect(x=10,y=43,w=190,h=5)
                        pdf.text(x=11, y=46.5, txt= 'OBSERVACIONES:')
                        ### CONTRUCTOR DE OBS
                        observaciones = str(data_principal[3])
                        lista_observaciones = observaciones.split("_")
                        for j in lista_observaciones:
                            pdf.set_font('Arial', '', 10)
                            pdf.multi_cell(w=0, h=5, txt= str(j) or "Sin Observaciones", border='LBR', align='L', fill=0)                        

                    ##CONSULTA IMAGENES
                    consulta_data_images = ("SELECT Fotos FROM Fotos_Control_Camaras WHERE ID_Reporte='" + id_reporte + "'")
                    cursorZetoApp.execute(consulta_data_images)
                    consulta_images = cursorZetoApp.fetchall()
                    if consulta_images:
                        ### IMAGENES
                        pdf.rect(x=10,y=98,w=190,h=5)
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=11, y=102, txt= 'IMÁGENES:')
                        name_decoded_image = []
                        k_index = 0
                        for k in consulta_images:
                            nombre_foto = decode_base64_to_image(k_index,fecha_name, hora_name, id_reporte, k[0])
                            name_decoded_image.append(str(nombre_foto))
                            k_index = k_index + 1
                        valores_x = [10,80,150,10,80,150]
                        valores_y = [105,105,105,190,190,190]
                        cant_images = len(name_decoded_image)
                        if cant_images > 6:
                            cant_images = 6
                        index = 0
                        #for k in name_decoded_image:
                        while index < cant_images:
                            name_image = str(name_decoded_image[index])
                            pdf.image("App/Empaque/data/images/" + name_image, x = valores_x[index], y = valores_y[index], w = 50, h = 82, type = '', link = '')
                            index = index + 1
                    
                    name_pdf = 'Reporte_Cámaras_' + fecha_name + "_" + hora_name + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name_pdf  , 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name_pdf}) 
                    return JsonResponse(jsonList, safe=False)
                else:
                    jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                    return JsonResponse(jsonList, safe=False)
            except Exception as e:
                error = "Ocurrió un error: " + str(e)
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            finally:
                cursorZetoApp.close()
                ZetoApp.close()
        elif str(Tipo) == "Control Empaque":
            Top_Caja = consultaTopCaja(fecha)
            print(Top_Caja)
            if Top_Caja != "0":
                try:
                    conexion = zetoneApp()
                    cursor = conexion.cursor()
                    consultaSQL = ("SELECT        Bulto.Id_bulto AS id, Marca.Nombre_marca AS Marca, Calidad.nombre_calidad AS Calidad, Variedad.nombre_variedad AS Variedad, Especie.nombre_especie AS Especie, Bulto.id_galpon AS Galpon, \n" +
                                                            "Envase.nombre_envase AS Envase, Calibre.nombre_calibre AS Calibre, USR_MCCUADRO.USR_CUAD_UMI AS UMI, USR_MCCUADRO.USR_CUAD_UP AS UP, Embalador.nombre_embalador AS Embalador, \n" +
                                                            "USR_MCLOTE.USR_LOTE_NUMERO AS Lote, CONVERT(varchar(10), Bulto.fecha_alta_bulto, 103) AS FechaEmbalado, CONVERT(varchar(8), Bulto.fecha_alta_bulto, 108) AS HoraEmbalado, numeroCaja, CONVERT(varchar(10), DefectosCaja.Fecha, 103) AS FechaControl, CONVERT(varchar(8), DefectosCaja.Hora, 108) AS HoraControl, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, \n" +
                                                            "Heridas, HeridasViejas, Cracking, Bitterpit, Granizo, DañoPorInsecto, FaltaDePedunculo, DesvioDeClasificacion, SegundaFlor, Madurez, Deshidratacion, Decaimiento, MohoHumedo, MohoSeco, MohoAcuoso, Rameado, \n" +
                                                            "FirmezaPulpaMax, FirmezaPulpaMin, FirmezaPulpaPromedio, faltaDeBoro, Maquina, Usuario\n" +
                                    "FROM            servidordb.trazabilidad.dbo.Especie AS Especie INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Variedad AS Variedad ON Especie.id_especie = Variedad.id_especie INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Bulto AS Bulto INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Configuracion AS Configuracion ON Bulto.id_configuracion = Configuracion.id_configuracion INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Marca AS Marca ON Configuracion.id_marca = Marca.id_marca INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Calidad AS Calidad ON Configuracion.id_calidad = Calidad.Id_calidad ON Variedad.Id_variedad = Configuracion.id_variedad INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Envase AS Envase ON Configuracion.id_envase = Envase.id_envase INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Calibre AS Calibre ON Configuracion.id_calibre = Calibre.Id_calibre INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.LoteEtiquetado AS LoteEtiquetado ON Bulto.id_loteEtiquetado = LoteEtiquetado.id_loteEtiquetado INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCLOTE AS USR_MCLOTE ON LoteEtiquetado.id_lote = USR_MCLOTE.USR_LOTE_NUMERO INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCCUADRO AS USR_MCCUADRO ON USR_MCLOTE.USR_CUAD_ALIAS = USR_MCCUADRO.USR_CUAD_ALIAS INNER JOIN\n" +
                                                            "servidordb.trazabilidad.dbo.Embalador AS Embalador ON Bulto.id_embalador = Embalador.Id_embalador INNER JOIN\n" +
                                                            "servidordb.General.dbo.USR_MCCHACRA AS USR_MCCHACRA ON USR_MCCUADRO.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS INNER JOIN\n" +
                                                            "DefectosCaja ON Bulto.Id_bulto = DefectosCaja.IdCaja\n" +
                                    "WHERE        (Bulto.Id_bulto > '" + str(Top_Caja) + "') AND  TRY_CONVERT(DATE, DefectosCaja.Fecha) ='" + str(fecha) + "'")
                    cursor.execute(consultaSQL)
                    consulta = cursor.fetchall()
                    if consulta:
                        pdf = Control_Cajas()
                        pdf.alias_nb_pages()
                        index = 0
                        for i in consulta:
                            if index == 0:
                                if str(i[5]) == "1":
                                    empaque = "Pera"
                                else:
                                    empaque = "Manzana"
                                pdf.add_page()
                                pdf.set_font('Arial', '', 7)
                                pdf.text(x=148, y=16.5, txt= 'Miercoles, 05 de Abril de 2023')
                                pdf.text(x=165.5, y=19.5, txt= '10:23:33 Hs.')
                                ###DATOS PRINCIPALES CAJA
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=48, txt= str(i[14]))
                                pdf.text(x=56, y=48, txt= str(i[0]))
                                pdf.text(x=90, y=48, txt= str(i[15]))
                                pdf.text(x=122, y=48, txt= str(i[16]))
                                pdf.text(x=160, y=48, txt= empaque)
                                pdf.text(x=196, y=48, txt= str(i[52]))#MAQUINA

                                pdf.set_font('Arial', '', 8)
                                pdf.text(x=12, y=59, txt= str(i[3]))#VARIEDAD
                                pdf.text(x=46, y=59, txt= str(i[6]))#ENVASE
                                pdf.text(x=78, y=59, txt= str(i[1]))#MARCA
                                pdf.text(x=120, y=59, txt= str(i[7]))#TAMAÑO
                                pdf.text(x=12, y=69, txt= str(i[2]))#CATEGORÍA
                                pdf.text(x=46, y=69, txt= str(i[10]))#EMBALADOR
                                pdf.text(x=78, y=69, txt= str(i[9]))#UP
                                pdf.text(x=104, y=69, txt= str(i[12]) + ' ' + str(i[13]) +' Hs.')#FECHA HORA EMBALADO
                                pdf.text(x=22, y=79, txt= str(i[11]) + ' / ' + str(i[8]))#LOTE Y UMI
                                pdf.text(x=64, y=79, txt= str(i[19]))#PLU
                                pdf.text(x=86, y=79, txt= str(i[18]) + ' Kg.')# PESO BRUTO
                                pdf.text(x=116, y=79, txt= str(i[17]) + ' Kg.')#PESO NETO
                                ##DEFECTOS
                                ###IZQUIERDAAA
                                pdf.text(x=50, y=88.5, txt= str(i[21]))#DESFORMADAS
                                pdf.text(x=50, y=94, txt= str(i[22]))#T INCORRECTO
                                pdf.text(x=50, y=99, txt= str(i[23]))#F COLOR
                                pdf.text(x=50, y=104, txt= str(i[24]))#RUSSETING
                                pdf.text(x=50, y=109, txt= str(i[25]))#HELADAS
                                pdf.text(x=50, y=114, txt= str(i[26]))#ROC BINS
                                pdf.text(x=50, y=119, txt= str(i[27]))##ASOLEADo
                                pdf.text(x=50, y=124, txt= str(i[28]))#QUEMADO SOL
                                pdf.text(x=50, y=129, txt= str(i[29]))
                                pdf.text(x=50, y=134, txt= str(i[30]))
                                pdf.text(x=50, y=139, txt= str(i[31]))
                                pdf.text(x=50, y=144, txt= str(i[32]))
                                pdf.text(x=50, y=149, txt= str(i[33]))
                                ### DERECHA
                                pdf.text(x=129, y=88.5, txt= str(i[34]))
                                pdf.text(x=129, y=94, txt= str(i[35]))
                                pdf.text(x=129, y=99, txt= str(i[36]))
                                pdf.text(x=129, y=104, txt= str(i[37]))
                                pdf.text(x=129, y=109, txt= str(i[38]))
                                pdf.text(x=129, y=114, txt= str(i[39]))
                                pdf.text(x=129, y=119, txt= str(i[40]))
                                pdf.text(x=129, y=124, txt= str(i[41]))
                                pdf.text(x=129, y=129, txt= str(i[42]))
                                pdf.text(x=129, y=134, txt= str(i[43]))
                                pdf.text(x=118, y=139, txt= str(i[44]) + ' / ' + str(i[45]) + ' / ' + str(i[46]) )
                                pdf.text(x=118, y=144, txt= str(i[48]) + ' / ' + str(i[50]) + ' / ' + str(i[49]) )
                                pdf.text(x=129, y=149, txt= str(i[51]))
                                ## OBSERVACIONES
                                pdf.text(x=22, y=153, txt= str(i[20]))##OBSERVACION
                                ###FOTOS

                                bulto = str(i[0])
                                ruta_caja = 'App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg'
                                ruta_plu = 'App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg'
                                if os.path.exists(ruta_caja):
                                    pdf.image('plu_image_' + bulto + '.jpeg', x=160, y=178, w=15, h=15)
                                else:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=65, txt='NOT IMAGE')
                                if os.path.exists(ruta_plu):
                                    pdf.image('caja_image_' + bulto + '.jpeg', x=146, y=201, w=45, h=70)
                                else:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=119, txt='NOT IMAGE')
                                pdf.set_font('Arial', '', 8)
                                pdf.text(x=12, y=100, txt= str(i[53]))#USER
                                index = index + 1
                            else:
                                if str(i[5]) == "1":
                                    empaque = "Pera"
                                else:
                                    empaque = "Manzana"
                                #CONDICIONAL CUANDO VALE 1
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=168, txt= str(i[14]))#CAJA
                                pdf.text(x=56, y=168, txt= str(i[14]))#BULTO
                                pdf.text(x=90, y=168, txt= str(i[15]))#FECHA CONTROL
                                pdf.text(x=122, y=168, txt= str(i[16]) + ' Hs.')#HORA CONTROL
                                pdf.text(x=160, y=168, txt= empaque)#EMPAQUE
                                pdf.text(x=196, y=168, txt= str(i[52]))#MÁQUINA

                                pdf.set_font('Arial', '', 8)
                                pdf.text(x=12, y=178, txt= str(i[3]))#VARIEDAD
                                pdf.text(x=47, y=178, txt= str(i[6]))#ENVASE
                                pdf.text(x=80, y=178, txt= str(i[1]))#MARCA
                                pdf.text(x=121, y=178, txt= str(i[7]))#TAMAÑO
                                pdf.text(x=12, y=188, txt= str(i[2]))#CATEGORÍA
                                pdf.text(x=47, y=188, txt= str(i[10]))#EMBALADOR
                                pdf.text(x=77, y=188, txt= str(i[9]))#UP
                                pdf.text(x=102, y=188, txt= str(i[12]) + ' ' + str(i[13]) +' Hs.')#FECHA HORA EMBALADO
                                pdf.text(x=22, y=198, txt= str(i[11]) + ' / ' + str(i[8]))#LOTE UMI
                                pdf.text(x=62, y=198, txt= str(i[19]))#PLU
                                pdf.text(x=86, y=198, txt= str(i[18]) + ' Kg.')#PESO BRUTO
                                pdf.text(x=114, y=198, txt= str(i[17]) + ' Kg.')#PESO NETO
                                ###IZQUIERDAAA
                                pdf.text(x=50, y=208, txt= str(i[21]))
                                pdf.text(x=50, y=213, txt= str(i[22]))
                                pdf.text(x=50, y=218, txt= str(i[23]))
                                pdf.text(x=50, y=223, txt= str(i[24]))
                                pdf.text(x=50, y=228, txt= str(i[25]))
                                pdf.text(x=50, y=233, txt= str(i[26]))
                                pdf.text(x=50, y=238, txt= str(i[27]))
                                pdf.text(x=50, y=243, txt= str(i[28]))
                                pdf.text(x=50, y=248, txt= str(i[29]))
                                pdf.text(x=50, y=253, txt= str(i[30]))
                                pdf.text(x=50, y=258, txt= str(i[31]))
                                pdf.text(x=50, y=263, txt= str(i[32]))
                                pdf.text(x=50, y=268, txt= str(i[33]))
                                ### DERECHA
                                pdf.text(x=129, y=208, txt= str(i[34]))
                                pdf.text(x=129, y=213, txt= str(i[35]))
                                pdf.text(x=129, y=218, txt= str(i[36]))
                                pdf.text(x=129, y=223, txt= str(i[37]))
                                pdf.text(x=129, y=228, txt= str(i[38]))
                                pdf.text(x=129, y=233, txt= str(i[39]))
                                pdf.text(x=129, y=238, txt= str(i[40]))
                                pdf.text(x=129, y=243, txt= str(i[41]))
                                pdf.text(x=129, y=248, txt= str(i[42]))
                                pdf.text(x=129, y=253, txt= str(i[43]))
                                pdf.text(x=118, y=258, txt= str(i[44]) + ' / ' + str(i[45]) + ' / ' + str(i[46]))
                                pdf.text(x=118, y=263, txt= str(i[48]) + ' / ' + str(i[50]) + ' / ' + str(i[49]))
                                pdf.text(x=129, y=268, txt= str(i[51]))
                                ## OBSERVACIONES
                                pdf.text(x=22, y=274, txt= str(i[20]))
                                ##FOTOS

                                bulto = str(i[0])
                                ruta_caja = 'App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg'
                                ruta_plu = 'App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg'
                                if os.path.exists(ruta_caja):
                                    pdf.image('plu_image_' + bulto + '.jpeg', x=160, y=178, w=15, h=15)
                                else:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=188, txt='NOT IMAGE')
                                if os.path.exists(ruta_plu):
                                    pdf.image('caja_image_' + bulto + '.jpeg', x=146, y=201, w=45, h=70)
                                else:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=235, txt='NOT IMAGE')
                                index = 0
                        name_pdf = "Control_Empaque_" + str(fecha) + ".pdf"
                        pdf.output('App/Empaque/data/pdf/' + name_pdf, 'F')
                        jsonList = json.dumps({'message': 'Success', 'pdf': name_pdf}) 
                        return JsonResponse(jsonList, safe=False)
                    else:
                        jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                        return JsonResponse(jsonList, safe=False)
                except Exception as e:
                    print(e)
                    error = "Ocurrió un error: " + str(e)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
    else:
        error = "Ocurrió un error: "
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    

def descarga_pdf_control_camaras(request, filename):
    nombre = filename
    filename = 'App/Empaque/data/pdf/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404

def modelo():
    try:
        ZetoneApp = zetoneApp()
        cursorZetoneApp = ZetoneApp.cursor()
        Consulta_SQL = ("SELECT nombrePDF FROM Pdf_Generados WHERE nombrePDF=''")
        cursorZetoneApp.execute(Consulta_SQL)
        consultaPDF = cursorZetoneApp.fetchone()
        if consultaPDF:
            pdf = "Reporte_Camaras_Calidad_.pdf"
            jsonList = json.dumps({'message':'Success', 'pdf': pdf}) 
            return JsonResponse(jsonList, safe=False)
        else:
            data_camaras = []
            try:
                ZetoApp = zetoneApp()
                cursorZetoApp = ZetoApp.cursor()
                consulta_data_camaras = ("SELECT Fecha, Hora, Observaciones, Usuario FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
                cursorZetoApp.execute(consulta_data_camaras)
                
            except Exception as e:
                print(e)
                error = str(e)
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            finally:
                cursorZetoApp.close()
                ZetoApp.close()


            jsonList = json.dumps({'message':'Not Found'}) 
            return JsonResponse(jsonList, safe=False)
    except Exception as e:
        print(e)
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    finally:
        cursorZetoneApp.close()
        ZetoneApp.close()


def recolecta_horas_control_camaras(request, fecha):
    try:
        ZetoneApp = zetoneApp()
        cursorZetoneApp = ZetoneApp.cursor()
        Consulta_SQL = ("SELECT Hora FROM Reporte_Control_Camaras WHERE Fecha='" + str(fecha) + "'")
        cursorZetoneApp.execute(Consulta_SQL)
        consulta_horas = cursorZetoneApp.fetchall()
        if consulta_horas:
            lista_horas = []
            for i in consulta_horas:
                lista_horas.append(i)
                print(i)
        else:
            jsonList = json.dumps({'message':'No se encontraron reportes'}) 
            return JsonResponse(jsonList, safe=False)
            
    except Exception as e:
        print(e)
        error = str(e)
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    finally:
        cursorZetoneApp.close()
        ZetoneApp.close()    