from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import JsonResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.static import serve
from App.ZTime.conexion import *
from App.Empaque.modelosPDF.modelosPDF import *
import os
import matplotlib.pyplot as plt
from django.db import connections

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

def fechaNombre(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    now = datetime.now()
    #stringFecha = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
    di = datetime.strptime(str(fecha), "%Y-%m-%d")
    dianum = now.day
    mes = meses[now.month]
    año = now.year
    diaNombre = dias[di.weekday()]
    hora_actual = datetime.now().strftime("%H:%M:%S")
    fechaN = (diaNombre + ", " + str(dianum) + " de " + str(mes) + " del " + str(año) + " - " + str(hora_actual) +" Hs.")
    return fechaN

def data_general(fecha):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT ID, CONVERT(VARCHAR(10), Fecha, 103) AS Fecha, CONVERT(VARCHAR(5),Hora, 108) AS Hora, Observaciones, Usuario\n" +
                "FROM Reporte_Control_Camaras \n" +
                "WHERE TRY_CONVERT(DATE,Fecha)='" + str(fecha) +"'")
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if consulta:
            lista_datos_general = []
            for i in consulta:
                dato = str(i)
                lista_datos_general.append(dato)
            return lista_datos_general
        else:
            return 0
    except Exception as e:
            print(e)
            return 5
    finally:
        cursor.close()
        conexion.close()

def data_distinct_camaras(id):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT DISTINCT RIGHT('00' + Camara, 2) AS Camara\n" +
                "FROM Control_Camaras\n" +
                "WHERE ID_Reporte='" + str(id) + "' AND Camara NOT LIKE 'ANTE-CAM-%'\n" +
                "UNION \n" +
                "SELECT DISTINCT Camara\n" +
                "FROM Control_Camaras\n" +
                "WHERE ID_Reporte='" + str(id) + "' AND Camara LIKE 'ANTE%' ")
        cursor.execute(sql)
        consulta = cursor.fetchall()
        if consulta:
            lista_camaras = []
            for i in consulta:
                camara = str(i[0])
                new_camara = camara[1:] if camara.startswith("0") else camara
                lista_camaras.append(new_camara)
            return lista_camaras
    except Exception as e:
            print(e)
            return 5
    finally:
        cursor.close()
        conexion.close()

def delete_jpeg_files_control_camaras():
    directory = "App/Empaque/data/images"
    for filename in os.listdir(directory):
        if filename.endswith('.JPEG'):
            os.remove(os.path.join(directory, filename))


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
                lista_data_general = data_general(fecha)
                if lista_data_general != 0:
                    id = lista_data_general[0]
                    fechaReporte = str(lista_data_general[1])
                    horaReporte = str(lista_data_general[2])
                    observaciones = str(lista_data_general[3])
                    usuario = str(lista_data_general[4])
                    listado_camaras = data_distinct_camaras(id)
                    fechaActual = str(fecha_actual())
                    pdf = control_camaras_PDF(fechaReporte, horaReporte, fechaActual, usuario)
                    pdf.alias_nb_pages()
                    pdf.add_page()
                    for i in listado_camaras:
                        pdf.set_font('Arial', 'B', 11)
                        pdf.set_fill_color(186, 233, 175)
                        pdf.multi_cell(w=0, h=8, txt='Cámara:      ' + str(i), border='', align='L', fill=True)
                        try:
                            conexion = zetoneApp()
                            cursor = conexion.cursor()
                            sql = ("SELECT Especie, Envase, Temperatura \n " +
                                    "FROM Control_Camaras \n " +
                                    "WHERE ID_Reporte='" + str(id) + "' AND Camara='" + str(i) + "'\n " +
                                    "ORDER BY Camara, Envase")
                            cursor.execute(sql)
                            consulta = cursor.fetchall()
                            if consulta:
                                for j in consulta:
                                    pdf.set_font('Arial', '', 8)
                                    pdf.cell(w=40, h=5, txt= str(j[0]), border='LTBR', align='C', fill=0)
                                    pdf.cell(w=40, h=5, txt= str(j[1]), border='LBTR', align='C', fill=0)
                                    pdf.multi_cell(w=0, h=5, txt= str(j[2]) +  ' °C', border='LBTR', align='C', fill=0)
                        except Exception as e:
                                print(e)
                        finally:
                            cursor.close()
                            conexion.close()


                    ### AGREGA PÁGINA DE OBSERVACIONES E IMÁGENES
                    pdf.add_page()
                    pdf.rect(x=10,y=43,w=190,h=5)
                    pdf.text(x=11, y=46.5, txt= 'OBSERVACIONES:')
                    ### CONTRUCTOR DE OBS
                    observaciones = observaciones
                    lista_observaciones = observaciones.split("_")
                    for j in lista_observaciones:
                        pdf.set_font('Arial', '', 10)
                        pdf.multi_cell(w=0, h=5, txt= str(j) or "Sin Observaciones", border='LBR', align='L', fill=0)

                    ##CONSULTA IMAGENES
                    ZetoApp = zetoneApp()
                    cursorZetoApp = ZetoApp.cursor()
                    consulta_data_images = ("SELECT Fotos FROM Fotos_Control_Camaras WHERE ID_Reporte='" + str(id) + "'")
                    cursorZetoApp.execute(consulta_data_images)
                    consulta_images = cursorZetoApp.fetchall()
                    if consulta_images:
                        ### IMAGENES
                        pdf.rect(x=10,y=98,w=190,h=5)
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=11, y=102, txt= 'IMÁGENES:')
                        name_decoded_image = []
                        k_index = 0
                        fecha_name = fechaReporte.replace('/', '')
                        hora_name = horaReporte.replace(':', '')
                        for k in consulta_images:
                            nombre_foto = decode_base64_to_image(k_index,fecha_name, hora_name, str(id), k[0])
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
                    fecha = fechaReporte.replace('/', '')
                    name = "Reporte_Control_Cámaras_" + fecha + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name, 'F') 
                    delete_jpeg_files_control_camaras() 
                    jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                    return JsonResponse(jsonList, safe=False)

                else:
                    jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                    return JsonResponse(jsonList, safe=False)
                
            except Exception as e:
                error = "Ocurrió un error: " + str(e)
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
        elif str(Tipo) == "Control Empaque":
            Top_Caja = consultaTopCaja(fecha)
            if Top_Caja != "0":
                try:
                    conexion = zetoneApp()
                    cursor = conexion.cursor()
                    consultaSQL = ("SELECT        Bulto.Id_bulto AS id, Marca.Nombre_marca AS Marca, Calidad.nombre_calidad AS Calidad, Variedad.nombre_variedad AS Variedad, Especie.nombre_especie AS Especie, Bulto.id_galpon AS Galpon, \n" +
                                                            "Envase.nombre_envase AS Envase, Calibre.nombre_calibre AS Calibre, USR_MCCUADRO.USR_CUAD_UMI AS UMI, USR_MCCUADRO.USR_CUAD_UP AS UP, Embalador.nombre_embalador AS Embalador, \n" +
                                                            "USR_MCLOTE.USR_LOTE_NUMERO AS Lote, CONVERT(varchar(10), Bulto.fecha_alta_bulto, 103) AS FechaEmbalado, CONVERT(varchar(5), Bulto.fecha_alta_bulto, 108) AS HoraEmbalado, numeroCaja, CONVERT(varchar(10), DefectosCaja.Fecha, 103) AS FechaControl, CONVERT(varchar(5), DefectosCaja.Hora, 108) AS HoraControl, PesoNeto, PesoBruto, PLU, Observaciones, Deformadas, TamañoIncorrecto, FaltaDeColor, Russeting, Heladas, roceBins, Asoleado, QuemadoPorSol, Fitotoxicidad, Rolado, Golpes, \n" +
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
                                pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                                #pdf.text(x=165.5, y=19.5, txt= '10:23:33 Hs.')
                                ###DATOS PRINCIPALES CAJA
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=48, txt= str(i[14]))
                                pdf.text(x=56, y=48, txt= str(i[0]))
                                pdf.text(x=90, y=48, txt= str(i[15]))
                                pdf.text(x=122, y=48, txt= str(i[16]) + ' Hs.')
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
                                pdf.set_font('Times', 'B', 10)
                                pdf.text(x=46, y=288, txt= str(fecha_actual()))
                                pdf.set_font('Times', 'I', 10)
                                user = str(i[53])
                                if user == "Nicole" or user == "nicole":
                                    pdf.set_font('Times', 'BI', 10)
                                    pdf.text(x=20, y=288, txt= 'Nicole')
                                else:
                                    pdf.text(x=20, y=288, txt= user)#USER
                                ###FOTOS
                                bulto = str(i[0])
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg', x=160, y=58, w=15, h=15)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=65, txt='NOT IMAGE')
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg', x=146, y=82, w=45, h=70)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=119, txt='NOT IMAGE')
                                index = index + 1
                            else:
                                if str(i[5]) == "1":
                                    empaque = "Pera"
                                else:
                                    empaque = "Manzana"
                                #CONDICIONAL CUANDO VALE 1
                                pdf.set_font('Arial', '', 10)
                                pdf.text(x=26, y=168, txt= str(i[14]))#CAJA
                                pdf.text(x=56, y=168, txt= str(i[0]))#BULTO
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
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/plu_image_' + bulto + '.jpeg', x=160, y=178, w=15, h=15)
                                except:
                                    pdf.set_font('Arial', '', 12)
                                    pdf.text(x=155, y=188, txt='NOT IMAGE')
                                try:
                                    pdf.image('App/API/media/images/Calidad/reportes_empaque/caja_image_' + bulto + '.jpeg', x=146, y=201, w=45, h=70)
                                except:
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
                    error = "Ocurrió un error: " + str(e)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
        elif str(Tipo) == "Control Descarte":
            try:
                conexion = zetoneApp()
                cursor = conexion.cursor()
                sql5 = ("SELECT        DescarteLote.Lote, Variedad.USR_VAR_NOMBRE as Variedad, DescarteLote.Empaque, CONVERT(varchar(10), DescarteLote.Fecha, 103) AS Fecha, CONVERT(varchar(5), DescarteLote.Hora, 108) AS Hora, DescarteLote.cantBins, DescarteLote.obsDescarte, DescarteLote.Usuario, DefectosDescarte.Agamuzado,\n" +
                                                "DefectosDescarte.Amarillo, DefectosDescarte.Arañuela, DefectosDescarte.Bicho, DefectosDescarte.binsRotos, DefectosDescarte.binsSinLlenar, DefectosDescarte.Bitterpit, DefectosDescarte.Caliz, \n" +
                                                "DefectosDescarte.Carpocapsa, DefectosDescarte.Acuoso, DefectosDescarte.Mohoso, DefectosDescarte.Corcho, DefectosDescarte.Cucharita, DefectosDescarte.Cracking, DefectosDescarte.Quimico, \n" +
                                                "DefectosDescarte.Decaimiento, DefectosDescarte.Deformada, DefectosDescarte.Deshidratada, DefectosDescarte.Desvio, DefectosDescarte.faltaBoro, DefectosDescarte.faltaColor, DefectosDescarte.Fondo, \n" +
                                                "DefectosDescarte.frutoGrande, DefectosDescarte.FrutoChico, DefectosDescarte.golpes, DefectosDescarte.Granizo, DefectosDescarte.Helada, DefectosDescarte.Heridas, DefectosDescarte.heridaMaquina, \n" +
                                                "DefectosDescarte.heridaPedunculo, DefectosDescarte.Herinosis, DefectosDescarte.Lenticelosis, DefectosDescarte.Machucones, DefectosDescarte.madurezAvanzada, DefectosDescarte.madurezSalpicada, \n" +
                                                "DefectosDescarte.malCosechada, DefectosDescarte.Mezcla, DefectosDescarte.Piojo, DefectosDescarte.Podridas, DefectosDescarte.Psilido, DefectosDescarte.Pulgon, DefectosDescarte.Quemada, \n" +
                                                "DefectosDescarte.Rameada, DefectosDescarte.Roce, DefectosDescarte.Rolado, DefectosDescarte.Russeting, DefectosDescarte.Sarna, DefectosDescarte.Flor, DefectosDescarte.sinPedunculo, \n" +
                                                "DefectosDescarte.Trips\n" +
                        "FROM            DescarteLote INNER JOIN\n" +
                                                "DefectosDescarte ON DescarteLote.Lote = DefectosDescarte.Lote INNER JOIN\n" +
                                                "servidordb.general.dbo.usr_mclote AS Lote ON DescarteLote.Lote = Lote.USR_LOTE_NUMERO INNER JOIN\n" +
                                                "servidordb.general.dbo.usr_mcvaried AS Variedad ON Lote.USR_VAR_ALIAS = Variedad.USR_VAR_ALIAS\n"+
                        "WHERE        (TRY_CONVERT(DATE, DescarteLote.Fecha) = '" + str(fecha) + "')")
                cursor.execute(sql5)
                consulta = cursor.fetchall()
                if consulta:
                    index = 0
                    pdf = Reporte_Descarte()
                    pdf.alias_nb_pages()
                    for i in consulta:
                        if i[2] == 1:
                            empaque = "Pera"
                        else:
                            empaque = "Manzana"
                        if index == 0:
                            pdf.add_page()
                            ###IZQUIERDA
                            pdf.set_font('Arial', '', 7)
                            pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                            pdf.set_font('Arial', '', 10)
                            pdf.text(x=32, y=44, txt= empaque)
                            pdf.text(x=66, y=44, txt= str(i[3]))
                            pdf.text(x=25, y=49, txt= str(i[4]) + ' Hs.')
                            pdf.text(x=66, y=49, txt= str(i[0]))
                            pdf.text(x=32, y=54, txt= str(i[5]))
                            pdf.text(x=58, y=54, txt= str(i[1]))
                            ##DEFECTOS
                            pdf.set_font('Arial', '', 8)
                            pdf.text(x=68, y=63, txt= str(i[8]))
                            pdf.text(x=68, y=67, txt= str(i[9]))
                            pdf.text(x=68, y=71, txt= str(i[10]))
                            pdf.text(x=68, y=75, txt= str(i[11]))
                            pdf.text(x=68, y=79, txt= str(i[12]))
                            pdf.text(x=68, y=83, txt= str(i[13]))
                            pdf.text(x=68, y=87, txt= str(i[14]))
                            pdf.text(x=68, y=91, txt= str(i[15]))
                            pdf.text(x=68, y=95, txt= str(i[16]))
                            pdf.text(x=68, y=99, txt= str(i[17]))
                            pdf.text(x=68, y=103, txt= str(i[18]))
                            pdf.text(x=68, y=107, txt= str(i[19]))
                            pdf.text(x=68, y=111, txt= str(i[20]))
                            pdf.text(x=68, y=115, txt= str(i[21]))
                            pdf.text(x=68, y=119, txt= str(i[22]))
                            pdf.text(x=68, y=123, txt= str(i[23]))
                            pdf.text(x=68, y=127, txt= str(i[24]))
                            pdf.text(x=68, y=131, txt= str(i[25]))
                            pdf.text(x=68, y=135, txt= str(i[26]))
                            pdf.text(x=68, y=139, txt= str(i[27]))
                            pdf.text(x=68, y=143, txt= str(i[28]))
                            pdf.text(x=68, y=147, txt= str(i[29]))
                            pdf.text(x=68, y=151, txt= str(i[30]))
                            pdf.text(x=68, y=155, txt= str(i[31]))
                            pdf.text(x=68, y=159, txt= str(i[32]))
                            pdf.text(x=68, y=163, txt= str(i[33]))
                            pdf.text(x=68, y=167, txt= str(i[34]))
                            pdf.text(x=68, y=171, txt= str(i[35]))
                            pdf.text(x=68, y=175, txt= str(i[36]))
                            pdf.text(x=68, y=179, txt= str(i[37]))
                            pdf.text(x=68, y=183, txt= str(i[38]))
                            pdf.text(x=68, y=187, txt= str(i[39]))
                            pdf.text(x=68, y=191, txt= str(i[40]))
                            pdf.text(x=68, y=195, txt= str(i[41]))
                            pdf.text(x=68, y=199, txt= str(i[42]))
                            pdf.text(x=68, y=203, txt= str(i[43]))
                            pdf.text(x=68, y=207, txt= str(i[44]))
                            pdf.text(x=68, y=211, txt= str(i[45]))
                            pdf.text(x=68, y=215, txt= str(i[46]))
                            pdf.text(x=68, y=219, txt= str(i[47]))
                            pdf.text(x=68, y=223, txt= str(i[48]))
                            pdf.text(x=68, y=227, txt= str(i[49]))
                            pdf.text(x=68, y=231, txt= str(i[50]))
                            pdf.text(x=68, y=235, txt= str(i[51]))
                            pdf.text(x=68, y=239, txt= str(i[52]))
                            pdf.text(x=68, y=243, txt= str(i[53]))
                            pdf.text(x=68, y=247, txt= str(i[54]))
                            pdf.text(x=68, y=251, txt= str(i[55]))
                            pdf.text(x=68, y=255, txt= str(i[56]))
                            pdf.text(x=68, y=259, txt= str(i[57]))
                            pdf.text(x=20, y=267, txt= str(i[6]))
                            pdf.set_font('Arial', 'B', 10)
                            pdf.text(x=46, y=288, txt= str(i[3]))#FECHA
                            ## CONDICIONAL DE USER
                            if str(i[7]) == "Nicole" or str(i[7]) == "nicole":
                                pdf.set_font('Times', 'BI', 10)
                                pdf.text(x=20, y=288, txt= 'Nicole')
                            else:
                                pdf.text(x=20, y=288, txt= str(i[7]))
                            index = index + 1
                        else:
                            ##DERECHA
                            pdf.set_font('Arial', '', 10)
                            pdf.text(x=142, y=44, txt= empaque)
                            pdf.text(x=176, y=44, txt= str(i[3]))
                            pdf.text(x=135, y=49, txt= str(i[4]) + ' Hs.')
                            pdf.text(x=176, y=49, txt= str(i[0]))
                            pdf.text(x=142, y=54, txt= str(i[5]))
                            pdf.text(x=168, y=54, txt= str(i[1]))
                            ##DEFECTOS
                            pdf.set_font('Arial', '', 8)
                            pdf.text(x=178, y=63, txt= str(i[8]))
                            pdf.text(x=178, y=67, txt= str(i[9]))
                            pdf.text(x=178, y=71, txt= str(i[10]))
                            pdf.text(x=178, y=75, txt= str(i[11]))
                            pdf.text(x=178, y=79, txt= str(i[12]))
                            pdf.text(x=178, y=83, txt= str(i[13]))
                            pdf.text(x=178, y=87, txt= str(i[14]))
                            pdf.text(x=178, y=91, txt= str(i[15]))
                            pdf.text(x=178, y=95, txt= str(i[16]))
                            pdf.text(x=178, y=99, txt= str(i[17]))
                            pdf.text(x=178, y=103, txt= str(i[18]))
                            pdf.text(x=178, y=107, txt= str(i[19]))
                            pdf.text(x=178, y=111, txt= str(i[20]))
                            pdf.text(x=178, y=115, txt= str(i[21]))
                            pdf.text(x=178, y=119, txt= str(i[22]))
                            pdf.text(x=178, y=123, txt= str(i[23]))
                            pdf.text(x=178, y=127, txt= str(i[24]))
                            pdf.text(x=178, y=131, txt= str(i[25]))
                            pdf.text(x=178, y=135, txt= str(i[26]))
                            pdf.text(x=178, y=139, txt= str(i[27]))
                            pdf.text(x=178, y=143, txt= str(i[28]))
                            pdf.text(x=178, y=147, txt= str(i[29]))
                            pdf.text(x=178, y=151, txt= str(i[30]))
                            pdf.text(x=178, y=155, txt= str(i[31]))
                            pdf.text(x=178, y=159, txt= str(i[32]))
                            pdf.text(x=178, y=163, txt= str(i[33]))
                            pdf.text(x=178, y=167, txt= str(i[34]))
                            pdf.text(x=178, y=171, txt= str(i[35]))
                            pdf.text(x=178, y=175, txt= str(i[36]))
                            pdf.text(x=178, y=179, txt= str(i[37]))
                            pdf.text(x=178, y=183, txt= str(i[38]))
                            pdf.text(x=178, y=187, txt= str(i[39]))
                            pdf.text(x=178, y=191, txt= str(i[40]))
                            pdf.text(x=178, y=195, txt= str(i[41]))
                            pdf.text(x=178, y=199, txt= str(i[42]))
                            pdf.text(x=178, y=203, txt= str(i[43]))
                            pdf.text(x=178, y=207, txt= str(i[44]))
                            pdf.text(x=178, y=211, txt= str(i[45]))
                            pdf.text(x=178, y=215, txt= str(i[46]))
                            pdf.text(x=178, y=219, txt= str(i[47]))
                            pdf.text(x=178, y=223, txt= str(i[48]))
                            pdf.text(x=178, y=227, txt= str(i[49]))
                            pdf.text(x=178, y=231, txt= str(i[50]))
                            pdf.text(x=178, y=235, txt= str(i[51]))
                            pdf.text(x=178, y=239, txt= str(i[52]))
                            pdf.text(x=178, y=243, txt= str(i[53]))
                            pdf.text(x=178, y=247, txt= str(i[54]))
                            pdf.text(x=178, y=251, txt= str(i[55]))
                            pdf.text(x=178, y=255, txt= str(i[56]))
                            pdf.text(x=178, y=259, txt= str(i[57]))
                            pdf.text(x=130, y=267, txt= str(i[6]))
                            index = 0
                    ###IMPRIMO PDF
                    name_fecha = str(fecha).replace('-','')
                    name = "Control_Descarte_" + name_fecha + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name, 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                    return JsonResponse(jsonList, safe=False)
                else:
                    jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                    return JsonResponse(jsonList, safe=False)
            except Exception as e:
                    error = "Ocurrió un error: " + str(e)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
            finally:
                cursor.close()
                conexion.close()
        elif str(Tipo) == "Control Presiones":
            if  listaHoras(fecha) == 5:
                error = "Ocurrió un error en la conexión."
                jsonList = json.dumps({'message': error}) 
                return JsonResponse(jsonList, safe=False)
            elif listaHoras(fecha) == 0:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
            else:
                ##CONSIGUIÓ LAS HORAS
                listado_de_horas = listaHoras(str(fecha))
                index = 0
                pdf = Reporte_Presiones()
                pdf.alias_nb_pages()
                for i in listado_de_horas:
                    hora = str(i)
                    hora_replace = hora.replace(':','')
                    lista_x = data_x(str(fecha),hora)
                    lista_y = data_y(str(fecha),hora)
                    Crea_grafico(lista_x,lista_y,hora_replace)
                    datos = data_Presiones(str(fecha),hora)
                    idGalpon = str(datos[0])
                    variedad = str(consultaVariedad(fecha,idGalpon))
                    if idGalpon == "1":
                        empaque = "Pera"
                    else:
                        empaque = "Manzana"
                    if index == 0:
                        pdf.add_page()
                        ###ARRIBA
                        pdf.set_font('Arial', '', 7)
                        pdf.text(x=146, y=16.5, txt= str(fechaNombre(fecha)))
                        pdf.set_font('Arial', '', 10)
                        pdf.text(x=44, y=49, txt= empaque)
                        pdf.text(x=100, y=49, txt= datos[1])
                        pdf.text(x=160, y=49, txt= datos[2]+' Hs.')
                        pdf.text(x=48, y=64, txt= str(datos[3]))
                        pdf.text(x=75, y=64, txt= variedad)
                        pdf.text(x=165, y=64, txt= datos[4] + ' Lb.')
                        pdf.image('App/API/media/images/Calidad/reportes_presiones/grafico_presion_' + hora_replace + '.png', x=12, y=85, w=180, h=50)
                        pdf.set_font('Arial', 'B', 10)
                        pdf.text(x=46, y=288, txt= datos[1])
                        ## CONDICIONAL DE USER
                        if str(datos[5]) == "Nicole" or str(datos[5]) == "nicole":
                            pdf.set_font('Times', 'BI', 10)
                            pdf.text(x=20, y=288, txt= 'Nicole')
                        else:
                            pdf.text(x=20, y=288, txt= str(datos[5]))
                        index = index + 1
                    else:
                        ###ABAJO
                        pdf.set_font('Arial', '', 10)
                        pdf.text(x=44, y=169, txt= empaque)
                        pdf.text(x=100, y=169, txt= datos[1])
                        pdf.text(x=160, y=169, txt= datos[2] + ' Hs.')
                        pdf.text(x=48, y=184, txt= str(datos[3]))
                        pdf.text(x=75, y=184, txt= variedad)
                        pdf.text(x=165, y=184, txt= datos[4] + ' Lb.')
                        pdf.image('App/API/media/images/Calidad/reportes_presiones/grafico_presion_' + hora_replace + '.png', x=12, y=205, w=180, h=50)
                        index = 0
                name_fecha = str(fecha).replace('-','')
                name = "Control_Presiones_" + name_fecha + '.pdf'
                pdf.output('App/Empaque/data/pdf/' + name, 'F')
                delete_png_files()
                jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                return JsonResponse(jsonList, safe=False)
        elif str(Tipo) == "Ingreso Bascula":

            variedadesDia =  traeVeriedades_Fecha(fecha)

            InsertaDataPrueba(fecha, str(variedadesDia))
            if variedadesDia:
                try:
                    pdf = Reporte_Ingreso_Bascula()
                    pdf.alias_nb_pages()
                    pdf.add_page()
                    for variedad in variedadesDia:
                        #print(variedad + " ##### VARIEDAD #####") ### VARIEDAD GRANDE
                        nombreVariedad = traeNombreVariedad(variedad)
                        InsertaDataPrueba(fecha, str(nombreVariedad))
                        cantidadBins = traeCantBinsPorFecha_variedad(fecha,variedad)
                        InsertaDataPrueba(fecha, str(cantidadBins))
                        #### CADA VEZ QUE CAMBIO LA VARIEDAD #### ENCABEZADO
                        pdf.set_fill_color(186, 233, 175)
                        pdf.set_font('Arial', 'B', 16)
                        pdf.cell(w=100, h=8, txt= str(nombreVariedad), border='', align='L', fill=True)
                        pdf.set_font('Arial', 'B', 9)
                        pdf.multi_cell(w=0, h=8, txt= "TOTAL BINS: " + str(cantidadBins) + " - Fecha: " + str(formatear_fecha(str(fecha))), border='', align='R', fill=True)
                        pdf.multi_cell(w=0, h=2, txt= "", border='', align='R', fill=0)

                        chacrasPorVariedad = traeChacrasPorVariedadFecha(variedad,fecha)
                        InsertaDataPrueba(fecha, str(chacrasPorVariedad))
                        for chacra in chacrasPorVariedad:
                            #print(chacra + " ##### CHACRA #####") ### ID CHACRA 
                            Listados = detalleGeneral(variedad,fecha,chacra)
                            nombreChacra = traeNombreChacra(chacra)
                            pdf.set_font('Arial', 'B', 12)
                            pdf.multi_cell(w=0, h=7, txt= "CHACRA: " +  str(nombreChacra) , border='LTR', align='L', fill=0)
                            pdf.set_font('Arial', '', 8)
                            pdf.cell(w=40, h=5, txt= "", border='LT', align='C', fill=True)
                            pdf.cell(w=55, h=5, txt= "FIRMEZA DE PULPA (lbs)", border='LTR', align='C', fill=True)
                            pdf.multi_cell(w=0, h=5, txt= "", border='LTR', align='C', fill=True)
                            pdf.cell(w=20, h=5, txt= "LOTE", border='TLRB', align='C', fill=True)
                            pdf.cell(w=20, h=5, txt= "CANT. BINS", border='TLRB', align='C', fill=True)
                            pdf.cell(w=15, h=5, txt= "MIN", border='TLRB', align='C', fill=True)
                            pdf.cell(w=25, h=5, txt= "PROMEDIO", border='TLRB', align='C', fill=True)
                            pdf.cell(w=15, h=5, txt= "MAX", border='TLRB', align='C', fill=True)
                            pdf.cell(w=30, h=5, txt= "SOLUBLES", border='TLRB', align='C', fill=True)
                            pdf.cell(w=30, h=5, txt= "ALMIDON", border='TLRB', align='C', fill=True)
                            pdf.multi_cell(w=0, h=5, txt= "ACIDEZ", border='TLRB', align='C', fill=True)
                            for lista in Listados:
                                #print(str(lista[4]))
                                min,promedio,max = presiones(str(lista[4]))
                                solubles,almidon,acidez = detallesControl(str(lista[4]))

                                pdf.cell(w=20, h=5, txt= str(lista[0]), border='LB', align='C', fill=0)
                                pdf.cell(w=20, h=5, txt= str(lista[3]), border='LB', align='C', fill=0)
                                pdf.cell(w=15, h=5, txt= str(min), border='LB', align='C', fill=0)
                                pdf.cell(w=25, h=5, txt= str(promedio), border='LB', align='C', fill=0)
                                pdf.cell(w=15, h=5, txt= str(max), border='LB', align='C', fill=0)
                                pdf.cell(w=30, h=5, txt= str(solubles), border='LB', align='C', fill=0)
                                pdf.cell(w=30, h=5, txt= str(almidon), border='LB', align='C', fill=0)
                                pdf.multi_cell(w=0, h=5, txt= str(acidez), border='LRB', align='C', fill=0)
                            pdf.multi_cell(w=0, h=8, txt= "", border='', align='C', fill=0)

                    name_fecha = str(fecha).replace('-','')
                    name = "Ingreso_Bascula_" + name_fecha + '.pdf'
                    pdf.output('App/Empaque/data/pdf/' + name, 'F')
                    jsonList = json.dumps({'message': 'Success', 'pdf': name}) 
                    return JsonResponse(jsonList, safe=False)
                except Exception as e:
                    error = str(e)
                    InsertaDataPrueba("PDF", error)
                    jsonList = json.dumps({'message': error}) 
                    return JsonResponse(jsonList, safe=False)
                
            else:
                jsonList = json.dumps({'message': 'No se encontraron Reportes para la fecha: ' + str(fecha)}) 
                return JsonResponse(jsonList, safe=False)
    else:
        error = "Ocurrió un error: "
        jsonList = json.dumps({'message': error}) 
        return JsonResponse(jsonList, safe=False)
    

def data_x(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT Fruto FROM Presiones WHERE TRY_CONVERT(DATE, Fecha) ='" + fecha + "' AND Hora='" + str(hora) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchall()
        if consulta:
            x_data = [] # FRUTOS
            for i in consulta:
                x_data.append(i[0])
        return x_data
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def data_y(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT CAST((ROUND(Presion, 0, 0)) AS INT) FROM Presiones WHERE TRY_CONVERT(DATE, Fecha) ='" + fecha + "' AND Hora='" + str(hora) + "'")
        cursor.execute(sql)
        consulta = cursor.fetchall()
        if consulta:
            y_data = [] # FRUTOS
            for i in consulta:
                y_data.append(i[0])
        return y_data
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def Crea_grafico(lista_x,lista_y,hora):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.plot(lista_x, lista_y, 'o-', label='Presiones')
    for x, y in zip(lista_x, lista_y):
        ax.scatter(x, y, color='black')
        ax.annotate(y, (x, y), textcoords="offset points", xytext=(0,5), ha='center')
    ax.set_xlabel("N° Fruto")
    ax.set_ylabel("Presión (Lb.)")
    ax.set_xticks(lista_x)
    ax.set_yticks(lista_y)
    ax.set_yticks(range(min(lista_y), max(lista_y)+1, 2))
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    name_image = 'grafico_presion_' + str(hora)
    plt.savefig('App/API/media/images/Calidad/reportes_presiones/'+ name_image + '.png')

def listaHoras(fecha):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT DISTINCT CONVERT(char(5),Hora) FROM Presiones WHERE Fecha='" + str(fecha) + "'")
        cursor.execute(sql5)
        consulta = cursor.fetchall()
        if consulta:
            horasLista = []
            for i in consulta:
                hora = str(i[0])
                horasLista.append(hora)
            return horasLista
        else:
            return 0
    except Exception as e:
            return 5
    finally:
        cursor.close()
        conexion.close()

def data_Presiones(fecha,hora):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql5 = ("SELECT Empaque, CONVERT(varchar(10), Fecha, 103) AS fecha, CONVERT(char(5),Hora) AS hora, MAX(Fruto) AS frutos, CONVERT(char(5),CAST(round(AVG(Presion),2) AS decimal(9,2))) AS Promedio, usuario\n"+
                "FROM Presiones\n" +
                "WHERE Fecha='" + str(fecha) + "' AND Hora='" + str(hora) + "'\n"
                "GROUP BY Empaque, Fecha, Hora, usuario")
        cursor.execute(sql5)
        consulta = cursor.fetchone()
        if consulta:
            lista_datos = []
            for i in consulta:
                dato = str(i)
                lista_datos.append(dato)
            return lista_datos
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()

def delete_png_files():
    directory = "App/API/media/images/Calidad/reportes_presiones"
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            os.remove(os.path.join(directory, filename))

def descarga_pdf_control_camaras(request, filename):
    nombre = filename
    filename = 'App/Empaque/data/pdf/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise Http404

def modelo(fecha):
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

### CONSULTA VARIEDAD PRESIONES 
def consultaVariedad(fecha,idGalpon):
    try:
        conexion = zetoneApp()
        cursor = conexion.cursor()
        sql = ("SELECT        TOP(1)MCVariedad.USR_VAR_NOMBRE AS Variedad\n" +
                "FROM            servidordb.Trazabilidad.dbo.LoteEtiquetado AS Lote INNER JOIN\n" +
                                        "servidordb.General.dbo.USR_MCLOTE AS MCLote ON Lote.id_lote = MCLote.USR_LOTE_NUMERO INNER JOIN\n" +
                                        "servidordb.General.dbo.USR_MCVARIED AS MCVariedad ON MCLote.USR_VAR_ALIAS = MCVariedad.USR_VAR_ALIAS\n" +
                "WHERE        (TRY_CONVERT(DATE, Lote.Fecha) = '" + str(fecha) + "' AND Lote.id_galpon ='" + str(idGalpon) + "')")
        cursor.execute(sql)
        consulta = cursor.fetchone()
        if consulta:
            variedad = str(consulta[0])
            return variedad
        else:
            variedad = "---"
            return variedad
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conexion.close()



#### CONSULTA PARTES NUEVAS!!!!


def traeVeriedades_Fecha(fecha):
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            sql = """
                DECLARE @@Fecha DATE;
                SET @@Fecha = %s;
                SELECT        DISTINCT General.dbo.USR_MCLOTE.USR_VAR_ALIAS
                FROM            LoteCalidad INNER JOIN
                                        General.dbo.USR_MCLOTE ON LoteCalidad.LoteNumero = General.dbo.USR_MCLOTE.USR_LOTE_NUMERO
                WHERE        (CONVERT(DATE, LoteCalidad.FechaIngresoCalidad) = CONVERT(DATE, @@Fecha))
            """
            cursor.execute(sql, [fecha])
            consulta = cursor.fetchall()
            if consulta:
                results = [] 
                for i in consulta:
                    results.append(str(i[0]))
            return results
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("traeVeriedades_Fecha", error)


def traeCantBinsPorFecha_variedad(fecha,variedad):
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            sql = """
                DECLARE @@Fecha DATE;
                DECLARE @@Variedad VARCHAR(255);
                SET @@Fecha = %s;
                SET @@Variedad = %s;
                SELECT SUM(General.dbo.USR_MCLOTE.USR_LOTE_CANTBINS)
                FROM            LoteCalidad INNER JOIN
                                        General.dbo.USR_MCLOTE ON LoteCalidad.LoteNumero = General.dbo.USR_MCLOTE.USR_LOTE_NUMERO
                WHERE        (CONVERT(DATE, LoteCalidad.FechaIngresoCalidad) = @@Fecha AND General.dbo.USR_MCLOTE.USR_VAR_ALIAS = @@Variedad)
            """
            cursor.execute(sql, [fecha,variedad])
            consulta = cursor.fetchone()
            if consulta:
                cantidad = str(consulta[0])
            return cantidad
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("traeCantBinsPorFecha_variedad", error)

def traeChacrasPorVariedadFecha(variedad,fecha):
    try:
        with connections['General'].cursor() as cursor:
            sql = """
                DECLARE @@Variedad VARCHAR(255);
                DECLARE @@Fecha DATE;
                SET @@Variedad = %s;
                SET @@Fecha = %s;
                SELECT        DISTINCT USR_MCCHACRA.USR_CHAC_ALIAS, USR_MCCHACRA.USR_CHAC_NOMBRE
                FROM            Trazabilidad.dbo.CalidadControl INNER JOIN
                                        Trazabilidad.dbo.LoteCalidad INNER JOIN
                                        USR_MCLOTE ON Trazabilidad.dbo.LoteCalidad.LoteNumero = USR_MCLOTE.USR_LOTE_NUMERO ON Trazabilidad.dbo.CalidadControl.idLote = USR_MCLOTE.USR_LOTE_NUMERO INNER JOIN
                                        USR_MCMOVCAM ON USR_MCLOTE.USR_MC_NUMERO = USR_MCMOVCAM.USR_MC_NUMERO INNER JOIN
                                        USR_MCCHACRA ON USR_MCMOVCAM.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS
                WHERE        (USR_MCLOTE.USR_VAR_ALIAS = @@Variedad) AND (CONVERT(DATE, Trazabilidad.dbo.LoteCalidad.FechaIngresoCalidad) = @@Fecha)
            """
            cursor.execute(sql, [variedad,fecha])
            consulta = cursor.fetchall()
            if consulta:
                results = [] 
                for i in consulta:
                    results.append(str(i[0]))
            InsertaDataPrueba("traeChacrasPorVariedadFecha", str(results))
            return results
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("traeChacrasPorVariedadFecha", error)

def detalleGeneral(variedad,fecha,chacra):
    try:
        with connections['General'].cursor() as cursor:
            sql = """
                DECLARE @@Variedad VARCHAR(255);
                DECLARE @@Fecha DATE;
                DECLARE @@Productor VARCHAR(255);
                SET @@Variedad = %s;
                SET @@Fecha = %s;
                SET @@Productor = %s;
                SELECT        USR_MCLOTE_1.USR_LOTE_NUMERO AS LOTE, USR_MCCHACRA.USR_CHAC_NOMBRE AS PRODUCTOR, USR_MCVARIED.USR_VAR_NOMBRE AS VARIEDAD, USR_MCLOTE_1.USR_LOTE_CANTBINS AS CANT_BINS, 
                                        CalidadControl_1.idCalidad AS ID_CALIDAD, USR_MCLOTE_1.USR_VAR_ALIAS AS ID_VARIEDAD,
                                            (SELECT        SUM(USR_MCLOTE.USR_LOTE_CANTBINS) AS Expr1
                                            FROM            Trazabilidad.dbo.CalidadControl INNER JOIN
                                                                        Trazabilidad.dbo.LoteCalidad INNER JOIN
                                                                        USR_MCLOTE ON Trazabilidad.dbo.LoteCalidad.LoteNumero = USR_MCLOTE.USR_LOTE_NUMERO ON Trazabilidad.dbo.CalidadControl.idLote = USR_MCLOTE.USR_LOTE_NUMERO
                                            WHERE        (USR_MCLOTE.USR_VAR_ALIAS = @@VARIEDAD) AND (CONVERT(DATE, Trazabilidad.dbo.LoteCalidad.FechaIngresoCalidad) = @@FECHA)) AS TOTAL_BINS, 
                                CONVERT(VARCHAR(10),CalidadControl_1.FechaCalidad, 103) AS FECHA
                FROM            Trazabilidad.dbo.CalidadControl AS CalidadControl_1 INNER JOIN
                                        Trazabilidad.dbo.LoteCalidad AS LoteCalidad_1 INNER JOIN
                                        USR_MCLOTE AS USR_MCLOTE_1 INNER JOIN
                                        USR_MCVARIED ON USR_MCLOTE_1.USR_VAR_ALIAS = USR_MCVARIED.USR_VAR_ALIAS ON LoteCalidad_1.LoteNumero = USR_MCLOTE_1.USR_LOTE_NUMERO ON 
                                        CalidadControl_1.idLote = USR_MCLOTE_1.USR_LOTE_NUMERO INNER JOIN
                                        USR_MCMOVCAM ON USR_MCLOTE_1.USR_MC_NUMERO = USR_MCMOVCAM.USR_MC_NUMERO INNER JOIN
                                        USR_MCCHACRA ON USR_MCMOVCAM.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS
                WHERE        (USR_MCLOTE_1.USR_VAR_ALIAS = @@VARIEDAD) 
                                AND (CONVERT(DATE, LoteCalidad_1.FechaIngresoCalidad) = @@FECHA)
                                AND USR_MCCHACRA.USR_CHAC_ALIAS = @@Productor
                ORDER BY PRODUCTOR
            """
            cursor.execute(sql, [variedad,fecha,chacra])
            consulta = cursor.fetchall()
            return consulta
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("detalleGeneral", error)


def presiones(idCalidad):
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            sql = """
                SELECT CONVERT(VARCHAR,CAST(MIN(Presion1) AS DECIMAL(18, 2))) AS MINIMA, CONVERT(VARCHAR,CAST((SUM(Presion1) + SUM(Presion2)) / (MAX(NroPresion) * 2) AS DECIMAL(18, 2))) AS PROMEDIO,
		                CONVERT(VARCHAR,CAST(MAX(Presion2) AS DECIMAL(18, 2))) AS MAXIMA
                FROM CalidadPresion
                WHERE idCalidad = %s AND Presion1 <> '0.0000' AND Presion2 <> '0.0000'
            """
            cursor.execute(sql, [idCalidad])
            consulta = cursor.fetchone()
            if consulta:
                min = str(consulta[0]).replace('.',',')
                promedio = str(consulta[1]).replace('.',',')
                max = str(consulta[2]).replace('.',',')
            return min,promedio,max
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("presiones", error)

def detallesControl(idCalidad):
    try:
        with connections['Trazabilidad'].cursor() as cursor:
            sql = """
                SELECT CONVERT(VARCHAR,CAST(Solubles AS DECIMAL(18, 2))),CONVERT(VARCHAR,CAST(Almidon AS DECIMAL(18, 2))),
                        CONVERT(VARCHAR,CAST(Acidez AS DECIMAL(18, 2)))
                FROM CalidadControl
                WHERE idCalidad = %s
            """
            cursor.execute(sql, [idCalidad])
            consulta = cursor.fetchone()
            if consulta:
                solubles = str(consulta[0]).replace('.',',')
                almidon = str(consulta[1]).replace('.',',')
                acidez = str(consulta[2]).replace('.',',')
            return solubles,almidon,acidez
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("detallesControl", error)


def traeNombreChacra(idChacra):
    try:
        with connections['General'].cursor() as cursor:
            sql = """
                SELECT USR_CHAC_NOMBRE
                FROM USR_MCCHACRA
                WHERE USR_CHAC_ALIAS = %s
            """
            cursor.execute(sql, [idChacra])
            consulta = cursor.fetchone()
            if consulta:
                nombreChacra = str(consulta[0])
            return nombreChacra
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("traeNombreChacra", error)

def traeNombreVariedad(idVariedad):
    try:
        with connections['General'].cursor() as cursor:
            sql = """
                SELECT USR_VAR_NOMBRE
                FROM USR_MCVARIED
                WHERE USR_VAR_ALIAS = %s
            """
            cursor.execute(sql, [idVariedad])
            consulta = cursor.fetchone()
            if consulta:
                nombreVariedad = str(consulta[0])
            return nombreVariedad
    except Exception as e:
        error = str(e)
        InsertaDataPrueba("traeNombreVariedad", error)
        
def formatear_fecha(fecha_str):
    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
    fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
    return fecha_formateada

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
# def a(fecha):
#     try:
#         conexion = Trazabilidad()
#         cursor = conexion.cursor()
#         sql = ("""
#                 DECLARE @@Fecha DATE;
#                 SET @@Fecha = '""" + fecha + """';
#                 SELECT        DISTINCT General.dbo.USR_MCLOTE.USR_VAR_ALIAS
#                 FROM            LoteCalidad INNER JOIN
#                                         General.dbo.USR_MCLOTE ON LoteCalidad.LoteNumero = General.dbo.USR_MCLOTE.USR_LOTE_NUMERO
#                 WHERE        (CONVERT(DATE, LoteCalidad.FechaIngresoCalidad) = @@Fecha)
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchall()
#         if consulta:
#             results = [] 
#             for i in consulta:
#                 results.append(str(i[0]))
#         return results
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def traeCantBinsPorFecha_variedad(fecha, variedad):
#     try:
#         conexion = Trazabilidad()
#         cursor = conexion.cursor()
#         sql = ("""
#                 DECLARE @@Fecha DATE;
#                 DECLARE @@Variedad VARCHAR(255);
#                 SET @@Fecha = '""" + fecha + """';
#                 SET @@Variedad = '""" + variedad + """';
#                 SELECT SUM(General.dbo.USR_MCLOTE.USR_LOTE_CANTBINS)
#                 FROM            LoteCalidad INNER JOIN
#                                         General.dbo.USR_MCLOTE ON LoteCalidad.LoteNumero = General.dbo.USR_MCLOTE.USR_LOTE_NUMERO
#                 WHERE        (CONVERT(DATE, LoteCalidad.FechaIngresoCalidad) = @@Fecha AND General.dbo.USR_MCLOTE.USR_VAR_ALIAS = @@Variedad)
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchone()
#         if consulta:
#             cantidad = str(consulta[0])
#         return cantidad
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def traeChacrasPorVariedadFecha(variedad,fecha):
#     try:
#         conexion = General()
#         cursor = conexion.cursor()
#         sql = ("""
#                 DECLARE @@Variedad VARCHAR(255);
#                 DECLARE @@Fecha DATE;
#                 SET @@Variedad = '""" + variedad + """';
#                 SET @@Fecha = '""" + fecha + """';
#                 SELECT        DISTINCT USR_MCCHACRA.USR_CHAC_ALIAS, USR_MCCHACRA.USR_CHAC_NOMBRE
#                 FROM            Trazabilidad.dbo.CalidadControl INNER JOIN
#                                         Trazabilidad.dbo.LoteCalidad INNER JOIN
#                                         USR_MCLOTE ON Trazabilidad.dbo.LoteCalidad.LoteNumero = USR_MCLOTE.USR_LOTE_NUMERO ON Trazabilidad.dbo.CalidadControl.idLote = USR_MCLOTE.USR_LOTE_NUMERO INNER JOIN
#                                         USR_MCMOVCAM ON USR_MCLOTE.USR_MC_NUMERO = USR_MCMOVCAM.USR_MC_NUMERO INNER JOIN
#                                         USR_MCCHACRA ON USR_MCMOVCAM.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS
#                 WHERE        (USR_MCLOTE.USR_VAR_ALIAS = @@Variedad) AND (CONVERT(DATE, Trazabilidad.dbo.LoteCalidad.FechaIngresoCalidad) = @@Fecha)
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchall()
#         if consulta:
#             results = [] 
#             for i in consulta:
#                 results.append(str(i[0]))
#         return results
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def detalleGeneral(variedad,fecha,chacra):
#     try:
#         conexion = General()
#         cursor = conexion.cursor()
#         sql = ("""
#                 DECLARE @@Variedad VARCHAR(255);
#                 DECLARE @@Fecha DATE;
#                 DECLARE @@Productor VARCHAR(255);
#                 SET @@Variedad = '""" + variedad + """';
#                 SET @@Fecha = '""" + fecha + """';
#                 SET @@Productor = '""" + chacra + """';
#                 SELECT        USR_MCLOTE_1.USR_LOTE_NUMERO AS LOTE, USR_MCCHACRA.USR_CHAC_NOMBRE AS PRODUCTOR, USR_MCVARIED.USR_VAR_NOMBRE AS VARIEDAD, USR_MCLOTE_1.USR_LOTE_CANTBINS AS CANT_BINS, 
#                                         CalidadControl_1.idCalidad AS ID_CALIDAD, USR_MCLOTE_1.USR_VAR_ALIAS AS ID_VARIEDAD,
#                                             (SELECT        SUM(USR_MCLOTE.USR_LOTE_CANTBINS) AS Expr1
#                                             FROM            Trazabilidad.dbo.CalidadControl INNER JOIN
#                                                                         Trazabilidad.dbo.LoteCalidad INNER JOIN
#                                                                         USR_MCLOTE ON Trazabilidad.dbo.LoteCalidad.LoteNumero = USR_MCLOTE.USR_LOTE_NUMERO ON Trazabilidad.dbo.CalidadControl.idLote = USR_MCLOTE.USR_LOTE_NUMERO
#                                             WHERE        (USR_MCLOTE.USR_VAR_ALIAS = @@VARIEDAD) AND (CONVERT(DATE, Trazabilidad.dbo.LoteCalidad.FechaIngresoCalidad) = @@FECHA)) AS TOTAL_BINS, 
#                                 CONVERT(VARCHAR(10),CalidadControl_1.FechaCalidad, 103) AS FECHA
#                 FROM            Trazabilidad.dbo.CalidadControl AS CalidadControl_1 INNER JOIN
#                                         Trazabilidad.dbo.LoteCalidad AS LoteCalidad_1 INNER JOIN
#                                         USR_MCLOTE AS USR_MCLOTE_1 INNER JOIN
#                                         USR_MCVARIED ON USR_MCLOTE_1.USR_VAR_ALIAS = USR_MCVARIED.USR_VAR_ALIAS ON LoteCalidad_1.LoteNumero = USR_MCLOTE_1.USR_LOTE_NUMERO ON 
#                                         CalidadControl_1.idLote = USR_MCLOTE_1.USR_LOTE_NUMERO INNER JOIN
#                                         USR_MCMOVCAM ON USR_MCLOTE_1.USR_MC_NUMERO = USR_MCMOVCAM.USR_MC_NUMERO INNER JOIN
#                                         USR_MCCHACRA ON USR_MCMOVCAM.USR_CHAC_ALIAS = USR_MCCHACRA.USR_CHAC_ALIAS
#                 WHERE        (USR_MCLOTE_1.USR_VAR_ALIAS = @@VARIEDAD) 
#                                 AND (CONVERT(DATE, LoteCalidad_1.FechaIngresoCalidad) = @@FECHA)
#                                 AND USR_MCCHACRA.USR_CHAC_ALIAS = @@Productor
#                 ORDER BY PRODUCTOR
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchall()
#         return consulta
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def presiones(idCalidad):
#     try:
#         conexion = Trazabilidad()
#         cursor = conexion.cursor()
#         sql = ("""
#                 SELECT CONVERT(VARCHAR,CAST(MIN(Presion1) AS DECIMAL(18, 2))) AS MINIMA, CONVERT(VARCHAR,CAST((SUM(Presion1) + SUM(Presion2)) / (MAX(NroPresion) * 2) AS DECIMAL(18, 2))) AS PROMEDIO,
# 		                CONVERT(VARCHAR,CAST(MAX(Presion2) AS DECIMAL(18, 2))) AS MAXIMA
#                 FROM CalidadPresion
#                 WHERE idCalidad = '""" + idCalidad + """'
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchone()
#         if consulta:
#             min = str(consulta[0]).replace('.',',')
#             promedio = str(consulta[1]).replace('.',',')
#             max = str(consulta[2]).replace('.',',')
#         return min,promedio,max
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def detallesControl(idCalidad):
#     try:
#         conexion = Trazabilidad()
#         cursor = conexion.cursor()
#         sql = ("""
#                 SELECT CONVERT(VARCHAR,CAST(Solubles AS DECIMAL(18, 2))),CONVERT(VARCHAR,CAST(Almidon AS DECIMAL(18, 2))),
#                         CONVERT(VARCHAR,CAST(Acidez AS DECIMAL(18, 2)))
#                 FROM CalidadControl
#                 WHERE idCalidad = '""" + idCalidad + """'
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchone()
#         if consulta:
#             solubles = str(consulta[0]).replace('.',',')
#             almidon = str(consulta[1]).replace('.',',')
#             acidez = str(consulta[2]).replace('.',',')
#         return solubles,almidon,acidez
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def traeNombreChacra(idChacra):
#     try:
#         conexion = General()
#         cursor = conexion.cursor()
#         sql = ("""
#                 SELECT USR_CHAC_NOMBRE
#                 FROM USR_MCCHACRA
#                 WHERE USR_CHAC_ALIAS = '""" + idChacra + """'
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchone()
#         if consulta:
#             nombreChacra = str(consulta[0])
#         return nombreChacra
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()

# def traeNombreVariedad(idVariedad):
#     try:
#         conexion = General()
#         cursor = conexion.cursor()
#         sql = ("""
#                 SELECT USR_VAR_NOMBRE
#                 FROM USR_MCVARIED
#                 WHERE USR_VAR_ALIAS = '""" + idVariedad + """'
#                 """)
#         cursor.execute(sql)
#         consulta = cursor.fetchone()
#         if consulta:
#             nombreVariedad = str(consulta[0])
#         return nombreVariedad
#     except Exception as e:
#             print(e)
#     finally:
#         cursor.close()
#         conexion.close()